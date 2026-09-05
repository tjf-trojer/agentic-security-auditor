#!/usr/bin/env python3
"""Normalise the layout of the OWASP Top 10 for Agentic Applications 2026 text
extraction so findings can cite it by line.

Changes made (and only these):
  1. Remove PDF page-footer lines ("genai.owasp.org  Page N").
  2. Rejoin the ten category headings that the PDF extraction split across
     lines, and mark them as level-2 markdown headings.
  3. Mark the five recurring subsection labels as level-3 markdown headings.

No wording is altered, added, or removed.
"""

import re
import sys

SRC = sys.argv[1]
DST = sys.argv[2]

CANONICAL = {
    "ASI01": "ASI01: Agent Goal Hijack",
    "ASI02": "ASI02: Tool Misuse and Exploitation",
    "ASI03": "ASI03: Identity and Privilege Abuse",
    "ASI04": "ASI04: Agentic Supply Chain Vulnerabilities",
    "ASI05": "ASI05: Unexpected Code Execution (RCE)",
    "ASI06": "ASI06: Memory & Context Poisoning",
    "ASI07": "ASI07: Insecure Inter-Agent Communication",
    "ASI08": "ASI08: Cascading Failures",
    "ASI09": "ASI09: Human-Agent Trust Exploitation",
    "ASI10": "ASI10: Rogue Agents",
}

SUBHEADINGS = {
    "Description",
    "Common Examples of the Vulnerability",
    "Example Attack Scenarios",
    "Prevention and Mitigation Guidelines",
    "References",
}

PAGE_FOOTER = re.compile(r"^genai\.owasp\.org\s+Page\s+\d+\s*$")
HEADING_START = re.compile(r"^(ASI\d{2}):")

lines = open(SRC, encoding="utf-8").read().split("\n")

# Pass 1: drop page footers.
lines = [ln for ln in lines if not PAGE_FOOTER.match(ln.strip())]

# Pass 2: promote body headings and subheadings.
out = []
i = 0
n = len(lines)
promoted = []
while i < n:
    line = lines[i]
    stripped = line.strip()
    m = HEADING_START.match(stripped)
    if m:
        code = m.group(1)
        # A body heading is followed (within 3 lines, ignoring blanks and
        # heading continuation fragments) by the literal line "Description".
        j = i + 1
        lookahead = []
        while j < n and len(lookahead) < 3:
            nxt = lines[j].strip()
            if nxt:
                lookahead.append(nxt)
            j += 1
        if "Description" in lookahead:
            # Consume this line plus any continuation fragments before
            # "Description".
            k = i + 1
            while k < n and lines[k].strip() != "Description":
                k += 1
            out.append("## " + CANONICAL[code])
            out.append("")
            promoted.append((code, len(out)))
            i = k
            continue
    if stripped in SUBHEADINGS:
        out.append("### " + stripped)
        i += 1
        continue
    out.append(line)
    i += 1

open(DST, "w", encoding="utf-8").write("\n".join(out))

print(f"wrote {DST}: {len(out)} lines (source {n})")
print(f"promoted {len(promoted)} category headings: {[c for c, _ in promoted]}")
