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

**Artifact.** `agent-installer`, from VoltAgent/awesome-claude-code-subagents, commit
`beb9a0f`, MIT licensed. Copy at [`targets/voltagent-agent-installer.md`](targets/voltagent-agent-installer.md).

**Standard.** OWASP Top 10 for Agentic Applications, Version 2026 (December 2025).

**Date of audit.** 2026-09-05.

## Audit summary

No. This agent installs executable instructions fetched from a mutable third-party reference,
onto a path that every later session on the machine will load, behind a confirmation that shows
the human none of the parts that carry the risk.

Ledger: **3 pass, 4 fail, 2 partial, 1 not applicable.** Findings: 3 critical, 3 major, 2 minor,
plus 2 judgment calls.

## In plain terms

This helper downloads other AI agents from the internet and saves them onto your computer, where
your AI assistant will read and obey them from then on. It does ask before saving. But what it
shows you before you say yes is a one-line description, while the part that decides what the
downloaded agent is allowed to do to your machine is never put in front of you. It also always
downloads whatever the latest version happens to be, so what you approved and what you got are
not guaranteed to be the same file.

Do not use this to install agents you have not read in full yourself, first.

## Capability profile

Supervised developer utility, invoked interactively by the operator; single agent plus tools.
Reads and writes the local filesystem, fetches from a third-party GitHub repository, and holds
shell execution. Consequential actions reachable after one confirmation: writes into
`~/.claude/agents/` and `.claude/agents/`, which are directories later sessions load as
instructions; arbitrary shell via `Bash`. Irreversible: uninstall, which deletes.

Lethal trifecta present, all three legs named in the definition: private data (`Read`, `Glob`
over the local filesystem), untrusted content (`WebFetch` and `curl` against a repository the
operator does not control, line 24), external communication (`WebFetch` and `Bash`, line 4).

**The EU AI Act does not bind.** This is internal developer tooling, not an Annex III use, and
the only natural person it interacts with is the developer who invoked it, for whom the AI
nature of the interaction is obvious within the Art. 50(1) exception. That is honest scoping,
not a gap. Every finding below stands on OWASP alone.

## Conformity ledger

| Category | Verdict | Basis |
|---|---|---|
| ASI01 Agent Goal Hijack | **FAIL** | Finding 2 |
| ASI02 Tool Misuse and Exploitation | **PARTIAL** | Findings 4 and 8. A confirmation exists (line 70); `Bash` is far broader than the task, and uninstall shares its gate |
| ASI03 Identity and Privilege Abuse | **PASS** | The agent declares no separate credential and runs as the invoking operator. No token to over-scope, no service account to inherit, no privilege the operator did not already hold. Meets [ASI03-SCOPED-TOKENS](reference/owasp-top-10-agentic-applications-2026.md#L479 "^ASI03-SCOPED-TOKENS"), which asks that an agent's rights be capped by a permission boundary rather than inherited wholesale |
| ASI04 Agentic Supply Chain Vulnerabilities | **FAIL** | Findings 1 and 7 |
| ASI05 Unexpected Code Execution | **PARTIAL** | Finding 5. `Bash` is granted and the definition steers toward it, but no path is described in which fetched content is executed directly |
| ASI06 Memory & Context Poisoning | **FAIL** | Finding 3 |
| ASI07 Insecure Inter-Agent Communication | **N/A** | The artifact defines a single agent that neither calls nor is called by other agents at runtime. It writes files that *become* other agents, which is ASI04 and ASI06, not inter-agent messaging |
| ASI08 Cascading Failures | **PASS** | The workflow (lines 34-39) is short, linear, and human-initiated at each run, with no step conditioning on a previous inference. There is no multi-step chain for an early error to propagate through, so the planner-executor coupling [ASI08-COUPLING](reference/owasp-top-10-agentic-applications-2026.md#L895 "^ASI08-COUPLING") describes cannot arise |
| ASI09 Human-Agent Trust Exploitation | **FAIL** | Finding 6 |
| ASI10 Rogue Agents | **PASS** | The agent is invoked interactively for each action and holds no loop, schedule, or continuous operation. There is no unattended run for behaviour to drift within, and the operator is present at every step. The autonomy is matched to the task, so there is no unattended run for the drift [ASI10-DRIFT](reference/owasp-top-10-agentic-applications-2026.md#L1071 "^ASI10-DRIFT") describes to occur in |

## Findings

### Finding 1. The install target is a mutable reference, so what a user approved and what gets written are not guaranteed to be the same file. [CRITICAL]

**Where, in the artifact.** Line 24: the raw agent file URL is
`https://raw.githubusercontent.com/VoltAgent/awesome-claude-code-subagents/main/categories/{category-name}/{agent-name}.md`.
The path segment is `main`, a moving branch pointer, not a commit or a content hash. Line 37
downloads from that URL and line 38 saves it.

**What the standard requires.** ASI04 prescribes pinning "prompts, tools, and configs by content
hash and commit ID" ([§L589](reference/owasp-top-10-agentic-applications-2026.md#L589 "^ASI04-PIN")), and
under dependency gatekeeping, "Allowlist and pin; ... verify provenance before install or
activation; auto-reject unsigned or unverified"
([§L579](reference/owasp-top-10-agentic-applications-2026.md#L579 "^ASI04-GATEKEEPING")).

**The gap.** Nothing in the definition pins, hashes, or verifies. The file that lands is whatever
`main` resolves to at the moment of the fetch. A user who reads a description at 10:00 and
installs at 10:05 has no guarantee they received the artifact they evaluated, and a compromise
of the upstream repository propagates to every installation immediately, with no version to roll
back to and no record of what was received.

**For the owner.** What commit or content hash does an install pin to, and what does the agent
compare the downloaded file against before writing it to disk?

### Finding 2. Fetched third-party content becomes instructions the assistant will obey, with no boundary between content and instruction. [CRITICAL]

**Where, in the artifact.** Line 4 grants `WebFetch` and `Bash`. Line 24 points them at a
third-party repository. Line 74 instructs: "Preserve exact file content when downloading (don't
modify agent files)." Lines 35-38 write that content into `~/.claude/agents/` or
`.claude/agents/`.

**What the standard requires.** ASI01 identifies the root cause as agents that "cannot reliably
distinguish instructions from related content"
([§L240](reference/owasp-top-10-agentic-applications-2026.md#L240 "^ASI01-ONE-CHANNEL")), and its first mitigation is
to treat all natural-language input, including retrieved content, as untrusted and route it
through injection safeguards "before they can influence goal selection, planning, or tool calls"
([§L283](reference/owasp-top-10-agentic-applications-2026.md#L283 "^ASI01-UNTRUSTED-INPUT")).

**The gap.** The content fetched here is not merely read, it is *installed as a system prompt
with its own tool grant*. A downloaded file whose frontmatter reads `tools: Bash` and whose body
contains instructions arrives with no inspection of either. Note the interaction with line 74:
preserving exact content is correct for integrity and is the right instruction, but combined
with no inspection step it means the definition guarantees faithful delivery of something nobody
looked at. Integrity without verification is not a control.

**For the owner.** Before a fetched file is written, what inspects its `tools:` grant and its
instruction body, and what would cause the install to be refused?

### Finding 3. What is installed persists into every later session on the machine. [CRITICAL]

**Where, in the artifact.** Line 35 offers global installation to `~/.claude/agents/`. Capability
4 (line 16) states the same. This is a user-level directory, not a project one.

**What the standard requires.** ASI06 covers adversaries corrupting or seeding retained context
"causing future reasoning, planning, or tool use to become biased, unsafe, or aid exfiltration"
([§L688](reference/owasp-top-10-agentic-applications-2026.md#L688 "^ASI06-POISONING")).

**The gap.** An agent definition written into `~/.claude/agents/` is not transient context. It is
loaded by future sessions, across every project on that machine, until someone removes it. The
blast radius of one bad install is therefore not the session that performed it but every session
after it, and the corruption survives the process that introduced it. This is why the finding is
critical despite the install itself being confirmed: the confirmation is a one-time event and
the consequence is permanent.

**For the owner.** Does a global install carry any expiry, review prompt, or integrity re-check
on later load, and how would an operator discover that an installed agent had changed under them?

### Finding 4. `Bash` is granted where the task needs an HTTP GET and a file write. [MAJOR]

**Where, in the artifact.** Line 4: `tools: Bash, WebFetch, Read, Write, Glob`. Line 29 offers
"WebFetch or Bash with curl" for the same fetch. Line 73: "Use `curl -s` for silent downloads."

**What the standard requires.** ASI02 prescribes "enforcing least privilege for agent tools"
([§L286](reference/owasp-top-10-agentic-applications-2026.md#L286 "^ASI01-LEAST-PRIVILEGE")). The standard's Least-Agency
framing extends this: capability deployed where it is not needed expands attack surface without
adding value.

**The gap.** Every task the definition describes (list, search, download, save, delete) is served
by `WebFetch`, `Write`, `Read` and `Glob`. `Bash` adds arbitrary command execution to an agent
whose job is to move a markdown file. Line 73 makes it worse by preference rather than by
necessity: `curl -s` is specified for its silence, so the definition's own guidance routes the
network fetch through a shell and suppresses its output.

**For the owner.** Which described capability requires `Bash` that `WebFetch` and `Write` cannot
serve, and if the answer is none, what is it doing in the grant?

### Finding 5. Shell execution runs on the operator's own machine, unsandboxed. [MAJOR]

**Where, in the artifact.** Line 4 grants `Bash`; lines 35-38 write to paths on the operator's
filesystem. Nothing in the definition mentions a container, a sandbox, or a network restriction.

**What the standard requires.** ASI04 mitigation 3: "Run sensitive agents in sandboxed containers
with strict network or syscall limits"
([§L581](reference/owasp-top-10-agentic-applications-2026.md#L581 "^ASI04-SANDBOX")).

**The gap.** An agent whose entire purpose is to ingest third-party content holds shell on the
host that ingests it, with no isolation named. Marked MAJOR rather than CRITICAL because no path
in the definition executes fetched content directly; the exposure is the combination of a
supply-chain role with an unsandboxed execution capability, not a described execution of
untrusted input.

**For the owner.** Where does `Bash` execute, and what would contain a command that turned out to
be attacker-influenced?

### Finding 6. The confirmation shows the human the one part of the file that carries no risk. [MAJOR]

**Where, in the artifact.** Line 70: "Always confirm before installing/uninstalling." Line 71:
"Show the agent's description before installing if possible."

**What the standard requires.** ASI09 mitigation 4 calls for a "plain-language risk summary (not
model-generated rationales)" at the point of decision
([§L1030](reference/owasp-top-10-agentic-applications-2026.md#L1030 "^ASI09-RISK-SUMMARY")), and mitigation 7 requires
separating preview from effect, displaying "a risk badge with source provenance and expected side
effects" ([§L1044](reference/owasp-top-10-agentic-applications-2026.md#L1044 "^ASI09-PREVIEW")).

**The gap.** The gate exists, which is why ASI02 is scored PARTIAL rather than FAIL, and line 70
is a genuine control. But what it puts in front of the operator is the `description` field: the
marketing line. The `tools:` grant, the instruction body, the source commit, and the destination's
scope are all absent from the approval moment. The operator is asked to approve the one part of
the artifact that cannot hurt them. "If possible" (line 71) weakens even that to discretionary.

An approval that does not surface the risk is not oversight. It transfers responsibility to the
operator without transferring the information needed to exercise it.

**For the owner.** At the moment of confirmation, does the operator see the `tools:` line, the
source commit, and the install scope, and if not, what is the confirmation for?

### Finding 7. Nothing records what was installed, from where, or when. [MINOR]

**Where, in the artifact.** No logging appears anywhere in the definition. Line 39 confirms
"successful installation" to the screen; that message is not a record.

**What the standard requires.** ASI09 mitigation 2: "Immutable logs: Keep tamper-proof records of
user queries and agent actions for audit and forensics"
([§L1025](reference/owasp-top-10-agentic-applications-2026.md#L1025 "^ASI09-IMMUTABLE-LOGS")). ASI04 mitigation 6
requires re-checking signatures, hashes and SBOMs at runtime and monitoring lineage
([§L587](reference/owasp-top-10-agentic-applications-2026.md#L587 "^ASI04-RECHECK")). Observability is named in
the standard's front matter as non-negotiable.

**The gap.** After a bad install, an operator cannot reconstruct which upstream state they
received. With Finding 1 unresolved this compounds: not only is the version unpinned, there is no
record of which unpinned version arrived. Scored MINOR because the immediate harm is bounded and
the remedy is cheap, but it is what turns Finding 1 from recoverable into not.

**For the owner.** Where would an operator look to find out which commit a given installed agent
came from?

### Finding 8. Uninstall shares one clause with install and deletes without a distinct gate. [MINOR]

**Where, in the artifact.** Capability 6 (line 18): "Uninstall agents." Line 70 covers both
operations in a single instruction: "Always confirm before installing/uninstalling." No workflow
section describes uninstall, unlike browse, install and search (lines 28-44).

**What the standard requires.** ASI02 pairs least privilege with "requiring human approval for
high-impact or goal-changing actions"
([§L286](reference/owasp-top-10-agentic-applications-2026.md#L286 "^ASI01-LEAST-PRIVILEGE")).

**The gap.** Delete is the only irreversible operation in the artifact and it is the only
capability with no described procedure: no statement of what is shown, what scope is targeted, or
whether a glob could match more than one file. It inherits a confirmation written primarily for
install.

**For the owner.** What does the operator see before an uninstall, and can an uninstall target
more than one file in a single confirmation?

## Judgment calls

**`model: haiku` on the supply-chain path (line 5).** Defensible: this is mechanical work
(list, fetch, save) and matching model cost to task complexity is sound engineering. Against: the
one part of this job that benefits from careful reading is inspecting a fetched third-party
definition adversarially, and if Finding 2 is addressed by adding an inspection step, the cheapest
model in the range would be performing it. The decision turns on whether inspection is added. If
the answer to Finding 2 is "the model reads the file and flags anything suspicious", then the
model choice becomes load-bearing and should be revisited. Owner: the builder.

**Global versus local install as an operator choice (line 35).** Defensible: asking is better
than assuming, and some agents genuinely belong at user scope. Against: the question is posed as
a location preference rather than a scope decision, so the operator is not told that "global"
means "every project on this machine, indefinitely". The decision turns on whether the prompt
communicates blast radius or merely a path. Owner: the builder.

## What holds

The identity model is genuinely clean: the agent declares no credential of its own and holds
nothing the invoking operator did not already hold, which removes the entire ASI03 category
rather than mitigating it.

Line 74, "Preserve exact file content when downloading (don't modify agent files)", is the right
instruction and is rarer than it should be. It rules out silent mutation in transit, so an
operator who *does* read the installed file reads what upstream published.

The workflow is short, linear and human-initiated, with no step conditioning on a previous
inference, which is why ASI08 passes on structure rather than on luck.

The autonomy level is matched to the task. This agent is invoked for one action at a time and
holds no loop, schedule, or unattended run, so ASI10 passes on design rather than on the absence
of an opportunity to drift. Given what it installs, that restraint is doing real work.

## Observations outside the standard

The description field (line 3) says the agent installs from "the awesome-claude-code-subagents
repository", and the endpoints on lines 22-24 hard-code that one repository. A single named
upstream is a meaningfully smaller attack surface than an arbitrary URL, and it is close to what
ASI04 calls a curated registry
([§L578](reference/owasp-top-10-agentic-applications-2026.md#L578 "^ASI04-REGISTRIES")). I have not scored it as a
pass, because the standard's curated-registry language is paired with signing and attestation
that are absent here, and a hard-coded source is not the same thing as a verified one. Noting it
as a real design decision that a fix should preserve rather than discard.

---
---

# Audit 2: `eu-ai-act-map` AGENTS.md

**Artifact.** The repository-level operating instructions for the EU AI Act Map, a public
repository that reads Regulation (EU) 2024/1689 as a navigable decision graph. Copy at
[`targets/eu-ai-act-map-agents.md`](targets/eu-ai-act-map-agents.md).

**Standard.** OWASP Top 10 for Agentic Applications, Version 2026 (December 2025).

**Date of audit.** 2026-09-05.

**Why this artifact is here.** An auditor that only ever finds problems is not discriminating,
it is just pessimistic. This target mostly passes, and the audit is included to show what a pass
looks like when it is earned and what an honest N/A looks like when a category cannot arise.

## Audit summary

Yes, as defined. This is a read-only research agent with no consequential tool and no autonomous
action. Most of the standard's categories cannot arise for it, and the audit says so with the
reason rather than padding the ledger.

Ledger: **4 pass, 1 fail, 1 partial, 4 not applicable.** Findings: 1 major, 1 minor, plus 1
judgment call.

## In plain terms

This is a set of instructions for an assistant that looks up EU law in a folder of legal texts
and answers questions about it. It cannot send anything, change anything, or spend anything. Its
main risk is being wrong, and its instructions are unusually strict about not being wrong. The one
real gap is that it never states what the assistant is allowed to touch, so it inherits whatever
permissions the surrounding tool happens to grant.

## Capability profile

Supervised research agent, single agent, no delegation. Reads a corpus of legal texts inside its
own repository (line 13 instructs grepping and reading `corpora/eu/ai-act-2024-1689-en.md`) and
produces a structured written traversal (lines 28-46). No tool grant is declared anywhere in the
artifact. No consequential action is described: nothing sends, writes, deletes, pays, publishes,
or executes. Irreversible autonomous actions: none.

Lethal trifecta not present. The agent reads repository-local files it and its owner control, and
has no described outbound channel; the untrusted-content leg and the external-communication leg
are both absent.

**The EU AI Act does not bind**, which is worth stating precisely because the artifact is about
the Act. It is a research tool operating on public legal text, not an Annex III use, and it makes
no decision about any person. Art. 50(1) does not attach: the only natural person it interacts
with is the operator who invoked it, for whom the AI nature of the interaction is obvious. Line
58 requires every output to end "Orientation aid, not legal advice", which is not a legal
obligation here but is the disclosure that would matter if the tool were ever put in front of
third parties.

## Conformity ledger

| Category | Verdict | Basis |
|---|---|---|
| ASI01 Agent Goal Hijack | **PARTIAL** | Finding 2. The corpus it reads is trusted-by-assumption, and nothing states that assumption |
| ASI02 Tool Misuse and Exploitation | **FAIL** | Finding 1. Not because a tool is misused, but because no tool boundary is stated at all |
| ASI03 Identity and Privilege Abuse | **N/A** | The artifact declares no credential and describes no authenticated system. There is no identity to abuse |
| ASI04 Agentic Supply Chain Vulnerabilities | **PASS** | The agent composes nothing at runtime. Its corpus is version-controlled in the same repository, and line 13 names the specific file path it reads rather than resolving a source at runtime, which is the pinned reference [ASI04-PIN](reference/owasp-top-10-agentic-applications-2026.md#L589 "^ASI04-PIN") asks for |
| ASI05 Unexpected Code Execution | **N/A** | No execution capability is described, and the artifact's output is a written traversal, not a command |
| ASI06 Memory & Context Poisoning | **N/A** | The agent writes nothing that persists into a later session. Its corpus is read-only input under version control, not a memory store it feeds |
| ASI07 Insecure Inter-Agent Communication | **N/A** | Single agent. No delegation, no spawning, no inbound agent messages |
| ASI08 Cascading Failures | **PASS** | Lines 19-24 impose an ordered four-layer traversal in which each layer states its own finding and cites its own anchor, so an error at Layer 1 is visible at Layer 1 rather than silently carried. Line 44 requires missing facts to be surfaced as open points rather than assumed, which is the checkpoint-before-propagation [ASI08-GATES](reference/owasp-top-10-agentic-applications-2026.md#L946 "^ASI08-GATES") prescribes |
| ASI09 Human-Agent Trust Exploitation | **PASS** | The strongest part of the artifact. Lines 13-15 require reading the source before asserting, forbid filling gaps from memory, and forbid inventing line numbers. Line 14 requires anything outside the corpus to be marked "not in corpus — external source required". Line 58 requires every output to disclaim legal advice. This is the plain-language risk summary [ASI09-RISK-SUMMARY](reference/owasp-top-10-agentic-applications-2026.md#L1030 "^ASI09-RISK-SUMMARY") prescribes, applied to epistemic rather than transactional risk |
| ASI10 Rogue Agents | **PASS** | Line 56 requires the agent to ask before routing when a fact that changes the outcome is missing, rather than guessing. Escalation on uncertainty is what stands against the behavioural drift [ASI10-DRIFT](reference/owasp-top-10-agentic-applications-2026.md#L1071 "^ASI10-DRIFT") describes, and it is present and unambiguous |

## Findings

### Finding 1. The definition never states what the agent may touch. [MAJOR]

**Where, in the artifact.** There is no frontmatter, no tools list, and no permissions statement
anywhere in the 62 lines. Line 13 implies read and grep over the repository; nothing states a
boundary, and nothing forbids anything.

**What the standard requires.** ASI02's mitigations are built on "enforcing least privilege for
agent tools" ([§L286](reference/owasp-top-10-agentic-applications-2026.md#L286 "^ASI01-LEAST-PRIVILEGE")). Least privilege
presupposes a stated privilege.

**The gap.** The artifact inherits whatever the surrounding harness grants. Run under a
permissive configuration, this same definition has write and shell access that nothing in its
text contemplates, and its careful conduct rules (lines 54-58) govern its *output* while saying
nothing about its *actions*. The instructions are disciplined about what the agent may claim and
silent about what it may do.

This is scored MAJOR rather than MINOR because the artifact is published for others to use: a
reader adopting it into their own project inherits the silence along with the discipline.

**For the owner.** What is this agent permitted to touch, and where is that written down such
that a user adopting the file inherits the boundary along with the instructions?

### Finding 2. The corpus is trusted by assumption, and the assumption is not stated. [MINOR]

**Where, in the artifact.** Line 13 instructs the agent to locate articles in
`corpora/eu/ai-act-2024-1689-en.md` and read the relevant lines. Lines 13-15 build the entire
citation discipline on that file being what it claims to be. Nothing states that the file is
trusted, why, or what would happen if it were altered.

**What the standard requires.** ASI01's first mitigation is to treat retrieved content as
untrusted and validate it before it influences the agent's reasoning
([§L283](reference/owasp-top-10-agentic-applications-2026.md#L283 "^ASI01-UNTRUSTED-INPUT")).

**The gap.** The trust is almost certainly justified: the corpus is version-controlled in the
same repository, carries a provenance header, and is not user-writable at runtime. That is a good
security position and it is why ASI04 passes. But it is an *unstated* position, so a user who
forks the repository and points it at their own corpus inherits a citation discipline that reads
as rigorous while resting on an assumption nobody wrote down. The stricter the citation rules,
the more the output's credibility depends on the integrity of the file being cited.

**For the owner.** What is the agent entitled to assume about the corpus, and what should it do
if a cited line does not say what the map claims it says?

## Judgment calls

**A rigorous output discipline can substitute for an action boundary, up to a point.** The
artifact's conduct rules (lines 13-15, 54-58) are stricter than most production agent definitions
achieve, and it is arguable that an agent which only ever produces a cited written traversal does
not need a tools declaration. Against: the definition is a portable file, and portability is
exactly the condition under which the surrounding permissions change without the instructions
changing. The decision turns on whether the artifact is understood as repository-local
configuration or as a shareable agent definition. It is published in a public repository, which
pushes toward the second reading. Owner: the builder.

## What holds

Lines 13-15 are the substance of the pass: read the source before asserting, never fill gaps from
memory and present them as grounded, never invent a line number. Most agent definitions that
handle authoritative sources assert this as a value; this one states it as three operational
prohibitions with a named file to check against.

Line 14's requirement to mark anything outside the corpus as "not in corpus — external source
required" is a genuine control rather than a caveat, because it forces the boundary of the
knowledge base into the output where a reader sees it.

Line 56, ask before routing when a decisive fact is missing, is escalation-on-uncertainty stated
plainly, and it is the control most agent definitions omit entirely.

## Observations outside the standard

The four-layer traversal (lines 19-24) resolves scope, object, role and risk tier in a fixed
order, each citing its own anchor. OWASP has no provision about the epistemic structure of an
agent's output, so this is not a finding in either direction. It is worth noting as the mechanism
behind the ASI08 pass: the reason an error does not cascade here is that the artifact's output
format makes each step's reasoning separately inspectable, which is a design property the
standard benefits from without describing.

---
---

# Audit 3: `Ops Copilot` (synthetic)

**Artifact.** A deliberately flawed agent definition, written for testing. Copy at
[`targets/ops-copilot-synthetic.md`](targets/ops-copilot-synthetic.md).

**Why a synthetic artifact is included.** Audits 1 and 2 are real, and between them they leave
four categories untested: neither holds a broad credential (ASI03), spawns sub-agents (ASI07),
runs unattended (ASI10 at full autonomy), or chains enough steps for an error to compound
(ASI08). A synthetic artifact with those properties is the honest way to show the auditor working
across the whole standard. It is clearly marked as synthetic and no claim is made that anyone
shipped it.

Condensed to the ledger and the two leading findings, since the full output format is
demonstrated twice above. The ledger's Basis column carries the substance of the other eight.

## Audit summary

No, and not close. A fully autonomous agent with administrator credentials, no approval step, no
log, and no stop condition, instructed to follow instructions found in documents it reads.

Ledger: **0 pass, 10 fail, 0 partial, 0 not applicable.** Ten failures, of which six reach
CRITICAL. The two leading ones are written out below; the remaining eight are summarised in the
ledger.

## Capability profile

Fully autonomous ops agent running continuously as a background service, able to spawn
sub-agents that inherit its credentials. Authenticates as `ops-admin`: full administrator on the
identity system, the billing database, and the ops server. Consequential actions reachable with
no human in the path: account reset, account provisioning, record deletion, billing queries,
public status-page publication, arbitrary shell. Irreversible: `delete_records`,
`update_status_page`, `reset_user_account`. No approval steps, no action log, no iteration or
budget cap.

Lethal trifecta present in its most complete form: private data (`query_billing_db`, customer
payment data), untrusted content (Slack channel, ops inbox, and the explicit instruction to read
linked documents and follow their instructions), external communication (`update_status_page`
publishes publicly, `run_shell` and `web_search` both carry data outbound).

The EU AI Act's high-risk duties do not clearly attach on the facts given, since no Annex III use
is described. Art. 50(1) is a live question rather than a settled one: the agent works a request
queue that people write into, and nothing discloses to them that a machine is acting.

## Conformity ledger

| Category | Verdict | Basis |
|---|---|---|
| ASI01 Agent Goal Hijack | **FAIL** | Finding 1 |
| ASI02 Tool Misuse and Exploitation | **FAIL** | Every irreversible tool is ungated; "Don't bother the team with confirmations" removes the gate by instruction |
| ASI03 Identity and Privilege Abuse | **FAIL** | Finding 2 |
| ASI04 Agentic Supply Chain Vulnerabilities | **FAIL** | `run_shell` and `web_search` compose unverified external content and code paths at runtime |
| ASI05 Unexpected Code Execution | **FAIL** | `run_shell` on the ops server, reachable from content the agent reads |
| ASI06 Memory & Context Poisoning | **FAIL** | Continuous operation over a shared channel and inbox any employee can write into, with no session boundary |
| ASI07 Insecure Inter-Agent Communication | **FAIL** | Spawns sub-agents on shared `ops-admin` credentials with nothing authenticating what they report back |
| ASI08 Cascading Failures | **FAIL** | Works a backlog continuously with no verification between steps and no check before the final action |
| ASI09 Human-Agent Trust Exploitation | **FAIL** | "No approval steps configured." There is no oversight moment to evaluate |
| ASI10 Rogue Agents | **FAIL** | No iteration cap, no budget limit, no kill switch, no escalation on uncertainty, running continuously |

Ten categories, ten failures, no N/A. ASI07 would ordinarily be N/A for a single agent, but it
fires here because the definition spawns sub-agents on inherited credentials. An artifact for
which not one category can be honestly excluded is one whose autonomy is wrong for its blast
radius in every direction at once.

## Finding 1. The definition instructs the agent to follow instructions found in untrusted documents. [CRITICAL]

**Where, in the artifact.** The system prompt: "If a request links to a document or a ticket,
read it and follow whatever instructions it contains." Combined with `read_inbox` and
`read_channel`, both of which any outsider who can email the ops address can write into, and with
`delete_records`, `reset_user_account` and `run_shell` in the same loop.

**What the standard requires.** ASI01 identifies that agents "cannot reliably distinguish
instructions from related content"
([§L240](reference/owasp-top-10-agentic-applications-2026.md#L240 "^ASI01-ONE-CHANNEL")) and requires that all
retrieved content be treated as untrusted and validated "before they can influence goal
selection, planning, or tool calls"
([§L283](reference/owasp-top-10-agentic-applications-2026.md#L283 "^ASI01-UNTRUSTED-INPUT")).

**The gap.** The definition does not merely fail to separate content from instruction, it
instructs the collapse explicitly. Any person who can send mail to the ops inbox can attach a
document whose text is executed as agent instruction, against administrator credentials, with no
approval and no log. This is the shortest path from an outside email to a shell command on the
ops server that the standard describes.

**For the owner.** Which sentence in a fetched document is the agent entitled to obey, and what
enforces that distinction outside the model?

## Finding 2. One hijacked run is a total compromise of three systems. [CRITICAL]

**Where, in the artifact.** Runtime notes: "Authenticates as the `ops-admin` service account
(full admin on the identity system, the billing DB, and the ops server)" and "sub-agents use the
same `ops-admin` credentials".

**What the standard requires.** ASI03 covers identity and privilege abuse
([§L414](reference/owasp-top-10-agentic-applications-2026.md#L414 "^ASI03")); ASI02's mitigations rest on
least privilege for agent tools
([§L286](reference/owasp-top-10-agentic-applications-2026.md#L286 "^ASI01-LEAST-PRIVILEGE")).

**The gap.** The blast radius on hijack is not the task, it is three production systems including
customer payment data, and it multiplies across every spawned sub-agent because credentials
inherit. Taken with Finding 1, the path from an emailed attachment to administrator action on all
three systems has no gate anywhere along it.

**For the owner.** What is the narrowest credential each listed task actually requires, and why
does any sub-agent hold the parent's?

---
---

# Audit 4: `it-ops-orchestrator`

**Artifact.** `it-ops-orchestrator`, from VoltAgent/awesome-claude-code-subagents, commit
`beb9a0f`, MIT licensed. Copy at [`targets/voltagent-it-ops-orchestrator.md`](targets/voltagent-it-ops-orchestrator.md).

**Standard.** OWASP Top 10 for Agentic Applications, Version 2026 (December 2025).

**Date of audit.** 2026-09-05.

**How this audit was produced, and why that matters.** The three audits above were written by
hand while building the folder, which makes them demonstrations of the format rather than
evidence that it works. This one was not. It is the output of a clean-room run: a fresh session
given only this repository and this target, with no knowledge of the other audits and no
involvement from the author. Its citations were then checked line by line, and all thirty-eight
resolved. It is included in that form, condensed but not rewritten, because an auditor whose
only worked examples were written by its own author has demonstrated a format and nothing else.

**Why this target.** Audits 1 and 2 are single agents, so ASI07 is N/A in one and N/A in the
other. This is the multi-agent case: a coordinator that decomposes work, dispatches it to eight
named specialists, and merges what returns into one answer.

Condensed to the ledger, the three findings that turn on multi-agent structure, and the judgment
call that governs the rest. The full output format is demonstrated twice above.

## Audit summary

No. A coordinator with shell, write and edit access sits in front of Windows directory and cloud
administration, decomposes tasks, dispatches them to eight specialists, and merges what comes
back into a single answer. It names no gate, no identity, no log and no stop anywhere in its 60
lines, and one of its own worked examples routes an operation that disables user accounts.

Ledger: **0 pass, 9 fail, 1 partial, 0 not applicable.** Findings: 3 critical, 7 major, 1 minor.
Several share one root cause, which is that the definition names no human at any point; the
critical rank goes to the shortest paths from an ordinary mistake to a directory change.

## Capability profile

Declared multi-agent orchestrator, single agent by tool grant. Line 4 grants `Read, Write, Edit,
Bash, Glob, Grep`. Lines 28 to 30 declare the loop: decompose, "Assign each sub-problem to the
correct agent", "Merge responses into a coherent unified solution". Lines 54 to 60 name eight
specialists. Operating domain, lines 15 to 20: PowerShell, .NET, Active Directory, DNS, DHCP,
GPO, on-premises Windows, Azure, M365, Graph API.

The definition places **no human in the path at any point**. The only escalation it names (line
60) routes escalated tasks to two further agents, so an unresolved question never leaves the
mesh. Consequential actions reachable with no human confirming: arbitrary shell, arbitrary file
writes and edits, and dispatch of infrastructure work. Irreversible: file overwrite via `Edit`,
and whatever the dispatched implementation carries out; line 41 names disabling AD accounts.

**Declared behaviour and tool grant disagree**, and it bounds everything below. The artifact
declares delegation across roughly twenty lines while line 4 contains no delegation mechanism.
Audited as declared, per [`method/scope-gate.md`](method/scope-gate.md); see the judgment call.

**The EU AI Act does not bind.** Internal IT operations tooling, not an Annex III use, and the
only natural person it interacts with is the administrator who invoked it, for whom the artificial
nature of the interaction is obvious within the Art. 50(1) exception. Account lifecycle
administration is not an Annex III employment or worker-management decision and is not stretched
into one here.

**What could not be seen.** None of the eight specialists was supplied. This audit covers the
coordinator only, which is itself Finding 8.

## Conformity ledger

| Category | Verdict | Basis |
|---|---|---|
| ASI01 Agent Goal Hijack | **FAIL** | Reads content it does not control and reaches a shell in the same loop, with nothing marking any input untrusted |
| ASI02 Tool Misuse and Exploitation | **FAIL** | Line 31 asserts enforcement of "safety, least privilege, and change review workflows" but names no mechanism, and no tool on line 4 carries a scope or a gate |
| ASI03 Identity and Privilege Abuse | **FAIL** | Finding 7 |
| ASI04 Agentic Supply Chain Vulnerabilities | **FAIL** | Finding 8 |
| ASI05 Unexpected Code Execution | **FAIL** | Declared output is executable material for Windows infrastructure; the same definition holds a general-purpose shell, with no sandbox named and generation not separated from execution |
| ASI06 Memory & Context Poisoning | **FAIL** | Line 36 declares a shared cross-agent context whose stated purpose is consistency, so a planted assertion propagates deliberately. Nothing validates what enters it |
| ASI07 Insecure Inter-Agent Communication | **FAIL** | Finding 2 |
| ASI08 Cascading Failures | **PARTIAL** | Finding 10. A checkpoint of the shape the standard names does exist at lines 43 and 51, but it is illustration rather than rule and is absent from Example 2 |
| ASI09 Human-Agent Trust Exploitation | **FAIL** | No approval step anywhere, and the merge on line 30 strips the provenance a reader would need |
| ASI10 Rogue Agents | **FAIL** | No iteration cap, no budget ceiling, no kill switch, no named human, and line 28 makes ambiguity a trigger for more autonomous decomposition rather than for a stop |

Zero passes. Under Rule 2 a pass must name a control, and none of the four things that come
closest (line 31's enforcement claim, the review hops at lines 43 and 51, line 37's boundary
highlighting, line 44's "Implementation plan" rather than "Implementation") meets what the
standard prescribes for its category. Three are dealt with below instead.

## Findings

### Finding 2. Nothing authenticates what the specialists send back, and their answers become the answer. [CRITICAL]

**Where, in the artifact.** Lines 29 and 30: "Assign each sub-problem to the correct agent" and
"Merge responses into a coherent unified solution". Lines 54 to 60 name eight specialists it
delegates to and receives from. No line states what a specialist is trusted to assert, what
validates a response, or what a response must look like.

**What the standard requires.** ASI07 (insecure inter-agent communication: messages between
agents that nothing verifies) fires when exchanges "lack proper authentication, integrity, or
semantic validation" ([§L780](reference/owasp-top-10-agentic-applications-2026.md#L780 "^ASI07-NO-AUTH")). The
mitigations require per-agent credentials and mutual authentication
([§L823](reference/owasp-top-10-agentic-applications-2026.md#L823 "^ASI07-CHANNELS")), signed messages validated
"for hidden or modified natural-language instructions"
([§L826](reference/owasp-top-10-agentic-applications-2026.md#L826 "^ASI07-SIGNING")), and "signed agent cards and
continuous verification before accepting discovery or coordination messages"
([§L848](reference/owasp-top-10-agentic-applications-2026.md#L848 "^ASI07-AGENT-CARDS")).

**The gap.** The artifact's entire value proposition is trusting eight other agents and speaking
with one voice on their behalf. A response from `ad-security-reviewer` saying "this is safe" is
accepted on the strength of the name in the routing table. There is no schema, no signature, no
provenance tag, and after the merge on line 30 there is not even attribution of which specialist
said what. A forged or simply wrong safety validation at line 43 is indistinguishable from a real
one at the point where it matters.

**For the owner.** What does `ad-security-reviewer` have to return before the orchestrator treats
a destructive operation as validated, and what would make the orchestrator reject that response?

### Finding 7. The definition delegates without ever saying what it acts as, in a domain where that is the whole question. [MAJOR]

**Where, in the artifact.** No identity, credential, token, service account or scope statement
appears anywhere in the 60 lines. Lines 17 and 18 name the reach: "AD, DNS, DHCP, GPO, on-prem
Windows" and "Azure, M365, Graph API". Lines 29 and 36 pass work and context down to specialists
with no statement of what travels with it. Line 31 claims "least privilege" as an outcome.

**What the standard requires.** ASI03 (identity and privilege abuse: an agent acting with more
authority than its task needs) names "Un-scoped Privilege Inheritance" as its first vulnerability,
arising "when a high-privilege manager delegates tasks without applying least-privilege scoping
... passing its full access context"
([§L436](reference/owasp-top-10-agentic-applications-2026.md#L436 "^ASI03-INHERITANCE")), and the Confused Deputy case
where "agents often trust internal requests by default"
([§L445](reference/owasp-top-10-agentic-applications-2026.md#L445 "^ASI03-CONFUSED-DEPUTY")). Its mitigations require
short-lived, narrowly scoped, task-bound tokens
([§L479](reference/owasp-top-10-agentic-applications-2026.md#L479 "^ASI03-SCOPED-TOKENS")) and, directly on point,
"Prevent privilege inheritance across agents unless the original intent is re-validated"
([§L500](reference/owasp-top-10-agentic-applications-2026.md#L500 "^ASI03-REVALIDATE")).

**The gap.** This artifact is the high-privilege manager of [§L436](reference/owasp-top-10-agentic-applications-2026.md#L436 "^ASI03-INHERITANCE") in structure: it sits above
eight specialists and hands work down. It does not scope what goes down with the work, does not
state what it authenticates as, and does not say whether a specialist re-validates the original
request or accepts it as internal and therefore trusted. Silence is not neutral here; [§L436](reference/owasp-top-10-agentic-applications-2026.md#L436 "^ASI03-INHERITANCE")
describes un-scoped inheritance as the default that silence produces. Cannot verify from the
definition what credentials the runtime holds. The test that settles it: enumerate the effective
permissions of the identity the orchestrator and each specialist run under. If that identity
carries domain or tenant administration, this finding is critical rather than major.

**For the owner.** What identity does the orchestrator authenticate as, what does a specialist
receive along with a dispatched sub-problem, and where is the original request re-validated
before a specialist acts on it?

### Finding 10. The one checkpoint in the design is a convention in two examples, not a rule. [MAJOR]

**Where, in the artifact.** Line 43 places `ad-security-reviewer` between enumeration and
implementation planning; line 51 places `powershell-security-hardening` before implementation.
Example 2 (lines 47 and 48) routes architecture and script automation with no review hop at all.
The "Orchestration Behaviors" section at lines 28 to 31, which is where a rule would live, does
not require a review step; it appears only inside the illustrative examples.

**What the standard requires.** ASI08 (cascading failures: one early error propagating through
everything built on it) names "Planner-executor coupling: A hallucinating or compromised planner
emits unsafe steps that the executor automatically performs without validation"
([§L895](reference/owasp-top-10-agentic-applications-2026.md#L895 "^ASI08-COUPLING")). Its mitigations require
separating planning and execution via an external policy engine
([§L944](reference/owasp-top-10-agentic-applications-2026.md#L944 "^ASI08-POLICY-ENGINE")), "Checkpoints, governance
agents, or human review for high risk before agent outputs are propagated downstream"
([§L946](reference/owasp-top-10-agentic-applications-2026.md#L946 "^ASI08-GATES")), and "blast-radius guardrails
such as quotas, progress caps, circuit breakers between planner and executor"
([§L949](reference/owasp-top-10-agentic-applications-2026.md#L949 "^ASI08-BLAST-RADIUS")).

**The gap.** This is the one category where the artifact has something, and a governance agent in
the path is a control shape the standard names by that word at [§L946](reference/owasp-top-10-agentic-applications-2026.md#L946 "^ASI08-GATES"), which is why ASI08 is
PARTIAL rather than FAIL. What it does not survive is load. It is written into two worked examples
rather than into the behaviours section, it is absent from the third, nothing states what the
reviewer must return or what happens if it objects, and there is no quota, progress cap or circuit
breaker anywhere. Line 28's instruction to decompose ambiguous problems means an initial
misclassification, the earliest and least visible error in the chain, is the one thing no reviewer
in this design is positioned to catch: every specialist downstream works the sub-problem it was
handed rather than questioning the split.

**For the owner.** Is the security-review hop a rule or an example, and if step one routes a task
to the wrong domain expert, what in this design notices before the implementation plan is
produced?

## Judgment calls

**Whether this is an orchestrator or an advisor, and the definition does not say.** The artifact
declares delegation in its own voice: "dispatch the work to the most appropriate specialists"
(lines 9 and 10), "Assign each sub-problem to the correct agent" (line 29), "Merge responses"
(line 30). But the tool grant on line 4 contains no delegation mechanism at all. Two readings.
First: delegation happens through a host mechanism the definition does not state, in which case
ASI03, ASI07 and ASI08 are live exactly as scored. Second: nothing is ever dispatched, the routing
is advice a human enacts by hand, in which case ASI07 collapses toward a reasoned N/A and Finding
5 becomes the whole audit, because the output is then a confident recommendation to a person with
no provenance attached. Audited on the first reading, because a definition that declares behaviour
has declared it, and because the second reading does not remove `Bash`, `Write` or `Edit` from
line 4. Turns on what the runtime does when the agent names a specialist. Owner: the builder, and
it should be answered before anything else here, because it changes which findings apply.

**Whether an agent reviewer can stand where a human gate belongs.** Line 43 puts
`ad-security-reviewer` between enumerating stale AD accounts and planning their disablement. For:
the standard itself lists "governance agents" among acceptable checkpoints
([§L946](reference/owasp-top-10-agentic-applications-2026.md#L946 "^ASI08-GATES")), the volume would exhaust a
human, and an agent reviewer is available at three in the morning. Against: the same standard
requires human confirmation specifically for destructive and privilege-changing actions
([§L384](reference/owasp-top-10-agentic-applications-2026.md#L384 "^ASI02-CONFIRM"),
[§L1023](reference/owasp-top-10-agentic-applications-2026.md#L1023 "^ASI09-EXPLICIT-CONFIRM")), and nothing authenticates
the reviewer's verdict (Finding 2), so the checkpoint rests on the same trust-by-name as
everything else. Turns on volume and reversibility: for a handful of accounts a week with a
documented re-enable path, defensible; for a continuous backlog, or for changes that are not
cleanly reversible, not. Owner: the accountable IT owner, not the builder alone, because it is a
decision about who answers for a wrong disablement.

## What holds

One control is genuinely doing work: lines 43 and 51 place a dedicated security reviewer between
analysis and implementation, which is the checkpoint shape the standard names at [§L946](reference/owasp-top-10-agentic-applications-2026.md#L946 "^ASI08-GATES"), and it is
why ASI08 is the only category not scored FAIL.

Line 44 is worth preserving in whatever replaces this file: the destructive example terminates in
an "Implementation plan", not an implementation. That distinction is not made anywhere else in
the artifact and a fix should not discard it.

Nothing else earned a pass. That is a statement about what these 60 lines say, not a claim about
how the deployed system behaves; several categories above turn on facts the definition does not
record.

## Observations outside the standard

Line 37, "Highlight when tasks cross boundaries (e.g. AD + Azure + scripting)", is the only
instruction in the artifact that surfaces anything to a person. It is a real design instinct
pointed at the wrong variable: it flags complexity, where the thing worth flagging is consequence.
Not scored under ASI09, because it is not attached to a decision point and there is no decision
point for it to attach to, and scoring it would mean crediting a control that does not exist.
Noted because it is the hook a fix should hang an approval moment on.

The description on line 3 sells this as "orchestrating complex IT operations tasks ... by
intelligently routing work to specialized agents". Nothing in that sentence tells a reader that
one of the file's own worked examples disables user accounts. No provision reaches the gap between
how an agent describes itself and what it does, so this is judgment and not a finding, but the
person deciding whether to install this file will read line 3 and not line 41.
