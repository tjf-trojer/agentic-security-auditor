# The sweep: the audit itself

_Last updated: 2026-09-18_

Rule 3. The scope gate, then ASI01 to ASI10 in order, with two checks that run throughout.

---

## Rule 3: The sweep

### Move 1: the scope gate

Before looking for any finding, run [`method/scope-gate.md`](../method/scope-gate.md). It produces a
three-to-five line **capability profile**:

1. **Is this an agent, at what autonomy level?** Supervised, semi-autonomous, or fully autonomous.
   No tools means not in scope: say so and stop.
2. **What can it do without a human confirming?** Consequential actions reachable autonomously,
   and the subset that are irreversible. This is the governing question of the audit.
3. **Who does it decide about?** Name the population whose case it ranks, scores, filters or
   flags, what follows for them, and whether they are told. "Nobody" is a common and legitimate
   answer. Anything else sharpens ASI09 and puts any fairness exposure in the profile rather than
   in Observations.

The gate also runs the **lethal trifecta** pre-check.

### Move 2: ten categories, in order

Walk ASI01 to ASI10. For each: open the category in `reference/`, read what it says, run the
probe, record a verdict.

The probes are in [`method/detection-probes.md`](../method/detection-probes.md): what each failure
looks like on the page, and the question that surfaces it. **Where a probe and the text disagree,
the text wins and you cite the text.** A probe that reaches further than the text holds only
where a sentence of the standard carries that reach, and the finding cites that sentence.

Two cross-cutting checks, applied throughout rather than as separate categories, each filed under
whichever category it sits in:

- **Least-Agency** ([Letter from the Leaders](../reference/owasp-top-10-agentic-applications-2026.txt#L182 "^ASI00-LEAST-AGENCY")).
  Capability present but unnecessary is attack surface with no upside.
- **Observability** ([Letter from the Leaders](../reference/owasp-top-10-agentic-applications-2026.txt#L183 "^ASI00-OBSERVABILITY")).
  No action log or reasoning trace is a finding. File it under ASI10, whose first mitigation asks
  for logs of all agent actions, unless the gap belongs to one category's own record.
