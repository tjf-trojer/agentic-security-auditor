#!/usr/bin/env python3
"""build_register.py — generate provisions.md, the register of citable provisions.

Why a register exists. A finding cites a line. Line numbers move, and a citation
that has moved is worse than no citation: it still looks authoritative. So each
citable provision gets a stable id, and the line number becomes a *derived*,
clickable form of that id rather than the identity itself.

Why the anchor is not written into the reference text. In the workspace this
convention comes from, anchors are markers appended to the corpus (`^art22-abs1`)
because that corpus is ours to mark. This corpus is not: it is OWASP's document,
redistributed under CC BY-SA 4.0 with a disclosure that no word was added. So the
anchor here is the provision's **own opening words**, recorded in the register,
and the line is found by matching them.

That turns out to be the stronger form. An inline marker survives an edit to the
text it marks; a text key does not, and must not. If OWASP publishes a 2027
edition and a provision is reworded, `--check` fails loudly and names the id that
moved, which is exactly the moment a human should look. A marker would have
followed the change silently and kept a stale citation looking correct.

    python3 scripts/build_register.py            # regenerate provisions.md
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "reference" / "owasp-top-10-agentic-applications-2026.md"
OUT = ROOT / "provisions.md"

# id -> line number in the reference at the time of writing. The line is a hint
# for the generator only; the text it finds there becomes the durable key.
REGISTER = [
    # (id, line, what a finding uses it for)
    ("ASI00-LEAST-AGENCY", 182, "The standard's Least-Agency principle, cross-cutting"),
    ("ASI00-OBSERVABILITY", 183, "Observability as non-negotiable, cross-cutting"),

    ("ASI01", 235, "Category heading: Agent Goal Hijack"),
    ("ASI01-ONE-CHANNEL", 240, "Root cause: instructions and content are indistinguishable"),
    ("ASI01-MIT", 282, "Mitigation section heading"),
    ("ASI01-UNTRUSTED-INPUT", 283, "Treat all natural-language input as untrusted, before it reaches tool calls"),
    ("ASI01-LEAST-PRIVILEGE", 286, "Least privilege for tools plus human approval for high-impact actions"),

    ("ASI02", 318, "Category heading: Tool Misuse and Exploitation"),
    ("ASI02-MIT", 372, "Mitigation section heading"),
    ("ASI02-CONFIRM", 384, "Human confirmation for destructive actions; pre-execution plan or dry-run diff"),

    ("ASI03", 414, "Category heading: Identity and Privilege Abuse"),
    ("ASI03-INHERITANCE", 436, "Un-scoped privilege inheritance from a high-privilege manager"),
    ("ASI03-CONFUSED-DEPUTY", 445, "Cross-agent trust exploitation: internal requests trusted by default"),
    ("ASI03-MIT", 478, "Mitigation section heading"),
    ("ASI03-SCOPED-TOKENS", 479, "Short-lived, narrowly scoped, task-bound tokens"),
    ("ASI03-REVALIDATE", 500, "Prevent privilege inheritance across agents unless intent is re-validated"),

    ("ASI04", 514, "Category heading: Agentic Supply Chain Vulnerabilities"),
    ("ASI04-MIT", 575, "Mitigation section heading"),
    ("ASI04-REGISTRIES", 578, "Curated registries; block untrusted sources"),
    ("ASI04-GATEKEEPING", 579, "Allowlist and pin; verify provenance before install; auto-reject unverified"),
    ("ASI04-SANDBOX", 581, "Run sensitive agents in sandboxed containers with network or syscall limits"),
    ("ASI04-RECHECK", 587, "Re-check signatures, hashes and SBOMs at runtime; monitor lineage"),
    ("ASI04-PIN", 589, "Pin prompts, tools and configs by content hash and commit id"),

    ("ASI05", 606, "Category heading: Unexpected Code Execution (RCE)"),
    ("ASI05-MIT", 658, "Mitigation section heading"),

    ("ASI06", 681, "Category heading: Memory and Context Poisoning"),
    ("ASI06-POISONING", 688, "Adversaries corrupt or seed retained context, biasing future reasoning"),
    ("ASI06-MIT", 733, "Mitigation section heading"),

    ("ASI07", 772, "Category heading: Insecure Inter-Agent Communication"),
    ("ASI07-NO-AUTH", 780, "Exchanges lacking authentication, integrity or semantic validation"),
    ("ASI07-MIT", 822, "Mitigation section heading"),
    ("ASI07-CHANNELS", 823, "Per-agent credentials and mutual authentication"),
    ("ASI07-SIGNING", 826, "Sign messages; validate for hidden or modified instructions"),
    ("ASI07-AGENT-CARDS", 848, "Signed agent cards and continuous verification before accepting coordination"),

    ("ASI08", 863, "Category heading: Cascading Failures"),
    ("ASI08-COUPLING", 895, "Planner-executor coupling: unsafe steps performed without validation"),
    ("ASI08-MIT", 935, "Mitigation section heading"),
    ("ASI08-POLICY-ENGINE", 944, "Separate planning and execution via an external policy engine"),
    ("ASI08-GATES", 946, "Checkpoints, governance agents, or human review before outputs propagate"),
    ("ASI08-BLAST-RADIUS", 949, "Quotas, progress caps, circuit breakers between planner and executor"),

    ("ASI09", 965, "Category heading: Human-Agent Trust Exploitation"),
    ("ASI09-MIT", 1022, "Mitigation section heading"),
    ("ASI09-EXPLICIT-CONFIRM", 1023, "Multi-step approval or human in the loop before risky actions"),
    ("ASI09-IMMUTABLE-LOGS", 1025, "Tamper-proof records of queries and agent actions"),
    ("ASI09-RISK-SUMMARY", 1030, "Plain-language risk summary, not model-generated rationales"),
    ("ASI09-PREVIEW", 1044, "Separate preview from effect; risk badge with provenance and side effects"),

    ("ASI10", 1062, "Category heading: Rogue Agents"),
    ("ASI10-MIT", 1107, "Mitigation section heading"),
]

HEADER = """<!--
  GENERATED by scripts/build_register.py. Do not edit by hand.
  Regenerate:  python3 scripts/build_register.py
  Verify:      python3 scripts/verify.py
-->

# The register: every provision this auditor may cite

A finding cites a line of the standard. Line numbers move. A citation that has
moved is worse than no citation, because it still looks authoritative.

So every citable provision has a **stable id**, and the line number in a citation
is a *derived*, clickable form of that id:

```
[ASI04-PIN](reference/owasp-top-10-agentic-applications-2026.md#L589 "^ASI04-PIN")
```

The id sits in the link title, where it survives; the line number sits in the
link target, where it is convenient. `scripts/verify.py` recomputes every line
from its id and fails if any has drifted.

**The id resolves against the provision's own words, not against a marker.** The
reference text is OWASP's, redistributed unaltered, so nothing was inserted into
it to serve as an anchor. Each id is bound to the opening words of its provision,
recorded below, and located by matching them. If OWASP publishes a new edition and
a provision is reworded, that match fails and names the id, which is exactly when a
human should look. A marker would have moved with the edit and kept a stale
citation looking correct.

**To read a provision without opening a file:**

```bash
bash scripts/cite.sh ASI04-PIN          # print the provision
bash scripts/cite.sh --from examples.md # every citation in a document
```

Ids ending in `-MIT` are the mitigation-section headings, cited when a finding
rests on a category's remedies as a whole rather than on one of them. Bare
category ids (`ASI04`) are the section headings.

| id | line | the provision, verbatim | cited for |
|---|---|---|---|
"""


def main() -> int:
    lines = REF.read_text(encoding="utf-8").split("\n")
    rows, problems = [], []
    for pid, ln, purpose in REGISTER:
        if not 0 < ln <= len(lines):
            problems.append(f"{pid}: line {ln} out of range")
            continue
        text = lines[ln - 1].strip()
        if not text:
            problems.append(f"{pid}: line {ln} is blank")
            continue
        # The register stores the line verbatim. Pipes would break the table.
        cell = text.replace("|", "\\|")
        rows.append(f"| `{pid}` | {ln} | {cell} | {purpose} |")

    if problems:
        print("REFUSING to write the register:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1

    OUT.write_text(HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} provisions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
