# Evidence: what makes a finding a finding

_Last updated: 2026-09-18_

Rule 1. The three parts of a finding, and how a citation is written so that a stranger can
open it.

---

## Rule 1: Every finding cites the standard by line

A finding has three parts and does not exist without all three:

1. **Where, in the artifact.** The quoted instruction, named tool, or specific permission. Not
   "poor input handling" but the line that creates the exposure. Where the finding is an absence,
   say what is missing and quote the line nearest to where it would have to be: the tool grant, the
   step that acts, the message that reports success.
2. **Where, in the standard.** A citation whose text is OWASP's address for the provision, whose
   title is its id, and whose target is its current line:

   ```
   [ASI04 Mitigation 7](../reference/owasp-top-10-agentic-applications-2026.txt#L589 "^ASI04-PIN")
   ```

   The **address is where a reader finds the provision in the PDF**: the category, then
   `Description`, `Common Example n`, `Attack Scenario n`, `Mitigation n` or `Reference n` for the
   numbered item in that subsection. `ASI04` alone is the category heading, `ASI04 Mitigations` the
   section heading, `Letter from the Leaders` the front matter. The **id is the identity**, in the
   link title. The **line is derived**, in the link target. Ids and addresses are in
   [`provisions.md`](../provisions.md). `bash scripts/cite.sh ASI04-PIN` prints the provision;
   `python3 scripts/verify.py` fails if a line has drifted or a citation's text is not its address.

   **Never cite from the register alone.** Each row holds one line and most provisions run across
   two or three. Open the category in `reference/` and read it, or run `cite.sh`, which prints the
   whole provision.
3. **The gap.** One sentence: what the standard requires, what the artifact does instead.

**Before you write a line number, read that line.** Never cite from memory of what a category is
called.

**Cite the narrowest thing that carries the claim**, registered or not: the specific mitigation,
not the section heading. Never invent an id.

**A provision with no id is still citable.** Cite the line with its address and no title, which is
all that marks it as unregistered:
`[ASI01 Mitigation 5](../reference/owasp-top-10-agentic-applications-2026.txt#L295)`. `cite.sh` takes
a bare line number as well as an id, and prints the address either way:

```bash
bash scripts/cite.sh 295            # a line in the standard
bash scripts/cite.sh ASI01-MIT      # or by register id
```

Never stretch to a registered provision that nearly fits.

**A citation means "beginning at this line".** The reference preserves the source PDF's hard
wraps, so most provisions span two or three lines. Quote across the wrap. For a passage rather
than a sentence, cite a range (`#L1030-L1031`). Never cite a line that begins a *different*
provision from the one you rely on.

**Quote the standard in two places only**: a finding's Standard line (in the long form, "What the
standard requires") and "What holds". Every quoted passage there must appear verbatim in
`reference/`. Quotes anywhere else are read as quotes of the artifact.

**In a ledger Basis cell, never quote the standard.** Quote the artifact if you need to, and carry
a citation link to the provision. If a pass needs the standard's own words, put them in "What
holds".

**Line numbers in the artifact count from line 1 including frontmatter**, so in a
`.claude/agents/*.md` file `tools:` is usually line 4. If the artifact was pasted rather than
supplied as a file, say so and quote verbatim instead of numbering.

**The generic test.** Could you paste this finding, unchanged, into an audit of a different
agent? Then it is slop. Rewrite it until it quotes *this* artifact, or delete it.
