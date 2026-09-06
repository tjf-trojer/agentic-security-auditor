# The scope gate

_Last updated: 2026-09-05_

The opening move of every audit (rules.md, Rule 3, Move 1). It answers four questions and
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

### When the declared behaviour and the tool grant disagree

Common, and it changes several verdicts, so resolve it here rather than mid-sweep. A definition
often *declares* delegation in prose ("dispatch the work to the specialist", "spawn a helper")
while its `tools:` line contains no delegation mechanism at all. Or the reverse: a narrow stated
purpose sitting on top of a broad grant.

**Audit what the artifact declares, and record the conflict as a judgment call.** A definition
that describes delegation across twenty lines has declared delegation, and a reader adopting the
file will get whatever the surrounding harness provides. Auditing only the tool line would let an
artifact escape the categories it spends most of its text describing.

Two things follow. Name the conflict explicitly in the capability profile, because it bounds
everything after it. And put it first in the judgment calls, with both readings and what changes
under each, because the owner is the only one who can say what their runtime actually does when
the agent names a specialist. Note that the reverse case rarely rescues an artifact: a narrow
purpose does not remove a broad grant, and the grant is what an attacker gets.

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
[ASI01](../reference/owasp-top-10-agentic-applications-2026.md#L240 "^ASI01-ONE-CHANNEL"): agents "cannot reliably
distinguish instructions from related content".

---

## Question 3: Who does this agent decide about?

Questions 1 and 2 ask what the agent can do *to systems*. This one asks what it can do *to
people*, and it is a different question with a different answer. An agent with no shell, no
credential and no irreversible tool can still rank a person, score them, flag them, filter them
out, or write something into their record. The lethal trifecta does not see that, and neither
does an action-shaped severity test.

Three sub-questions. Answer them in one line each, or say "nobody" and move on.

1. **Whose case does it decide or shape?** Job applicants, customers, claimants, patients,
   employees, students, tenants, beneficiaries. Name the population, not the data.
2. **What follows from its output for that person?** A rejection, a price, a queue position, a
   score in a file somebody later reads, a flag that changes how they are treated. Say whether it
   is reversible *for them*, which is not the same as reversible for the operator: a rejection
   email that can be followed by an apology has still been received.
3. **Is there a route back to a human?** Can the person reach someone who can change the outcome,
   and are they given anything they could argue with. (Whether they are *told* an AI was involved
   is Question 4's Art. 50 check; do not answer it twice.)

**What changes when the answer is not "nobody".**

- **ASI09 changes shape.** It stops being only about whether an operator's approval screen shows
  enough, and becomes about whether anyone at all sees the decision before the person does. A
  review that runs after the affected party has been told is not a gate, whatever it is called.
- **The Annex III check in Question 4 has something to bite on.** Most of Annex III is defined by
  who is affected rather than by what the system touches, so an artifact that decides about people
  is where the Act is most likely to bind.
- **Fairness exposure gets named in the capability profile**, not left for Observations. If the
  agent scores people on proxies (tenure, gaps, similarity to an existing population, postcode,
  institution), say so in the profile. It is usually not citable against this standard, and it is
  usually the most consequential thing in the artifact, so it belongs where a reader will see it
  rather than at the end.
- **A data-protection pointer becomes mandatory**, in one line, marked as outside this audit's
  scope. Do not assess it.

**Severity, when the subject is a person.** Do not reach for Rule 4's fourth CRITICAL test unless
it actually fits: that one is about an artifact whose *output is an assurance nothing requires to
be true*, which is a different failure from deciding about someone. An agent that rejects people on
an honestly derived score, with no fabricated rationale, trips this question and not that test.
Grade it on reachability like anything else, and let the consequence for the person carry the
weight: an irreversible outcome delivered to someone with no route back to a human is a short path
from an ordinary mistake to serious harm, which is CRITICAL on the first test, not the fourth.

The trap this question exists to catch: an agent whose tool grant is narrow and whose subject is a
person can look clean on every action-shaped check while being the most consequential artifact you
audit.

---

## Question 4: Does the EU AI Act bind, and how?

You are not classifying the system. You are locating it against the obligations that most often
bite, so that findings can anchor when the Act applies and drop the anchor when it does not.

**Run the four checks and report what they find.** Do not carry a prior in either direction.
Many agent definitions are internal developer tooling, and for those the Act's high-risk duties
will not attach; writing that plainly is a correct result and not a gap in the audit. But that is
a conclusion the checks produce, not an assumption you start from, and an auditor that decides
before it looks is doing the thing this folder exists to catch in others.

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

2. **Is the underlying use high-risk?** If the agent operates in an Annex III domain, deployer
   obligations attach and Art. 14 human oversight is mandatory rather than optional. Annex III
   ships in full at [`AIA-ANNEX-III`](../reference/eu-ai-act-2024-1689-excerpts.md#L871 "^AIA-ANNEX-III"),
   with each of its eight points separately citable (`AIA-III-1` to `AIA-III-8`), so **name the
   point and cite it** rather than asserting one from memory. Read the point before naming it:
   several are narrower than their headings suggest. **Art. 6(3), the derogation that decides
   whether an Annex III system is actually high-risk, is not shipped in `reference/`**, so say it
   was not checked rather than implying the classification is settled. Do not assert the final
   classification,
   which is a lawyer's call. **Never stretch Annex III to manufacture a legal hook**; an audit
   that invents jurisdiction is worse than one that reports none.

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
> agent, and nothing in the definition discloses it. Decides about: customers whose tickets it
> triages and refunds, reversibly; they are not told a machine handled them.

> **Capability profile.** Supervised developer utility, single agent plus tools, invoked
> interactively. Fetches files from a third-party GitHub repository and writes them into the
> operator's own agent directory after a stated confirmation. Consequential autonomous actions:
> file writes into a location later sessions load; shell execution via `Bash`. Irreversible:
> uninstall (delete). Lethal trifecta present (local filesystem read, fetched third-party
> content, outbound fetch and shell). The EU AI Act does not bind: this is internal developer
> tooling, not an Annex III use, and the only natural person it interacts with is the developer
> who invoked it, for whom the AI nature of the interaction is obvious within the Art. 50(1)
> exception. Decides about: nobody. The OWASP findings below stand on their own.

Then sweep the ten categories against that profile.
