# The Agentic Security Auditor

**An auditor that checks an AI agent's definition against the OWASP Top 10 for Agentic
Applications 2026, and reports where it conforms and where it does not, citing the standard by
line.**

Drop this folder into a Claude project. Paste in an agent's instructions and its tool list. You
get back a conformity ledger covering all ten categories, then numbered findings, each one
quoting the line of your agent that creates the exposure and the line of the standard it fails.

The standard is in [`reference/`](reference/). Not a summary of it. The document, plus the
original PDF beside it, so you can open any finding, open the provision it cites, and check that
the two match.

---

## What problem this solves

When you write ordinary software you can run a linter before you ship. When you build an
**agent**, something that holds tools and takes actions on its own, there is no equivalent. You
write the instructions, hand it permissions, and deploy. Nothing checks whether the way you set
it up is defensible.

In December 2025 OWASP published a standard for exactly this: the Top 10 for Agentic
Applications, ASI01 to ASI10. It is good, it is free, and almost nobody checks their agents
against it, because doing so by hand means holding a 50-page document in your head while reading
a config file.

This folder does that check.

## What it is not

It is not a reviewer and it is not a critic. The difference is the whole design:

- A **critic** tells you what they dislike. Their authority is their taste.
- A **reviewer** tells you what will go wrong. Their authority is their experience.
- An **auditor** tells you where your artifact stands against a written rule that exists
  independently of them. Their authority is the rule, and anyone who can read can check it.

Which means: **the auditor's opinion carries no weight in its own output.** If a finding cannot
cite a provision, it does not appear as a finding. It goes in a section called "Observations
outside the standard", marked as judgment, or it goes nowhere.

And it reports **pass as well as fail**. Every audit opens with all ten categories and a verdict
on each, before it reaches the failures. An audit that lists only problems is a complaint.

---

## Quick start

1. Clone this repository.
2. Create a Claude project and add this folder to its knowledge, or open the folder in Claude
   Code.
3. Paste in the agent definition you want audited and say:

   > Audit this agent definition.

4. To check the auditor before you trust it, paste
   [`targets/ops-copilot-synthetic.md`](targets/ops-copilot-synthetic.md) first. It is written to
   fail all ten categories, and [`examples.md`](examples.md) records what a working audit of it
   produces.

## What to feed it

The definition of an agent: **its instructions and its tools**. That is the whole input
requirement.

- a `.claude/agents/*.md` file, an `AGENTS.md`, a Cursor rule, a system prompt plus a tool list
- an assistant config, an n8n or LangGraph node with its wiring described
- a rough paragraph describing what you told it to do and what you let it touch

Polished or rough, one paragraph or a full config. If you also have a run transcript or the
config files, the audit goes deeper; it never requires them.

**If you were handed a running assistant rather than a document**, ask whoever built it for two
things, and those two are enough:

1. **Its instructions.** The system prompt, the "you are an assistant that..." text. Copy it
   as-is.
2. **Its tools and permissions.** What it is allowed to do and touch: which systems, which
   accounts, what it can send, delete, install, or pay, and what identity it runs as.

If they cannot produce those two things, that is itself worth knowing. An agent whose
instructions and permissions nobody can state plainly is not one anybody can defend.

## What comes back

```
Audit summary          Verdict, ledger arithmetic, findings by severity
In plain terms         Three lines, no codes, for forwarding on its own
Capability profile     What it is, what it does unattended, whether the AI Act binds
Conformity ledger      All ten categories: PASS / FAIL / PARTIAL / N/A
Findings               Numbered, by severity, each citing the standard by line
Judgment calls         Decisions that must be made rather than left implicit
What holds             The passes, restated. The audit is not only a complaint
Observations           Anything real but outside the standard, marked as judgment
```

Every finding has the same four parts: **where in your artifact**, **what the standard
requires** (with the citation), **the gap**, and **the question you have to answer**. It never
hands you fixed configuration. An agent whose owner did not reason their way to why it is safe
is one the organisation cannot defend when someone asks who decided it was safe.

---

## How to check the auditor

This is the part that matters, and it is why the repository is laid out the way it is.

Open [`examples.md`](examples.md). Take any finding. It cites something like:

```
[ASI04](reference/owasp-top-10-agentic-applications-2026.md#L589)
```

Open that file at that line. It reads: *"Pinning: Pin prompts, tools, and configs by content hash
and commit ID."* Then open the artifact the finding is about, in
[`targets/`](targets/), at the line the finding quotes. Line 24 of
`voltagent-agent-installer.md` is a raw GitHub URL with `/main/` in the path.

Now you can decide for yourself whether the finding is right. That is the only test of an auditor
that means anything, and every finding in this repository is built to survive it.

If a citation ever does not say what a finding claims, that is a bug and the finding is void.
Please open an issue.

## Layout

```
identity.md      Who the auditor is and which standard it enforces
rules.md         How it audits: the sweep, the ledger, severity, output format
examples.md      Three worked audits against the artifacts in targets/
reference/       THE STANDARD. OWASP's text and the PDF. Plus the seven EU AI Act
                 articles the auditor may cite, when the scope gate says it may
method/          The working layer: scope gate, detection probes. Written by me,
                 carries no authority, and no finding may ever cite it
targets/         The artifacts audited in examples.md, so you can check the work
NOTICES.md       What is redistributed here, from where, under which licence
```

The split between `reference/` and `method/` is the load-bearing decision in this repository.
`reference/` is other people's text and it is where authority lives. `method/` is mine and it is
navigation. **A finding may cite `reference/`. A finding may never cite `method/`.** If a
detection probe and the standard disagree, the standard wins and the probe is a bug.

## Scope and honesty

**It audits a definition, not a running system.** Where a finding depends on runtime behaviour or
on the base model's own properties, the audit says "cannot verify from the definition" and names
the test that would settle it.

**The EU AI Act is a conditional second anchor, and usually it does not apply.** Most agent
definitions are internal developer tooling; for those the Act's high-risk duties do not attach,
and the audit says so plainly rather than stretching an Annex III classification to manufacture a
legal hook. Both real audits in `examples.md` reach exactly that conclusion. The Art. 50
transparency duties are checked separately, because they bind by behaviour rather than by risk
tier.

**It is not a penetration test and not legal advice.** It is a design review against a published
standard.

**OWASP's ten categories are not everything that can be wrong with an agent.** When something is
concerning and no provision reaches it, it goes in "Observations outside the standard", marked as
judgment. A strained citation is worse than an honest observation.

## Licence

This repository's own files: MIT, see [`LICENSE`](LICENSE).

The OWASP standard in `reference/` is CC BY-SA 4.0 and stays that way. The EU AI Act excerpts are
reused under Commission Decision 2011/833/EU. The audited artifact in
`targets/voltagent-agent-installer.md` is MIT, reproduced byte-for-byte and pinned to a commit.
Full detail, including the disclosure of what was changed in the OWASP transcription and why, is
in [`NOTICES.md`](NOTICES.md).

Neither OWASP nor the EU nor the authors of any audited artifact endorse this repository.
