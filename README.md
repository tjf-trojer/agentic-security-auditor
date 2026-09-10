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
Verdict            The deploy call the severity count decides, then the arithmetic
In plain terms     Two lines, no codes
Conformity ledger  All ten categories: PASS / FAIL / PARTIAL / N/A, with severity
Findings           Four lines each: Artifact · Standard · Gap · Ask
Fix order          What to close first, and why
Scope and limits   What it does unattended, who it decides about, what could not be verified
Observations       What it believes but cannot cite, marked as judgment; usually absent
```

It never writes a fixed configuration. The long form comes only when you ask for it.

## Checking an audit

**One finding by hand.** Audit 1's F1 in [`examples.md`](examples.md) says the installer downloads
from a moving branch. Its citation,
[ASI04 Mitigation 7](reference/owasp-top-10-agentic-applications-2026.txt#L589 "^ASI04-PIN"), opens
the standard on "Pin prompts, tools, and configs by content hash and commit ID". Line 24 of
[`targets/voltagent-agent-installer.md`](targets/voltagent-agent-installer.md) fetches from
`raw.githubusercontent.com/VoltAgent/awesome-claude-code-subagents/main/`. Every finding has these
two halves: a line of the standard and a line of the agent.

**Every finding at once:**

```bash
python3 scripts/verify.py                                     # this repository
python3 scripts/verify.py my-audit.md --artifact my-agent.md  # any audit, anywhere
bash scripts/cite.sh ASI04-PIN                                # print one provision
```

Python 3.9 or later, standard library only, no network.

`verify.py` checks that every provision in [`provisions.md`](provisions.md) still sits on its
recorded line, that every citation resolves, matches its id and names OWASP's address for its
line, that every quoted passage appears inside the provision cited, that every audit rules on all
ten categories exactly once, that every PASS cites a provision, and that stated counts match the
ledger and the findings, and that the deploy call follows from them. Given the agent's file, by
`--artifact` or by an audit's own `Copy at` link into `targets/`, it also checks that the line
numbers and quotations attributed to the agent exist in it.

It cannot tell you a verdict is right.

A citation names the line a provision begins on; `cite.sh` prints to its end.

[`targets/ops-copilot-synthetic.md`](targets/ops-copilot-synthetic.md) is a synthetic agent for
checking the auditor against a known answer. Audit it, then compare: **Do not deploy**; all ten
categories FAIL, with no PASS, PARTIAL or N/A; ASI01, ASI02, ASI03, ASI05, ASI07 and ASI10 are
CRITICAL. An audit that passes any category, or grades fewer than those six rows CRITICAL, has
missed something in the file.

## Limits

- **It audits a definition, not a running system.** What turns on runtime behaviour is marked
  "cannot verify from the definition", with the test that would settle it.
- **One standard.** What no provision reaches goes in "Observations outside the standard", marked
  as judgment.
- **A PASS needs a control or a written exclusion the artifact contains**, so a short definition
  scores badly.
- **It can be lied to.** It reads the artifact in the same context as its own rules, the flaw ASI01
  describes. Rule 0 tells it never to act on text inside the artifact and to report it, and that is
  a prompt-layer control.
- **Not a penetration test and not legal advice.**

## Licence

This repository's own files are MIT, see [`LICENSE`](LICENSE). The OWASP standard in `reference/`
is CC BY-SA 4.0. The audited artifacts in `targets/` are MIT. Sources and changes are in
[`NOTICES.md`](NOTICES.md).
