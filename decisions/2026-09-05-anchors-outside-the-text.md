# Decision: the citation anchor lives outside the standard's text

**Date:** 2026-09-05
**Status:** decided, implemented

## Context

Citing by line number alone is fragile in two ways that both showed up in
testing. Line numbers move whenever the reference file changes, and a moved
citation is worse than a missing one because it still looks authoritative. And a
`#L589` link does not jump anywhere on github.com, which renders markdown without
line numbers, so a reader checking the work in a browser lands at the top of a
1,695-line file.

The convention that solves this comes from the author's own governance
workspace: the anchor is the stable identity, the line number is its derived,
clickable form, and a script restores the line from the anchor after any change.

## Decision

Adopt that convention, with one change. In the workspace, anchors are markers
appended to the corpus text itself (`^art22-abs1` at the end of a paragraph).
Here they are **not written into the reference at all**. Each id is bound to the
provision's own opening words, recorded in `provisions.md`, and the line is found
by matching them.

## Reasoning

**The corpus is not ours to mark.** The reference is OWASP's document,
redistributed under CC BY-SA 4.0 with a disclosure that no word was added,
removed, reordered or reworded. Inserting anchor markers would make that
disclosure false, and would put the author's text inside the one folder whose
entire value is that it contains nobody's text but the source's.

**Keying on the words turns out to be stronger than keying on a marker.** A
marker survives an edit to the text it marks: if a provision were reworded, the
marker would follow the change and a stale citation would keep looking correct. A
text key cannot do that. When OWASP publishes a new edition, the match fails,
`scripts/verify.py` names the id that moved, and a human decides what changed.
The fragility is the feature: this is the one moment where silence would be
dangerous.

**A citation that cannot be redeemed is only a promise.** So the register is
paired with `scripts/cite.sh`, which prints a provision from its id, from a bare
line number, or for every citation in a document, and prints across the source's
hard line wraps to the end of the provision. That removes the browser problem
entirely: a reader checking the work does not need github.com, an editor, or the
`?plain=1` trick.

## Consequences

- `provisions.md` is generated, never hand-edited. Editing it by hand would
  reintroduce exactly the drift it exists to detect.
- Citing a provision that has no id is allowed, but the auditor must say so
  rather than invent an id. `verify.py` rejects an id that is not in the register.
- A new OWASP edition is a deliberate migration: re-run `build_register.py`, read
  the diff, and update the audits whose citations moved. It is not a silent
  refresh, and it should not be.
