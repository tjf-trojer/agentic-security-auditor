#!/usr/bin/env python3
"""verify.py: check an audit, or this whole repository, offline.

It cannot tell whether a verdict is right. It checks:

  drift         every registered provision still holds its recorded words on its recorded line
  invented      every citation points at a line the standard has
  id            a citation's id and line agree with the register
  misquote      every passage quoted from the standard sits inside the provision cited
  artifact      the lines and quotations a finding attributes to the agent exist in its file
  skipped       every audit rules on all ten categories, exactly once
  ledger        the stated pass, fail, partial and not-applicable counts match the ledger
  severity      the stated critical, major and minor counts match the finding headings
  numbering     findings run F1 to Fn with no gaps, and none is referred to that does not exist
  uncited-pass  every PASS cites the provision it satisfies
  unlinked      no citation is written as prose instead of a link
  link          internal links resolve (repository run only)

An audit that links its copy in targets/ ("Copy at [..](targets/..)") is checked against that
file. --artifact names the file for an audit that does not.

    python3 scripts/verify.py                               # the repository
    python3 scripts/verify.py audit.md --artifact agent.md  # any audit, anywhere
"""
from __future__ import annotations

import glob
import os
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Resolve paths against the caller's directory before moving to the repository root.
ARGV = [a if a.startswith("-") else str(Path(a).resolve()) for a in sys.argv[1:]]
os.chdir(ROOT)

REF = Path("reference/owasp-top-10-agentic-applications-2026.txt")
REGISTER = Path("provisions.md")
# Longest a provision may run when nothing is registered after it.
SPAN_CAP = 14

CITE = re.compile(
    r"owasp-top-10-agentic-applications-2026\.txt#L(?P<line>\d+)(?:-L(?P<end>\d+))?"
    r"(?:\s+\"\^(?P<id>[A-Za-z0-9-]+)\")?"
)

failures: list[str] = []
notes: list[str] = []


def fail(check: str, msg: str) -> None:
    failures.append(f"[{check}] {msg}")


def norm(s: str) -> str:
    """Collapse whitespace, so a quotation matches across the source's hard wraps."""
    return re.sub(r"\s+", " ", s).strip()


def fold(s: str) -> str:
    """norm(), with curly quotes, dashes and non-breaking spaces folded to plain ASCII."""
    s = norm(s)
    for a, b in ((chr(0x201C), '"'), (chr(0x201D), '"'), (chr(0x2018), "'"), (chr(0x2019), "'"),
                 (chr(0x2013), "-"), (chr(0x2014), "-"), (chr(0x2212), "-"), (chr(0x00A0), " ")):
        s = s.replace(a, b)
    return s


def hyphen_variants(text: str) -> list[str]:
    """Both readings of a word the source splits at a hyphen across a line break: hyphen kept
    ("per-message") and dropped ("information"). A quotation matching either is accepted."""
    return [fold(re.sub(r"-\s*\n\s*", "-", text)), fold(re.sub(r"-\s*\n\s*", "", text))]


def quoted(text: str) -> list[str]:
    """Double-quoted passages, then code spans outside them. Each delimiter pairs only with its
    own kind, so a code span next to a quotation cannot swallow it."""
    found = re.findall(r'"([^"]+)"', text)
    found += re.findall(r"`([^`]+)`", re.sub(r'"[^"]*"', " ", text))
    return found


def strip_link_targets(text: str) -> str:
    return re.sub(r"\]\([^)]*\)", "] ", text)


def md_files() -> list[str]:
    return sorted(p for p in glob.glob("**/*.md", recursive=True) if ".git" not in p)


def load_register() -> dict[str, tuple[int, str]]:
    reg: dict[str, tuple[int, str]] = {}
    if not REGISTER.exists():
        fail("register", f"{REGISTER} missing; run scripts/build_register.py")
        return reg
    for row in REGISTER.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*`([A-Za-z0-9-]+)`\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|", row)
        if m:
            reg[m.group(1)] = (int(m.group(2)), m.group(3).replace("\\|", "|"))
    return reg


def audits_in(text: str) -> list[str]:
    """Each "# Audit <n>" section, or the whole file when it has no such heading but has a ledger."""
    chunks = re.split(r"\n# Audit (?=\d)", text)[1:]
    if not chunks and len(re.findall(r"^\|\s*ASI\d\d\b", text, re.M)) >= 5:
        chunks = [text]
    return chunks


def check_artifact(rel: str, text: str, artifact: Path) -> None:
    lines = artifact.read_text(encoding="utf-8", errors="replace").split("\n")
    whole = fold("\n".join(lines))
    for para in re.findall(r"^\*\*Artifact\*\*(.*?)(?=\n\*\*|\n\n|\Z)", text, re.M | re.S):
        for n in sorted({int(x) for x in re.findall(r"\blines?\s+(\d+)", para)}):
            if not 0 < n <= len(lines):
                fail("artifact", f"{rel}: cites line {n} of {artifact.name}, which has "
                                 f"{len(lines)} lines")
        for q in quoted(strip_link_targets(para)):
            if 12 <= len(norm(q)) <= 300 and fold(q) not in whole:
                fail("artifact", f"{rel}: quoted as being in {artifact.name} but not found there: "
                                 f"\"{q[:70]}\"")


def check_audit(rel: str, audit: str) -> None:
    title = audit.split("\n")[0].strip()[:40] or rel
    where = f"{rel} [{title}]"

    rows = re.findall(r"^\|\s*(ASI\d\d)\b[^|]*\|\s*\*\*(PASS|FAIL|PARTIAL|N/A)\*\*", audit, re.M)
    seen = Counter(code for code, _ in rows)
    for n in range(1, 11):
        code = f"ASI{n:02d}"
        if seen[code] == 0:
            fail("skipped", f"{where}: {code} has no verdict")
        elif seen[code] > 1:
            fail("skipped", f"{where}: {code} ruled on {seen[code]} times")

    for row in re.findall(r"^\|\s*ASI\d\d\b.*$", audit, re.M):
        if "**PASS**" in row and not CITE.search(row):
            code = re.match(r"^\|\s*(ASI\d\d)", row).group(1)
            fail("uncited-pass", f"{where}: {code} is PASS with no citation in its Basis cell")

    flat = re.sub(r"\s+", " ", audit)
    stated = re.search(r"(\d+) pass, (\d+) fail, (\d+) partial, (\d+) not applicable", flat)
    verdicts = Counter(v for _, v in rows)
    if not stated:
        fail("ledger", f"{where}: no stated ledger arithmetic")
    else:
        want = tuple(int(x) for x in stated.groups())
        got = (verdicts["PASS"], verdicts["FAIL"], verdicts["PARTIAL"], verdicts["N/A"])
        if want != got:
            fail("ledger", f"{where}: states {want}, table shows {got}")

    sev_found = Counter(re.findall(r"^#+ F\d+ *[·・] *(CRITICAL|MAJOR|MINOR)\b", audit, re.M))
    sev_stated = re.search(r"(\d+) critical, (\d+) major, (\d+) minor", flat)
    if sev_stated and sum(sev_found.values()):
        want = tuple(int(x) for x in sev_stated.groups())
        got = (sev_found["CRITICAL"], sev_found["MAJOR"], sev_found["MINOR"])
        if want != got:
            fail("severity", f"{where}: states {want[0]} critical, {want[1]} major, {want[2]} "
                             f"minor; the findings show {got[0]}/{got[1]}/{got[2]}")

    nums = [int(n) for n in re.findall(r"^#+ F(\d+) [·・]", audit, re.M)]
    if nums:
        if sorted(nums) != list(range(1, len(nums) + 1)):
            fail("numbering", f"{where}: finding headings are F{sorted(nums)}, expected "
                              f"F1..F{len(nums)} with no gaps")
        missing = sorted({int(n) for n in re.findall(r"\bF(\d+)\b", audit)} - set(nums))
        if missing:
            fail("numbering", f"{where}: refers to {', '.join('F' + str(m) for m in missing)} "
                              f"but no such finding exists")


def main() -> int:
    targets = [a for a in ARGV if not a.startswith("-")]
    artifact = None
    if "--artifact" in ARGV:
        i = ARGV.index("--artifact")
        if i + 1 < len(ARGV):
            artifact = Path(ARGV[i + 1])
            targets = [t for t in targets if t != str(artifact)]
            if not artifact.exists():
                fail("input", f"--artifact {artifact}: no such file")
                artifact = None
        else:
            fail("input", "--artifact needs a file")

    ref_lines = REF.read_text(encoding="utf-8").split("\n") if REF.exists() else []
    if not ref_lines:
        fail("input", f"{REF} missing")
    reg = load_register()
    reg_lines = sorted(ln for ln, _ in reg.values())

    for pid, (ln, words) in reg.items():
        if not 0 < ln <= len(ref_lines):
            fail("drift", f"{pid}: line {ln} is outside the standard")
        elif norm(ref_lines[ln - 1]) != norm(words):
            fail("drift", f"{pid}: line {ln} of the standard no longer holds its recorded words. "
                          f"If the standard was replaced, run scripts/build_register.py and read "
                          f"the diff.")
    notes.append(f"register: {len(reg)} provisions")

    repo_files = md_files()
    files = targets or repo_files
    if targets:
        notes.append(f"checking {len(files)} file(s) given on the command line")

    cites = audits = against_targets = 0
    out_of_scope = False
    for f in files:
        path = Path(f)
        if not path.exists():
            fail("input", f"{f}: no such file")
            continue
        text = path.read_text(encoding="utf-8")
        rel = f if f in repo_files else str(path)
        if re.search(r"\b(?:out of scope|not an agent|not in scope)\b", text, re.I):
            out_of_scope = True

        for m in CITE.finditer(text):
            cites += 1
            ln = int(m.group("line"))
            for n in [ln] + ([int(m.group("end"))] if m.group("end") else []):
                if not 0 < n <= len(ref_lines):
                    fail("invented", f"{rel}: #L{n} is outside the standard")
            pid = m.group("id")
            if pid and pid not in reg:
                fail("id", f"{rel}: link title ^{pid} is not in the register")
            elif pid and reg[pid][0] != ln:
                fail("id", f"{rel}: ^{pid} cited at L{ln}, register says L{reg[pid][0]}")

        blocks = re.findall(r"\*\*What the standard requires[.:]\*\*(.*?)(?=\n\n|\Z)", text, re.S)
        blocks += re.findall(r"^\*\*Standard\*\*(.*?)(?=\n\*\*|\n\n|\Z)", text, re.M | re.S)
        blocks += re.findall(r"^#+ What holds\s*$(.*?)(?=^#+ |\Z)", text, re.M | re.S)
        for block in blocks:
            spans = [(int(m.group("line")), int(m.group("end") or m.group("line")))
                     for m in CITE.finditer(block)]
            if not spans:
                continue
            # A quotation may come only from a provision the block cites: from its line to the
            # line before the next registered provision, capped at SPAN_CAP.
            allowed = []
            for a, b in spans:
                nxt = next((ln for ln in reg_lines if ln > b), None)
                hi = min(len(ref_lines), (nxt - 1) if nxt else b + SPAN_CAP, b + SPAN_CAP)
                allowed.extend(hyphen_variants("\n".join(ref_lines[a - 1:hi])))
            for q in re.findall(r'"([^"]+)"', strip_link_targets(block)):
                if not 20 <= len(q) <= 400:
                    continue
                parts = [x for x in re.split(r"\s*\.\.\.\s*", q) if len(norm(x)) >= 20]
                missing = [x for x in parts if not any(fold(x) in v for v in allowed)]
                if missing:
                    lines_cited = ", ".join(f"L{a}" for a, _ in spans)
                    fail("misquote", f"{rel}: quoted passage is not inside any provision cited in "
                                     f"its own block ({lines_cited}): \"{missing[0][:70]}\"")

        linked = [(m.start(), m.end()) for m in CITE.finditer(text)]
        linked += [(m.start(), m.end()) for m in re.finditer(r"```.*?```", text, re.S)]
        linked += [(m.start(), m.end()) for m in re.finditer(r"\[[^\]\n]*\]\([^)\n]*\)", text)]
        for m in re.finditer(r"§\s*L(\d+)\b", text):
            if any(a <= m.start() < b for a, b in linked):
                continue
            if re.search(r"\bartifact\b", text[max(0, m.start() - 160):m.start()]):
                continue
            fail("unlinked", f"{rel}: \"§L{m.group(1)}\" reads as a citation but is not a link. "
                             f"Write it as [..](reference/<file>#L{m.group(1)}).")

        chunks = audits_in(text)
        if artifact is not None:
            check_artifact(rel, text, artifact)
        for a in chunks:
            audits += 1
            check_audit(rel, a)
            copy = re.search(r"Copy at\s+\[[^\]]*\]\((targets/[^)\s]+)\)", a)
            if artifact is None and copy and Path(copy.group(1)).exists():
                against_targets += 1
                check_artifact(rel, a, Path(copy.group(1)))

    notes.append(f"citations: {cites} checked")
    notes.append(f"audits: {audits}, {against_targets} checked against their copy in targets/")
    if artifact is not None:
        notes.append(f"artifact: {artifact.name}")

    missing_input = any(x.startswith("[input]") for x in failures)
    if targets and cites == 0 and audits == 0 and not missing_input:
        if out_of_scope:
            notes.append("out-of-scope result: nothing to cite, which is correct here")
        else:
            fail("input", "nothing to check in the file(s) given: no citation to the standard and "
                          "no conformity ledger. An audit that cites nothing breaks Rule 1.")

    if not targets:
        broken = 0
        for f in repo_files:
            if f.startswith("targets/"):
                continue
            body = re.sub(r"```.*?```", "", Path(f).read_text(encoding="utf-8"), flags=re.S)
            for m in re.finditer(r"\[[^\]]*\]\(([^)#\s?]+)(?:\?[^)#]*)?(?:#[^)]*)?\)", body):
                t = m.group(1)
                if t.startswith(("http", "mailto")):
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), t))):
                    fail("link", f"{f} -> {t}")
                    broken += 1
        notes.append(f"links: {broken} broken")

    print("=" * 68)
    for n in notes:
        print(f"  {n}")
    print("=" * 68)
    if failures:
        print(f"FAILED: {len(failures)} problem(s)\n")
        for x in failures:
            print("  " + x)
        return 1
    print("OK: no check failed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
