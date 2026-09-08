# reference/ is the standard itself

_Last updated: 2026-09-08_

Everything in this folder was written by someone else. A finding can only be checked if the
provision it cites is here, in the words its authors used.

| File | What it is |
|---|---|
| [`owasp-top-10-agentic-applications-2026.md`](owasp-top-10-agentic-applications-2026.md) | **The standard.** OWASP Top 10 for Agentic Applications, Version 2026. Full text, cited by line throughout this repository |
| [`owasp-top-10-agentic-applications-2026.pdf`](owasp-top-10-agentic-applications-2026.pdf) | The official PDF the markdown was transcribed from, so the transcription can be checked |

## What was changed

The markdown is a text extraction of the PDF. Three layout normalisations were applied so that
findings can cite it by line:

1. PDF page-footer lines (`genai.owasp.org  Page N`) removed.
2. The ten category headings, split across lines by the extraction, rejoined and marked as headings.
3. The five recurring subsection labels marked as headings.

No wording was added, removed, reordered, or reworded.
[`../method/normalise-source.py`](../method/normalise-source.py) performs exactly these three
changes, so you can run it against the PDF text and get this file back. The CC BY-SA 4.0
disclosure is in the file's own header and in [`../NOTICES.md`](../NOTICES.md).

Multi-column material (the front-matter diagram, the appendix mapping tables) does not survive
linear extraction and is left exactly as extracted. Read those in the PDF. The ten category
sections, which are what this auditor cites, came through cleanly.

## The citable provisions

[`../provisions.md`](../provisions.md) is the register: every provision this auditor may cite,
with a stable id, its current line, and its opening words verbatim. It is generated from this
folder by `scripts/build_register.py` and checked by `scripts/verify.py`.

```bash
bash ../scripts/cite.sh --list          # every id
bash ../scripts/cite.sh ASI04-PIN       # read one provision
```
