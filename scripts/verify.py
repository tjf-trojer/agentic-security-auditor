#!/usr/bin/env python3
"""verify.py — prove this auditor's own claims, offline, in one command.

This script does not judge whether a verdict is right; no script can. It proves
the things that go wrong when a language model writes a compliance document, and
each check exists because one of them actually happened while this repo was built:

  1. DRIFTED PROVISION   every registered id still sits at the line the register
                         records, holding the words the register recorded.
  2. INVENTED CITATION   every citation in the repo points at a line that exists.
  3. MISLABELLED ID      where a citation carries an id in its link title, that id
                         and that line number agree with the register.
  4. MISQUOTED STANDARD  every passage quoted next to a citation appears verbatim
                         in the standard, ignoring only the hard line wraps.
  5. SKIPPED CATEGORY    every audit rules on all ten ASI categories, exactly once.
                         An audit cannot quietly omit the inconvenient ones.
  6. UNSOUND LEDGER      the pass/fail/partial/N-A counts an audit states match the
                         verdicts in its own table.
  7. BROKEN LINK         internal links resolve, except inside verbatim artifacts
                         in targets/, which point at their own repositories.
  8. STALE VOCABULARY    no severity word survives that the rules no longer define.

    python3 scripts/verify.py             # check everything, exit 1 on failure
    python3 scripts/verify.py --relink    # rewrite citations to carry their ids
"""
from __future__ import annotations

import glob
import os
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

REF_NAME = "owasp-top-10-agentic-applications-2026.md"
REF = Path("reference") / REF_NAME
ACT = Path("reference") / "eu-ai-act-2024-1689-excerpts.md"
REGISTER = Path("provisions.md")

# Links inside a byte-for-byte copy of someone else's artifact point at their
# repository, not ours. Rewriting them would corrupt the thing being audited.
VERBATIM = {"targets/eu-ai-act-map-agents.md"}

CITE = re.compile(
    r"(?P<file>owasp-top-10-agentic-applications-2026\.md|eu-ai-act-2024-1689-excerpts\.md)"
    r"(?P<plain>\?plain=1)?#L(?P<line>\d+)(?:-L(?P<end>\d+))?"
    r"(?P<title>\s+\"\^(?P<id>[A-Za-z0-9-]+)\")?"
)

failures: list[str] = []
notes: list[str] = []


def fail(check: str, msg: str) -> None:
    failures.append(f"[{check}] {msg}")


def norm(s: str) -> str:
    """Collapse whitespace so a quote can match across the source's hard wraps."""
    return re.sub(r"\s+", " ", s).strip()


def fold(s: str) -> str:
    """norm(), plus fold the typography the OJ and OWASP PDFs use.

    The source uses curly quotes, en dashes and non-breaking spaces that a person
    retyping a quotation will not reproduce. Folding them keeps the check on
    wording rather than on punctuation the author never chose.
    """
    s = norm(s)
    for a, b in (("\u201c", '"'), ("\u201d", '"'), ("\u2018", "'"), ("\u2019", "'"),
                 ("\u2013", "-"), ("\u2014", "-"), ("\u2212", "-"), ("\u00a0", " ")):
        s = s.replace(a, b)
    return s


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


def md_files() -> list[str]:
    return sorted(p for p in glob.glob("**/*.md", recursive=True) if ".git" not in p)


def main(relink: bool = False) -> int:
    ref_lines = REF.read_text(encoding="utf-8").split("\n") if REF.exists() else []
    act_lines = ACT.read_text(encoding="utf-8").split("\n") if ACT.exists() else []
    ref_folded = fold(REF.read_text(encoding="utf-8")) if REF.exists() else ""
    reg = load_register()
    line_to_id = {ln: pid for pid, (ln, _) in reg.items()}

    # 1. DRIFTED PROVISION
    for pid, (ln, text) in reg.items():
        if not 0 < ln <= len(ref_lines):
            fail("drift", f"{pid}: line {ln} is outside the reference")
        elif norm(ref_lines[ln - 1]) != norm(text):
            fail("drift", f"{pid}: line {ln} no longer holds its recorded words. "
                          f"The standard may have been replaced. Re-run build_register.py deliberately.")
    notes.append(f"register: {len(reg)} provisions")

    # 2, 3, 4: citations
    total_cites = 0
    rewritten = 0
    for f in md_files():
        raw = original = Path(f).read_text(encoding="utf-8")
        for m in CITE.finditer(original):
            total_cites += 1
            src = ref_lines if m.group("file").startswith("owasp") else act_lines
            ln = int(m.group("line"))
            ends = [ln] + ([int(m.group("end"))] if m.group("end") else [])
            for n in ends:
                if not 0 < n <= len(src):
                    fail("invented", f"{f}: #L{n} is outside {m.group('file')}")
            pid = m.group("id")
            if pid:
                if pid not in reg:
                    fail("id", f"{f}: link title ^{pid} is not in the register")
                elif reg[pid][0] != ln:
                    fail("id", f"{f}: ^{pid} cited at L{ln}, register says L{reg[pid][0]}")

        # 4. MISQUOTED STANDARD. By Rule 5 the block that quotes the standard is
        # "What the standard requires"; a quote there must appear in the standard.
        # Quotes elsewhere in a finding are of the audited artifact, not of OWASP.
        for para in re.findall(r"\*\*What the standard requires[.:]\*\*(.*?)(?=\n\n|\Z)",
                               original, re.S):
            if REF_NAME not in para:
                continue
            # Strip the link targets first. Since citations carry their id as a
            # quoted link title, leaving them in would make the quote extractor
            # read across them and invent quotations nobody wrote.
            para = re.sub(r"\]\([^)]*\)", "] ", para)
            for q in re.findall(r"\"([^\"]{20,400})\"", para):
                parts = [x for x in re.split(r"\s*\.\.\.\s*", q) if len(norm(x)) >= 20]
                if not parts:
                    continue
                missing = [x for x in parts if fold(x) not in ref_folded]
                if missing:
                    fail("misquote", f"{f}: in a \"What the standard requires\" block, "
                                     f"not verbatim in the standard: \"{missing[0][:80]}\"")

        if relink and f not in VERBATIM:
            def add_id(m: re.Match) -> str:
                if m.group("id") or not m.group("file").startswith("owasp"):
                    return m.group(0)
                pid = line_to_id.get(int(m.group("line")))
                if not pid:
                    return m.group(0)
                return (f"{m.group('file')}{m.group('plain') or ''}"
                        f"#L{m.group('line')}"
                        f"{'-L' + m.group('end') if m.group('end') else ''}"
                        f' "^{pid}"')
            raw = CITE.sub(add_id, original)
            if raw != original:
                Path(f).write_text(raw, encoding="utf-8")
                rewritten += 1
    notes.append(f"citations: {total_cites} checked")
    if relink:
        notes.append(f"relink: rewrote citations in {rewritten} files")

    # 5, 6: the ledgers
    ex = Path("examples.md").read_text(encoding="utf-8") if Path("examples.md").exists() else ""
    audits = re.split(r"\n# Audit ", ex)[1:]
    for a in audits:
        title = a.split("\n")[0].strip()
        rows = re.findall(r"^\|\s*(ASI\d\d)[^|]*\|\s*\*\*(PASS|FAIL|PARTIAL|N/A)\*\*", a, re.M)
        seen = Counter(code for code, _ in rows)
        for n in range(1, 11):
            code = f"ASI{n:02d}"
            if seen[code] == 0:
                fail("skipped", f"Audit {title}: {code} has no verdict")
            elif seen[code] > 1:
                fail("skipped", f"Audit {title}: {code} ruled on {seen[code]} times")
        c = Counter(v for _, v in rows)
        stated = re.search(r"Ledger: \*\*(\d+) pass, (\d+) fail, (\d+) partial, (\d+) not applicable", a)
        if not stated:
            fail("ledger", f"Audit {title}: no stated ledger arithmetic")
        else:
            want = tuple(int(x) for x in stated.groups())
            got = (c["PASS"], c["FAIL"], c["PARTIAL"], c["N/A"])
            if want != got:
                fail("ledger", f"Audit {title}: states {want}, table shows {got}")
    notes.append(f"ledgers: {len(audits)} audits, all ten categories each")

    # 7. BROKEN LINK
    broken = 0
    for f in md_files():
        d = os.path.dirname(f)
        for m in re.finditer(r"\[[^\]]*\]\(([^)#\s?]+)(?:\?[^)#]*)?(?:#[^)]*)?\)",
                             Path(f).read_text(encoding="utf-8")):
            t = m.group(1)
            if t.startswith(("http", "mailto")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(d, t))):
                if f in VERBATIM:
                    continue
                fail("link", f"{f} -> {t}")
                broken += 1
    notes.append(f"links: resolved, {broken} broken outside verbatim artifacts")

    # 8. STALE VOCABULARY
    defined = {"CRITICAL", "MAJOR", "MINOR", "JUDGMENT CALL"}
    for f in md_files():
        if f in VERBATIM:
            continue
        for word in ("WEAKNESS", "BLOCKER"):
            if re.search(rf"\b{word}\b", Path(f).read_text(encoding="utf-8")):
                fail("vocabulary", f"{f}: uses '{word}', which rules.md does not define "
                                   f"(defined: {', '.join(sorted(defined))})")

    # report
    width = 68
    print("=" * width)
    for n in notes:
        print(f"  {n}")
    print("=" * width)
    if failures:
        print(f"FAILED: {len(failures)} problem(s)\n")
        for x in failures:
            print("  " + x)
        return 1
    print("OK: the standard is intact, every citation resolves and is quoted")
    print("    correctly, and no audit skipped a category.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(relink="--relink" in sys.argv))
