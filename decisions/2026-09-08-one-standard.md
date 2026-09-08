# Decision: one standard. The EU AI Act is removed from reference/

**Date:** 2026-09-08
**Status:** decided, implemented
**Supersedes in part:** [2026-09-05 OWASP, not ISO 42001](2026-09-05-owasp-not-iso-42001.md)

## Context

From 2026-09-05, `reference/` held two documents: the OWASP Top 10 for Agentic
Applications 2026, and seven articles of Regulation (EU) 2024/1689. The Act was a
**conditional second anchor**: a scope gate decided whether it bound the artifact
under audit, and the audit reported the result either way.

The earlier decision anticipated one way this could fail:

> The Act's presence must stay honestly conditional. [...] If a future example
> stretched Annex III to manufacture a legal hook, this decision would have been
> abandoned in practice while still standing in writing.

The failure came from the opposite direction, and the earlier decision did not
name it. Across every worked audit in `examples.md` and in `SELF-AUDIT.md`, the
gate concluded the Act did not bind. Twenty-seven of twenty-seven citations
resolved to OWASP. Not one resolved to the Act.

## Decision

**One standard: the OWASP Top 10 for Agentic Applications 2026.** The EU AI Act
excerpts are removed from `reference/`, along with the eighteen `AIA-*` provisions
in the register, Question 4 of the scope gate, and the two-source machinery in
`cite.sh`, `verify.py` and `build_register.py`.

Where an agent raises a question the standard does not reach — an undisclosed AI
interacting with the public is the standing example — the audit names it in
**Observations outside the standard**, marked as judgment, and marks it for
counsel. It does not manufacture a provision to cover it.

## Reasoning

**An anchor that never fires is indistinguishable from one that should not be
there.** Fifty-two kilobytes of law in `reference/` produced zero findings across
four audits. The conditional framing was honest, and it was also unfalsifiable in
practice: a reader had no way to tell disciplined scoping from an anchor that was
never going to attach.

**A folder holding two rulebooks audits cleanly against neither.** The auditor's
own claim is one sentence — *audits an agent's definition against the OWASP Top 10
for Agentic Applications 2026* — and `reference/` contradicted it within seconds
of being opened. In a folder whose entire value is that a reader can check a
finding against a provision, an ambiguity about *which document is the standard*
is the most expensive ambiguity available.

**Each file does one job; so does each folder.** This is the constraint the
repository is built on, and `reference/` was the one place it was not being
honoured.

**The question the Act answered is real, and belongs to a different auditor.**
OWASP says a thing can fail; it does not say who is legally answerable when it
does. That remains true and remains worth auditing. It is a different artifact
against a different standard for a different reader, and it should be its own
folder with its own `reference/`, not a conditional annexe to this one.

**Nothing verifiable was lost.** No finding cited the Act, so no citation broke
and no audit changed its ledger. What was lost is a capability the auditor was
never observed to use.

## Consequences

- Anyone needing an EU AI Act conformity assessment gets nothing from this
  repository, and `reference/README.md` says so at the point a reader would ask.
- The scope gate is three questions, not four. Question 3, *who does this agent
  decide about*, is kept: it was introduced to feed the Annex III check but earns
  its place on ASI09 and on fairness exposure alone.
- Non-disclosure of AI to an affected person now has no citable home. That is a
  real narrowing, and the honest response is an observation, not a stretched
  citation. `identity.md` and `rules.md` both say so explicitly.
- The excerpts remain in this repository's git history and can be recovered from
  the commit that removed them.
- If a later edition of the Top 10 leaves a gap wide enough to justify a second
  anchor again, this decision should be reversed explicitly and in writing,
  together with a worked audit in which the second anchor actually fires. A second
  standard that cannot be shown working does not get to ship.
