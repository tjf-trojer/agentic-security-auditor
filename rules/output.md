# Output: the brief, the long form, and the markup

_Last updated: 2026-09-18_

Rule 5. What an audit looks like on the page, and the elements `scripts/verify.py` reads.

---

## Rule 5: Output format

**Deliver the brief. Never deliver the long form unasked.** The brief ends on Scope and limits, or
on Observations when there is one. Do not close by offering more.

### The brief

```
## Verdict
The call, in bold, from the severity count: any CRITICAL, **Do not deploy.**
No CRITICAL but a MAJOR, **Deploy after closing F<n>, F<n>.**, naming every
MAJOR finding. Otherwise **Deploy.** Then the arithmetic:
X pass, Y fail, Z partial, N not applicable; A critical, B major, C minor.
The severity count counts findings, by the level in each heading.
Then one or two sentences naming the governing fact, and, where findings
share a root cause, saying so and how many causes there really are.

## In plain terms
Two lines, no codes, for someone with no security background. What this
agent can do that is dangerous, and the one thing the reader should do.

## Conformity ledger
| Category | Verdict | Sev | Basis |
|---|---|---|---|
| ASI01 Agent Goal Hijack (outside text redirects the agent) | **FAIL** | CRITICAL | F2 |
| ASI05 Unexpected Code Execution (model output becomes an executed command)
  | **PASS** | - | Written exclusion: the grant is Read, Grep, Glob, no execution
  tool. Meets [ASI05 Mitigation 5](...) |
All ten, in order, none skipped. A FAIL or PARTIAL cites its finding by
number. A PASS or N/A carries its whole basis here, in one line, with a
citation for a PASS.

## Findings
### F1 · CRITICAL · ASI04 · <the claim, in six words or so>
**Artifact** the line or tool, quoted, with its number
**Standard** [address](citation) plus the words that carry the requirement
**Gap** one sentence: what the artifact does instead
**Ask** the question the owner must answer

Ordered by severity. One finding per defect, not per category: where one
defect fails three categories, list all three in the heading, give the
heading the highest level among their rows, cite at least one provision
for each on the Standard line (a provision from another category may
support, never replace), and point the three ledger rows at it.

## Fix order
Numbered, shortest path to safe first, with the reason in half a line.
Sequencing is not building: you say what to close first and why, never
what to write. Three to five items.

## Scope and limits
The capability profile from the scope gate: what the agent is, what it
does unattended, the lethal-trifecta legs, who it decides about and what
follows for them. Any judgment call, both readings in a sentence each.
Then what you were not given, and anything you could not verify, with the
test that would settle it. Two paragraphs, longer when the agent
decides about people: the fairness exposure and the disclosure question
go here, not in Observations.

## Observations outside the standard
Only if you have one. What you believe but cannot cite, in a line or two,
marked as judgment and not as a finding. Usually empty; a brief with no
uncitable concern omits the heading.
```

Target length: **the verdict and the ledger on one screen, then four lines per finding.** A
ten-category sweep with real findings lands near two pages; past three you are writing the long
form. Merge findings that share a cause ([Rule 4](grading.md)) before you cut anything that locates a finding.

### The long form (only when asked)

When the reader asks for depth, on the whole audit or on one finding, expand into prose. The long
form adds, and only these:

- **Capability profile** in full: autonomy level, composition pattern, the two lists of
  consequential and irreversible actions, the lethal-trifecta legs named.
- **Findings in prose**, keeping the same four parts but arguing them, with the interaction
  between findings drawn out.
- **Judgment calls**: both readings, what the decision turns on, who decides.
- **What holds**: the passes restated, with the standard quoted where it earns it.
- **Observations outside the standard**: what you believe but cannot cite, marked as judgment.

Nothing in the long form may contradict the brief. If writing it changes your mind, the brief was
wrong and you say so.

### Both forms

**Lead with meaning.** Codes go in the citation, not stacked mid-sentence.

**Gloss every code on first use.** Your reader may hold only your output. A code the verdict names
gets a few plain words there; in the ledger, every category name is followed by a few plain words
in brackets, as in "ASI04 Agentic Supply Chain Vulnerabilities (third-party parts trusted
unverified)". Do not turn findings into a glossary.

**Personal data is a pointer, not your assessment**: "a data-protection exposure for your DPIA,
outside this audit's scope".

### The markup the checker enforces

`scripts/verify.py` reads the output as text, so these must be written exactly.

| Element | Must be written as |
|---|---|
| A ledger row | `\| ASI04 <name> (<gloss>) \| **FAIL** \| <sev> \| <basis> \|`. The category cell begins with the code, the verdict is bold, and the four verdicts are spelled `PASS` `FAIL` `PARTIAL` `N/A` |
| The arithmetic | literally `X pass, Y fail, Z partial, N not applicable` |
| The call | the first bold text under `## Verdict`: `Do not deploy.`, `Deploy after closing ...` or `Deploy.`, as the severity count decides |
| A PASS | a Basis cell linking a `Mitigation` address, or the Letter from the Leaders at line 182 |
| A citation | a markdown link whose text is the provision's address, never prose. A bare section-and-line reference in running text is invisible to the checker and cannot be redeemed |
| A quoted provision | on a `**Standard**` line in the brief, or inside `**What the standard requires.**` or `What holds` in the long form, and at least 20 characters, or the check skips it |
| An audit in a multi-audit file | under a top-level `# Audit <n>` heading |
| Text in angle brackets | inside a code span, or the rendered page drops it |
| A hypothetical | in italics, never in quotation marks, which the checker reads as the artifact's words |
| A fenced block | around the artifact's own lines or the standard's own words, and nothing else. Anything else fails as a build ([Rule 0](posture.md)) |
| A configuration line, in Fix order or on an **Ask** line | the artifact's whole line. `tools: Read` where the file says `tools: Read, Grep` is a build, not a quotation |

**If you have a shell**, run `python3 scripts/verify.py <your-audit.md> --artifact <the-agent-file>`
before you deliver. `--artifact` checks the half of each finding that quotes the agent, down to
the line: every quotation must sit on a line its clause names.

**If you do not** (a Claude project has no shell), the table above is your checklist. For every
citation, open the cited line in `reference/` and confirm it says what you claimed.
