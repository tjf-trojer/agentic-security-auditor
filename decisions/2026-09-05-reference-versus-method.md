# Decision: quarantine the author's analysis from the standard

**Date:** 2026-09-05
**Status:** decided, implemented

## Context

Building this auditor produced two kinds of writing. One is OWASP's text. The
other is knowledge about how those categories show up in a real definition: that
the tell for an unpinned supply chain in a Claude Code agent is a raw GitHub URL
ending in `/main/`, that "always confirm" is the phrase most often mistaken for a
control, that a shared cross-agent context is ASI06 rather than ASI01 because it
persists.

The second kind is genuinely useful and it is not the standard. Mixed together,
it reads as though OWASP said it.

## Decision

Two folders with different authority.

- `reference/` holds text written by other people, redistributed unaltered.
- `method/` holds text written by this repository's author.

**A finding may cite `reference/`. A finding may never cite `method/`.** Where a
detection probe and the standard disagree, the standard wins and the probe is a
bug.

## Reasoning

**This is the failure the auditor exists to prevent, applied to itself.** The
whole argument against a critic is that their authority is their taste. An
auditor that quietly promoted its own heuristics into citable rules would be a
critic wearing a standard's clothes, and it would be harder to detect than an
honest opinion, because the format would look rigorous.

**Keeping the working layer is still right.** Deleting `method/` would not make
the auditor more disciplined, it would make it worse at finding evidence while
leaving the same judgments implicit in `rules.md`. Naming the layer and denying
it citation authority is stricter than hiding it.

**The split has to be enforced somewhere other than good intentions.** It is
stated in `identity.md`, in `rules.md`, in `method/README.md`, and it is visible
in the citation format: every citation resolves into `reference/`, so a probe
cannot be cited without the reader seeing the wrong path.

## Consequences

- `method/` files may be wrong without the audit being wrong, and correcting a
  probe is a routine edit, not a correction to the standard.
- New knowledge from running the auditor lands in `method/`, never in
  `reference/`. If it feels like it belongs in `reference/`, that is a sign it is
  an opinion that wants authority it has not earned.
- A reader who trusts nothing in this repository can delete `method/` entirely
  and still check every finding, because nothing a finding rests on lives there.
