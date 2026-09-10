# The Agentic Security Auditor

An auditor that answers one question: **does this agent's definition conform to the OWASP Top 10
for Agentic Applications 2026?**

_Last updated: 2026-09-10_

Give it an agent's instructions and its tool grant. It rules on all ten categories, pass as well
as fail, and every verdict cites the line of the standard it rests on. The standard is in
[`reference/`](reference/), in full, beside the original PDF.

## Using it

**In Claude Code**, clone the repository and open the folder. [`CLAUDE.md`](CLAUDE.md) routes and
the scripts run.

```bash
git clone https://github.com/tjf-trojer/agentic-security-auditor
```

**In a Claude project**, add `identity.md`, `rules.md`, `examples.md`, `provisions.md`, `method/`
and `reference/owasp-top-10-agentic-applications-2026.txt` to its knowledge. Scripts do not run
there; Rule 5 in [`rules.md`](rules.md) says how to verify by hand.

Paste the definition and say **"Audit this agent definition."** Paste it; do not ask the auditor to
fetch it.

**What to feed it:** the agent's instructions and its tools. A `.claude/agents/*.md` file, an
`AGENTS.md`, a Cursor rule, a system prompt plus a tool list, an n8n or LangGraph node with its
wiring described, or a rough paragraph on what the agent is told to do and what it may touch. A
transcript or config files deepen the audit; it does not need them. If you hold a running
assistant rather than a document, ask its builder for the system prompt and the list of what it
may do and touch.

**What comes back** is a brief of around two pages:

```
Verdict            Deploy or not, in the first three words, then the arithmetic
In plain terms     Two lines, no codes
Conformity ledger  All ten categories: PASS / FAIL / PARTIAL / N/A, with severity
Findings           Four lines each: Artifact · Standard · Gap · Ask
Fix order          What to close first, and why
Scope and limits   What it does unattended, who it decides about, what could not be verified
Observations       What it believes but cannot cite, marked as judgment; usually absent
```

It never writes a fixed configuration. The long form comes only when you ask for it.

## Checking an audit

```bash
python3 scripts/verify.py                                     # this repository
python3 scripts/verify.py my-audit.md --artifact my-agent.md  # any audit, anywhere
bash scripts/cite.sh ASI04-PIN                                # print one provision
```

Python 3.9 or later, standard library only, no network.

`verify.py` checks that every provision in [`provisions.md`](provisions.md) still sits on its
recorded line, that every citation resolves and matches its id, that every quoted passage appears
inside the provision cited, that every audit rules on all ten categories exactly once, that every
PASS cites a provision, and that stated counts match the ledger and the findings. With
`--artifact` it also checks that the line numbers and quotations attributed to the agent exist in
the agent's file.

It cannot tell you a verdict is right, and without `--artifact` it never opens the agent.

A citation names the line a provision begins on; `cite.sh` prints to its end.

[`targets/ops-copilot-synthetic.md`](targets/ops-copilot-synthetic.md) is a synthetic agent written
to fail all ten categories, with its expected result at the end.

## Limits

- **It audits a definition, not a running system.** What turns on runtime behaviour is marked
  "cannot verify from the definition", with the test that would settle it.
- **One standard.** What no provision reaches goes in "Observations outside the standard", marked
  as judgment.
- **A PASS needs a control the artifact contains**, so a short definition scores badly.
- **It can be lied to.** It reads the artifact in the same context as its own rules, the flaw ASI01
  describes. Rule 0 tells it never to act on text inside the artifact and to report it, and that is
  a prompt-layer control.
- **Boilerplate safety stanzas have no scoring rule.** Two careful auditors can score the same block
  differently.
- **The ledger cannot express reflexivity.** When the artifact is itself a category's mitigation for
  other agents (a watchdog under ASI10, a governance agent under ASI08), its own exposure has to go
  in prose.
- **Not a penetration test and not legal advice.**

## Licence

This repository's own files are MIT, see [`LICENSE`](LICENSE). The OWASP standard in `reference/`
is CC BY-SA 4.0. The audited artifacts in `targets/` are MIT. Sources and changes are in
[`NOTICES.md`](NOTICES.md).
