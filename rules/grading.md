# Grading: the ledger's verdicts and the severity levels

_Last updated: 2026-09-18_

Rule 2 and Rule 4. Which of the four verdicts a category takes, and what level a FAIL or a
PARTIAL carries.

---

## Rule 2: The conformity ledger, before the findings

Every audit rules on **all ten categories**, in order, none skipped. The ledger comes first, before
the failures. Four verdicts, and only these four:

| Verdict | Meaning |
|---|---|
| **PASS** | A control is present that meets what the standard prescribes, or a written exclusion a provision reaches keeps the category from arising, and you can name it |
| **FAIL** | The category applies and the artifact does not meet it. A numbered finding follows |
| **PARTIAL** | A control is present but incomplete or would not survive load. A finding follows, usually MAJOR |
| **N/A** | The category cannot arise here, with the reason in the same line: the artifact is silent on it, or excludes it where no provision reaches the exclusion |

**The ledger is the complete account of the audit's findings.** A numbered finding exists because
a category was graded FAIL or PARTIAL; there is no other route into the F-sequence. What the
standard does not reach is not a finding and does not enter the ledger. It goes in "Observations
outside the standard", unnumbered and marked as judgment.

**The Sev column grades the row, not the finding.** Where one finding is cited by three rows, each
row carries the severity *for that category*. A shared root cause can be critical where it is most
reachable and major in the others. Each row takes the level its own category earns, so more than
one row can be CRITICAL.

**A PASS must name the control *and cite the provision it satisfies*.** "No supply chain issues
found" is an unexamined category, not a pass. Name the line of the artifact that earns it and the
provision it meets, in the Basis column. If you cannot cite what the control satisfies, the verdict
is FAIL or N/A. That provision is a mitigation, or the Least-Agency line of the Letter from the
Leaders; a Description, Common Example or Attack Scenario describes a risk and cannot carry a PASS.

**An N/A must be argued.** "Single agent: delegates to no agent, and no agent's message steers it" is
reasoned. "Not applicable" is a category you skipped.

**A PASS resting on a capability the artifact does not grant cites the least-privilege clause.** A
closed tool allowlist containing no shell earns ASI05, but ASI05's mitigations are about running
code safely and none says "grant no execution tool". Cite the least-privilege or scope clause
nearest the category and say in the Basis cell that the control is an exclusion rather than a
safeguard. Where no clause reaches it, the verdict is N/A with the exclusion named. A capability counts as granted when any granted tool
can reach it: `Bash` reaches every credential the invoking account holds.

**A tool that is named and never defined is unverified, and that is an ASI04 finding.** Ownership
excuses only a *file at a fixed path inside the operator's own repository*, which you can see. A
tool name resolving to something you cannot see (`send_email`, `query_hris`, `publish_site`) is
runtime composition, whether it turns out to be in-house or a vendor endpoint. Grade it on what the
name and its use in the file imply, default to FAIL where the tool reaches anything outside the
operator's control, and say in the finding that its scope and provenance could not be verified from
the definition. Where the definition shows that the tool touches nothing outside, a reasoned
N/A naming that is defensible; a tool you cannot read never shows it. The same holds for a prompt, pattern or config the definition loads by name without
showing it.

**A harness's own built-in tools belong to the platform.** `Bash`, `Read`, `Write` or `WebFetch` in
Claude Code are graded on what they reach, under ASI02 and ASI05; ASI04 does not ask for their
provenance. So does the model a `model:` alias names: put its version check in Scope and limits. A
file you were not given is unverified, even at a relative path.

**Owning something is not pinning it.** A file the operator controls, at a fixed path inside their
own repository, does not raise ASI04: the category is about what an agent composes at runtime *that
it does not own*. That is a reasoned N/A, never a PASS citing `ASI04-PIN`, which asks for a content
hash and a commit id that a relative path does not provide.

**PASS and N/A are separated by whether a provision credits what the artifact decided.** A **written
exclusion** a provision reaches is a PASS: `tools: Read, Grep, Glob` is a closed allowlist that rules
out execution, and ASI05's least-privilege clause reaches it. **Silence**, or an exclusion no
provision reaches, is N/A. Say in the Basis column which one you are looking at.

**A category applies when the definition grants or names what it is about**: a store it reads
back, a peer agent, a component loaded at runtime. Where the category could arise only through an
environment the definition never mentions, the verdict is N/A: name that dependency in the Basis
cell and its test in Scope and limits.

**Silence is not a control.** Where a category applies, the artifact says nothing, and the
consequence turns on a fact you cannot see, the verdict is still FAIL. Put the uncertainty in the
finding ([Rule 6](posture.md)), not in the ledger, and do not invent a fifth verdict. Where the unseen fact
decides between two severity levels, grade the level the definition's own text supports and name
the fact that would move it.

**A control on the artifact's outputs is not a control on the artifact.** A definition that requires
something of the documents, plans or scripts the agent produces (a runbook must contain a rollback
section, a report must cite its sources) while requiring nothing of the agent's own execution is
PARTIAL at most. Say in the Basis column which of the two it governs. A sentence that scopes the
task counts as a control only where it limits the exposure the category is about.

**Grade a row against the mitigations its exposure turns on.** Name the exposure the definition
creates in that category and the mitigations that answer it: PASS where the definition meets them,
PARTIAL where it meets some and misses others, FAIL where it meets none. A mitigation for an exposure
the definition does not create (a store it lacks, a peer it never messages) does not count against
it, and the finding names what is missing.

**A control the model is told to perform is PARTIAL at most.** Nothing outside the model enforces
it: a confirmation the model is told to ask for, a check it runs on its own work, a stop it applies
to itself and a clause telling it to distrust what it reads are all instructions to the model. A
PASS rests on the tool grant, or on a mechanism outside the model that the definition names: a
harness setting, a hook, a separate reviewer. A distrust clause earns PARTIAL where it covers the
inputs this agent reads, by name or by a class that plainly includes them, and FAIL where it covers
none of them. A block of safety clauses is graded clause by clause, each clause in every category
whose mitigation its effect meets, named in the Basis cell.

**An artifact that is itself a category's mitigation is graded on its own exposure.** A watchdog
under ASI10 or a governance agent under ASI08 gets the verdict for its own exposure in that
category, and the Basis cell names the mitigation it provides to others. Controls it applies to the
agents it supervises count toward its own row only where they also bind its own actions.

**Never credit a control the artifact does not contain** to balance a harsh audit, and never mark
PASS because the author seems careful. The ledger measures what a definition commits to in writing.

---

## Rule 4: Severity

Every FAIL and PARTIAL carries one level, defined by consequence:

| Level | Meaning | Test |
|---|---|---|
| **CRITICAL** | An unmitigated path to serious harm | Untrusted input reaches an irreversible action with no human gate; severe blast radius on hijack; high autonomy with no stop; **or the artifact's own output, or text in it aimed at whoever reviews it, carries an assurance that nothing requires to be true** |
| **MAJOR** | A control exists but would not survive load or attack | Approval that shows the human nothing judgeable; logging with no reasoning trace; a tool broader than its task; an unverified dependency that executes; no record of actions, or no stop, where the agent acts while nobody watches |
| **MINOR** | A real gap whose realistic consequence is bounded | Missing disclosure on an internal-only path; an unpinned dependency that is read but never executed; no record where every action is a read, or where a person starts and sees every action |

**A gate that shows the person nothing they can judge does not gate the path.** Grade the path as
ungated for the CRITICAL test, and the gate itself under ASI09.

**JUDGMENT CALL** is separate and never mixed into the numbered findings: defensible either way,
but the decision must be *made*. State both readings, what it turns on, and who decides (builder,
accountable owner, counsel).

Never inflate a judgment call to seem rigorous; never soften a CRITICAL to be kind.

**When several findings share one root cause** (an artifact naming no human fails ASI02, ASI05 and
ASI09 for the same reason), do not stamp them all CRITICAL. Rank by **reachability**: the shortest
path from attacker input or ordinary mistake to serious harm. Say in the summary that they share a
cause, so the owner fixes it once.

**Merge findings that share a cause.** Rule 2 requires a verdict on every category, not a separate
finding per category. Where one defect fails three categories, write one finding, name the
categories it fails, and point all three ledger rows at it. A cause is shared when one change to
the definition would close every finding that carries it.

**An assurance is CRITICAL whatever the tool grant.** Where the artifact's product is a claim
someone will act on (a compliance verdict, a security sign-off, a risk score, "safe to deploy") and
nothing in the definition requires that claim to be derived from what the agent actually checked,
grade it CRITICAL. An empty tool grant does not reduce it. Where the definition ties the claim to
what was checked but not to how much had to be checked, grade it MAJOR.
