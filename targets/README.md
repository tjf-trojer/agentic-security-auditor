# targets/ holds the artifacts audited in examples.md

_Last updated: 2026-09-08_

The inputs, so a reader can hold the audit and the artifact side by side and check that every
quoted line says what the finding claims.

| File | Origin | Licence | Audited in |
|---|---|---|---|
| [`voltagent-agent-installer.md`](voltagent-agent-installer.md) | `categories/09-meta-orchestration/agent-installer.md` from [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents), pinned at [`beb9a0f`](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/beb9a0f0d74a222f5e24aeb390e6d7c3005d9e27/categories/09-meta-orchestration/agent-installer.md) | MIT | Audit 1 |
| [`ecc-loop-operator.md`](ecc-loop-operator.md) | `agents/loop-operator.md` from [affaan-m/ECC](https://github.com/affaan-m/ECC), pinned at [`e04ea0b`](https://github.com/affaan-m/ECC/blob/e04ea0b/agents/loop-operator.md) | MIT | Audit 2 |
| [`swe-agent-default.yaml`](swe-agent-default.yaml) | `config/default.yaml` from [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent), upstream commit not recorded | MIT | Audit 3 |
| [`ops-copilot-synthetic.md`](ops-copilot-synthetic.md) | Written for this repository | MIT, with the rest of this repo | Not audited; the self-test fixture |

Audit 4's target is not here. The community workflow kit carries no licence covering its own text,
so [`../examples.md`](../examples.md) quotes it without copying it.

## What each one covers

**`agent-installer`** is a shipped agent whose job is installing other agents: it fetches
third-party definitions from a mutable branch reference and writes them where later sessions load
them as instructions. Three earned passes alongside three criticals.

**`loop-operator`** is the safety control for other autonomous loops, and it opens with an
explicit prompt-injection defence worded close to the standard's own text. The audit lands on
PARTIAL, and it is the only target with no pass.

**`swe-agent`** is YAML rather than markdown, with the instructions in `agent.templates` and the
grant in `agent.tools`. Its four non-FAIL verdicts each arise from a different mechanism. Its
`bundles:` paths look like a pinning failure, and `rules.md` forbids that reading because they sit
inside the operator's own checkout.

**`ops-copilot`** is synthetic and labelled as such. It holds administrator credentials and runs
unattended in a continuous loop, which the three vendored artifacts do not. It fails all ten and
ships with an expected result, so you can check the auditor against a known answer.

## Pinning

Two of the three vendored files are pinned to an upstream commit, and the audits are audits of
that state. The SWE-agent config was copied byte-for-byte but its upstream commit was not
recorded, so it cannot be resolved to a revision, and Audit 3 is an audit of the file as vendored
here. Upstream may have moved in any of the three cases.

No upstream author endorses these audits, and none has been reported as a vulnerability
disclosure. All are public, MIT licensed, and audited as published work.
