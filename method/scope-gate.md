# The scope gate

The opening move of every audit (rules.md, Rule 3, Move 1). It answers three questions and
produces a **capability profile** that the rest of the audit refers back to. Run it before
looking for findings: the profile determines which categories can even fire.

Navigation, not standard. See [`README.md`](README.md).

---

## Question 1: Is this an agent, and at what autonomy level?

A model that only produces text in response to a prompt is **not in scope**. This auditor is for
systems that *act*: they hold tools or permissions and take steps toward a goal. If the
definition has no tools and cannot trigger actions, say so in one line and stop. Do not audit a
chatbot against a standard written for agents; that is how an auditor manufactures findings.

One note on vocabulary, because the market blurs it. An **AI agent** is the deployed system in
front of you: instructions plus tools, acting toward a goal. **Agentic AI** names the capability
class it belongs to, up to architectures where several agents compose. You audit definitions of
the former wherever the latter is in play, and no finding changes with the label.

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

---

## Question 2: What can it do without a human confirming the action?

The single governing question of the audit. Frameworks argue about agent *types*; the risk lives
in *reachable autonomous action*. Produce two lists from the tool set and the instructions:

- **Consequential actions reachable autonomously.** Anything that changes the world outside the
  agent: send, post, pay, provision, install, write to a shared or persistent store, call an
  external API that acts.
- **Irreversible actions reachable autonomously.** The subset that cannot be cleanly undone:
  delete, transfer funds, publish externally, send to a third party, overwrite a file that
  later sessions will load.

An empty second list is a good sign. A populated second list with no gates is the audit's main
event.

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
and route it out, with no bug in the model: the model did exactly what the text told it. The
check earns its place because the remedy is decisive. **Remove any one leg and this specific
exfiltration path closes.** If the profile has all three, name the three legs in the capability
profile and carry them into the ASI01 and ASI02 findings as the exact config elements to quote.

This is the structural form of what the standard describes as the root cause under
[ASI01](../reference/owasp-top-10-agentic-applications-2026.md#L240): agents "cannot reliably
distinguish instructions from related content".

---

## Question 3: Does the EU AI Act bind, and how?

You are not classifying the system. You are locating it against the obligations that most often
bite, so that findings can anchor when the Act applies and drop the anchor when it does not.

**Expect the answer to be no.** Most agent definitions are internal developer tooling: a coding
subagent, a build helper, a research assistant. For those the Act's high-risk duties do not
attach, and writing that plainly is the correct result, not a gap in the audit.

Four checks, in this order:

1. **Does the agent reach natural persons? Art. 50 binds without any high-risk finding.**
   Transparency duties attach by behaviour, not by risk tier. An agent that interacts directly
   with people (mail, chat, voice, negotiating or purchasing on someone's behalf, including as
   the human-facing member of a multi-agent chain) must disclose its artificial nature and the
   person on whose behalf it acts (Art. 50(1)). Perceptible synthetic content it produces must
   be machine-readable-marked and detectable (Art. 50(2)). The one escape from 50(1) is
   interaction that is obvious to a reasonably well-informed member of the *actual* audience,
   read narrowly: a developer who invoked the agent themselves qualifies; a customer or member
   of the public almost never does.

2. **Is the underlying use high-risk?** If the agent operates in an Annex III domain (employment
   and worker management, essential public and private services, credit, law enforcement,
   migration, education, critical infrastructure), deployer obligations attach and Art. 14 human
   oversight is mandatory rather than optional. Name which Annex III point plausibly applies. Do
   not assert the final classification. **Never stretch Annex III to manufacture a legal hook**;
   an audit that invents jurisdiction is worse than one that reports none.

3. **Is the reader a bound deployer?** Public bodies, private providers of public services, and
   Annex III deployers carry the heaviest duties.

4. **Could runtime behaviour exceed what was assessed?** An agent that composes new workflows at
   runtime can drift past whatever any assessment described. Under Art. 3(23) a substantial
   modification re-triggers obligations, and under Art. 25 a deployer that changes purpose or
   behaviour can become a provider. Flag this as a judgment call to be named, not a settled
   finding.

Behind all four sits one question that survives even when the Act does not bind: **when this
agent acts and something goes wrong, who is on the record as answerable, and can anyone
actually reach them?** An agent assembled from unpinned third-party components with no
identifiable owner is a governance failure in any jurisdiction.

---

## Output of the gate

Three to five lines. Two worked shapes:

> **Capability profile.** Semi-autonomous email-triage agent, single agent plus tools. Reads
> untrusted inbound mail; can `send_email`, `create_ticket` and `update_crm` without
> confirmation; `refund_customer` is gated behind human approval. Irreversible autonomous
> actions: outbound mail to third parties. Lethal trifecta present (CRM data, inbound mail,
> `send_email`). The Act's high-risk duties do not clearly attach, as this is not an Annex III
> use, but Art. 50(1) binds on its own because the agent mails people who cannot tell it is an
> agent, and nothing in the definition discloses it.

> **Capability profile.** Supervised developer utility, single agent plus tools, invoked
> interactively. Fetches files from a third-party GitHub repository and writes them into the
> operator's own agent directory after a stated confirmation. Consequential autonomous actions:
> file writes into a location later sessions load; shell execution via `Bash`. Irreversible:
> uninstall (delete). Lethal trifecta present (local filesystem read, fetched third-party
> content, outbound fetch and shell). The EU AI Act does not bind: this is internal developer
> tooling, not an Annex III use, and the only natural person it interacts with is the developer
> who invoked it, for whom the AI nature of the interaction is obvious within the Art. 50(1)
> exception. The OWASP findings below stand on their own.

Then sweep the ten categories against that profile.
