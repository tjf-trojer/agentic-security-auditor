# Decision: sweep all ten categories rather than narrowing to one

**Date:** 2026-09-05
**Status:** decided, implemented

## Context

Narrowing is a real option and a defensible one. An auditor for ASI04 alone
(agentic supply chain) could carry more depth per finding, ship a smaller
reference, and be easier to verify exhaustively.

## Decision

Audit an agent definition against all ten categories, ASI01 to ASI10, with a
verdict on each in every audit.

## Reasoning

**Specificity here means pinned, not narrow.** The pairing that makes an audit
checkable is a named artifact type against a named, versioned standard. This
auditor's pairing is "an AI agent definition" against "OWASP Top 10 for Agentic
Applications, Version 2026". Both halves are pointable. Narrowing to one category
would sharpen the second half of a pairing that is already sharp, at the cost of
the first.

**The categories are not independent, and the interesting findings live between
them.** An agent that installs third-party definitions fails ASI04 (unpinned
supply chain) and ASI06 (what it installs persists into later sessions) and ASI09
(the human approves without seeing the tool grant), and the three together are
the actual risk. An ASI04-only auditor reports one third of that and reports it
as smaller than it is. The sweep is what surfaces the interaction.

**A ten-category sweep is what makes the conformity ledger possible**, and the
ledger is the thing that separates this from a critique. A single-category
auditor can report pass or fail on one axis. Ten verdicts, none skippable, is a
statement about the artifact as a whole, and `scripts/verify.py` can enforce that
none was quietly omitted.

## Consequences

- Every audit is longer, and a terse artifact produces a ledger with several
  reasoned N/A rows. That is accepted: an argued N/A is information.
- The reference must ship whole, not as a single-provision excerpt. At 1,695
  lines that is manageable; for a larger standard it would not be.
- The auditor cannot go as deep on any one category as a specialist would. Where
  a finding needs depth OWASP does not supply, it belongs in "Observations
  outside the standard", not in a stretched citation.
