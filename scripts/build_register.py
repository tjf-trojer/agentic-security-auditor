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
OUT = ROOT / "provisions.md"

REGISTER = [
    # (id, source, line, what a finding uses it for)
    # ---- cross-cutting, from the standard's own front matter ----
    ("ASI00-LEAST-AGENCY", "owasp", 182, "Least-Agency: autonomy where not needed is attack surface"),
    ("ASI00-OBSERVABILITY", "owasp", 183, "Observability as non-negotiable"),

    # ---- ASI01 Agent Goal Hijack ----
    ("ASI01", "owasp", 235, "Category heading"),
    ("ASI01-ONE-CHANNEL", "owasp", 240, "Root cause: instructions and content are indistinguishable"),
    ("ASI01-VECTORS", "owasp", 242, "Vectors incl. deceptive tool outputs and forged agent messages"),
    ("ASI01-MIT", "owasp", 282, "Mitigation section heading"),
    ("ASI01-UNTRUSTED-INPUT", "owasp", 283, "Treat all natural-language input as untrusted before tool calls"),
    ("ASI01-LEAST-PRIVILEGE", "owasp", 286, "Least privilege plus human approval for high-impact actions"),

    # ---- ASI02 Tool Misuse and Exploitation ----
    ("ASI02", "owasp", 318, "Category heading"),
    ("ASI02-MIT", "owasp", 372, "Mitigation section heading"),
    ("ASI02-TOOL-PROFILES", "owasp", 376, "Per-tool least-privilege profiles; read-only queries, no send/delete rights. The provision a well-scoped tool grant satisfies"),
    ("ASI02-IAM-STANZAS", "owasp", 380, "Express those profiles as policy stanzas rather than ad-hoc convention"),
    ("ASI02-EGRESS", "owasp", 388, "Outbound allowlists; deny non-approved network destinations"),
    ("ASI02-CONFIRM", "owasp", 384, "Human confirmation for destructive actions; dry-run diff"),
    ("ASI02-QUALIFIED-NAMES", "owasp", 396, "Fully qualified tool names and version pins"),
    ("ASI02-TOOL-LOGS", "owasp", 400, "Immutable logs of all tool invocations"),

    # ---- ASI03 Identity and Privilege Abuse ----
    ("ASI03", "owasp", 414, "Category heading"),
    ("ASI03-INHERITANCE", "owasp", 436, "Un-scoped privilege inheritance from a high-privilege manager"),
    ("ASI03-CONFUSED-DEPUTY", "owasp", 445, "Internal requests trusted by default"),
    ("ASI03-SYNTHETIC-IDENTITY", "owasp", 452, "Impersonation via unverified self-declared descriptors"),
    ("ASI03-MIT", "owasp", 478, "Mitigation section heading"),
    ("ASI03-SCOPED-TOKENS", "owasp", 479, "Short-lived, narrowly scoped, task-bound tokens"),
    ("ASI03-REVALIDATE", "owasp", 500, "No privilege inheritance unless intent is re-validated"),

    # ---- ASI04 Agentic Supply Chain ----
    ("ASI04", "owasp", 514, "Category heading"),
    ("ASI04-SCOPE", "owasp", 520, "Other agents, MCP and A2A interfaces are in scope"),
    ("ASI04-RUNTIME-LOADING", "owasp", 525, "Runtime loading of external tools and agent personas"),
    ("ASI04-THIRD-PARTY-AGENT", "owasp", 546, "A peer agent used to pivot, leak, or relay instructions"),
    ("ASI04-MIT", "owasp", 575, "Mitigation section heading"),
    ("ASI04-REGISTRIES", "owasp", 578, "Curated registries; block untrusted sources"),
    ("ASI04-GATEKEEPING", "owasp", 579, "Allowlist and pin; verify provenance; auto-reject unverified"),
    ("ASI04-SANDBOX", "owasp", 581, "Sandboxed containers with network or syscall limits"),
    ("ASI04-RECHECK", "owasp", 587, "Re-check signatures, hashes and SBOMs at runtime"),
    ("ASI04-PIN", "owasp", 589, "Pin prompts, tools and configs by content hash and commit id"),

    # ---- ASI05 Unexpected Code Execution ----
    ("ASI05", "owasp", 606, "Category heading"),
    ("ASI05-RUNAWAY", "owasp", 634, "Scenario: unreviewed generated commands destroy production data"),
    ("ASI05-MIT", "owasp", 658, "Mitigation section heading"),
    ("ASI05-OUTPUT-HANDLING", "owasp", 659, "Validate and encode agent-generated code"),
    ("ASI05-NO-DIRECT-PROD", "owasp", 661, "No direct agent-to-production; pre-production checks"),
    ("ASI05-BAN-EVAL", "owasp", 664, "Ban eval; safe interpreters and taint tracking"),
    ("ASI05-ENV-SECURITY", "owasp", 665, "Never run as root; sandboxed containers; restrict filesystem"),
    ("ASI05-SEPARATE-EXEC", "owasp", 670, "Separate code generation from execution with validation gates"),
    ("ASI05-APPROVALS", "owasp", 672, "Human approval for elevated runs; versioned auto-execution allowlist"),

    # ---- ASI06 Memory and Context Poisoning ----
    ("ASI06", "owasp", 681, "Category heading"),
    ("ASI06-POISONING", "owasp", 688, "Corrupted context biases future reasoning and tool use"),
    ("ASI06-UNTRUSTED-SOURCES", "owasp", 690, "Peer-agent exchanges among untrusted ingestion sources"),
    ("ASI06-CROSS-AGENT", "owasp", 718, "Contaminated shared memory spreads between agents"),
    ("ASI06-MIT", "owasp", 733, "Mitigation section heading"),
    ("ASI06-BASELINE", "owasp", 734, "Encryption plus least-privilege access to memory"),
    ("ASI06-VALIDATE-WRITES", "owasp", 735, "Scan all memory writes and model outputs before commit"),
    ("ASI06-SEGMENTATION", "owasp", 737, "Isolate sessions and domain contexts"),
    ("ASI06-CURATED-SOURCES", "owasp", 739, "Only authenticated, curated sources; minimise retention"),
    ("ASI06-PROVENANCE", "owasp", 741, "Source attribution and anomaly detection on updates"),
    ("ASI06-NO-SELF-INGEST", "owasp", 744, "No automatic re-ingestion of the agent's own output (bootstrap poisoning)"),
    ("ASI06-ROLLBACK", "owasp", 746, "Adversarial test, snapshots, rollback, human review for high risk"),
    ("ASI06-EXPIRE", "owasp", 750, "Expire unverified memory to limit poison persistence"),

    # ---- ASI07 Insecure Inter-Agent Communication ----
    ("ASI07", "owasp", 772, "Category heading"),
    ("ASI07-NO-AUTH", "owasp", 780, "Exchanges lacking authentication, integrity or semantic validation"),
    ("ASI07-MIT", "owasp", 822, "Mitigation section heading"),
    ("ASI07-CHANNELS", "owasp", 823, "Per-agent credentials and mutual authentication"),
    ("ASI07-SIGNING", "owasp", 826, "Sign messages; validate for hidden or modified instructions"),
    ("ASI07-AGENT-CARDS", "owasp", 848, "Signed agent cards; verification before accepting coordination"),
    ("ASI07-TYPED-CONTRACTS", "owasp", 852, "Versioned, typed message schemas with explicit audiences"),

    # ---- ASI08 Cascading Failures ----
    ("ASI08", "owasp", 863, "Category heading"),
    ("ASI08-COUPLING", "owasp", 895, "Planner-executor coupling: unsafe steps performed without validation"),
    ("ASI08-AUTOREMEDIATION", "owasp", 925, "Scenario: suppressed alerts read as success, automation widens"),
    ("ASI08-MIT", "owasp", 935, "Mitigation section heading"),
    ("ASI08-POLICY-ENGINE", "owasp", 944, "Separate planning and execution via an external policy engine"),
    ("ASI08-GATES", "owasp", 946, "Checkpoints, governance agents, or human review before propagation"),
    ("ASI08-BLAST-RADIUS", "owasp", 949, "Quotas, progress caps, circuit breakers between planner and executor"),
    ("ASI08-NON-REPUDIATION", "owasp", 957, "Tamper-evident logs of inter-agent messages and decisions"),

    # ---- ASI09 Human-Agent Trust Exploitation ----
    ("ASI09", "owasp", 965, "Category heading"),
    ("ASI09-EXPLAINABILITY", "owasp", 986, "Opaque reasoning forces users to trust what they cannot question"),
    ("ASI09-MISSING-CONFIRM", "owasp", 989, "No final verification step turns trust into irreversible action"),
    ("ASI09-FAKE-EXPLAIN", "owasp", 997, "Fabricated rationales that hide unsafe logic"),
    ("ASI09-MIT", "owasp", 1022, "Mitigation section heading"),
    ("ASI09-EXPLICIT-CONFIRM", "owasp", 1023, "Multi-step approval or human in the loop before risky actions"),
    ("ASI09-IMMUTABLE-LOGS", "owasp", 1025, "Tamper-proof records of queries and agent actions"),
    ("ASI09-RISK-SUMMARY", "owasp", 1030, "Plain-language risk summary, not model-generated rationales"),
    ("ASI09-CONTENT-PROVENANCE", "owasp", 1040, "Verifiable metadata on all recommendations and external data"),
    ("ASI09-PREVIEW", "owasp", 1044, "Separate preview from effect; risk badge with side effects"),

    # ---- ASI10 Rogue Agents ----
    ("ASI10", "owasp", 1062, "Category heading"),
    ("ASI10-DEFINITION", "owasp", 1065, "Agents deviating from intended function or authorised scope"),
    ("ASI10-DRIFT", "owasp", 1071, "Loss of behavioural integrity once drift begins"),
    ("ASI10-REWARD-HACKING", "owasp", 1089, "Agents game flawed metrics into misaligned strategies"),
    ("ASI10-REWARD-SCENARIO", "owasp", 1104, "Scenario: cost-minimising agent deletes production backups"),
    ("ASI10-MIT", "owasp", 1107, "Mitigation section heading"),
    ("ASI10-AUDIT-LOGS", "owasp", 1108, "Immutable, signed audit logs of all actions and tool calls"),
    ("ASI10-ISOLATION", "owasp", 1111, "Trust zones and restricted execution environments"),
    ("ASI10-WATCHDOG", "owasp", 1114, "Behavioural detection; watchdog agents validating peer output"),
    ("ASI10-KILL-SWITCH", "owasp", 1117, "Kill switches and credential revocation to disable rogue agents"),
    ("ASI10-ATTESTATION", "owasp", 1120, "Per-agent cryptographic identity attestation"),
    ("ASI10-MANIFESTS", "owasp", 1122, "Signed behavioural manifests validated before each action"),

    # ---- EU AI Act, the conditional second anchor ----
    ("AIA-3", "act", 58, "Article 3, definitions"),
    ("AIA-3-23", "act", 167, "3(23) substantial modification"),
    ("AIA-12", "act", 418, "Article 12, record-keeping"),
    ("AIA-14", "act", 460, "Article 14, human oversight"),
    ("AIA-25", "act", 538, "Article 25, responsibilities along the value chain"),
    ("AIA-26", "act", 607, "Article 26, deployer obligations"),
    ("AIA-50-1", "act", 742, "50(1) disclosure that a person is interacting with an AI system"),
    ("AIA-50-2", "act", 750, "50(2) machine-readable marking of synthetic output"),
    ("AIA-72", "act", 825, "Article 72, post-market monitoring"),
    ("AIA-ANNEX-III", "act", 871, "Annex III, the list of high-risk uses"),
    ("AIA-III-1", "act", 877, "Annex III(1) biometrics"),
    ("AIA-III-2", "act", 892, "Annex III(2) critical infrastructure"),
    ("AIA-III-3", "act", 897, "Annex III(3) education and vocational training"),
    ("AIA-III-4", "act", 917, "Annex III(4) employment and workers' management"),
    ("AIA-III-5", "act", 930, "Annex III(5) essential private and public services"),
    ("AIA-III-6", "act", 959, "Annex III(6) law enforcement"),
    ("AIA-III-7", "act", 986, "Annex III(7) migration, asylum and border control"),
    ("AIA-III-8", "act", 1008, "Annex III(8) administration of justice and democratic processes"),
]

SOURCES = {
    "owasp": ("reference/owasp-top-10-agentic-applications-2026.md", "OWASP"),
    "act": ("reference/eu-ai-act-2024-1689-excerpts.md", "AI Act"),
}

HEADER = """<!--
  GENERATED by scripts/build_register.py. Do not edit by hand.
  Regenerate:  python3 scripts/build_register.py
  Verify:      python3 scripts/verify.py
-->

# The register: every provision this auditor may cite

_Last updated: 2026-09-05_

A finding cites a line. Line numbers move. A citation that has moved is worse than
no citation, because it still looks authoritative.

So every citable provision has a **stable id**, and the line number in a citation
is a *derived*, clickable form of that id:

```
[ASI04-PIN](reference/owasp-top-10-agentic-applications-2026.md#L589 "^ASI04-PIN")
```

The id sits in the link title, where it survives; the line number sits in the link
target, where it is convenient. `python3 scripts/verify.py` recomputes every line
from its id and fails if any has drifted.

**The id resolves against the provision's own words, not against a marker.** The
reference texts are OWASP's and the EU's, redistributed unaltered, so nothing was
inserted into them to serve as an anchor. Each id is bound to the opening words of
its provision, recorded below, and located by matching them. If a new edition
rewords a provision, that match fails and names the id, which is exactly when a
human should look. A marker would have moved with the edit and kept a stale
citation looking correct.

**This register is not a substitute for reading the standard.** Each row holds one
line, and most provisions wrap across two or three. Open the category in
`reference/` and read it before you cite it. `cite.sh` prints the whole provision:

```bash
bash scripts/cite.sh ASI04-PIN           # print the provision
bash scripts/cite.sh AIA-50-1            # works for the AI Act too
bash scripts/cite.sh --from examples.md  # every citation in a document
```

Ids ending in `-MIT` are mitigation-section headings, cited when a finding rests on
a category's remedies as a whole. Bare category ids (`ASI04`) are section headings.
Prefer the narrowest id that carries your claim.

| id | source | line | the provision, verbatim | cited for |
|---|---|---|---|---|
"""


def main() -> int:
    cache = {}
    rows, problems = [], []
    for pid, src, ln, purpose in REGISTER:
        if src not in SOURCES:
            problems.append(f"{pid}: unknown source {src!r}")
            continue
        rel, label = SOURCES[src]
        if src not in cache:
            f = ROOT / rel
            if not f.exists():
                problems.append(f"{pid}: {rel} missing")
                continue
            cache[src] = f.read_text(encoding="utf-8").split("\n")
        lines = cache[src]
        if not 0 < ln <= len(lines):
            problems.append(f"{pid}: line {ln} outside {rel}")
            continue
        text = lines[ln - 1].strip()
        if not text:
            problems.append(f"{pid}: {rel} line {ln} is blank")
            continue
        cell = text.replace("|", "\\|")
        rows.append(f"| `{pid}` | {label} | {ln} | {cell} | {purpose} |")

    if problems:
        print("REFUSING to write the register:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1

    OUT.write_text(HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    n_owasp = sum(1 for r in REGISTER if r[1] == "owasp")
    n_act = sum(1 for r in REGISTER if r[1] == "act")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} provisions "
          f"({n_owasp} OWASP, {n_act} AI Act)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
