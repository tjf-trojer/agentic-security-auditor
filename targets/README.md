# targets/ — the artifacts audited in examples.md

_Last updated: 2026-09-05_

These are the inputs. They are here so a reader can hold the audit and the artifact side by side
and check that every quoted line says what the finding claims.

All three audited artifacts are **real agent definitions written by other people and published**,
each vendored byte-for-byte and pinned. None is the author's own work: an auditor demonstrated
only on artifacts its author controls has demonstrated very little.

| File | Origin | Licence | Audited in |
|---|---|---|---|
| [`voltagent-agent-installer.md`](voltagent-agent-installer.md) | `categories/09-meta-orchestration/agent-installer.md` from [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents), pinned at [`beb9a0f`](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/beb9a0f0d74a222f5e24aeb390e6d7c3005d9e27/categories/09-meta-orchestration/agent-installer.md) | MIT | Audit 1 |
| [`ecc-loop-operator.md`](ecc-loop-operator.md) | `agents/loop-operator.md` from [affaan-m/ECC](https://github.com/affaan-m/ECC), pinned at [`e04ea0b`](https://github.com/affaan-m/ECC/blob/e04ea0b/agents/loop-operator.md) | MIT | Audit 2 |
| [`swe-agent-default.yaml`](swe-agent-default.yaml) | `config/default.yaml` from [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) | MIT | Audit 3 |
| [`ops-copilot-synthetic.md`](ops-copilot-synthetic.md) | Written for this repository | MIT, with the rest of this repo | Not audited; the self-test fixture |

## Why these

**`agent-installer` is the balanced one.** A real, shipped agent whose job is installing other
agents: it fetches third-party definitions from a mutable branch reference and writes them where
later sessions load them as instructions. It produces three earned passes alongside three
criticals, which is the whole ledger working on one artifact.

**`loop-operator` is the hardest to audit honestly.** It is the safety control for other
autonomous loops, and it opens with an explicit prompt-injection defence worded close to the
standard's own text. A reviewer credits that; a cynic dismisses it. The audit is forced to a third
answer by the root cause two hundred lines earlier in the same standard, and lands on PARTIAL with
both halves of the reasoning redeemable. It is also the only target with no pass, which is
reported rather than softened.

**`swe-agent` proves the auditor is not format-locked.** YAML, not markdown, with the instructions
in `agent.templates` and the grant in `agent.tools`. Its four non-FAIL verdicts each arise from a
different mechanism. It also demonstrates a rule preventing a plausible false finding: the
`bundles:` paths look exactly like a pinning failure, and `rules.md` forbids that reading because
they sit inside the operator's own checkout.

**`ops-copilot` is synthetic and labelled as such.** The three real artifacts leave the far end of
the range untested: none holds administrator credentials or runs unattended in a continuous loop.
This one fails all ten and ships with an expected result, so a reader can check the auditor
against a known answer before trusting it on their own agent. Nobody shipped it.

## A note on auditing live third-party artifacts

Each file is pinned to a commit and the audits are audits of that state. Upstream may have moved
since. That is not incidental: it is the subject of Audit 1's first finding, that the audited
artifact resolves its own installs against a moving `main`. Pinning here is the discipline the
audited artifact lacks, and it was the only way to write audits whose citations stay true.

No claim is made that any upstream author endorses these audits, and none has been reported as a
vulnerability disclosure. All are public, MIT licensed, and audited as published work.
