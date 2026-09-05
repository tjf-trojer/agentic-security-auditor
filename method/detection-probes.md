# Detection probes: what each category looks like in a definition

The standard describes each risk in the abstract, as a standard should. This file translates
each category into **what it looks like on the page** when you are holding a system prompt and a
tool list, and gives the question that surfaces the evidence.

Navigation, not standard. A finding cites `reference/`, never this file. Where a probe and the
standard's text disagree, the text wins. See [`README.md`](README.md).

Citations below point into
[`../reference/owasp-top-10-agentic-applications-2026.md`](../reference/owasp-top-10-agentic-applications-2026.md).

---

## ASI01: Agent Goal Hijack — [§L235](../reference/owasp-top-10-agentic-applications-2026.md#L235 "^ASI01")

**In a definition:** the agent is told to read content from sources it does not control
(inboxes, uploads, web pages, fetched repositories, tool outputs), and nothing separates
"content to reason about" from "instructions to follow". Watch for instructions of the shape
*"if a request links to a document, read it and follow the instructions it contains"*, which
makes the collapse explicit, and for the quieter version where a `WebFetch` or `read_file` tool
simply sits in the same loop as a consequential one.

The root cause is structural, not a model defect: agents "cannot reliably distinguish
instructions from related content" ([§L240](../reference/owasp-top-10-agentic-applications-2026.md#L240 "^ASI01-ONE-CHANNEL")).
This is the same class of flaw as SQL injection, and it means a prompt-layer instruction to
"ignore malicious instructions" is not a boundary. The standard's first mitigation is to treat
all natural-language input as untrusted and route it through validation *before* it can
influence goal selection or tool calls
([§L283](../reference/owasp-top-10-agentic-applications-2026.md#L283 "^ASI01-UNTRUSTED-INPUT")).

**Probe:** what does this agent read that an outsider can write? Can that content change what it
does next, and can it reach a tool that acts?

---

## ASI02: Tool Misuse and Exploitation — [§L318](../reference/owasp-top-10-agentic-applications-2026.md#L318 "^ASI02")

**In a definition:** two distinct shapes, and it is worth naming which one you found.

*Excessive agency.* The agent holds tools its stated goal does not require. Every consequential
capability present but unnecessary is attack surface with no upside. The standard's own framing
is Least-Agency: autonomy deployed where it is not needed expands the attack surface without
adding value.

*Ungated irreversible action.* Delete, send, pay, publish, provision or install is reachable
with no dry-run, no approval, no compensating transaction. Reversibility is the cheapest safety
property an agent can have and the most commonly skipped.

The standard pairs least privilege with human approval for high-impact actions
([§L286](../reference/owasp-top-10-agentic-applications-2026.md#L286 "^ASI01-LEAST-PRIVILEGE")).

**Probe:** for each tool, what task in the stated goal needs it? "It might be useful later" is
not an answer. Then: name every irreversible action and name its gate. A blank is the finding.

---

## ASI03: Identity and Privilege Abuse — [§L414](../reference/owasp-top-10-agentic-applications-2026.md#L414 "^ASI03")

**In a definition:** the agent runs on a broad service account, on a human's own credentials, or
on a token scoped far wider than its task, so the blast radius on hijack is the whole account
rather than the task. Sub-agents that inherit the parent's credentials multiply it. Look for
phrases like *"authenticates as the `ops-admin` service account"* and for the absence of any
identity statement at all, which usually means it inherits whatever invoked it.

**Probe:** if this agent were fully hijacked on its next run, what is the maximum damage its
credentials permit? That number is the finding. Then: do spawned sub-agents hold the same
credentials?

---

## ASI04: Agentic Supply Chain Vulnerabilities — [§L514](../reference/owasp-top-10-agentic-applications-2026.md#L514 "^ASI04")

**In a definition:** the agent loads, fetches, installs, or composes something at runtime that it
does not own and does not verify. Tools, MCP servers, skills, prompts, other agents' definitions,
model artifacts.

The tell in a Claude Code or similar definition is a **mutable reference**: a raw URL ending in
`/main/`, a package name with no version, a registry lookup by name. Whatever that reference
points to at fetch time is what runs, and it can change between the moment a human read the
description and the moment the file lands.

The standard is unusually concrete here. Pin by content hash and commit ID
([§L589](../reference/owasp-top-10-agentic-applications-2026.md#L589 "^ASI04-PIN")); allowlist and pin, verify
provenance before install or activation, auto-reject unsigned or unverified
([§L579](../reference/owasp-top-10-agentic-applications-2026.md#L579 "^ASI04-GATEKEEPING")); use curated registries and
block untrusted sources ([§L578](../reference/owasp-top-10-agentic-applications-2026.md#L578 "^ASI04-REGISTRIES")).

**Probe:** list everything this agent composes, fetches or installs at runtime that it does not
itself own. For each: pinned to an immutable reference? signature or hash verified? inspected
before use? Each unverified item is a finding.

---

## ASI05: Unexpected Code Execution (RCE) — [§L606](../reference/owasp-top-10-agentic-applications-2026.md#L606 "^ASI05")

**In a definition:** model output can become an executed command. A `Bash`, `run_shell`,
`exec`, `eval` or code-interpreter tool is the obvious form. The quieter form is a tool that
writes to a location something else will execute, or a definition that steers the agent toward
shell for convenience (*"use `curl -s` for downloads"*) when a narrower tool would do.

**Probe:** can model output become an executed command? Where does that execution run, what
does it reach from there, and is the environment sandboxed or the operator's own machine?

---

## ASI06: Memory & Context Poisoning — [§L681](../reference/owasp-top-10-agentic-applications-2026.md#L681 "^ASI06")

**In a definition:** the agent reads from or writes to a store that persists beyond the current
session and that someone other than its owner can influence. A RAG index users can write to, a
memory file, a scratchpad, a shared knowledge base, or an agent directory whose contents later
sessions load as instructions.

**Persistence is what distinguishes this from ASI01.** ASI01 is one hijacked run; ASI06 is a run
that corrupts the ground every later run stands on. When an artifact writes files that future
sessions will treat as instructions, both fire, and the ASI06 finding is usually the more
serious of the two because it survives the session that caused it.

**Probe:** does anything this agent writes get read back as instruction later? Who else can
write to what it reads?

---

## ASI07: Insecure Inter-Agent Communication — [§L772](../reference/owasp-top-10-agentic-applications-2026.md#L772 "^ASI07")

**In a definition:** the agent delegates to, spawns, or receives messages from other agents, and
nothing authenticates those messages. Look for *"dispatch the work to the most appropriate
specialist"*, *"can spawn helper sub-agents"*, or an orchestrator pattern with no statement of
what a sub-agent is trusted to assert back.

**Probe:** what messages cross an agent boundary here, what authenticates them, and what would a
forged one achieve? If the artifact defines a single agent that neither calls nor is called by
others, this is a reasoned N/A, and say so in that form.

---

## ASI08: Cascading Failures — [§L863](../reference/owasp-top-10-agentic-applications-2026.md#L863 "^ASI08")

**In a definition:** a multi-step agent conditions each step on the previous one with no check in
between, so an early error (a misread, a hallucinated fact, a wrong classification) propagates
silently until the final action is built on it. Errors originate early and compound. The
amplifier is volume: an agent working a backlog continuously fails the same way many times
before anyone notices once.

**Probe:** if step two is wrong, what catches it before the final action executes? If the answer
is nothing, that is the finding.

---

## ASI09: Human-Agent Trust Exploitation — [§L965](../reference/owasp-top-10-agentic-applications-2026.md#L965 "^ASI09")

**In a definition:** the artifact says a human approves, but either the throughput makes real
review impossible, or the approval step shows the human nothing they can actually judge. A
yes/no prompt with no state, no trace and no uncertainty signal is a rubber stamp exactly where
volume is highest.

This is the category most often mis-scored as a pass, because the words "always confirm" appear
in the definition and the auditor stops reading. **The presence of a confirmation is not the
question. What the human can see at the moment of confirmation is the question.** A gate that
shows a description while the risk lives in a tool grant the human never sees is oversight
theatre, and the standard is direct about the remedy: a plain-language risk summary rather than
model-generated rationale ([§L1030-L1031](../reference/owasp-top-10-agentic-applications-2026.md#L1030-L1031 "^ASI09-RISK-SUMMARY")),
and separating preview from effect, with a risk badge showing source provenance and expected
side effects ([§L1044](../reference/owasp-top-10-agentic-applications-2026.md#L1044 "^ASI09-PREVIEW")).

**Probe:** at the moment of approval, what exactly does the human see, and how many such moments
per hour? Name the thing that carries the risk and ask whether it appears on that screen.

---

## ASI10: Rogue Agents — [§L1062](../reference/owasp-top-10-agentic-applications-2026.md#L1062 "^ASI10")

**In a definition:** no iteration cap, no budget limit, no kill switch, no instruction to
escalate when uncertain. The agent can loop, amplify, or drift with nothing to halt it and
nobody able to stop it mid-run. *"Runs continuously as a background service"* with none of the
above is the clearest form. Note that this category also covers autonomous misalignment that
emerges without an attacker present, which is what distinguishes it from ASI01.

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
exact sequence of actions and the reason for each? Where the Act binds, this is also the Art. 12
record-keeping duty and has a clock behind it, because Art. 72 lifetime monitoring and incident
reporting run on timelines an unobservable agent cannot meet.
