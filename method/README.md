# method/ — the working layer. This is not the standard.

_Last updated: 2026-09-05_

Read this boundary before you read anything else in this folder.

**`reference/` holds the standard.** It is OWASP's document and the EU's Regulation, reproduced
so that any finding can be checked against the provision it cites. Nothing in `reference/` is
written by this repository's author.

**`method/` holds the working layer.** Everything here is written by this repository's author.
It is procedure: how to navigate the standard, where to look in an artifact, what question
surfaces the evidence. It carries no authority of its own.

The distinction is operational, not decorative:

- A finding may cite `reference/`. **A finding may never cite `method/`.**
- If a probe in this folder and the text in `reference/` disagree, the text wins, and the probe
  is wrong and should be fixed.
- If you find yourself citing a detection probe as though it were a requirement, you have
  produced an opinion wearing a standard's clothes. That is the specific failure this folder is
  arranged to prevent.

A working layer is worth having anyway. The standard tells you that unverified runtime
composition is a risk; it does not tell you that the giveaway in a Claude Code agent definition
is a raw GitHub URL ending in `/main/`. That kind of knowledge is real and useful, and it
belongs here, clearly labelled as navigation rather than as rule.

## Contents

| File | What it is |
|---|---|
| [`scope-gate.md`](scope-gate.md) | The opening move: is this an agent, what can it do unattended, does the AI Act bind |
| [`detection-probes.md`](detection-probes.md) | Per-category detection guidance: what the failure looks like in a definition, and the question that surfaces it |
| [`normalise-source.py`](normalise-source.py) | The script that produced the markdown in `reference/` from the official PDF, so the transformation is reproducible and auditable |

The scripts that check this repository's claims live one level up in
[`../scripts/`](../scripts/), not here, because they verify `reference/` rather than navigate it.
`make verify` runs them.
