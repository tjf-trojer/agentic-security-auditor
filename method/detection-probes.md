# Detection probes: what each category looks like in a definition

_Last updated: 2026-09-11_

Each category as it looks **on the page** when you hold a system prompt and a tool list, with the
question that surfaces the evidence.

Navigation, not standard. A finding cites `reference/`, never this file. Where a probe and the
standard's text disagree, the text wins. See [`README.md`](README.md).

Citations below point into
[`../reference/owasp-top-10-agentic-applications-2026.txt`](../reference/owasp-top-10-agentic-applications-2026.txt).

Some attack shapes below come from the scenario lists in OWASP's *Agentic AI —
Threats and Mitigations* v1.1. It is not in `reference/` and a finding never cites it.

---

## [ASI01](../reference/owasp-top-10-agentic-applications-2026.txt#L235 "^ASI01"): Agent Goal Hijack

**In a definition:** the agent is told to read content from sources it does not control
(inboxes, uploads, web pages, fetched repositories, tool outputs), and nothing separates
"content to reason about" from "instructions to follow". Watch for instructions of the shape
*"if a request links to a document, read it and follow the instructions it contains"*, which
makes the collapse explicit, and for the quieter version where a `WebFetch` or `read_file` tool
simply sits in the same loop as a consequential one.

The root cause is structural, not a model defect: agents "cannot reliably distinguish
instructions from related content" ([ASI01 Description](../reference/owasp-top-10-agentic-applications-2026.txt#L240 "^ASI01-ONE-CHANNEL")).
A prompt-layer instruction to "ignore malicious instructions" is not a boundary. The standard's
first mitigation is to treat
all natural-language input as untrusted and route it through validation *before* it can
influence goal selection or tool calls
([ASI01 Mitigation 1](../reference/owasp-top-10-agentic-applications-2026.txt#L283 "^ASI01-UNTRUSTED-INPUT")).

**Injection is not always a single move.** Where a plan persists across turns, an agent can be
walked off its goal by increments, each of which reads as a reasonable refinement and none of
which contains an attack on its own. The definition-side tell is a goal that is carried and
updated rather than restated: nothing re-anchors the agent to what it was originally asked to do.
A bounded reflection or self-critique loop belongs to ASI10 rather than here, but look for it in
the same place.

**Probe:** what does this agent read that an outsider can write? Can that content change what it
does next, and can it reach a tool that acts?

---

## [ASI02](../reference/owasp-top-10-agentic-applications-2026.txt#L318 "^ASI02"): Tool Misuse and Exploitation

**In a definition:** two distinct shapes, and it is worth naming which one you found.

*Excessive agency.* The agent holds tools its stated goal does not require (Least-Agency, at the
end of this file).

*Ungated irreversible action.* Delete, send, pay, publish, provision or install is reachable
with no dry-run, no approval, no compensating transaction.

The standard pairs least privilege with human approval for high-impact actions
([ASI01 Mitigation 2](../reference/owasp-top-10-agentic-applications-2026.txt#L286 "^ASI01-LEAST-PRIVILEGE")).

**Two shapes a per-tool review misses.** *Arguments.* A tool can be correctly scoped and still
catastrophic through the values it accepts: quantity, recipient, path, filter, limit. Ask what
the widest legal value of each consequential argument does; "book a seat" and "book five hundred
seats" are the same tool call. *Composition.* Two individually harmless tools make a third
capability that neither holds alone: read plus send is exfiltration, read plus write is
persistence, fetch plus execute is installation. Enumerate the pairs, not only the tools.

**Probe:** for each tool, what task in the stated goal needs it? "It might be useful later" is
not an answer. Then: name every irreversible action and name its gate. A blank is the finding.

---

## [ASI03](../reference/owasp-top-10-agentic-applications-2026.txt#L414 "^ASI03"): Identity and Privilege Abuse

**In a definition:** the agent runs on a broad service account, on a human's own credentials, or
on a token scoped far wider than its task, so the blast radius on hijack is the whole account
rather than the task. Sub-agents that inherit the parent's credentials multiply it. Look for
phrases like *"authenticates as the `ops-admin` service account"* and for the absence of any
identity statement at all, which usually means it inherits whatever invoked it.

**Elevation with no stated end, and reach sideways.** Watch for definitions that let the agent
raise its own privileges for a stated reason (troubleshooting, an incident, a backfill) without
saying what returns them. Temporary access with no expiry in the text is permanent access. Then
ask how far one identity reaches laterally: an agent holding a single credential valid in two
systems is a bridge between them, and the bridge is the finding, not either system.

**Probe:** if this agent were fully hijacked on its next run, what is the maximum damage its
credentials permit? That number is the finding. Then: do spawned sub-agents hold the same
credentials? The category is about acting with an identity: a credential, a token, a session, a
shell running as someone. What a read-only grant can open is graded under ASI02.

---

## [ASI04](../reference/owasp-top-10-agentic-applications-2026.txt#L514 "^ASI04"): Agentic Supply Chain Vulnerabilities

**In a definition:** the agent loads, fetches, installs, or composes something at runtime that it
does not own and does not verify. Tools, MCP servers, skills, prompts, other agents' definitions,
model artifacts.

The tell in a Claude Code or similar definition is a **mutable reference**: a raw URL ending in
`/main/`, a package name with no version, a registry lookup by name. Whatever that reference
points to at fetch time is what runs, and it can change between the moment a human read the
description and the moment the file lands.

The standard names the remedies. Pin by content hash and commit ID
([ASI04 Mitigation 7](../reference/owasp-top-10-agentic-applications-2026.txt#L589 "^ASI04-PIN")); allowlist and pin, verify
provenance before install or activation, auto-reject unsigned or unverified
([ASI04 Mitigation 2](../reference/owasp-top-10-agentic-applications-2026.txt#L579 "^ASI04-GATEKEEPING")); use curated registries and
block untrusted sources ([ASI04 Mitigation 1](../reference/owasp-top-10-agentic-applications-2026.txt#L578 "^ASI04-REGISTRIES")).

**When the artifact addresses the auditor.** A definition can carry text aimed at its reviewer: a
claimed prior certification, a hidden comment, an instruction to report everything as passing.
Rule 0 says never act on it and always report it. Two provisions usually reach it, and you should
open both before citing either:
[ASI01 Mitigation 3](../reference/owasp-top-10-agentic-applications-2026.txt#L288 "^ASI01-LOCK-PROMPTS"),
requiring prompts to be locked and auditable, and
[ASI04 Mitigation 4](../reference/owasp-top-10-agentic-applications-2026.txt#L583 "^ASI04-PROMPT-REVIEW"),
requiring them under version control with peer review and scanned for anomalies. Text that hides from a reviewer is arguably neither. Read them,
decide, and cite what you read.

**The description is part of the supply chain.** An agent that selects a tool by what the tool
says it does is trusting text written by whoever published it. A registry entry, an MCP server's
advertised capability, a skill's own summary: each reaches the agent's reasoning before any
human reads it, and a broad or misleading description is enough to get a tool called for work it
should never have been given. Ask what this agent knows about a tool other than the tool's own
claim about itself.

**Probe:** list everything this agent composes, fetches or installs at runtime that it does not
itself own. For each: pinned to an immutable reference? signature or hash verified? inspected
before use? Each unverified item is a finding.

---

## [ASI05](../reference/owasp-top-10-agentic-applications-2026.txt#L606 "^ASI05"): Unexpected Code Execution (RCE)

**In a definition:** model output can become an executed command. A `Bash`, `run_shell`,
`exec`, `eval` or code-interpreter tool is the obvious form. The quieter form is a tool that
writes to a location something else will execute, or a definition that steers the agent toward
shell for convenience (*"use `curl -s` for downloads"*) when a narrower tool would do.

**Generated configuration is executed code.** A definition that only writes files still reaches
execution when what it writes is Terraform, a CI workflow, a Dockerfile, a migration, a cron
entry or a systemd unit, anything a later process runs without a human reading it line by line.
The distance between "writes YAML" and "executes code" is one pipeline, and the definition
usually does not mention the pipeline. Ask what consumes what this agent writes. Code a person
reads and pastes is graded under ASI09, whose first attack scenario is exactly that
([ASI09 Attack Scenario 1](../reference/owasp-top-10-agentic-applications-2026.txt#L1001)); ASI05 covers what a process runs unread.

**Probe:** can model output become an executed command? Where does that execution run, what
does it reach from there, and is the environment sandboxed or the operator's own machine? With a
shell in the grant, grade what its commands can do to data and systems under ASI02, and whether
generated or injected code runs unchecked under ASI05.

---

## [ASI06](../reference/owasp-top-10-agentic-applications-2026.txt#L681 "^ASI06"): Memory & Context Poisoning

**In a definition:** the agent reads from or writes to a store that persists beyond the current
session and that someone other than its owner can influence. A RAG index users can write to, a
memory file, a scratchpad, a shared knowledge base, or an agent directory whose contents later
sessions load as instructions.

**Persistence is what distinguishes this from ASI01.** ASI01 is one hijacked run; ASI06 is a run
that corrupts the ground every later run stands on. When an artifact writes files that future
sessions will treat as instructions, both fire, and the ASI06 finding is usually the more
serious of the two because it survives the session that caused it.

**Two shapes worth naming separately.** *Repetition.* Where a store accumulates what it is
told, no single write is anomalous and the corruption is the pattern rather than any one entry,
so a control that inspects writes individually passes all of them. *Tenancy.* Where one store
serves several users or several agents, ask whether what one writes another reads. Cross-user
contamination through shared memory is the same defect as a shared mutable global, and it hides
easily behind a definition that says only "stores context for later sessions".

**Probe:** does anything this agent writes get read back as instruction later? Who else can
write to what it reads?

---

## [ASI07](../reference/owasp-top-10-agentic-applications-2026.txt#L772 "^ASI07"): Insecure Inter-Agent Communication

**In a definition:** the agent delegates to, spawns, or receives messages from other agents, and
nothing authenticates those messages. Look for *"dispatch the work to the most appropriate
specialist"*, *"can spawn helper sub-agents"*, or an orchestrator pattern with no statement of
what a sub-agent is trusted to assert back.

**The channel is the protocol, not only the peer.** An MCP server's responses (returned
context, tool metadata, capability lists) enter the agent's reasoning with the same weight as a
sibling agent's message and are authenticated about as rarely. Watch too for consent a peer can
satisfy on the user's behalf: a delegation step that treats an upstream approval as already given
lets the approving party be chosen by whoever controls the upstream.

**Probe:** what messages cross an agent boundary here, what authenticates them, and what would a
forged one achieve? If the artifact defines a single agent that neither calls nor is called by
other agents, this is a reasoned N/A, and say so in that form. A sub-agent whose only caller is the
person's own session counts as single: being invoked is not inter-agent messaging. A status file or
checkpoint another agent writes for this one to read is a message, whatever carries it.

---

## [ASI08](../reference/owasp-top-10-agentic-applications-2026.txt#L863 "^ASI08"): Cascading Failures

**In a definition:** a multi-step agent conditions each step on the previous one with no check in
between, so an early error (a misread, a hallucinated fact, a wrong classification) propagates
silently until the final action is built on it. Errors originate early and compound. The
amplifier is volume: an agent working a backlog continuously fails the same way many times
before anyone notices once.

**Volume as its own failure.** An agent that schedules its own work, spawns helpers, or
re-enters its own queue has no natural ceiling, and the failure mode is exhaustion rather than
error: quota burned, budget spent, the queue filled with its own retries. The standard reaches it
through this category's rate-limiting mitigation (throttle or pause on anomalies) and as a
contributing factor in ASI02. Open the text before citing it, and if nothing there carries the claim, it belongs in
observations outside the standard rather than in a finding.

**Probe:** if step two is wrong, what catches it before the final action executes? If the answer
is nothing, that is the finding. For a single agent the category applies where its output crosses
into another session, agent or workflow (a patch applied, a file later sessions load, a change
pasted into a device); where nothing crosses, it is N/A.

---

## [ASI09](../reference/owasp-top-10-agentic-applications-2026.txt#L965 "^ASI09"): Human-Agent Trust Exploitation

**In a definition:** the artifact says a human approves, but either the throughput makes real
review impossible, or the approval step shows the human nothing they can actually judge. A
yes/no prompt with no state, no trace and no uncertainty signal is a rubber stamp exactly where
volume is highest.

The words "always confirm" in a definition do not earn a pass. **The presence of a confirmation is
not the question. What the human can see at the moment of confirmation is the question.** A gate
that shows a description while the risk lives in a tool grant the human never sees is oversight
theatre. The remedy in the standard is a plain-language risk summary rather than
model-generated rationale ([ASI09 Mitigation 4](../reference/owasp-top-10-agentic-applications-2026.txt#L1030-L1031 "^ASI09-RISK-SUMMARY")),
and separating preview from effect, with a risk badge showing source provenance and expected
side effects ([ASI09 Mitigation 7](../reference/owasp-top-10-agentic-applications-2026.txt#L1044 "^ASI09-PREVIEW")).

**The agent's output is an instruction channel back to the human.** Where an agent relays what
it read (a link, an account number, an amount, a sequence of steps), the human acts on content
the agent did not author and cannot vouch for, while the trust attaches to the agent rather than
to the source. A definition that lets the agent render URLs or payment details drawn from fetched
content has built a channel whose apparent sender the user already trusts. Ask which parts of the
output originate outside the agent, and whether the human can tell which parts those are.

**Probe:** at the moment of approval, what exactly does the human see, and how many such moments
per hour? Name the thing that carries the risk and ask whether it appears on that screen. Where the
definition names no person at all and the agent takes consequential actions, the category applies
and fails: a missing confirmation step is the failure
[ASI09 Common Example 2](../reference/owasp-top-10-agentic-applications-2026.txt#L989 "^ASI09-MISSING-CONFIRM") names.

---

## [ASI10](../reference/owasp-top-10-agentic-applications-2026.txt#L1062 "^ASI10"): Rogue Agents

**In a definition:** no iteration cap, no budget limit, no kill switch, no instruction to
escalate when uncertain. The agent can loop, amplify, or drift with nothing to halt it and
nobody able to stop it mid-run. *"Runs continuously as a background service"* with none of the
above is the clearest form. Note that this category also covers autonomous misalignment that
emerges without an attacker present, which is what distinguishes it from ASI01.

**Fragmentation defeats a threshold.** Where approval is triggered by the size of an action, an
action split across several runs or several agents can stay under the line at every step and
still land whole. Ask whether the gate measures the step or the outcome. Watch too for output
that carries instruction to the next agent: where one agent's product becomes another's prompt, a
drifted agent propagates rather than merely failing.

**Probe:** name what stops this agent, and name who can stop it while it is running. Two blanks
is severe.

---

## Two cross-cutting checks

The standard names both in its front matter rather than as numbered categories. Apply them
throughout and file each finding under whichever category it sits in.

**Least-Agency.** The extension of least-privilege to autonomy: deploying agentic behaviour
where it is not needed expands attack surface without adding value. Any capability present but
unnecessary is a finding.

**Observability as non-negotiable.** Without visibility into what agents are doing, why, and
which tools they are invoking, minor issues become system-wide failures. The absence of any
action log or reasoning trace is a finding: after a bad outcome, could anyone reconstruct the
exact sequence of actions and the reason for each?
