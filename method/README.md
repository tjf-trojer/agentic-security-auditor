# method/ is the working layer. It carries no authority.

_Last updated: 2026-09-10_

Written by this repository's author: how to navigate the standard, where to look in an artifact,
and what question surfaces the evidence.

- A finding may cite `reference/`. **A finding may never cite `method/`.**
- Where a probe here and the text in `reference/` disagree, the text wins.

| File | What it is |
|---|---|
| [`scope-gate.md`](scope-gate.md) | The opening move: is this an agent, what can it do unattended, and who does it decide about |
| [`detection-probes.md`](detection-probes.md) | What each category's failure looks like in a definition, and the question that surfaces it |
| [`normalise-source.py`](normalise-source.py) | Produces the markdown in `reference/` from a text extraction of the official PDF |
