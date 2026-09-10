# Notices: third-party material and its licences

_Last updated: 2026-09-10_

## OWASP Top 10 for Agentic Applications 2026

- **Files:** `reference/owasp-top-10-agentic-applications-2026.md` and
  `reference/owasp-top-10-agentic-applications-2026.pdf`
- **Author:** OWASP GenAI Security Project, Agentic Security Initiative
- **Version:** 2026, published December 2025
- **Source:** <https://genai.owasp.org>
- **Licence:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0),
  <https://creativecommons.org/licenses/by-sa/4.0/>
- **Changes:** the PDF is unmodified. The markdown is a text extraction of it with three layout
  normalisations, listed in its header and reproducible with `method/normalise-source.py`: page
  footers removed, the ten category headings rejoined, the five subsection labels marked as
  headings. No wording changed. The markdown stays under CC BY-SA 4.0.

## Audited artifacts

Reproduced byte-for-byte.

| File | Source | Licence |
|---|---|---|
| `targets/voltagent-agent-installer.md` | `categories/09-meta-orchestration/agent-installer.md` from <https://github.com/VoltAgent/awesome-claude-code-subagents>, commit `beb9a0f0d74a222f5e24aeb390e6d7c3005d9e27` | MIT |
| `targets/ecc-loop-operator.md` | `agents/loop-operator.md` from <https://github.com/affaan-m/ECC>, commit `e04ea0b` | MIT |
| `targets/swe-agent-default.yaml` | `config/default.yaml` from <https://github.com/SWE-agent/SWE-agent>, commit not recorded | MIT |

## Everything else

Original work under the MIT Licence in [`LICENSE`](LICENSE), including
`targets/ops-copilot-synthetic.md`.

Neither OWASP nor the authors of the audited artifacts endorse this repository.
