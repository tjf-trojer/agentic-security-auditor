# Notices: third-party content and its licences

This repository redistributes material it did not write. Everything redistributed is listed here
with its source and its licence. Where a licence differs from this repository's, the file's own
licence governs that file.

## The standard

### OWASP Top 10 for Agentic Applications 2026

- **File:** `reference/owasp-top-10-agentic-applications-2026.md` and
  `reference/owasp-top-10-agentic-applications-2026.pdf`
- **Author:** OWASP GenAI Security Project, Agentic Security Initiative
- **Version:** 2026, published December 2025
- **Source:** <https://genai.owasp.org>
- **Licence:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0),
  <https://creativecommons.org/licenses/by-sa/4.0/>

The licence permits sharing and adaptation, including commercially, under three conditions,
which are met as follows.

**Attribution.** Credited above and in the header of the file itself. The project name is given
as required by OWASP's attribution guidelines.

**Indication of changes.** The PDF is redistributed unmodified. The markdown transcription
carries three layout normalisations, disclosed in the file's own header and reproducible from the
PDF with `method/normalise-source.py`: page-footer lines removed, the ten category headings
rejoined after the extraction split them across lines, and the five recurring subsection labels
marked as headings. No wording was added, removed, reordered, or reworded.

**ShareAlike.** The markdown transcription in `reference/` remains under CC BY-SA 4.0. It is
redistributed alongside this repository's own files rather than merged into them, and no file in
`identity.md`, `rules.md`, `examples.md`, `method/` or `targets/` incorporates the standard's
text beyond short quotation for the purpose of citation.

## The conditional second anchor

### Regulation (EU) 2024/1689 (EU AI Act)

- **File:** `reference/eu-ai-act-2024-1689-excerpts.md`
- **Source:** Official Journal of the European Union, L series, 12 July 2024. EUR-Lex CELEX
  32024R1689, official English version.
  <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689>
- **Licence:** Commission Decision 2011/833/EU on the reuse of Commission documents.
  <https://eur-lex.europa.eu/eli/dec/2011/833/oj>

Reuse for commercial and non-commercial purposes is permitted with acknowledgement of the source,
given above and in the file's own header. The file contains seven articles reproduced verbatim
and unabridged, not the full Regulation; the excerpt boundaries are stated in the file. For any
legal purpose, use the Official Journal text at the link above.

## Audited artifacts

### `agent-installer`

- **File:** `targets/voltagent-agent-installer.md`
- **Source:** `categories/09-meta-orchestration/agent-installer.md` from
  <https://github.com/VoltAgent/awesome-claude-code-subagents>, at commit
  `beb9a0f0d74a222f5e24aeb390e6d7c3005d9e27` (2026-09-04)
- **Licence:** MIT
- **Modifications:** none. Reproduced byte-for-byte, because Audit 1 cites it by line.

### `eu-ai-act-map` AGENTS.md

- **File:** `targets/eu-ai-act-map-agents.md`
- **Source:** `AGENTS.md` from <https://github.com/tjf-trojer/eu-ai-act-map>
- **Modifications:** none. Reproduced byte-for-byte, because Audit 2 cites it by line.

## Everything else

All other files in this repository are original work and are licensed under the MIT Licence in
`LICENSE`.

## Endorsement

Neither OWASP, the European Union, nor the authors of any audited artifact endorse this
repository or the audits in it. Citations to their work are for verification, which is the point
of the exercise.
