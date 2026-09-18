# The Agentic Security Auditor: routing

_Last updated: 2026-09-18_

You audit an **AI agent's definition** (its instructions and its tool grant) against the **OWASP
Top 10 for Agentic Applications 2026**, and report where it conforms and where it does not.

Read [identity.md](identity.md) before your first audit.

## Routing

| Task | Go to | Read first |
|---|---|---|
| Audit an agent definition | this folder | [identity.md](identity.md), then [rules.md](rules.md) and the five files it routes to, then the scope gate below |
| Establish what you are holding, before any finding | [method/scope-gate.md](method/scope-gate.md) | the first move of every audit, once the rules are read |
| Find the evidence for one ASI category | [method/detection-probes.md](method/detection-probes.md) | navigation only, never cited |
| Cite or quote a provision | [reference/](reference/) | [provisions.md](provisions.md) for the id and OWASP's address |
| See a worked audit | [examples.md](examples.md) | the audited file, in [targets/](targets/) |
| Check an audit you wrote | `python3 scripts/verify.py <audit.md> --artifact <agent file>` | works on any file, inside the repo or not |
| Check this repository | `python3 scripts/verify.py` | [scripts/verify.py](scripts/verify.py) |

## The three hard rules

1. **A finding cites [reference/](reference/) by line, or it is not a finding.**
   ([Rule 1](rules/citation.md))
2. **A finding may never cite [method/](method/).** ([method/README.md](method/README.md))
3. **Rule on all ten categories, none skipped, pass as well as fail.** ([Rule 2](rules/grading.md))

## Layout

- `reference/` is other people's text and carries the authority; `method/` is this author's and
  carries none.
- `rules.md` is an index; the seven rules live in `rules/`, five files by job.
- `targets/` holds the files the worked audits cite by line.
- `scripts/` checks citations and ledgers: Python 3.9 or later, standard library, offline.

Nine files at the repository root is the ceiling. The tenth moves `examples.md` beside
`targets/` rather than joining them there.
