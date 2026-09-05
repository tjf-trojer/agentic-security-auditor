# reference/ — the standard itself

Everything in this folder was written by someone else. That is the point.

An auditor that ships its own summary of a standard has shipped an opinion with a citation
format. The only way a reader can check a finding is if the provision it cites is here, in the
words its authors used, so that opening the citation settles the question.

| File | What it is |
|---|---|
| [`owasp-top-10-agentic-applications-2026.md`](owasp-top-10-agentic-applications-2026.md) | **The standard.** OWASP Top 10 for Agentic Applications, Version 2026. Full text, cited by line throughout this repository |
| [`owasp-top-10-agentic-applications-2026.pdf`](owasp-top-10-agentic-applications-2026.pdf) | The official PDF the markdown was transcribed from, so the transcription itself can be checked |
| [`eu-ai-act-2024-1689-excerpts.md`](eu-ai-act-2024-1689-excerpts.md) | The seven articles of Regulation (EU) 2024/1689 the auditor is permitted to cite, verbatim and unabridged. Conditional: used only when the scope gate finds the Act binds |

## The one thing that was changed, and why

The OWASP markdown is a text extraction of the PDF. Three layout normalisations were applied so
that findings can cite it by line:

1. PDF page-footer lines (`genai.owasp.org  Page N`) removed.
2. The ten category headings, split across two or three lines by the extraction, rejoined and
   marked as headings.
3. The five recurring subsection labels marked as headings.

No wording was added, removed, reordered, or reworded. The script that performed exactly these
three changes is [`../method/normalise-source.py`](../method/normalise-source.py), so you can run
it against the PDF text yourself and get this file back. The disclosure required by CC BY-SA 4.0
is in the file's own header and in [`../NOTICES.md`](../NOTICES.md).

Multi-column material (the front-matter diagram, the appendix mapping tables) does not survive
linear extraction and is left exactly as extracted rather than reconstructed, because
reconstructing it would mean altering the standard. Read those in the PDF. The ten category
sections, which are what this auditor cites, are continuous prose and came through cleanly.

## Where the citable provisions live

Not here. [`../provisions.md`](../provisions.md) is the register: every provision this auditor may
cite, with a stable id, its current line, and its opening words verbatim. It is generated from
this folder by `scripts/build_register.py` and checked by `scripts/verify.py`.

A second copy of that index used to sit in this file and in `rules.md`. Both were removed: a
duplicated index drifts, and a drifted index inside the folder whose whole purpose is verifiable
citation is the worst possible place for one.

```bash
bash ../scripts/cite.sh --list          # every id
bash ../scripts/cite.sh ASI04-PIN       # read one provision
```
