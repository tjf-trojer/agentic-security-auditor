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

**3. Check your own audit, once you have one.** The same checker runs against any file:

```bash
python3 scripts/verify.py my-audit.md
```

It confirms your citations resolve, your ids match the register, every passage you quoted from
the standard appears in it verbatim, your ledger covers all ten categories, and your stated
arithmetic matches your own table. The file does not have to live in this repository.

**4. Run it on a known-bad artifact.** [`targets/ops-copilot-synthetic.md`](targets/ops-copilot-synthetic.md)
is written to fail all ten categories. Paste it in and compare against Audit 3.

**5. See that it works in someone else's hands.** Audits 1 to 3 were written by hand while
building this folder, which demonstrates a format and proves nothing. **Audit 4 was produced by a
clean-room run**: a fresh session given only this repository and a target it had never seen, with
no knowledge of the other audits. All thirty-eight of its citations were then checked and
resolved. That run also found four real defects in these rules, which are fixed and recorded in
the git history.

## What it is not

Not a reviewer and not a critic. A **critic**'s authority is their taste; a **reviewer**'s is
their experience; an **auditor**'s is the rule, which anyone who can read can check. So **the
auditor's opinion carries no weight in its own output.** A finding that cannot cite a provision
is not a finding; it goes in "Observations outside the standard", marked as judgment, or nowhere.

And it reports **pass as well as fail**. Every audit opens with a verdict on all ten categories
before it reaches the failures. One honest qualification: a pass has to name a control the
artifact *contains*, so a terse definition that is simply silent about identity, logging and
stopping will collect few passes. That is a real result, not a defect. What the ledger measures
is what a definition commits to in writing.

## Using it

Create a Claude project, add this folder to its knowledge (or open the folder in Claude Code),
paste your agent definition and say **"Audit this agent definition."**

**In a Claude project**, the five files the brief asks for are all you need: `identity.md`,
`rules.md`, `examples.md`, `reference/` and this README. `provisions.md` and `method/` make it
sharper. You can leave the PDF out of the knowledge base, since the markdown carries the same text
and the PDF is there so a reader can check the transcription. `scripts/` and the Makefile will not
run there and are not needed: they verify this repository's claims, they do not perform audits.
`rules.md` tells the auditor how to verify by hand when there is no shell.

**In Claude Code**, open the folder and `CLAUDE.md` routes automatically, and the tooling works.

**What to feed it:** the agent's **instructions and its tools**. A `.claude/agents/*.md` file, an
`AGENTS.md`, a Cursor rule, a system prompt plus a tool list, an n8n or LangGraph node with its
wiring described, or a rough paragraph describing what you told it to do and what you let it
touch. Polished or rough. A transcript or config files make the audit deeper; it never needs them.

If you were handed a running assistant rather than a document, ask whoever built it for exactly
two things: the system prompt, and the list of what it is allowed to do and touch. If they cannot
produce those, that is itself worth knowing.

**What comes back: a brief, not an essay.** Around two pages, scannable, ending with an offer of
more depth if you want it.

```
Verdict            Deploy or not, in the first three words, then the arithmetic
In plain terms     Two lines, no codes, for someone with no security background
Conformity ledger  All ten categories: PASS / FAIL / PARTIAL / N/A, with severity
Findings           Four lines each: Artifact · Standard · Gap · Ask
Fix order          What to close first, and why
Scope and limits   What it is, what it does unattended, what could not be verified
Want more?         The long form, on any finding, on request
```

Every finding has the same four parts: **where in your artifact**, **what the standard requires**
with the citation, **the gap**, and **the question you have to answer**.

It never hands you fixed configuration. It does tell you what to fix **first**, which is
sequencing rather than building, and is what makes the output actionable without making the
result something you cannot defend. An agent whose owner did not reason their way to why it is
safe is one the organisation cannot defend when someone asks who decided it was safe.

## Layout

The map and the routing table live in [`CLAUDE.md`](CLAUDE.md), which is the file Claude reads
first. In short: `reference/` holds the standard, `provisions.md` indexes it, `rules.md` and
`identity.md` are the auditor, `method/` is navigation, `examples.md` and `targets/` are the
worked audits and their inputs, `decisions/` records why, `scripts/` checks the lot.

The load-bearing decision is the split between `reference/` (other people's text, where
authority lives) and `method/` (mine, navigation only). **A finding may cite `reference/`, never
`method/`.** A reader who trusts nothing here can delete `method/` and still check every finding.

That decision and three others, including why ids rather than bare line numbers, are written up
one per file in [`decisions/`](decisions/). The operating rules Claude follows are in
[`CLAUDE.md`](CLAUDE.md) and [`rules.md`](rules.md); this README does not restate them.

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
