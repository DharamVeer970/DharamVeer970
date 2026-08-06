#!/usr/bin/env python3
"""Profile agent — regenerates the live section of the profile README.

Runs on a schedule from .github/workflows/profile-agent.yml. Queries the GitHub
REST API for what actually happened recently, renders it as markdown, and swaps
it into README.md between the AGENT-LOG markers.

Design constraints:
  * stdlib only — the workflow installs nothing
  * fail soft — if the API is unreachable, leave the README untouched and exit 0
    so a transient outage never shows up as a red X on the profile
  * idempotent — writes only when the rendered output differs

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
MAX_AGE_DAYS = 120  # anything older isn't a "recent signal"

# Commits the agent makes itself — never report them back as activity.
SELF_COMMIT_PREFIX = "chore(profile-agent)"

# Repos that are scaffolding rather than work worth surfacing.
SKIP_REPOS = {"localrepo", "GIthub-Tutorial", "Test_Remote_Server", USER}


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

def parse_ts(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def ago(when: datetime) -> str:
    """'3h ago', '2d ago', '5mo ago' — compact enough for a table cell."""
    seconds = (datetime.now(timezone.utc) - when).total_seconds()
    for cutoff, divisor, unit in (
        (90, 1, "s"), (5400, 60, "m"), (86400, 3600, "h"),
        (1209600, 86400, "d"), (5184000, 604800, "w"), (31536000, 2592000, "mo"),
    ):
        if seconds < cutoff:
            return f"{max(1, int(seconds // divisor))}{unit} ago"
    return f"{int(seconds // 31536000)}y ago"


def plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def repo_link(full_name: str) -> str:
    return f"[`{full_name.split('/')[-1]}`](https://github.com/{full_name})"


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
        if name and repo["name"] not in SKIP_REPOS:
            counts[name] = counts.get(name, 0) + 1

    if not counts:
        return []

    grand = sum(counts.values())
    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:TOP_LANGS]
    pad = max(len(name) for name, _ in ranked)

    rows = ["```text"]
    for name, n in ranked:
        share = n / grand
        filled = round(share * BAR_WIDTH)
        bar = "█" * filled + "░" * (BAR_WIDTH - filled)
        rows.append(f"{name:<{pad}}  {bar}  {share * 100:5.1f}%  {plural(n, 'project')}")
    rows.append("```")
    return rows


def activity_feed(events: list[dict]) -> list[str]:
    """Recent public events, newest first.

    Consecutive pushes to the same repo collapse into a single row with the
    commit counts summed — six rows of "pushed 1 commit to Wilco" is noise,
    "pushed 11 commits to Wilco" is a signal.
    """
    fresh = []
    for event in events:
        try:
            when = parse_ts(event["created_at"])
        except (KeyError, ValueError):
            continue
        if (datetime.now(timezone.utc) - when).days <= MAX_AGE_DAYS:
            fresh.append((when, event))
    fresh.sort(key=lambda pair: pair[0], reverse=True)

    # Roll up pushes per repo before rendering.
    pushes: dict[str, int] = {}
    for _, event in fresh:
        if event.get("type") != "PushEvent":
            continue
        repo = (event.get("repo") or {}).get("name", "")
        payload = event.get("payload") or {}
        commits = payload.get("commits") or []
        if not repo or repo.split("/")[-1] in SKIP_REPOS or any(
            str(c.get("message", "")).startswith(SELF_COMMIT_PREFIX) for c in commits
        ):
            continue  # the agent's own commits, and profile-repo housekeeping
        pushes[repo] = pushes.get(repo, 0) + int(payload.get("size", len(commits)) or 0)

    seen: set[tuple[str, str]] = set()
    rows: list[str] = []

    for when, event in fresh:
        kind = event.get("type", "")
        repo = (event.get("repo") or {}).get("name", "")
        payload = event.get("payload") or {}
        if not repo or repo.split("/")[-1] in SKIP_REPOS:
            continue  # editing the profile README is not a career signal

        if kind == "PushEvent":
            total = pushes.get(repo)
            if not total:
                continue  # self-commits only, or already rendered
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

        rows.append(f"| `{ago(when)}` | {what} {repo_link(repo)} |")
        if len(rows) == FEED_ROWS:
            break

    if not rows:
        return []
    return ["| when | what |", "|:--|:--|", *rows]


def spotlight(repos: list[dict]) -> list[str]:
    """The most recently touched repo worth showing off."""
    for repo in repos:
        if repo["name"] in SKIP_REPOS:
            continue
        desc = repo.get("description") or "_no description yet_"
        meta = [
            f"`{repo['language']}`" if repo.get("language") else None,
            f"⭐ {repo['stargazers_count']}" if repo.get("stargazers_count") else None,
            f"🍴 {repo['forks_count']}" if repo.get("forks_count") else None,
            f"updated {ago(parse_ts(repo['pushed_at']))}",
        ]
        return [
            f"### 🔦 Currently in the workshop — {repo_link(repo['full_name'])}",
            "",
            f"> {desc}",
            "",
            " · ".join(m for m in meta if m),
        ]
    return []


def render() -> str | None:
    """Build the full agent-log section. None means 'not enough data, skip'."""
    print(f"→ fetching activity for {USER}")
    repos = api(f"/users/{USER}/repos?per_page=100&sort=pushed&type=owner")
    events = api(f"/users/{USER}/events/public?per_page=100")

    if not isinstance(repos, list) or not repos:
        return None

    repos = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    print(f"  {len(repos)} repos · {stars} stars · {len(events or [])} events")

    blocks: list[list[str]] = []

    if shine := spotlight(repos):
        blocks.append(shine)

    if feed := activity_feed(events if isinstance(events, list) else []):
        blocks.append(["### 📡 Recent signals", "", *feed])

    if bar := language_bar(repos):
        blocks.append([
            "### 🧬 What I actually write",
            "",
            "<sub>share of public projects by primary language</sub>",
            "",
            *bar,
        ])

    if not blocks:
        return None

    stamp = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")
    # A "0 stars" badge on your own profile is worse than saying nothing.
    facts = [f"{len(repos)} public repos"]
    if stars:
        facts.append(plural(stars, "star"))
    facts.append(f"last run {stamp}")
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
        original = open(README, encoding="utf-8").read()
    except OSError as exc:
        print(f"✗ cannot read {README}: {exc}", file=sys.stderr)
        return 1

    if START not in original or END not in original:
        print(f"✗ markers {START} / {END} not found in {README}", file=sys.stderr)
        return 1

    head, _, rest = original.partition(START)
    _, _, tail = rest.partition(END)
    updated = f"{head}{START}\n\n{section}\n\n{END}{tail}"

    if updated == original:
        print("✓ already current — nothing to commit")
        return 0

    with open(README, "w", encoding="utf-8") as handle:
        handle.write(updated)
    print(f"✓ {README} updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
