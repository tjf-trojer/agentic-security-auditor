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

## Category anchors

| Category | Section | Prevention and Mitigation |
|---|---|---|
| ASI01 Agent Goal Hijack | [L235](owasp-top-10-agentic-applications-2026.md#L235) | [L282](owasp-top-10-agentic-applications-2026.md#L282) |
| ASI02 Tool Misuse and Exploitation | [L318](owasp-top-10-agentic-applications-2026.md#L318) | [L372](owasp-top-10-agentic-applications-2026.md#L372) |
| ASI03 Identity and Privilege Abuse | [L414](owasp-top-10-agentic-applications-2026.md#L414) | [L478](owasp-top-10-agentic-applications-2026.md#L478) |
| ASI04 Agentic Supply Chain Vulnerabilities | [L514](owasp-top-10-agentic-applications-2026.md#L514) | [L575](owasp-top-10-agentic-applications-2026.md#L575) |
| ASI05 Unexpected Code Execution (RCE) | [L606](owasp-top-10-agentic-applications-2026.md#L606) | [L658](owasp-top-10-agentic-applications-2026.md#L658) |
| ASI06 Memory & Context Poisoning | [L681](owasp-top-10-agentic-applications-2026.md#L681) | [L733](owasp-top-10-agentic-applications-2026.md#L733) |
| ASI07 Insecure Inter-Agent Communication | [L772](owasp-top-10-agentic-applications-2026.md#L772) | [L822](owasp-top-10-agentic-applications-2026.md#L822) |
| ASI08 Cascading Failures | [L863](owasp-top-10-agentic-applications-2026.md#L863) | [L935](owasp-top-10-agentic-applications-2026.md#L935) |
| ASI09 Human-Agent Trust Exploitation | [L965](owasp-top-10-agentic-applications-2026.md#L965) | [L1022](owasp-top-10-agentic-applications-2026.md#L1022) |
| ASI10 Rogue Agents | [L1062](owasp-top-10-agentic-applications-2026.md#L1062) | [L1107](owasp-top-10-agentic-applications-2026.md#L1107) |

These are section starts, for navigation. A finding should cite the line its claim actually rests
on, which is usually inside the section rather than at its heading.
