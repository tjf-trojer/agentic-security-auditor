# The scope gate

_Last updated: 2026-09-10_

The opening move of every audit (rules.md, Rule 3, Move 1). It answers three questions and
produces a **capability profile** that the rest of the audit refers back to. Run it before
looking for findings: the profile determines which categories can even fire.

Navigation, not standard. See [`README.md`](README.md).

---

## Question 1: Is this an agent, and at what autonomy level?

A model that only produces text in response to a prompt is **not in scope**. This auditor is for
systems that *act*: they hold tools or permissions and take steps toward a goal. If the
definition has no tools and cannot trigger actions, say so in one line and stop.

Place the artifact on the autonomy scale. The scale is about **what happens without a human**,
not about how capable the model is:

| Level | Definition | What the audit weights |
|---|---|---|
| **Supervised** | A human confirms every consequential action before it happens | What the human sees at the moment of approval, and whether their job is actually possible (ASI09) |
| **Semi-autonomous** | Acts within defined limits, escalates when it hits them or is uncertain | Where the limits are, whether anything enforces them, what triggers escalation (ASI10) |
| **Fully autonomous** | Takes consequential actions with no human in the path | Blast radius, reversibility, stop conditions, observability (ASI02, ASI03, ASI10) |

Note the **composition pattern** too, because it sets the trust boundaries: single agent plus
tools; multi-agent (one agent delegating to others); agent-spawning (agents that create agents,
where credentials and trust inherit down a mesh). Spawning and multi-agent designs pull ASI03,
ASI04 and ASI07 forward, and make ASI08 live rather than theoretical.

### When the declared behaviour and the tool grant disagree

Resolve it here, before the sweep. A definition
often *declares* delegation in prose ("dispatch the work to the specialist", "spawn a helper")
while its `tools:` line contains no delegation mechanism at all. Or the reverse: a narrow stated
purpose sitting on top of a broad grant.

**Audit what the artifact declares, and record the conflict as a judgment call.** Name the
conflict in the capability profile. Put it first in the judgment calls, with both readings and
what changes under each; only the owner can say what their runtime does when the agent names a
specialist. A narrow stated purpose does not remove a broad grant: audit the grant.

---

## Question 2: What can it do without a human confirming the action?

The governing question of the audit. Produce two lists from the tool set and the instructions:

- **Consequential actions reachable autonomously.** Anything that changes the world outside the
  agent: send, post, pay, provision, install, write to a shared or persistent store, call an
  external API that acts.
- **Irreversible actions reachable autonomously.** The subset that cannot be cleanly undone:
  delete, transfer funds, publish externally, send to a third party, overwrite a file that
  later sessions will load.

A populated second list with no gates is the audit's main event.

Be concrete about what counts as "no human confirming". A definition that says *"always confirm
before installing"* has a gate. Whether that gate is worth anything is an ASI09 question, not a
capability-profile question. Record the gate here; judge it in the sweep.

### The lethal trifecta

A fast pre-check before the full ASI01 trace. An agent is exposed to data theft the moment a
single session combines all three of:

1. **access to private data** (a tool or context that reads something an attacker wants),
2. **exposure to untrusted content** (web pages, email bodies, uploaded files, fetched
   repositories, tool output the agent does not control), and
3. **the ability to communicate externally** (send, post, an outbound API call, a write to a
   shared store, or even a plain URL fetch, which carries data out in the request).

Hold all three and an injected instruction in the untrusted content can read the private data
and route it out. **Remove any one leg and this specific exfiltration path closes.** If the profile has all three, name the three legs in the capability
profile and carry them into the ASI01 and ASI02 findings as the exact config elements to quote.

This is the structural form of what the standard describes as the root cause under
[ASI01 Description](../reference/owasp-top-10-agentic-applications-2026.txt#L240 "^ASI01-ONE-CHANNEL"): agents "cannot reliably
distinguish instructions from related content".

---

## Question 3: Who does this agent decide about?

Questions 1 and 2 ask what the agent can do *to systems*; this one asks what it can do *to
people*. An agent with no shell, no credential and no irreversible tool can still rank a person,
score them, flag them, filter them out, or write something into their record.

Three sub-questions. Answer them in one line each, or say "nobody" and move on.

1. **Whose case does it decide or shape?** Job applicants, customers, claimants, patients,
   employees, students, tenants, beneficiaries. Name the population, not the data.
2. **What follows from its output for that person?** A rejection, a price, a queue position, a
   score in a file somebody later reads, a flag that changes how they are treated. Say whether it
   is reversible *for them*, which is not the same as reversible for the operator: a rejection
   email that can be followed by an apology has still been received.
3. **Is there a route back to a human?** Can the person reach someone who can change the outcome,
   and are they given anything they could argue with. Whether they are *told* an AI was involved
   at all belongs here too: no ASI provision reaches non-disclosure, so it is never a finding. It
   goes in the profile and in Scope and limits.

**What changes when the answer is not "nobody".**

- **ASI09 changes shape.** It stops being only about whether an operator's approval screen shows
  enough, and becomes about whether anyone at all sees the decision before the person does. A
  review that runs after the affected party has been told is not a gate, whatever it is called.
- **Fairness exposure gets named in the capability profile**, not left for Observations. If the
  agent scores people on proxies (tenure, gaps, similarity to an existing population, postcode,
  institution), say so in the profile, citable or not.
- **A data-protection pointer becomes mandatory**, in one line, marked as outside this audit's
  scope. Do not assess it.

**Severity, when the subject is a person.** Rule 4's assurance test is for an artifact whose
*output is an assurance nothing requires to be true*, not for deciding about someone. An agent that
rejects people on an honestly derived score trips this question and not that test. Grade it on
reachability: an irreversible outcome delivered to someone with no route back to a human is an
unmitigated path from an ordinary mistake to serious harm, and that is CRITICAL.

## Output of the gate

Three to five lines. Two worked shapes:

> **Capability profile.** Semi-autonomous email-triage agent, single agent plus tools. Reads
> untrusted inbound mail; can `send_email`, `create_ticket` and `update_crm` without
> confirmation; `refund_customer` is gated behind human approval. Irreversible autonomous
> actions: outbound mail to third parties. Lethal trifecta present (CRM data, inbound mail,
> `send_email`). Decides about: customers whose tickets it triages and refunds, reversibly. They
> are never told a machine handled them, which no ASI provision reaches and is named here rather
> than as a finding.

> **Capability profile.** Supervised developer utility, single agent plus tools, invoked
> interactively. Fetches files from a third-party GitHub repository and writes them into the
> operator's own agent directory after a stated confirmation. Consequential autonomous actions:
> file writes into a location later sessions load; shell execution via `Bash`. Irreversible:
> uninstall (delete). Lethal trifecta present (local filesystem read, fetched third-party
> content, outbound fetch and shell). Decides about: nobody; the only person it interacts with
> is the developer who invoked it.

Then sweep the ten categories against that profile.
