#!/usr/bin/env python3
"""Render the agent-architecture diagram to assets/agent-architecture.svg.

This diagram used to be a ```mermaid fence. GitHub's web UI renders those
natively, but the GitHub mobile app does not — it falls back to printing the
raw mermaid source as a syntax-highlighted code block, so mobile visitors saw
about forty lines of markup where the diagram should be. An SVG renders
identically everywhere.

The SVG is deliberately theme-agnostic: saturated node fills with white text
and mid-grey edges stay legible on both the light and dark GitHub themes, so
no <picture> element or duplicate dark variant is needed.

Regenerate after editing:
    python scripts/render_architecture.py
"""

COLORS = {"entry":"#1f6feb","brain":"#8957e5","tool":"#0d7d6c","check":"#9e6a03","out":"#238636"}
EDGE, W, H = "#8b949e", 1040, 700
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
COLS = {"l":235,"c":540,"r":845}
BW = 270

N = {
 "U":   ("c",  26, 46, "User · Voice · API",   None,                            "entry"),
 "G":   ("c", 112, 52, "Guardrails + Intent",  "classification",                "entry"),
 "FAST":("l", 206, 56, "Deterministic Handler","regex · rules · zero LLM cost", "check"),
 "P":   ("c", 206, 56, "Planner Agent",        "decompose into task graph",     "brain"),
 "R":   ("c", 300, 46, "Orchestrator / Router",None,                            "brain"),
 "A1":  ("l", 376, 46, "Research Agent",       None,                            "brain"),
 "A2":  ("c", 376, 46, "Code Agent",           None,                            "brain"),
 "A3":  ("r", 376, 46, "System / Ops Agent",   None,                            "brain"),
 "T":   ("c", 462, 56, "Tool Layer",           "MCP · REST · Shell · DB",       "tool"),
 "M":   ("r", 462, 56, "Memory",               "short-term · vector · episodic","tool"),
 "C":   ("c", 556, 46, "Critic / Reflection",  None,                            "check"),
 "O":   ("c", 632, 46, "Final Response",       None,                            "out"),
}
def box(k):
    col, t, h = N[k][0], N[k][1], N[k][2]
    c = COLS[col]
    return c - BW/2, t, BW, h, c, t + h/2
def cx(k): return box(k)[4]
def cy(k): return box(k)[5]
def top(k): return box(k)[1]
def bot(k): return box(k)[1] + box(k)[3]
def left(k): return box(k)[0]
def right(k): return box(k)[0] + box(k)[2]

ARIA = ("Agent architecture diagram. User, voice or API input passes through guardrails and intent "
        "classification, which routes either to a deterministic handler on the fast path or to a "
        "planner agent. The planner feeds an orchestrator that routes to research, code, and system "
        "agents. All three call a shared tool layer, which reads and writes memory. A critic then "
        "either sends work back to the planner to replan, or releases the verified final response. "
        "The deterministic fast path bypasses the agents and returns directly.")

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
       f'role="img" aria-label="{ARIA}">',
       '<defs>',
       f'<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="11" markerHeight="11" markerUnits="userSpaceOnUse" '
       f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{EDGE}"/></marker>',
       f'<marker id="b" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="11" markerHeight="11" markerUnits="userSpaceOnUse" '
       f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{EDGE}"/></marker>',
       '</defs>']

def edge(p, label=None, lx=None, ly=None, start=False):
    ms = ' marker-start="url(#b)"' if start else ''
    out.append(f'<path d="{p}" fill="none" stroke="{EDGE}" stroke-width="2" '
               f'marker-end="url(#a)"{ms}/>')
    if label:
        w = len(label) * 6.6 + 18
        out.append(f'<rect x="{lx-w/2:.0f}" y="{ly-10:.0f}" width="{w:.0f}" height="20" rx="10" fill="{EDGE}"/>')
        out.append(f'<text x="{lx:.0f}" y="{ly+4:.0f}" font-family="{FONT}" font-size="11" '
                   f'font-weight="600" fill="#ffffff" text-anchor="middle">{label}</text>')

def vert(a, b, label=None):
    lx = cx(a) if label else None
    ly = (bot(a) + top(b)) / 2 if label else None
    edge(f"M{cx(a):.0f},{bot(a):.0f} L{cx(b):.0f},{top(b):.0f}", label, lx, ly)

def curve(x1, y1, x2, y2, label=None, lx=None, ly=None):
    m = (y1 + y2) / 2
    edge(f"M{x1:.0f},{y1:.0f} C{x1:.0f},{m:.0f} {x2:.0f},{m:.0f} {x2:.0f},{y2:.0f}", label, lx, ly)

vert("U", "G")
vert("G", "P", "reasoning path")
curve(left("G")+45, bot("G"), cx("FAST"), top("FAST"), "fast path", 318, 180)
vert("P", "R")
vert("R", "A2", "build")
curve(left("R")+45, bot("R"), cx("A1"), top("A1"), "research", 318, 350)
curve(right("R")-45, bot("R"), cx("A3"), top("A3"), "operate", 762, 350)
vert("A2", "T")
curve(cx("A1"), bot("A1"), left("T")+60, top("T"))
curve(cx("A3"), bot("A3"), right("T")-60, top("T"))
edge(f'M{right("T"):.0f},{cy("T"):.0f} L{left("M"):.0f},{cy("M"):.0f}')
edge(f'M{left("M"):.0f},{cy("M"):.0f} L{right("T"):.0f},{cy("T"):.0f}')
vert("T", "C")
vert("C", "O", "verified")
edge(f'M{left("C"):.0f},{cy("C"):.0f} L52,{cy("C"):.0f} L52,{cy("P"):.0f} L{left("P"):.0f},{cy("P"):.0f}',
     "incomplete → replan", 330, cy("C"))
edge(f'M{cx("FAST"):.0f},{bot("FAST"):.0f} L{cx("FAST"):.0f},{cy("O"):.0f} L{left("O"):.0f},{cy("O"):.0f}')

for k in N:
    col, t, h, title, sub, cls = N[k]
    x, y, w, hh, c, ccy = box(k)
    out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{hh}" rx="10" fill="{COLORS[cls]}"/>')
    ty = ccy + 5 if not sub else ccy - 3
    out.append(f'<text x="{c:.0f}" y="{ty:.0f}" font-family="{FONT}" font-size="15" font-weight="600" '
               f'fill="#ffffff" text-anchor="middle">{title}</text>')
    if sub:
        out.append(f'<text x="{c:.0f}" y="{ccy+16:.0f}" font-family="{MONO}" font-size="11" '
                   f'fill="#ffffff" fill-opacity="0.85" text-anchor="middle">{sub}</text>')
    assert len(title)*8.3 < w-16, f"{k}: title too wide"
    if sub: assert len(sub)*6.4 < w-16, f"{k}: subtitle too wide"

out.append("</svg>")
open("assets/agent-architecture.svg", "w", encoding="utf-8").write("\n".join(out))
print(f"✓ wrote assets/agent-architecture.svg — {len(N)} nodes")
