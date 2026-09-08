# method/ is the working layer. This is not the standard.

_Last updated: 2026-09-08_

`reference/` holds the standard. Everything here was written by this repository's author, and it
is procedure: how to navigate the standard, where to look in an artifact, what question surfaces
the evidence.

- A finding may cite `reference/`. **A finding may never cite `method/`.**
- Where a probe here and the text in `reference/` disagree, the text wins and the probe is wrong.

| File | What it is |
|---|---|
| [`scope-gate.md`](scope-gate.md) | The opening move: is this an agent, what can it do unattended, and who does it decide about |
| [`detection-probes.md`](detection-probes.md) | Per-category detection guidance: what the failure looks like in a definition, and the question that surfaces it |
| [`normalise-source.py`](normalise-source.py) | The script that produced the markdown in `reference/` from the official PDF |

The scripts that check this repository's claims are in [`../scripts/`](../scripts/). `make verify`
runs them.
