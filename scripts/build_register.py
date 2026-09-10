#!/usr/bin/env python3
"""build_register.py: generate provisions.md, the register of citable provisions.

Each id is bound to the words on its recorded line of the standard and carries OWASP's own address
for that line: the category, the subsection and the item number, as a reader finds them in the PDF.
verify.py fails when the words move. Run this only when the standard itself has been replaced, then
read `git diff provisions.md` before committing.

    python3 scripts/build_register.py                 # write provisions.md
    python3 scripts/build_register.py --address 295   # print the address of one line
"""
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = "reference/owasp-top-10-agentic-applications-2026.txt"
OUT = ROOT / "provisions.md"

REGISTER = [
    # (id, line, what a finding uses it for)
    # ---- cross-cutting, from the standard's own front matter ----
    ("ASI00-LEAST-AGENCY", 182, "Least-Agency: autonomy where not needed is attack surface"),
    ("ASI00-OBSERVABILITY", 183, "Observability as non-negotiable"),

    # ---- ASI01 Agent Goal Hijack ----
    ("ASI01", 235, "Category heading"),
    ("ASI01-ONE-CHANNEL", 240, "Root cause: instructions and content are indistinguishable"),
    ("ASI01-VECTORS", 242, "Vectors incl. deceptive tool outputs and forged agent messages"),
    ("ASI01-MIT", 282, "Mitigation section heading"),
    ("ASI01-UNTRUSTED-INPUT", 283, "Treat all natural-language input as untrusted before tool calls"),
    ("ASI01-LEAST-PRIVILEGE", 286, "Least privilege plus human approval for high-impact actions"),
    ("ASI01-LOCK-PROMPTS", 288, "Define and lock system prompts so goals and permitted actions are explicit and auditable"),

    # ---- ASI02 Tool Misuse and Exploitation ----
    ("ASI02", 318, "Category heading"),
    ("ASI02-MIT", 372, "Mitigation section heading"),
    ("ASI02-TOOL-PROFILES", 376, "Per-tool least-privilege profiles; read-only queries, no send/delete rights. The provision a well-scoped tool grant satisfies"),
    ("ASI02-IAM-STANZAS", 380, "Express those profiles as policy stanzas rather than ad-hoc convention"),
    ("ASI02-EGRESS", 388, "Outbound allowlists; deny non-approved network destinations"),
    ("ASI02-CONFIRM", 384, "Human confirmation for destructive actions; dry-run diff"),
    ("ASI02-QUALIFIED-NAMES", 396, "Fully qualified tool names and version pins"),
    ("ASI02-TOOL-LOGS", 400, "Immutable logs of all tool invocations"),

    # ---- ASI03 Identity and Privilege Abuse ----
    ("ASI03", 414, "Category heading"),
    ("ASI03-INHERITANCE", 436, "Un-scoped privilege inheritance from a high-privilege manager"),
    ("ASI03-CONFUSED-DEPUTY", 445, "Internal requests trusted by default"),
    ("ASI03-SYNTHETIC-IDENTITY", 452, "Impersonation via unverified self-declared descriptors"),
    ("ASI03-MIT", 478, "Mitigation section heading"),
    ("ASI03-SCOPED-TOKENS", 479, "Short-lived, narrowly scoped, task-bound tokens"),
    ("ASI03-REVALIDATE", 500, "No privilege inheritance unless intent is re-validated"),

    # ---- ASI04 Agentic Supply Chain ----
    ("ASI04", 514, "Category heading"),
    ("ASI04-SCOPE", 520, "Other agents, MCP and A2A interfaces are in scope"),
    ("ASI04-RUNTIME-LOADING", 525, "Runtime loading of external tools and agent personas"),
    ("ASI04-THIRD-PARTY-AGENT", 546, "A peer agent used to pivot, leak, or relay instructions"),
    ("ASI04-MIT", 575, "Mitigation section heading"),
    ("ASI04-PROMPT-REVIEW", 583, "Prompts and orchestration scripts under version control with peer review; scan for anomalies"),
    ("ASI04-REGISTRIES", 578, "Curated registries; block untrusted sources"),
    ("ASI04-GATEKEEPING", 579, "Allowlist and pin; verify provenance; auto-reject unverified"),
    ("ASI04-SANDBOX", 581, "Sandboxed containers with network or syscall limits"),
    ("ASI04-RECHECK", 587, "Re-check signatures, hashes and SBOMs at runtime"),
    ("ASI04-PIN", 589, "Pin prompts, tools and configs by content hash and commit id"),

    # ---- ASI05 Unexpected Code Execution ----
    ("ASI05", 606, "Category heading"),
    ("ASI05-RUNAWAY", 634, "Scenario: unreviewed generated commands destroy production data"),
    ("ASI05-MIT", 658, "Mitigation section heading"),
    ("ASI05-OUTPUT-HANDLING", 659, "Validate and encode agent-generated code"),
    ("ASI05-NO-DIRECT-PROD", 661, "No direct agent-to-production; pre-production checks"),
    ("ASI05-BAN-EVAL", 664, "Ban eval; safe interpreters and taint tracking"),
    ("ASI05-ENV-SECURITY", 665, "Never run as root; sandboxed containers; restrict filesystem"),
    ("ASI05-SEPARATE-EXEC", 670, "Separate code generation from execution with validation gates"),
    ("ASI05-APPROVALS", 672, "Human approval for elevated runs; versioned auto-execution allowlist"),

    # ---- ASI06 Memory and Context Poisoning ----
    ("ASI06", 681, "Category heading"),
    ("ASI06-POISONING", 688, "Corrupted context biases future reasoning and tool use"),
    ("ASI06-UNTRUSTED-SOURCES", 690, "Peer-agent exchanges among untrusted ingestion sources"),
    ("ASI06-CROSS-AGENT", 718, "Contaminated shared memory spreads between agents"),
    ("ASI06-MIT", 733, "Mitigation section heading"),
    ("ASI06-BASELINE", 734, "Encryption plus least-privilege access to memory"),
    ("ASI06-VALIDATE-WRITES", 735, "Scan all memory writes and model outputs before commit"),
    ("ASI06-SEGMENTATION", 737, "Isolate sessions and domain contexts"),
    ("ASI06-CURATED-SOURCES", 739, "Only authenticated, curated sources; minimise retention"),
    ("ASI06-PROVENANCE", 741, "Source attribution and anomaly detection on updates"),
    ("ASI06-NO-SELF-INGEST", 744, "No automatic re-ingestion of the agent's own output (bootstrap poisoning)"),
    ("ASI06-ROLLBACK", 746, "Adversarial test, snapshots, rollback, human review for high risk"),
    ("ASI06-EXPIRE", 750, "Expire unverified memory to limit poison persistence"),

    # ---- ASI07 Insecure Inter-Agent Communication ----
    ("ASI07", 772, "Category heading"),
    ("ASI07-NO-AUTH", 780, "Exchanges lacking authentication, integrity or semantic validation"),
    ("ASI07-MIT", 822, "Mitigation section heading"),
    ("ASI07-CHANNELS", 823, "Per-agent credentials and mutual authentication"),
    ("ASI07-SIGNING", 826, "Sign messages; validate for hidden or modified instructions"),
    ("ASI07-AGENT-CARDS", 848, "Signed agent cards; verification before accepting coordination"),
    ("ASI07-TYPED-CONTRACTS", 852, "Versioned, typed message schemas with explicit audiences"),

    # ---- ASI08 Cascading Failures ----
    ("ASI08", 863, "Category heading"),
    ("ASI08-COUPLING", 895, "Planner-executor coupling: unsafe steps performed without validation"),
    ("ASI08-AUTOREMEDIATION", 925, "Scenario: suppressed alerts read as success, automation widens"),
    ("ASI08-MIT", 935, "Mitigation section heading"),
    ("ASI08-POLICY-ENGINE", 944, "Separate planning and execution via an external policy engine"),
    ("ASI08-GATES", 946, "Checkpoints, governance agents, or human review before propagation"),
    ("ASI08-BLAST-RADIUS", 949, "Quotas, progress caps, circuit breakers between planner and executor"),
    ("ASI08-NON-REPUDIATION", 957, "Tamper-evident logs of inter-agent messages and decisions"),

    # ---- ASI09 Human-Agent Trust Exploitation ----
    ("ASI09", 965, "Category heading"),
    ("ASI09-EXPLAINABILITY", 986, "Opaque reasoning forces users to trust what they cannot question"),
    ("ASI09-MISSING-CONFIRM", 989, "No final verification step turns trust into irreversible action"),
    ("ASI09-FAKE-EXPLAIN", 997, "Fabricated rationales that hide unsafe logic"),
    ("ASI09-MIT", 1022, "Mitigation section heading"),
    ("ASI09-EXPLICIT-CONFIRM", 1023, "Multi-step approval or human in the loop before risky actions"),
    ("ASI09-IMMUTABLE-LOGS", 1025, "Tamper-proof records of queries and agent actions"),
    ("ASI09-RISK-SUMMARY", 1030, "Plain-language risk summary, not model-generated rationales"),
    ("ASI09-CONTENT-PROVENANCE", 1040, "Verifiable metadata on all recommendations and external data"),
    ("ASI09-PREVIEW", 1044, "Separate preview from effect; risk badge with side effects"),

    # ---- ASI10 Rogue Agents ----
    ("ASI10", 1062, "Category heading"),
    ("ASI10-DEFINITION", 1065, "Agents deviating from intended function or authorised scope"),
    ("ASI10-DRIFT", 1071, "Loss of behavioural integrity once drift begins"),
    ("ASI10-REWARD-HACKING", 1089, "Agents game flawed metrics into misaligned strategies"),
    ("ASI10-REWARD-SCENARIO", 1104, "Scenario: cost-minimising agent deletes production backups"),
    ("ASI10-MIT", 1107, "Mitigation section heading"),
    ("ASI10-AUDIT-LOGS", 1108, "Immutable, signed audit logs of all actions and tool calls"),
    ("ASI10-ISOLATION", 1111, "Trust zones and restricted execution environments"),
    ("ASI10-WATCHDOG", 1114, "Behavioural detection; watchdog agents validating peer output"),
    ("ASI10-KILL-SWITCH", 1117, "Kill switches and credential revocation to disable rogue agents"),
    ("ASI10-ATTESTATION", 1120, "Per-agent cryptographic identity attestation"),
    ("ASI10-MANIFESTS", 1122, "Signed behavioural manifests validated before each action"),
]

# OWASP's five subsection labels: the name of the subsection, and of a numbered item inside it.
SUBSECTIONS = {
    "Description": ("Description", None),
    "Common Examples of the Vulnerability": ("Common Examples", "Common Example"),
    "Example Attack Scenarios": ("Attack Scenarios", "Attack Scenario"),
    "Prevention and Mitigation Guidelines": ("Mitigations", "Mitigation"),
    "References": ("References", "Reference"),
}

# The parts outside the ten categories, by the exact line that opens each.
PARTS = {
    "Table of Content": "Table of Content",
    "Letter from The Agentic Top 10": "Letter from the Leaders",
    "Agentic Top 10 At A Glance": "Agentic Top 10 At A Glance",
    "Acknowledgements": "Acknowledgements",
    "Project Supporters": "Project Supporters",
}
APPENDIX = re.compile(r"^Appendix ([A-E]) [-–]")
CATEGORY = re.compile(r"^## (ASI\d\d):")
SUBSECTION = re.compile(r"^### (.+)$")
ITEM = re.compile(r"^(\d+)\. ")


def address(lines, n):
    """OWASP's address for line n of the standard: a part of the document, or a category with its
    subsection and item number ("ASI04 Mitigation 7")."""
    part, category, section, item = "Front matter", None, None, None
    seen_category = False
    for text in (ln.strip() for ln in lines[:n]):
        heading = CATEGORY.match(text)
        appendix = APPENDIX.match(text)
        sub = SUBSECTION.match(text)
        if heading:
            category, section, item, seen_category = heading.group(1), None, None, True
        elif text in PARTS or (appendix and seen_category):
            part = PARTS[text] if text in PARTS else f"Appendix {appendix.group(1)}"
            category, section, item = None, None, None
        elif category and sub and sub.group(1) in SUBSECTIONS:
            section, item = sub.group(1), None
        elif category and section and SUBSECTIONS[section][1] and ITEM.match(text):
            item = ITEM.match(text).group(1)
    if not category:
        return part
    if not section:
        return category
    name, item_name = SUBSECTIONS[section]
    return f"{category} {item_name} {item}" if item and item_name else f"{category} {name}"


HEADER = """<!--
  GENERATED by scripts/build_register.py. Do not edit by hand.
-->

# The register: every provision this auditor may cite

_Last updated: {date}_

Cite a provision by its OWASP address, with the id as the link title and the current line as the
link target:

```
[ASI04 Mitigation 7](reference/owasp-top-10-agentic-applications-2026.txt#L589 "^ASI04-PIN")
```

The address is where the provision sits in the PDF: category, subsection, item number. Each row
records the first line of a provision; most run across two or three. Read the provision in
`reference/`, or print it whole, before citing it:

```bash
bash scripts/cite.sh ASI04-PIN           # one provision
bash scripts/cite.sh --from examples.md  # every citation in a document
```

`python3 scripts/verify.py` fails when a recorded line no longer holds its recorded words, or when a
citation's text is not the address of the line it cites.

Bare ids (`ASI04`) are category headings; ids ending in `-MIT` are mitigation-section headings.
Cite the narrowest id that carries the claim.

| id | line | address | the provision, verbatim | cited for |
|---|---|---|---|---|
"""


def main() -> int:
    path = ROOT / REF
    if not path.exists():
        print(f"REFUSING to write the register: {REF} missing", file=sys.stderr)
        return 1
    lines = path.read_text(encoding="utf-8").split("\n")
    if len(sys.argv) == 3 and sys.argv[1] == "--address":
        print(address(lines, int(sys.argv[2])))
        return 0
    rows, problems = [], []
    for pid, ln, purpose in REGISTER:
        if not 0 < ln <= len(lines):
            problems.append(f"{pid}: line {ln} outside {REF}")
            continue
        text = lines[ln - 1].strip()
        if not text:
            problems.append(f"{pid}: {REF} line {ln} is blank")
            continue
        cell = text.replace("|", "\\|")
        rows.append(f"| `{pid}` | {ln} | {address(lines, ln)} | {cell} | {purpose} |")

    if problems:
        print("REFUSING to write the register:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1

    header = HEADER.format(date=datetime.date.today().isoformat())
    OUT.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"wrote provisions.md: {len(rows)} provisions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
