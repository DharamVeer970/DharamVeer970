#!/usr/bin/env python3
"""Profile agent — regenerates the live section of the profile README.

Runs on a schedule from .github/workflows/profile-agent.yml. Queries the GitHub
REST API for what actually happened recently, renders it as markdown, and swaps
it into README.md between the AGENT-LOG markers.

Design constraints:
  * stdlib only — the workflow installs nothing
  * fail soft — if the API is unreachable, leave the README untouched and exit 0
    so a transient outage never shows up as a red X on the profile
  * idempotent — the output contains absolute dates only (no "3h ago", no run
    timestamp), so the README changes — and a commit happens — only when the
    underlying data actually changed

Usage:
    python scripts/profile_agent.py            # rewrite README.md in place
    python scripts/profile_agent.py --dry-run  # print the section, touch nothing
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

USER = os.environ.get("PROFILE_USER", "DharamVeer970")
README = os.environ.get("PROFILE_README", "README.md")
START = "<!-- AGENT-LOG:START -->"
END = "<!-- AGENT-LOG:END -->"

API = "https://api.github.com"
TIMEOUT = 20
BAR_WIDTH = 34
TOP_LANGS = 6
FEED_ROWS = 6
MAX_AGE_DAYS = 120   # anything older isn't a "recent signal"
MAX_COMPARES = 40    # cap on compare-API lookups per run (rate-limit safety)

# Commits the agent makes itself — never report them back as activity.
SELF_COMMIT_PREFIX = "chore(profile-agent)"

# Repos that are scaffolding, tutorials or practice exercises rather than work
# worth surfacing. They are excluded from the spotlight, the feed and the
# language chart (they still count towards the public-repo total).
SKIP_REPOS = {
    USER,                          # this profile repo — README edits aren't a signal
    "localrepo",
    "GIthub-Tutorial",
    "Test_Remote_Server",
    "ReactsBasics",
    "Calculator_using_html",
    "Responsive_Website",
    "CodeAlpha_Portfolio_Website",
    "CodeAlpha_Resume_Builder",
}

# GitHub reports notebooks as their own "language", but a .ipynb is Python code
# with a different file format. Folding them together describes the work, not
# the container.
LANGUAGE_ALIASES = {"Jupyter Notebook": "Python"}


# --------------------------------------------------------------------------- #
# GitHub API
# --------------------------------------------------------------------------- #

def api(path: str) -> list | dict | None:
    """GET a JSON path from the GitHub API. Returns None on any failure."""
    req = urllib.request.Request(
        f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{USER}-profile-agent",
            **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
               if os.environ.get("GITHUB_TOKEN") else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.load(resp)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        print(f"  ! {path} → {exc}", file=sys.stderr)
        return None


# --------------------------------------------------------------------------- #
# Formatting helpers
# --------------------------------------------------------------------------- #

def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def fmt_date(when: datetime) -> str:
    """'03 Oct 2026' — absolute, so it never goes stale on the rendered page."""
    return when.strftime("%d %b %Y")


def plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def repo_link(full_name: str) -> str:
    return f"[`{full_name.split('/')[-1]}`](https://github.com/{full_name})"


def is_skipped(full_or_short_name: str) -> bool:
    return full_or_short_name.split("/")[-1] in SKIP_REPOS


# --------------------------------------------------------------------------- #
# Push-event commit counting
# --------------------------------------------------------------------------- #

class CommitCounter:
    """Works out how many commits a PushEvent carried.

    GitHub stripped `commits`, `size` and `distinct_size` from PushEvent
    payloads in the public Events API (late 2025); a push now only carries
    `before` and `head`. Reading `size` therefore returned 0 for every push and
    the feed silently dropped all of them. The compare endpoint recovers the
    real number from the two SHAs.
    """

    ZERO_SHA = "0" * 40

    def __init__(self) -> None:
        self.lookups = 0
        self.cache: dict[tuple[str, str, str], int] = {}

    def count(self, repo: str, payload: dict) -> int:
        # Legacy payloads (or GitHub restoring the field) — trust it directly.
        if isinstance(payload.get("size"), int):
            commits = payload.get("commits") or []
            if any(str(c.get("message", "")).startswith(SELF_COMMIT_PREFIX) for c in commits):
                return 0
            return payload["size"]

        before, head = payload.get("before") or "", payload.get("head") or ""
        if not head:
            return 1
        if not before or before == self.ZERO_SHA:
            return 1  # brand-new branch: no base to compare against

        key = (repo, before, head)
        if key in self.cache:
            return self.cache[key]
        if self.lookups >= MAX_COMPARES:
            return 1  # over budget — a push happened, count it once

        self.lookups += 1
        data = api(f"/repos/{repo}/compare/{before}...{head}")
        n = 1
        if isinstance(data, dict):
            ahead = data.get("ahead_by", data.get("total_commits"))
            if isinstance(ahead, int):
                n = ahead
            commits = data.get("commits") or []
            if commits and all(
                str((c.get("commit") or {}).get("message", "")).startswith(SELF_COMMIT_PREFIX)
                for c in commits
            ):
                n = 0
        self.cache[key] = n
        return n


# --------------------------------------------------------------------------- #
# Section renderers
# --------------------------------------------------------------------------- #

def language_bar(repos: list[dict]) -> list[str]:
    """Share of projects by primary language, as a unicode bar chart.

    Deliberately NOT byte-weighted. `.ipynb` files embed base64 image data for
    every saved plot, so a handful of notebooks outweighs every line of Python
    in the account — the first byte-weighted run reported 95.7% Jupyter and
    2.7% Python, which describes the file format, not the work. Counting each
    project once is coarser but honest.
    """
    counts: dict[str, int] = {}
    for repo in repos:
        name = repo.get("language")
        repo_name = repo.get("name")
        if name and repo_name and not is_skipped(repo_name):
            name = LANGUAGE_ALIASES.get(name, name)
            counts[name] = counts.get(name, 0) + 1

    if not counts:
        return []

    grand = sum(counts.values())
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP_LANGS]
    pad = max(len(name) for name, _ in ranked)

    rows = ["```text"]
    for name, n in ranked:
        share = n / grand
        filled = round(share * BAR_WIDTH)
        bar = "█" * filled + "░" * (BAR_WIDTH - filled)
        rows.append(f"{name:<{pad}}  {bar}  {share * 100:5.1f}%  {plural(n, 'project')}")
    rows.append("```")
    return rows


def fresh_events(events: list[dict]) -> list[tuple[datetime, dict]]:
    """Events inside the MAX_AGE_DAYS window, newest first."""
    now = datetime.now(timezone.utc)
    fresh = []
    for event in events:
        when = parse_ts(event.get("created_at"))
        if when and (now - when).days <= MAX_AGE_DAYS:
            fresh.append((when, event))
    fresh.sort(key=lambda pair: pair[0], reverse=True)
    return fresh


def activity_feed(fresh: list[tuple[datetime, dict]]) -> list[str]:
    """Recent public events, newest first.

    Pushes to the same repo collapse into a single row with the commit counts
    summed — six rows of "pushed 1 commit to Wilco" is noise, "pushed 11
    commits to Wilco" is a signal.
    """
    counter = CommitCounter()

    # Roll up pushes per repo before rendering.
    pushes: dict[str, int] = {}
    for _, event in fresh:
        if event.get("type") != "PushEvent":
            continue
        repo = (event.get("repo") or {}).get("name", "")
        if not repo or is_skipped(repo):
            continue
        pushes[repo] = pushes.get(repo, 0) + counter.count(repo, event.get("payload") or {})

    seen: set[tuple[str, str]] = set()
    rows: list[str] = []

    for when, event in fresh:
        kind = event.get("type", "")
        repo = (event.get("repo") or {}).get("name", "")
        payload = event.get("payload") or {}
        if not repo or is_skipped(repo):
            continue  # editing the profile README is not a career signal

        if kind == "PushEvent":
            total = pushes.get(repo)
            if not total:
                continue  # self-commits only
            what = f"pushed **{plural(total, 'commit')}** to"
        elif kind == "CreateEvent" and payload.get("ref_type") == "repository":
            what = "**created**"
        elif kind == "CreateEvent" and payload.get("ref_type") == "branch":
            what = f"branched `{payload.get('ref', '?')}` on"
        elif kind == "PullRequestEvent":
            what = f"**{payload.get('action', 'updated')}** a PR on"
        elif kind == "IssuesEvent":
            what = f"**{payload.get('action', 'updated')}** an issue on"
        elif kind == "ReleaseEvent":
            what = f"**released** `{(payload.get('release') or {}).get('tag_name', '?')}` on"
        elif kind == "PublicEvent":
            what = "**open-sourced**"
        else:
            continue

        # Pushes dedupe per repo (counts are already rolled up); everything
        # else dedupes on the exact phrasing so distinct actions both show.
        key = (repo, "push" if kind == "PushEvent" else what)
        if key in seen:
            continue
        seen.add(key)

        rows.append(f"| `{fmt_date(when)}` | {what} {repo_link(repo)} |")
        if len(rows) == FEED_ROWS:
            break

    if counter.lookups:
        print(f"  {counter.lookups} compare lookups for push commit counts")
    if not rows:
        return []
    return ["| date | what |", "|:--|:--|", *rows]


def spotlight(repos: list[dict]) -> list[str]:
    """The most recently touched repo worth showing off.

    Prefers repos that have a description — a spotlight reading "no
    description yet" undersells the work.
    """
    candidates = [
        r for r in repos
        if r.get("name") and not is_skipped(r["name"]) and r.get("full_name")
    ]
    if not candidates:
        return []
    repo = next((r for r in candidates if r.get("description")), candidates[0])

    desc = repo.get("description") or "_no description yet_"
    pushed = parse_ts(repo.get("pushed_at"))
    meta = [
        f"`{repo['language']}`" if repo.get("language") else None,
        f"⭐ {repo['stargazers_count']}" if repo.get("stargazers_count") else None,
        f"🍴 {repo['forks_count']}" if repo.get("forks_count") else None,
        f"last push {fmt_date(pushed)}" if pushed else None,
    ]
    return [
        f"### 🔦 Currently in the workshop — {repo_link(repo['full_name'])}",
        "",
        f"> {desc}",
        "",
        " · ".join(m for m in meta if m),
    ]


def render() -> str | None:
    """Build the full agent-log section. None means 'not enough data, skip'."""
    print(f"→ fetching activity for {USER}")
    repos = api(f"/users/{USER}/repos?per_page=100&sort=pushed&type=owner")
    events = api(f"/users/{USER}/events/public?per_page=100")

    if not isinstance(repos, list) or not repos:
        return None

    repos = [r for r in repos if isinstance(r, dict) and not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    fresh = fresh_events(events if isinstance(events, list) else [])
    print(f"  {len(repos)} repos · {stars} stars · {len(fresh)} recent events")

    blocks: list[list[str]] = []

    if shine := spotlight(repos):
        blocks.append(shine)

    if feed := activity_feed(fresh):
        blocks.append(["### 📡 Recent signals", "", *feed])

    if bar := language_bar(repos):
        blocks.append([
            "### 🧬 What I actually write",
            "",
            "<sub>share of public projects by primary language · notebooks count as "
            "Python · tutorial and practice repos excluded</sub>",
            "",
            *bar,
        ])

    if not blocks:
        return None

    # "Data as of" = newest real activity, not the time the job ran. A run
    # timestamp would change the README on every run and force a daily commit
    # even when nothing happened.
    stamps = [parse_ts(r.get("pushed_at")) for r in repos
              if r.get("name") and not is_skipped(r["name"])]
    stamps += [when for when, event in fresh
               if not is_skipped((event.get("repo") or {}).get("name") or USER)]
    stamps = [s for s in stamps if s]

    # A "0 stars" badge on your own profile is worse than saying nothing.
    facts = [f"{len(repos)} public repos"]
    if stars:
        facts.append(plural(stars, "star"))
    if stamps:
        facts.append(f"data as of {fmt_date(max(stamps))}")
    blocks.append([
        "<div align=\"right\">",
        "",
        f"<sub>🤖 generated by <code>profile_agent.py</code> · "
        f"{' · '.join(facts)}</sub>",
        "",
        "</div>",
    ])

    return "\n\n".join("\n".join(block) for block in blocks)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def main() -> int:
    # Windows consoles default to cp1252, which can't encode → ✓ ✗ or the bar
    # glyphs; without this a local run dies on its first print.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="print the rendered section without writing")
    args = parser.parse_args()

    section = render()
    if section is None:
        print("✗ no usable data returned — leaving README untouched")
        return 0

    if args.dry_run:
        print("\n" + section)
        return 0

    try:
        with open(README, encoding="utf-8", newline="") as handle:
            original = handle.read()
    except OSError as exc:
        print(f"✗ cannot read {README}: {exc}", file=sys.stderr)
        return 1

    if START not in original or END not in original:
        print(f"✗ markers {START} / {END} not found in {README}", file=sys.stderr)
        return 1

    # Match the file's existing line endings so a local run on Windows doesn't
    # rewrite every line of the README.
    newline = "\r\n" if "\r\n" in original else "\n"
    section = section.replace("\n", newline)

    head, _, rest = original.partition(START)
    _, _, tail = rest.partition(END)
    updated = f"{head}{START}{newline}{newline}{section}{newline}{newline}{END}{tail}"

    if updated == original:
        print("✓ already current — nothing to commit")
        return 0

    with open(README, "w", encoding="utf-8", newline="") as handle:
        handle.write(updated)
    print(f"✓ {README} updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
