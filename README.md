# The Agentic Security Auditor

**Audits an AI agent's definition against the OWASP Top 10 for Agentic Applications 2026, and
reports where it conforms and where it does not, citing the standard by line.**

Drop this folder into a Claude project. Paste in an agent's instructions and its tool list. You
get back a verdict on all ten categories, then numbered findings, each quoting the line of your
agent that creates the exposure and the line of the standard it fails.

The standard is in [`reference/`](reference/). Not a summary of it. The document itself, plus the
original PDF, so any finding can be opened against the provision it cites.

```bash
git clone https://github.com/tjf-trojer/agentic-security-auditor
cd agentic-security-auditor
make verify          # prove the standard is intact and every citation is honest
```

---

## Check it before you trust it

Two minutes, no account, no API key, nothing to install.

**1. Verify the auditor's own claims.** `make verify` runs eight offline checks: every registered
provision still sits where the register says, every citation resolves, every passage quoted from
the standard appears in it verbatim, every audit ruled on all ten categories, and the stated
ledger arithmetic matches the tables. It exits non-zero if any of that is false.

**2. Redeem any citation from the terminal.**

```
$ bash scripts/cite.sh ASI04-PIN
── ASI04-PIN   reference/owasp-top-10-agentic-applications-2026.md#L589
  7. Pinning: Pin prompts, tools, and configs by content hash and commit ID. Require staged rollout with
  differential tests and auto-rollback on hash drift or behavioral change.
```

Now open Finding 1 of Audit 1 in [`examples.md`](examples.md), which claims the audited agent
installs from a moving `main` branch, and line 24 of
[`targets/voltagent-agent-installer.md`](targets/voltagent-agent-installer.md), which is a raw
GitHub URL with `/main/` in it. Decide for yourself whether the finding is right. That is the only
test of an auditor that means anything.

**3. Run it on a known-bad artifact.** [`targets/ops-copilot-synthetic.md`](targets/ops-copilot-synthetic.md)
is written to fail all ten categories. Paste it in and compare against Audit 3.

**4. See that it works in someone else's hands.** Audits 1 to 3 were written by hand while
building this folder, which demonstrates a format and proves nothing. **Audit 4 was produced by a
clean-room run**: a fresh session given only this repository and a target it had never seen, with
no knowledge of the other audits. All thirty-eight of its citations were then checked and
resolved. That run also found four real defects in these rules, which are fixed and recorded in
the git history.

## What it is not

Not a reviewer and not a critic, and the difference is the whole design:

- A **critic** tells you what they dislike. Their authority is their taste.
- A **reviewer** tells you what will go wrong. Their authority is their experience.
- An **auditor** tells you where your artifact stands against a written rule that exists
  independently of them. Their authority is the rule, and anyone who can read can check it.

So **the auditor's opinion carries no weight in its own output.** A finding that cannot cite a
provision is not a finding; it goes in "Observations outside the standard", marked as judgment,
or nowhere.

And it reports **pass as well as fail**. Every audit opens with a verdict on all ten categories
before it reaches the failures. One honest qualification: a pass has to name a control the
artifact *contains*, so a terse definition that is simply silent about identity, logging and
stopping will collect few passes. That is a real result, not a defect. What the ledger measures
is what a definition commits to in writing.

## Using it

Create a Claude project, add this folder to its knowledge (or open the folder in Claude Code),
paste your agent definition and say **"Audit this agent definition."**

**What to feed it:** the agent's **instructions and its tools**. A `.claude/agents/*.md` file, an
`AGENTS.md`, a Cursor rule, a system prompt plus a tool list, an n8n or LangGraph node with its
wiring described, or a rough paragraph describing what you told it to do and what you let it
touch. Polished or rough. A transcript or config files make the audit deeper; it never needs them.

If you were handed a running assistant rather than a document, ask whoever built it for exactly
two things: the system prompt, and the list of what it is allowed to do and touch. If they cannot
produce those, that is itself worth knowing.

**What comes back:**

```
Audit summary          Verdict, ledger arithmetic, findings by severity
In plain terms         Three lines, no codes, for forwarding on its own
Capability profile     What it is, what it does unattended, whether the AI Act binds
Conformity ledger      All ten categories: PASS / FAIL / PARTIAL / N/A
Findings               Numbered, by severity, each citing the standard by line
Judgment calls         Decisions that must be made rather than left implicit
What holds             The passes, restated
Observations           Anything real but outside the standard, marked as judgment
```

Every finding has four parts: **where in your artifact**, **what the standard requires** with the
citation, **the gap**, and **the question you have to answer**. It never hands you fixed
configuration. An agent whose owner did not reason their way to why it is safe is one the
organisation cannot defend when someone asks who decided it was safe.

## Layout

```
CLAUDE.md      The router: what to read for which task, and the three hard rules
identity.md    Who the auditor is and which standard it enforces
rules.md       How it audits: the sweep, the ledger, severity, output format
examples.md    Four worked audits, one of them a clean-room run on an unseen target
provisions.md  The register: every citable provision, its id, its line, its words
reference/     THE STANDARD. OWASP's text and the PDF. Plus the seven EU AI Act
               articles the auditor may cite, when the scope gate says it may
method/        The working layer: scope gate, detection probes. Written by me,
               carries no authority, and no finding may ever cite it
targets/       The four artifacts audited in examples.md, so you can check the work
decisions/     Why this folder is shaped this way, one decision per file
scripts/       verify.py, cite.sh, build_register.py
```

Two decisions carry the rest, and both are written up in [`decisions/`](decisions/):

**`reference/` versus `method/`.** `reference/` is other people's text and is where authority
lives. `method/` is mine and is navigation. A finding may cite `reference/`, never `method/`. A
reader who trusts nothing here can delete `method/` and still check every finding.

**Ids, not line numbers.** Line numbers move, and a moved citation still looks authoritative. So
every provision has a stable id in [`provisions.md`](provisions.md), the line number is derived
from it, and `verify.py` recomputes the lines and fails if one drifted. The id is bound to the
provision's own words rather than to a marker inserted into the text, because nothing was
inserted into the text.

## Scope and honesty

**It audits a definition, not a running system.** Where a finding depends on runtime behaviour or
on the base model's properties, the audit says "cannot verify from the definition" and names the
test that would settle it.

**The EU AI Act is a conditional second anchor and usually does not apply.** Most agent
definitions are internal developer tooling, and the audit says so plainly rather than stretching
Annex III to manufacture a legal hook. Both real audits reach exactly that conclusion. The Art. 50
transparency duties are checked separately, because they bind by behaviour rather than by risk
tier.

**ISO/IEC 42001 is deliberately absent.** It is copyrighted and cannot ship in `reference/`. A
standard that cannot ship cannot anchor a checkable finding. See
[`decisions/`](decisions/2026-09-05-owasp-not-iso-42001.md).

**OWASP's ten categories are not everything that can be wrong with an agent.** Where something is
concerning and no provision reaches it, it goes in "Observations outside the standard", marked as
judgment. A strained citation is worse than an honest observation.

**A short definition will score badly**, and the ledger says so rather than manufacturing balance.

**Not a penetration test and not legal advice.** It is a design review against a published
standard.

## Note for readers on github.com

GitHub renders `.md` files, and rendered markdown has no line numbers, so a `#L589` link lands at
the top of the file. Append `?plain=1` to see the numbered source, or use `scripts/cite.sh`, which
was written for exactly this reason. Provisions in this standard wrap across two or three lines,
so a citation names where a provision **begins**; `cite.sh` prints to the end of it.

## Licence

This repository's own files: MIT, see [`LICENSE`](LICENSE).

The OWASP standard in `reference/` is CC BY-SA 4.0 and stays that way. The EU AI Act excerpts are
reused under Commission Decision 2011/833/EU. The audited VoltAgent artifacts are MIT, reproduced
byte-for-byte and pinned to a commit. Full detail, including what was changed in the OWASP
transcription and why, is in [`NOTICES.md`](NOTICES.md).

Neither OWASP nor the EU nor the authors of any audited artifact endorse this repository.
