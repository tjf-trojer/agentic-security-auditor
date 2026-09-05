# Worked audits

_Last updated: 2026-09-05_

Four audits, chosen to show the auditor discriminating rather than complaining. Three are real
artifacts written by other people and shipped in public. The fourth is synthetic, and labelled as
such, because it reaches the far end of the range the real ones do not.

Audits 1 to 3 were written by hand while building this folder. **Audit 4 was not:** it is the
output of a clean-room run, a fresh session given only this repository and an unseen target, with
no knowledge of the other audits. Its thirty-eight citations were checked line by line afterwards
and all resolved. It is here because worked examples written by an auditor's own author
demonstrate a format, not that the format works.

Every artifact audited here is in [`targets/`](targets/), so you can read the input beside the
output. Every citation points into
[`reference/owasp-top-10-agentic-applications-2026.md`](reference/owasp-top-10-agentic-applications-2026.md)
by line, so you can open the provision and check that it says what the finding claims.

| # | Artifact | Real? | Result |
|---|---|---|---|
| 1 | [`voltagent-agent-installer.md`](targets/voltagent-agent-installer.md) | Real, MIT, third party | 3 pass, 4 fail, 2 partial, 1 N/A |
| 2 | [`eu-ai-act-map-agents.md`](targets/eu-ai-act-map-agents.md) | Real, third party | 4 pass, 1 fail, 1 partial, 4 N/A |
| 3 | [`ops-copilot-synthetic.md`](targets/ops-copilot-synthetic.md) | Synthetic | 0 pass, 10 fail, 0 partial, 0 N/A |
| 4 | [`voltagent-it-ops-orchestrator.md`](targets/voltagent-it-ops-orchestrator.md) | Real, MIT, third party. Clean-room run | 0 pass, 9 fail, 1 partial, 0 N/A |

---
---

# Audit 1: `agent-installer`

**Artifact.** `agent-installer`, VoltAgent/awesome-claude-code-subagents, commit `beb9a0f`, MIT.
Copy at [`targets/voltagent-agent-installer.md`](targets/voltagent-agent-installer.md).
**Standard.** OWASP Top 10 for Agentic Applications 2026. **Date.** 2026-09-05.

## Verdict

**Do not deploy.** 3 pass, 4 fail, 2 partial, 1 not applicable; 3 critical, 2 major, 2 minor.

This agent installs executable instructions, fetched from a mutable branch reference, onto a path
every later session on the machine loads, behind a confirmation that shows the operator none of
the parts that carry the risk. Seven findings, two root causes: nothing verifies what arrives
(F1, F2, F4), and nothing records or bounds what happened (F3, F7, F8).

## In plain terms

This helper downloads other AI agents from the internet and saves them where your assistant will
obey them from then on. It asks first, but what it shows you is a one-line description, while the
part deciding what the downloaded agent may do to your machine is never put in front of you.

## Conformity ledger

| Category | Verdict | Sev | Basis |
|---|---|---|---|
| ASI01 Agent Goal Hijack | **FAIL** | CRITICAL | F2 |
| ASI02 Tool Misuse and Exploitation | **PARTIAL** | MAJOR | F4, F8 |
| ASI03 Identity and Privilege Abuse | **PASS** | — | Declares no credential; runs as the invoking operator, holding nothing they did not already hold. Meets [ASI03-SCOPED-TOKENS](reference/owasp-top-10-agentic-applications-2026.md#L479 "^ASI03-SCOPED-TOKENS") |
| ASI04 Agentic Supply Chain Vulnerabilities | **FAIL** | CRITICAL | F1, F7 |
| ASI05 Unexpected Code Execution | **PARTIAL** | MAJOR | F4 |
| ASI06 Memory & Context Poisoning | **FAIL** | CRITICAL | F3 |
| ASI07 Insecure Inter-Agent Communication | **N/A** | — | Single agent; neither calls nor is called by others. It writes files that *become* agents, which is ASI04 and ASI06, not messaging |
| ASI08 Cascading Failures | **PASS** | — | Lines 34-39 are short, linear and human-initiated, no step conditioned on a previous inference, so the planner-executor coupling [ASI08-COUPLING](reference/owasp-top-10-agentic-applications-2026.md#L895 "^ASI08-COUPLING") describes cannot arise |
| ASI09 Human-Agent Trust Exploitation | **FAIL** | MAJOR | F6 |
| ASI10 Rogue Agents | **PASS** | — | Invoked interactively per action, no loop or schedule, operator present throughout, so there is no unattended run for the drift [ASI10-DRIFT](reference/owasp-top-10-agentic-applications-2026.md#L1071 "^ASI10-DRIFT") describes |

## Findings

### F1 · CRITICAL · ASI04 · The install target is a mutable reference
**Artifact** line 24 — the raw URL ends `/main/categories/{category}/{agent}.md`; line 37 downloads it, line 38 saves it
**Standard** [ASI04-PIN](reference/owasp-top-10-agentic-applications-2026.md#L589 "^ASI04-PIN") "Pin prompts, tools, and configs by content hash and commit ID"; [ASI04-GATEKEEPING](reference/owasp-top-10-agentic-applications-2026.md#L579 "^ASI04-GATEKEEPING") requires verifying provenance before install
**Gap** nothing pins, hashes or verifies. What lands is whatever `main` resolves to at fetch time, so a description read at 10:00 and installed at 10:05 are not guaranteed to be the same file
**Ask** what commit or hash does an install pin to, and what is the downloaded file compared against before it is written?

### F2 · CRITICAL · ASI01 · Fetched content becomes instructions, uninspected
**Artifact** line 4 grants `WebFetch` and `Bash`; line 24 points them at a third-party repo; line 74 instructs "Preserve exact file content when downloading"; lines 35-38 write it into the agents directory
**Standard** [ASI01-UNTRUSTED-INPUT](reference/owasp-top-10-agentic-applications-2026.md#L283 "^ASI01-UNTRUSTED-INPUT") "Treat all natural-language inputs (e.g., user-provided text, uploaded documents, retrieved content) as untrusted"
**Gap** what is fetched is not read, it is installed as a system prompt with its own tool grant. A file whose frontmatter says `tools: Bash` arrives with neither inspected. Line 74 is right for integrity and, without an inspection step, guarantees faithful delivery of something nobody looked at
**Ask** before a fetched file is written, what inspects its `tools:` grant and its body, and what would refuse the install?

### F3 · CRITICAL · ASI06 · What is installed persists into every later session
**Artifact** line 35 offers global installation to `~/.claude/agents/`; capability 4 at line 16 says the same
**Standard** [ASI06-POISONING](reference/owasp-top-10-agentic-applications-2026.md#L688 "^ASI06-POISONING") corrupted context causes "future reasoning, planning, or tool use to become biased, unsafe, or aid exfiltration"; [ASI06-NO-SELF-INGEST](reference/owasp-top-10-agentic-applications-2026.md#L744 "^ASI06-NO-SELF-INGEST") on re-ingestion
**Gap** a file written there is loaded by every future session across every project until removed. The confirmation is one moment; the consequence is permanent, which is why this outranks F2
**Ask** does a global install carry any expiry, re-check on load, or review prompt, and how would an operator discover an installed agent had changed under them?

### F4 · MAJOR · ASI02, ASI05 · `Bash` is granted where an HTTP GET would do, and runs unsandboxed
**Artifact** line 4 `tools: Bash, WebFetch, Read, Write, Glob`; line 29 offers "WebFetch or Bash with curl"; line 73 "Use `curl -s` for silent downloads"; no sandbox or network limit named anywhere
**Standard** [ASI02-TOOL-PROFILES](reference/owasp-top-10-agentic-applications-2026.md#L376 "^ASI02-TOOL-PROFILES") requires per-tool least-privilege profiles, "read-only queries for databases, no send/delete rights for email summarizers"; [ASI04-SANDBOX](reference/owasp-top-10-agentic-applications-2026.md#L581 "^ASI04-SANDBOX") requires sensitive agents to run "in sandboxed containers with strict network or syscall limits"
**Gap** every described task is served by `WebFetch`, `Write`, `Read` and `Glob`; line 73 routes the fetch through a shell and silences it by preference, not necessity. An agent whose purpose is ingesting third-party content then holds that shell on the host doing the ingesting
**Ask** which described capability needs `Bash` that `WebFetch` and `Write` cannot serve, and if none, where would it have executed?

### F6 · MAJOR · ASI09 · The gate shows the operator the one harmless part
**Artifact** line 70 "Always confirm before installing/uninstalling"; line 71 "Show the agent's description before installing if possible"
**Standard** [ASI09-RISK-SUMMARY](reference/owasp-top-10-agentic-applications-2026.md#L1030 "^ASI09-RISK-SUMMARY") requires a "plain-language risk summary (not model-generated rationales)"; [ASI09-PREVIEW](reference/owasp-top-10-agentic-applications-2026.md#L1044 "^ASI09-PREVIEW") requires separating preview from effect with expected side effects shown
**Gap** the gate is real, which is why ASI02 is PARTIAL. But what it surfaces is the `description` field. The `tools:` grant, the instruction body, the source commit and the install scope are all absent from the approval moment, and "if possible" makes even that discretionary
**Ask** at the moment of confirmation, does the operator see the `tools:` line, the source commit and the install scope?

### F7 · MINOR · ASI04 · Nothing records what was installed, from where, or when
**Artifact** no logging anywhere; line 39 confirms success to the screen, which is not a record
**Standard** [ASI09-IMMUTABLE-LOGS](reference/owasp-top-10-agentic-applications-2026.md#L1025 "^ASI09-IMMUTABLE-LOGS") "Keep tamper-proof records of user queries and agent actions"; [ASI04-RECHECK](reference/owasp-top-10-agentic-applications-2026.md#L587 "^ASI04-RECHECK") on monitoring lineage
**Gap** after a bad install nobody can reconstruct which upstream state arrived. With F1 unresolved this compounds: the version is unpinned *and* unrecorded, which is what turns F1 from recoverable into not
**Ask** where would an operator look to find which commit a given installed agent came from?

### F8 · MINOR · ASI02 · Uninstall deletes under a gate written for install
**Artifact** capability 6 at line 18; line 70 covers both operations in one clause; no workflow section describes uninstall, unlike browse, install and search at lines 28-44
**Standard** [ASI02-CONFIRM](reference/owasp-top-10-agentic-applications-2026.md#L384 "^ASI02-CONFIRM") requires confirmation for destructive actions and "a pre-execution plan or dry-run diff before final approval"
**Gap** delete is the only irreversible operation here and the only capability with no described procedure: no statement of what is shown, what scope is targeted, or whether a glob could match more than one file
**Ask** what does the operator see before an uninstall, and can one confirmation remove more than one file?

## Fix order

1. **Pin the source** (F1). Everything else is harder to reason about while the artifact under discussion can change between reading and writing.
2. **Inspect before writing** (F2, F6 together). The inspection step and the thing the approval screen should show are the same work.
3. **Record the install** (F7). Cheap, and it is what makes F1 recoverable if it recurs.
4. **Drop `Bash`, or say what needs it** (F4). Narrowing the grant removes the sandbox question rather than answering it.
5. **Give uninstall its own gate** (F8).

## Scope and limits

Supervised developer utility, invoked interactively, single agent plus tools. Consequential
actions reachable after one confirmation: writes into `~/.claude/agents/` and `.claude/agents/`,
and arbitrary shell. Irreversible: uninstall. Lethal trifecta present, all three legs named in the
definition: local filesystem read, third-party fetch, and outbound via `WebFetch` and `Bash`.

**The EU AI Act does not bind.** Internal developer tooling, not an Annex III use, and the only
natural person it interacts with is the developer who invoked it, for whom the AI nature of the
interaction is obvious within the Art. 50(1) exception. That is honest scoping, not a gap; every
finding stands on OWASP alone.

Not verifiable from the definition: where `Bash` executes, and whether the harness inserts its own
confirmation. The test that settles the first is to run an install and print the effective user,
working directory and network policy of the shell.

## Want more?

Say the word for the long form on any finding, the full capability trace, or the two judgment
calls this brief compresses: whether `model: haiku` is right on a supply-chain path, and whether
"global versus local" is posed to the operator as a location or as a blast radius.

---
---

# Audit 2: `eu-ai-act-map` AGENTS.md

**Artifact.** Repository operating instructions for a public repo that reads Regulation (EU)
2024/1689 as a decision graph, 62 lines. Copy at
[`targets/eu-ai-act-map-agents.md`](targets/eu-ai-act-map-agents.md).
**Standard.** OWASP Top 10 for Agentic Applications 2026. **Date.** 2026-09-05.

**Why this one is here.** An auditor that only ever finds problems is not discriminating, it is
pessimistic. This target mostly passes, and four categories genuinely cannot arise for it.

## Verdict

**Safe to run as defined.** 4 pass, 1 fail, 1 partial, 4 not applicable; 0 critical, 1 major,
1 minor.

A read-only research agent with no consequential tool and no autonomous action. Its main risk is
being wrong, and its instructions are unusually strict about that. The one real gap is that it
never states what it may touch, so it inherits whatever the harness grants.

## In plain terms

Instructions for an assistant that looks up EU law in a folder of legal texts and answers
questions about it. It cannot send, change or spend anything. Read it before adopting it into a
project, because the file itself never says what it is allowed to do.

## Conformity ledger

| Category | Verdict | Sev | Basis |
|---|---|---|---|
| ASI01 Agent Goal Hijack | **PARTIAL** | MINOR | F2 |
| ASI02 Tool Misuse and Exploitation | **FAIL** | MAJOR | F1 |
| ASI03 Identity and Privilege Abuse | **N/A** | — | Declares no credential and describes no authenticated system. There is no identity to abuse |
| ASI04 Agentic Supply Chain Vulnerabilities | **PASS** | — | Composes nothing at runtime; line 13 names the specific corpus file path rather than resolving a source, which is the pinned reference [ASI04-PIN](reference/owasp-top-10-agentic-applications-2026.md#L589 "^ASI04-PIN") asks for |
| ASI05 Unexpected Code Execution | **N/A** | — | No execution capability described; the output is a written traversal, not a command |
| ASI06 Memory & Context Poisoning | **N/A** | — | Writes nothing that persists into a later session. Its corpus is read-only input under version control, not a store it feeds |
| ASI07 Insecure Inter-Agent Communication | **N/A** | — | Single agent. No delegation, no spawning, no inbound agent messages |
| ASI08 Cascading Failures | **PASS** | — | Lines 19-24 impose an ordered four-layer traversal, each layer stating its own finding and anchor, and line 44 requires missing facts to surface as open points rather than be assumed. That is the checkpoint [ASI08-GATES](reference/owasp-top-10-agentic-applications-2026.md#L946 "^ASI08-GATES") prescribes |
| ASI09 Human-Agent Trust Exploitation | **PASS** | — | Lines 13-15 require reading the source before asserting, forbid filling gaps from memory, and forbid inventing line numbers; line 58 disclaims legal advice. That is the plain-language risk summary [ASI09-RISK-SUMMARY](reference/owasp-top-10-agentic-applications-2026.md#L1030 "^ASI09-RISK-SUMMARY") prescribes, applied to epistemic rather than transactional risk |
| ASI10 Rogue Agents | **PASS** | — | Line 56 requires asking before routing when a decisive fact is missing. Escalation on uncertainty is what stands against the drift [ASI10-DRIFT](reference/owasp-top-10-agentic-applications-2026.md#L1071 "^ASI10-DRIFT") describes, and it is present and unambiguous |

## Findings

### F1 · MAJOR · ASI02 · The definition never states what the agent may touch
**Artifact** no frontmatter, no tools list, no permissions statement in 62 lines. Line 13 implies read and grep; nothing states a boundary or forbids anything
**Standard** [ASI02-TOOL-PROFILES](reference/owasp-top-10-agentic-applications-2026.md#L376 "^ASI02-TOOL-PROFILES") requires per-tool least-privilege profiles with scopes; least privilege presupposes a stated privilege
**Gap** it inherits whatever the harness grants. Under a permissive configuration this same file has write and shell access nothing in its text contemplates, and its careful conduct rules at lines 54-58 govern its *output* while saying nothing about its *actions*. MAJOR because the file is published for others to adopt, so a reader inherits the silence along with the discipline
**Ask** what is this agent permitted to touch, and where is that written so a user adopting the file inherits the boundary too?

### F2 · MINOR · ASI01 · The corpus is trusted by assumption, unstated
**Artifact** line 13 sends the agent to `corpora/eu/ai-act-2024-1689-en.md`; lines 13-15 build the whole citation discipline on that file being what it claims
**Standard** [ASI01-UNTRUSTED-INPUT](reference/owasp-top-10-agentic-applications-2026.md#L283 "^ASI01-UNTRUSTED-INPUT") requires retrieved content to be treated as untrusted before it influences reasoning
**Gap** the trust is almost certainly justified, which is why ASI04 passes: version-controlled, provenance header, not user-writable. But it is unstated, so a fork pointing at its own corpus inherits a citation discipline that reads as rigorous while resting on an assumption nobody wrote down
**Ask** what may the agent assume about the corpus, and what should it do if a cited line does not say what the map claims?

## Fix order

1. **State the tool boundary** (F1). One frontmatter block, and it is the only change that affects anyone who adopts the file.
2. **State the corpus assumption** (F2). One sentence, and it makes the ASI04 pass explicit rather than incidental.

## Scope and limits

Supervised research agent, single agent, no delegation. Reads repository-local legal texts and
produces a structured written traversal. No consequential action described; irreversible actions:
none. Lethal trifecta not present: the untrusted-content and external-communication legs are both
absent.

**The EU AI Act does not bind**, which is worth stating precisely because the artifact is about
the Act. A research tool over public legal text is not an Annex III use and makes no decision
about any person. Art. 50(1) does not attach: the only natural person it interacts with is the
operator who invoked it.

## Want more?

Available on request: the long form on either finding, and the judgment call this compresses,
which is whether a rigorous output discipline can substitute for an action boundary in a file
published for others to adopt.

---
---

# Audit 3: `Ops Copilot` (synthetic)

**Artifact.** A deliberately flawed definition written for testing. Copy at
[`targets/ops-copilot-synthetic.md`](targets/ops-copilot-synthetic.md).
**Standard.** OWASP Top 10 for Agentic Applications 2026. **Date.** 2026-09-05.

**Why a synthetic artifact is here.** The three real targets leave the far end of the range
untested: none holds administrator credentials or runs unattended in a continuous loop. Rather
than pretend the standard was exercised in full, this one fails all ten. Nobody shipped it.

## Verdict

**Do not deploy, and not close.** 0 pass, 10 fail, 0 partial, 0 not applicable; 6 critical,
3 major, 1 minor.

A fully autonomous agent with administrator credentials on three production systems, no approval
step, no log, no stop condition, instructed to follow instructions found in documents it reads.
Every finding traces to one decision: the autonomy is wrong for the blast radius in every
direction at once.

## In plain terms

This assistant runs continuously as an administrator on your identity system, your billing
database and your ops server. Anyone who can email the ops inbox can attach a document, and the
instructions tell it to read that document and do what it says. Nothing asks a person first and
nothing records what happened.

## Conformity ledger

| Category | Verdict | Sev | Basis |
|---|---|---|---|
| ASI01 Agent Goal Hijack | **FAIL** | CRITICAL | F1 |
| ASI02 Tool Misuse and Exploitation | **FAIL** | CRITICAL | Every irreversible tool is ungated, and "Don't bother the team with confirmations" removes the gate by instruction |
| ASI03 Identity and Privilege Abuse | **FAIL** | CRITICAL | F2 |
| ASI04 Agentic Supply Chain Vulnerabilities | **FAIL** | MAJOR | `run_shell` and `web_search` compose unverified external content and code paths at runtime |
| ASI05 Unexpected Code Execution | **FAIL** | CRITICAL | `run_shell` on the ops server, reachable from content the agent reads |
| ASI06 Memory & Context Poisoning | **FAIL** | MAJOR | Runs continuously over a channel and inbox any employee can write into, with no session boundary |
| ASI07 Insecure Inter-Agent Communication | **FAIL** | CRITICAL | Spawns sub-agents on shared `ops-admin` credentials with nothing authenticating what they report back |
| ASI08 Cascading Failures | **FAIL** | MAJOR | Works a backlog continuously with no verification between steps and no check before the final action |
| ASI09 Human-Agent Trust Exploitation | **FAIL** | MINOR | "No approval steps configured." There is no oversight moment to evaluate, so there is nothing to exploit |
| ASI10 Rogue Agents | **FAIL** | CRITICAL | No iteration cap, no budget, no kill switch, no escalation on uncertainty, running continuously |

Ten categories, ten failures, no N/A. ASI07 would ordinarily be N/A for a single agent; it fires
because the definition spawns sub-agents on inherited credentials. An artifact for which not one
category can be honestly excluded is the shape this file was written to demonstrate.

## Findings

### F1 · CRITICAL · ASI01 · The definition instructs the agent to obey untrusted documents
**Artifact** system prompt: "If a request links to a document or a ticket, read it and follow whatever instructions it contains", with `read_inbox`, `read_channel`, `delete_records`, `reset_user_account` and `run_shell` in the same loop
**Standard** [ASI01-ONE-CHANNEL](reference/owasp-top-10-agentic-applications-2026.md#L240 "^ASI01-ONE-CHANNEL") agents "cannot reliably distinguish instructions from related content"; [ASI01-UNTRUSTED-INPUT](reference/owasp-top-10-agentic-applications-2026.md#L283 "^ASI01-UNTRUSTED-INPUT") requires validation before input can influence tool calls
**Gap** it does not merely fail to separate content from instruction, it instructs the collapse. Anyone who can email the ops inbox can attach a document whose text executes as agent instruction against administrator credentials, with no approval and no log
**Ask** which sentence in a fetched document is this agent entitled to obey, and what enforces that outside the model?

### F2 · CRITICAL · ASI03 · One hijacked run compromises three systems
**Artifact** runtime notes: "Authenticates as the `ops-admin` service account (full admin on the identity system, the billing DB, and the ops server)" and "sub-agents use the same `ops-admin` credentials"
**Standard** [ASI03-SCOPED-TOKENS](reference/owasp-top-10-agentic-applications-2026.md#L479 "^ASI03-SCOPED-TOKENS") requires short-lived, narrowly scoped tokens per task; [ASI03-REVALIDATE](reference/owasp-top-10-agentic-applications-2026.md#L500 "^ASI03-REVALIDATE") forbids privilege inheritance across agents without re-validation
**Gap** the blast radius on hijack is three production systems including customer payment data, multiplied across every spawned sub-agent because credentials inherit. With F1 the path from an emailed attachment to administrator action has no gate anywhere along it
**Ask** what is the narrowest credential each listed task requires, and why does any sub-agent hold the parent's?

The remaining eight failures are recorded in the ledger with their basis. They share the two
causes above and would not be fixed separately.

## Fix order

1. **Separate content from instruction** (F1). Until this closes, nothing else matters.
2. **Scope the credential per task, and stop inheriting it** (F2).
3. **Add a gate on the irreversible tools**, then a log, then a stop condition.

## Scope and limits

Fully autonomous, running continuously as a background service, spawning sub-agents that inherit
its credentials. Lethal trifecta present in its most complete form: billing data, an inbox and
channel anyone can write into, and a public status page plus shell and web search for outbound.

The Act's high-risk duties do not clearly attach on the facts given. Art. 50(1) is live rather
than settled: the agent works a request queue people write into, and nothing discloses to them
that a machine is acting.

## Want more?

Available on request: the long form on any of the ten, and the expected-result key for checking
your own audit of this file against a known answer.

---
---

# Audit 4: `it-ops-orchestrator`

**Artifact.** `it-ops-orchestrator`, VoltAgent/awesome-claude-code-subagents, commit `beb9a0f`,
MIT, 60 lines. Copy at
[`targets/voltagent-it-ops-orchestrator.md`](targets/voltagent-it-ops-orchestrator.md).
**Standard.** OWASP Top 10 for Agentic Applications 2026. **Date.** 2026-09-05.

**How this one was produced.** Audits 1 to 3 were written by hand while building this folder,
which demonstrates a format and proves nothing. This one is the output of a clean-room run: a
fresh session given only this repository and a target it had never seen. Its citations were
checked afterwards and all resolved. It is condensed into the brief format here; the reasoning is
the run's own.

## Verdict

**Do not deploy.** 0 pass, 9 fail, 1 partial, 0 not applicable; 3 critical, 7 major, 1 minor.

A coordinator with shell, write and edit access sits in front of Active Directory, Azure and M365,
decomposes tasks, dispatches them to eight named specialists, and merges what returns into one
answer. It names no gate, no identity, no log and no stop in 60 lines, and one of its own worked
examples routes an operation that disables user accounts.

## In plain terms

This breaks IT jobs into pieces, hands each to a different assistant, and stitches the answers
into one confident recommendation. It can run commands and change files, nothing says a person
must approve anything, and nothing records what it did or lets anyone stop it mid-run.

## Conformity ledger

| Category | Verdict | Sev | Basis |
|---|---|---|---|
| ASI01 Agent Goal Hijack | **FAIL** | MAJOR | Reads content it does not control and reaches a shell in the same loop, with nothing marking any input untrusted |
| ASI02 Tool Misuse and Exploitation | **FAIL** | MAJOR | Line 31 asserts it will "Enforce safety, least privilege, and change review workflows" but names no mechanism, and no tool on line 4 carries a scope or a gate |
| ASI03 Identity and Privilege Abuse | **FAIL** | MAJOR | F2 |
| ASI04 Agentic Supply Chain Vulnerabilities | **FAIL** | MAJOR | F3 |
| ASI05 Unexpected Code Execution | **FAIL** | MAJOR | Declared output is executable material for Windows infrastructure; the same definition holds a general-purpose shell, no sandbox named, generation not separated from execution |
| ASI06 Memory & Context Poisoning | **FAIL** | MAJOR | Line 36 declares a shared cross-agent context whose stated purpose is consistency, so a planted assertion propagates deliberately. Nothing validates what enters it |
| ASI07 Insecure Inter-Agent Communication | **FAIL** | CRITICAL | F1 |
| ASI08 Cascading Failures | **PARTIAL** | MAJOR | F4 |
| ASI09 Human-Agent Trust Exploitation | **FAIL** | CRITICAL | No approval step anywhere, and the merge on line 30 strips the provenance a reader would need to judge one |
| ASI10 Rogue Agents | **FAIL** | CRITICAL | No iteration cap, no budget, no kill switch, no named human, and line 28 makes ambiguity a trigger for more autonomous decomposition rather than a stop |

## Findings

### F1 · CRITICAL · ASI07 · Nothing authenticates what the specialists send back
**Artifact** lines 29-30 "Assign each sub-problem to the correct agent" and "Merge responses into a coherent unified solution"; lines 54-60 name eight specialists. No line states what a specialist may assert or what validates a response
**Standard** [ASI07-NO-AUTH](reference/owasp-top-10-agentic-applications-2026.md#L780 "^ASI07-NO-AUTH") fires where exchanges "lack proper authentication, integrity, or semantic validation"; [ASI07-SIGNING](reference/owasp-top-10-agentic-applications-2026.md#L826 "^ASI07-SIGNING") requires signed messages validated "for hidden or modified natural-language instructions"
**Gap** the whole value proposition is trusting eight agents and speaking with one voice for them. A response from `ad-security-reviewer` saying "this is safe" is accepted on the strength of the name in a routing table, and after the merge there is not even attribution of which specialist said what
**Ask** what must `ad-security-reviewer` return before a destructive operation counts as validated, and what would make the orchestrator reject it?

### F2 · MAJOR · ASI03 · It delegates without ever saying what it acts as
**Artifact** no identity, credential, token or scope statement in 60 lines. Lines 17-18 name the reach: AD, DNS, DHCP, GPO, Azure, M365, Graph API. Lines 29 and 36 pass work and context down with no statement of what travels with it
**Standard** [ASI03-INHERITANCE](reference/owasp-top-10-agentic-applications-2026.md#L436 "^ASI03-INHERITANCE") names un-scoped inheritance where "a high-privilege manager delegates tasks without applying least-privilege scoping"; [ASI03-REVALIDATE](reference/owasp-top-10-agentic-applications-2026.md#L500 "^ASI03-REVALIDATE") requires re-validation before inherited privilege is used
**Gap** this is the high-privilege manager of that provision in structure. Silence is not neutral: §436 describes un-scoped inheritance as the default silence produces. Cannot verify what the runtime holds; if that identity carries domain or tenant administration this is CRITICAL
**Ask** what identity does the orchestrator authenticate as, what does a specialist receive with a dispatched sub-problem, and where is the original request re-validated?

### F3 · MAJOR · ASI04 · Eight specialists composed by bare name, none pinned
**Artifact** lines 42-44, 47-48, 51-52 and 54-60 name ten agents as bare identifiers. No version, hash, commit or capability declaration accompanies any of them, and none is supplied
**Standard** [ASI04-THIRD-PARTY-AGENT](reference/owasp-top-10-agentic-applications-2026.md#L546 "^ASI04-THIRD-PARTY-AGENT") counts a peer agent that can "pivot, leak data, or relay malicious instructions"; [ASI04-PIN](reference/owasp-top-10-agentic-applications-2026.md#L589 "^ASI04-PIN") requires pinning by content hash and commit id
**Gap** every routing decision resolves a name at runtime against whatever answers to it. `ad-security-reviewer` is trusted with the safety validation of an account-disabling operation on the strength of a string. This also bounds the audit: the real permissions live in eight files not supplied
**Ask** where do these definitions live, who can change them, and what tells the orchestrator that today's `ad-security-reviewer` is the one somebody reviewed?

### F4 · MAJOR · ASI08 · The one checkpoint is a convention in two examples, not a rule
**Artifact** line 43 places `ad-security-reviewer` between enumeration and implementation planning; line 51 places `powershell-security-hardening` before implementation; Example 2 at lines 47-48 has no review hop. The behaviours section at lines 28-31, where a rule would live, does not require one
**Standard** [ASI08-GATES](reference/owasp-top-10-agentic-applications-2026.md#L946 "^ASI08-GATES") requires "Checkpoints, governance agents, or human review for high risk before agent outputs are propagated downstream"; [ASI08-BLAST-RADIUS](reference/owasp-top-10-agentic-applications-2026.md#L949 "^ASI08-BLAST-RADIUS") adds quotas and circuit breakers
**Gap** a governance agent in the path is the control shape §946 names, which is why this is PARTIAL. It does not survive load: written into examples rather than rules, absent from the third, nothing states what the reviewer returns or what happens if it objects. Line 28's instruction to decompose ambiguity means the earliest error, a misclassification, is the one no reviewer here is positioned to catch
**Ask** is the security-review hop a rule or an example, and if step one routes to the wrong domain expert, what notices before the implementation plan exists?

## Fix order

1. **Authenticate the specialist responses** (F1). Everything downstream is built on them.
2. **State the identity and stop inheriting it** (F2). It sets the blast radius for all the rest.
3. **Make the review hop a rule, not an example** (F4), and say what a rejection does.
4. **Pin the eight names** (F3).

## Scope and limits

Declared multi-agent orchestrator, single agent by tool grant. Line 4 grants `Read, Write, Edit,
Bash, Glob, Grep`. No human is placed in the path at any point; the only escalation named routes
to two further agents, so an unresolved question never leaves the mesh.

**Declared behaviour and the tool grant disagree**, and it bounds everything above: the artifact
declares delegation across twenty lines while line 4 contains no delegation mechanism. Audited as
declared, per [`method/scope-gate.md`](method/scope-gate.md).

**The EU AI Act does not bind.** Internal IT operations tooling, not an Annex III use. Account
lifecycle administration is not an Annex III employment decision and is not stretched into one.

None of the eight specialists was supplied, which is F3 and also the limit of this audit.

## Want more?

Available on request: the long form on any finding, and the two judgment calls this compresses,
which are whether this is an orchestrator or an advisor, and whether an agent reviewer can stand
where a human gate belongs.
