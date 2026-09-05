# targets/ — the artifacts audited in examples.md

These are the inputs. They are here so that a reader can hold the audit and the artifact side by
side and check that every quoted line says what the finding claims it says.

Three are real agent definitions written by other people and published. One is synthetic and
says so on its face.

| File | Origin | Licence | Audited in |
|---|---|---|---|
| [`voltagent-agent-installer.md`](voltagent-agent-installer.md) | `categories/09-meta-orchestration/agent-installer.md` from [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents), pinned at commit [`beb9a0f`](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/beb9a0f0d74a222f5e24aeb390e6d7c3005d9e27/categories/09-meta-orchestration/agent-installer.md) | MIT | Audit 1 |
| [`eu-ai-act-map-agents.md`](eu-ai-act-map-agents.md) | `AGENTS.md` from [tjf-trojer/eu-ai-act-map](https://github.com/tjf-trojer/eu-ai-act-map) | See that repository | Audit 2 |
| [`voltagent-it-ops-orchestrator.md`](voltagent-it-ops-orchestrator.md) | `categories/09-meta-orchestration/it-ops-orchestrator.md` from [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents), pinned at commit [`beb9a0f`](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/beb9a0f0d74a222f5e24aeb390e6d7c3005d9e27/categories/09-meta-orchestration/it-ops-orchestrator.md) | MIT | Audit 4 |
| [`ops-copilot-synthetic.md`](ops-copilot-synthetic.md) | Written for this repository | MIT, with the rest of this repo | Audit 3 |

## Why these four

**`agent-installer` is the centrepiece** because it is a real, shipped, permissively licensed
agent whose job is to install other agents. It fetches third-party definitions from a mutable
branch reference and writes them into a directory that later sessions load as instructions. That
puts genuine weight on ASI04, ASI06 and ASI09 without anything being contrived, and it produces
real passes alongside the failures, which is what an audit is supposed to look like.

**`eu-ai-act-map` AGENTS.md is audited because it mostly passes.** An auditor that only ever
returns failures has not demonstrated it can discriminate. This artifact is a read-only research
agent, four categories genuinely cannot arise for it, and the audit says so with a reason in each
case rather than padding the ledger. It is also the author's own published work, audited in
public with its gaps named, which is the cheapest available evidence that the auditor is not
tuned to flatter its owner.

**`it-ops-orchestrator` is the multi-agent case.** A real coordinator that decomposes IT
operations work, dispatches it to eight named specialists, and merges what comes back into a
single answer, across Active Directory, Azure and M365. It is the only target here where ASI07
(inter-agent communication) genuinely fires rather than being reasoned away, and it is the one
whose findings turn on trust between agents rather than trust in fetched content. One of its own
worked examples routes an operation that disables user accounts.

**`ops-copilot` is synthetic and labelled as such.** The three real artifacts still leave the far
end of the range untested: none of them holds administrator credentials or runs unattended in a
continuous loop. Rather than pretend the standard was exercised in full, this file supplies an
artifact that fails all ten, so the auditor's behaviour against a maximally bad definition is
visible too.

## A note on auditing a live third-party artifact

The two VoltAgent artifacts are pinned to commit `beb9a0f` (2026-09-04), and Audits 1 and 4 are
audits of that state. The upstream file may have changed since. That is not incidental: it is the subject of
Audit 1's first finding, which is that the artifact itself resolves its installs against a moving
`main` reference. The pin here is the discipline the audited artifact lacks, and pinning it was
the only way to write an audit whose citations stay true.

No claim is made that the upstream authors endorse this audit, and none of these findings has
been reported to them as a vulnerability disclosure. The artifact is public, MIT licensed, and
audited here as published work.
