#!/usr/bin/env python3
"""Generate the Selvage architecture diagram.

Hand-placed SVG coordinates drift into overlapping text the moment a label is
reworded. This builds the diagram from declared boxes and asserts the invariants
that a reader actually notices: every text line fits inside its own box, and no
two boxes collide. Monospace makes width predictable — 0.6em per character — so
the fit check is arithmetic rather than a guess.

    python3 tools/gen-architecture-svg.py > assets/visuals/selvage-architecture.svg
"""
import sys

W, H = 1600, 790
CREAM, INK, MUTED = "#f3f0ea", "#1c2530", "#8a8578"
SOFT, PANEL, NAVY = "#c9c3b6", "#fbfaf7", "#16212b"
TEAL, ORANGE, BLUE, GREEN = "#2a7f8f", "#c4552a", "#2f4e7e", "#5b7d5b"
CHAR_W = 0.6  # monospace advance width, in ems

boxes = []   # (x, y, w, h, label) — every rectangle, for the collision check
out = []


def fits(text, size, width, pad=32):
    return len(text) * size * CHAR_W <= width - pad


def box(x, y, w, h, label, fill=PANEL, stroke=SOFT, sw=1.0, rx=8, collide=True):
    if collide:
        boxes.append((x, y, w, h, label))
    s = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {s}/>')


def lines(x, y, items, box_x, box_w, step=18):
    """Text lines inside a box. Asserts each line fits the box's inner width."""
    for i, (text, size, colour, weight) in enumerate(items):
        assert fits(text, size, box_w, pad=2 * (x - box_x)), \
            f"text overflows its box: {text!r} ({size}px in {box_w}px)"
        wt = f' font-weight="{weight}"' if weight else ""
        out.append(f'<text x="{x}" y="{y + i * step}" font-size="{size}" fill="{colour}"{wt}>'
                   f'{text}</text>')


def free_text(x, y, text, size=11, colour=MUTED, weight=None, anchor=None):
    wt = f' font-weight="{weight}"' if weight else ""
    an = f' text-anchor="{anchor}"' if anchor else ""
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{colour}"{wt}{an}>{text}</text>')


def arrow(path, colour, marker, sw=1.8):
    out.append(f'<path d="{path}" stroke="{colour}" stroke-width="{sw}" fill="none" '
               f'marker-end="url(#{marker})"/>')


# ---------------------------------------------------------------- header
out.append(f'<rect width="{W}" height="{H}" fill="{CREAM}"/>')
out.append(f'<text x="60" y="50" font-size="13" letter-spacing="3.2" fill="{MUTED}">ARCHITECTURE</text>')
out.append(f'<text x="60" y="90" font-size="33" font-weight="600" fill="{INK}">'
           f'Selvage — from request to reviewed branch</text>')

legend = [("retrieval", TEAL), ("implementation", ORANGE), ("review", BLUE), ("approval", GREEN)]
lx = 1010
for name, colour in legend:
    out.append(f'<line x1="{lx}" y1="42" x2="{lx + 26}" y2="42" stroke="{colour}" stroke-width="3"/>')
    out.append(f'<text x="{lx + 34}" y="46" font-size="12.5" fill="#5c6672">{name}</text>')
    lx += 34 + int(len(name) * 12.5 * CHAR_W) + 26

# ------------------------------------------------- external CLIs (top strip)
free_text(60, 128, "EXTERNAL CODING CLIs — YOUR SUBSCRIPTIONS, YOUR AUTH", 11.5, MUTED)
clis = [("Claude Code", "anthropic · reports cost"), ("Kiro CLI", "kiro · reports credits"),
        ("OpenCode", "any authenticated provider"), ("Codex", "openai")]
cx = 60
for title, sub in clis:
    out.append(f'<rect x="{cx}" y="142" width="215" height="48" rx="6" fill="none" '
               f'stroke="{SOFT}" stroke-dasharray="4 4"/>')
    free_text(cx + 108, 163, title, 13, "#3d4653", anchor="middle")
    free_text(cx + 108, 180, sub, 10.5, MUTED, anchor="middle")
    cx += 227
free_text(cx + 4, 163, "Selvage drives these as processes.", 11.5, MUTED)
free_text(cx + 4, 180, "Context leaves under each provider's terms.", 11.5, MUTED)

# ------------------------------------------------------------- control plane
PLANE_Y, PLANE_H = 214, 488
out.append(f'<rect x="48" y="{PLANE_Y}" width="1352" height="{PLANE_H}" rx="10" fill="none" stroke="#b9b3a6"/>')
out.append(f'<rect x="60" y="{PLANE_Y - 9}" width="422" height="18" fill="{CREAM}"/>')
free_text(66, PLANE_Y + 5, "DEVELOPER MACHINE — LOCAL CONTROL PLANE", 11.5, "#6b7480")

# five columns, generous gutters so no label can reach its neighbour
COLS = {name: x for name, x in
        zip(("surfaces", "sched", "impl", "verify", "review"), (70, 286, 548, 810, 1072))}
CW = 214

# column 1 — surfaces
box(COLS["surfaces"], 244, 168, 50, "dashboard", stroke=INK, sw=1.6, rx=6)
lines(84, 265, [("Web dashboard", 14, INK, 600), ("primary surface", 10.5, MUTED, None)],
      COLS["surfaces"], 168)
box(COLS["surfaces"], 302, 168, 38, "cli", rx=6)
lines(84, 326, [("CLI · slv", 14, INK, None)], COLS["surfaces"], 168)
box(COLS["surfaces"], 348, 168, 50, "mcp", rx=6)
lines(84, 369, [("MCP server", 14, INK, None), ("agents submit + query", 10.5, MUTED, None)],
      COLS["surfaces"], 168)
lines(70, 424, [("prompt · issue · spec", 11, MUTED, None), ("epic batch", 11, MUTED, None)],
      70, 200, step=16)
arrow("M238 321 L280 321", MUTED, "am", 1.4)

# column 2 — scheduler and the durable ledger
box(COLS["sched"], 244, CW, 104, "scheduler", fill=NAVY, stroke=None)
lines(302, 272, [("Scheduler", 15.5, "#f7f5f0", 600), ("one per project", 11, "#9fb0bd", None)],
      COLS["sched"], CW, step=20)
lines(302, 316, [("leases · routing · budgets", 11, "#9fb0bd", None),
                 ("independence floor enforced", 11, "#9fb0bd", None)], COLS["sched"], CW, step=17)
tiles = [("task queue", "+ retries", 0, 0), ("adapter", "router", 112, 0),
         ("evidence", "ledger", 0, 48), ("usage +", "provenance", 112, 48)]
for a, b, dx, dy in tiles:
    box(COLS["sched"] + dx, 358 + dy, 102, 40, a, rx=5)
    lines(COLS["sched"] + dx + 10, 374 + dy, [(a, 10.5, "#3d4653", None), (b, 10.5, MUTED, None)],
          COLS["sched"] + dx, 102, step=14)
box(COLS["sched"], 454, CW, 42, "plans", rx=5)
lines(296, 470, [("per-attempt verification plans", 10.5, "#3d4653", None),
                 ("pinned · immutable", 10.5, MUTED, None)], COLS["sched"], CW, step=14)
lines(COLS["sched"], 522, [("Task state, evidence, plans,", 11, MUTED, None),
                           ("sessions and usage stay here.", 11, MUTED, None)],
      COLS["sched"], CW + 4, step=16)

# column 3 — retrieval, implementation, commit
box(COLS["impl"], 244, CW, 84, "index", fill="#eaf3f4", stroke=TEAL, sw=1.6)
lines(562, 268, [("Code index", 14.5, "#1c5b68", 600), ("AST + BM25 retrieval", 10.5, "#3d6b74", None),
                 ("bounded orientation budget", 10.5, "#3d6b74", None),
                 ("route-mirror guardrail", 10.5, "#3d6b74", None)], COLS["impl"], CW, step=17)
arrow(f'M{COLS["impl"] + 107} 328 L{COLS["impl"] + 107} 366', TEAL, "ac")
free_text(COLS["impl"] + 118, 352, "orients", 10.5, TEAL)
box(COLS["impl"], 374, CW, 70, "implementer", fill="#fbf1ec", stroke=ORANGE, sw=1.6)
lines(562, 398, [("Implementer", 14.5, "#a8461f", 600), ("model + provider A", 10.5, "#8a5a44", None),
                 ("isolated Git worktree", 10.5, "#8a5a44", None)], COLS["impl"], CW, step=17)
arrow(f'M{COLS["impl"] + 107} 444 L{COLS["impl"] + 107} 476', ORANGE, "ao")
box(COLS["impl"], 484, CW, 44, "commit", stroke="#e0b9a6", rx=6)
lines(562, 504, [("implementation commit", 12.5, INK, None),
                 ("your checkout never touched", 10.5, MUTED, None)], COLS["impl"], CW, step=16)
arrow(f'M{COLS["impl"] + CW} 506 L{COLS["verify"]} 506', ORANGE, "ao")

# column 4 — verification
box(COLS["verify"], 244, CW, 128, "verification", fill=NAVY, stroke=None)
lines(824, 270, [("Verification", 15.5, "#f7f5f0", 600),
                 ("the scheduler runs it", 10.5, "#9fb0bd", None)], COLS["verify"], CW, step=19)
for i, (name, note) in enumerate((("build", "plan pinned"), ("tests", "fresh DB"),
                                  ("project checks", "per attempt"))):
    free_text(824, 314 + i * 20, name, 11.5, "#dfe6ea")
    free_text(COLS["verify"] + CW - 14, 314 + i * 20, note, 10.5, "#7fd8c0", anchor="end")
box(COLS["verify"], 382, CW, 46, "evidence", rx=6)
lines(824, 402, [("verification evidence", 12.5, INK, None),
                 ("logs · exit codes · SHA", 10.5, MUTED, None)], COLS["verify"], CW, step=16)
arrow(f'M{COLS["verify"] + CW} 404 L{COLS["review"]} 404', BLUE, "ab")
# re-verify return path, routed below the commit box so it crosses nothing
arrow(f'M{COLS["verify"] + 60} 428 L{COLS["verify"] + 60} 452 L{COLS["impl"] + 160} 452 '
      f'L{COLS["impl"] + 160} 484', ORANGE, "ao", 1.6)

# column 5 — independent review
box(COLS["review"], 244, CW, 118, "review", fill="#eef1f7", stroke=BLUE, sw=1.6)
lines(1086, 270, [("Independent review", 15.5, "#26406b", 600),
                  ("model + provider B", 10.5, "#455a7e", None),
                  ("receives diff + evidence", 10.5, "#455a7e", None),
                  ("no write tools", 10.5, "#455a7e", None)], COLS["review"], CW, step=18)
free_text(1086, 348, "verdict + findings", 11, "#26406b", weight=600)
lines(COLS["review"], 384, [("✗ a model reviewing its own", 10.5, MUTED, None),
                            ("  work is not independent", 10.5, MUTED, None)],
      COLS["review"], CW + 6, step=15)
arrow(f'M{COLS["review"] + 107} 420 L{COLS["review"] + 107} 452', BLUE, "ab")

# fan-out: approve to the gate, defer to a follow-up, revise back into the loop
free_text(1286, 236, "approve →", 10.5, GREEN, anchor="end")
arrow(f'M{COLS["review"] + CW} 282 L1310 282', GREEN, "ag")
box(COLS["review"], 460, CW, 66, "defer", rx=8)
lines(1086, 482, [("DEFER", 13, INK, 600), ("valid but separable —", 10.5, MUTED, None),
                  ("tracked as a follow-up", 10.5, MUTED, None)], COLS["review"], CW, step=16)

# bottom band — receipt and the revision loop
box(70, 560, 430, 122, "receipt", rx=8)
lines(86, 584, [("WHAT THE RECEIPT CONTAINS", 13, INK, 600),
                ("implementation commits, per attempt", 11, "#5c6672", None),
                ("build, test and check output with exit codes", 11, "#5c6672", None),
                ("review verdict, findings, reviewer identity", 11, "#5c6672", None),
                ("usage per leg — reported or marked unavailable", 11, "#5c6672", None)],
      70, 430, step=22)
box(548, 560, 738, 122, "revise", fill="#fbf1ec", stroke=ORANGE, sw=1.4, rx=8)
lines(564, 584, [("REVISE — one micro-task per finding", 14, "#a8461f", 600),
                 ("findings become an ordered ledger, executed one item at a time", 11, "#8a5a44", None),
                 ("each item commits; the ledger is frozen when the batch ends", 11, "#8a5a44", None),
                 ("finalization is deterministic — same tail commit, composed plan", 11, "#8a5a44", None),
                 ("budgets bound the loop; every revision re-verifies before review", 11, "#8a5a44", None)],
      548, 738, step=22)
arrow(f'M{COLS["review"] + 60} 526 L{COLS["review"] + 60} 546 L1286 546', BLUE, "ab", 1.6)
arrow("M700 560 L700 532", ORANGE, "ao", 1.6)

# approval gate and outputs
box(1310, 244, 44, 438, "gate", fill=GREEN, stroke=None, rx=6)
out.append(f'<text x="1332" y="463" font-size="14" letter-spacing="3" fill="#f7f5f0" '
           f'text-anchor="middle" transform="rotate(-90 1332 463)">HUMAN APPROVAL</text>')
box(1390, 262, 170, 50, "merge", rx=6)
lines(1406, 284, [("Merge locally", 13.5, INK, None), ("per your config", 10.5, MUTED, None)],
      1390, 170, step=17)
box(1390, 326, 170, 50, "pr", rx=6)
lines(1406, 348, [("Open a PR", 13.5, INK, None), ("evidence attached", 10.5, MUTED, None)],
      1390, 170, step=17)
arrow("M1354 287 L1390 287", GREEN, "ag")
arrow("M1354 351 L1390 351", GREEN, "ag")
free_text(1390, 412, "You decide", 15, INK, weight=600)
free_text(1390, 434, "what ships.", 15, INK, weight=600)
lines(1390, 470, [("Nothing publishes", 11, MUTED, None), ("without this gate.", 11, MUTED, None)],
      1390, 180, step=16)

# footer
out.append(f'<line x1="60" y1="736" x2="1540" y2="736" stroke="#d8d3c8"/>')
free_text(60, 762, "Orchestration, worktrees, task state and evidence stay local. Worktree isolation "
                   "protects your checkout; it is not a security sandbox — tools run with your permissions.",
          11.5, MUTED)

# ------------------------------------------------------------ invariants
for i, a in enumerate(boxes):
    for b in boxes[i + 1:]:
        overlap = (a[0] < b[0] + b[2] and b[0] < a[0] + a[2]
                   and a[1] < b[1] + b[3] and b[1] < a[1] + a[3])
        assert not overlap, f"boxes overlap: {a[4]} and {b[4]}"

markers = "".join(
    f'<marker id="{mid}" markerWidth="9" markerHeight="9" refX="7.5" refY="3.5" orient="auto">'
    f'<path d="M0,0 L0,7 L8,3.5 z" fill="{colour}"/></marker>'
    for mid, colour in (("ac", TEAL), ("ao", ORANGE), ("ab", BLUE), ("ag", GREEN), ("am", MUTED)))

title = "Selvage architecture: from request to reviewed branch"
desc = ("A local control plane drives external coding CLIs. Surfaces — web dashboard, CLI and MCP — "
        "submit work to a project-scoped scheduler that owns leases, routing, budgets, the evidence "
        "ledger and per-attempt verification plans. The loop runs left to right: a structural code "
        "index orients the implementer, which works in an isolated Git worktree and commits; the "
        "scheduler verifies that commit against a plan pinned for the attempt with a fresh database; "
        "an independent model on a different provider reviews the diff and evidence with no write "
        "tools. Outcomes fan out three ways: approve reaches the human approval gate and then a local "
        "merge or a pull request, revise becomes one micro-task per finding executed in order and "
        "finalized deterministically before re-verification, and separable findings are deferred to a "
        "tracked follow-up. Nothing publishes without human approval.")

sys.stdout.write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'role="img" aria-labelledby="t d" '
    f'font-family="\'IBM Plex Mono\',\'SFMono-Regular\',ui-monospace,Menlo,monospace">'
    f'<title id="t">{title}</title><desc id="d">{desc}</desc>'
    f'<defs>{markers}</defs>' + "".join(out) + '</svg>\n')
