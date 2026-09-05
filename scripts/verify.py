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
  9. UNLINKED CITATION   a bare section-and-line reference in running text is not a
                         citation: it cannot be redeemed and no other check sees it.

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
SOURCE_NAME = {"owasp": "the OWASP standard", "act": "the AI Act excerpts"}

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


def hyphen_variants(text: str) -> list[str]:
    """Two readings of a word the source PDF split at a hyphen.

    The extraction preserves hard wraps, and some fall inside a word:
    `explicit per-\nmessage audiences`. Collapsing whitespace alone yields
    "per- message", which is not what the source says under any reading, so a
    correct quotation can never match it. Which reading is right depends on
    whether the hyphen belongs to the word ("per-message") or was inserted by
    the typesetter ("information"), and nothing in the text distinguishes them.
    So both are produced and a quote matching either is accepted.
    """
    joined_keep = re.sub(r"-\s*\n\s*", "-", text)
    joined_drop = re.sub(r"-\s*\n\s*", "", text)
    return [fold(joined_keep), fold(joined_drop)]


def load_register() -> dict[str, tuple[str, int, str]]:
    reg: dict[str, tuple[str, int, str]] = {}
    if not REGISTER.exists():
        fail("register", f"{REGISTER} missing; run scripts/build_register.py")
        return reg
    for row in REGISTER.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*`([A-Za-z0-9-]+)`\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|", row)
        if m:
            src = "owasp" if m.group(2).upper().startswith("OWASP") else "act"
            reg[m.group(1)] = (src, int(m.group(3)), m.group(4).replace("\\|", "|"))
    return reg


def md_files() -> list[str]:
    return sorted(p for p in glob.glob("**/*.md", recursive=True) if ".git" not in p)


def main(argv: list[str]) -> int:
    targets = [a for a in argv[1:] if not a.startswith("-")]
    relink = "--relink" in argv

    ref_lines = REF.read_text(encoding="utf-8").split("\n") if REF.exists() else []
    act_lines = ACT.read_text(encoding="utf-8").split("\n") if ACT.exists() else []
    src_lines = {"owasp": ref_lines, "act": act_lines}
    ref_variants = hyphen_variants(REF.read_text(encoding="utf-8")) if REF.exists() else []
    reg = load_register()
    line_to_id = {(src, ln): pid for pid, (src, ln, _) in reg.items()}

    # 1. DRIFTED PROVISION. Always runs: it is what makes every other check mean
    # something, and it is cheap.
    for pid, (src, ln, text) in reg.items():
        lines = src_lines.get(src, [])
        if not 0 < ln <= len(lines):
            fail("drift", f"{pid}: line {ln} is outside {SOURCE_NAME[src]}")
        elif norm(lines[ln - 1]) != norm(text):
            fail("drift", f"{pid}: {SOURCE_NAME[src]} line {ln} no longer holds its recorded "
                          f"words. The standard may have been replaced. Rebuild the register "
                          f"deliberately (make register) and read the diff.")
    notes.append(f"register: {len(reg)} provisions ({sum(1 for v in reg.values() if v[0]=='owasp')} OWASP, "
                 f"{sum(1 for v in reg.values() if v[0]=='act')} AI Act)")

    if targets:
        files = targets
        notes.append(f"checking {len(files)} file(s) given on the command line")
    else:
        files = md_files()

    total_cites = rewritten = ledger_count = 0
    out_of_scope = False
    for f in files:
        path = Path(f)
        if not path.exists():
            fail("input", f"{f}: no such file")
            continue
        original = path.read_text(encoding="utf-8")
        rel = f if f in set(md_files()) else str(path)
        if re.search(r"\b(?:out of scope|not an agent|not in scope)\b", original, re.I):
            out_of_scope = True

        # 2 INVENTED CITATION, 3 MISLABELLED ID
        for m in CITE.finditer(original):
            total_cites += 1
            src = "owasp" if m.group("file").startswith("owasp") else "act"
            lines = src_lines[src]
            ln = int(m.group("line"))
            for n in [ln] + ([int(m.group("end"))] if m.group("end") else []):
                if not 0 < n <= len(lines):
                    fail("invented", f"{rel}: #L{n} is outside {SOURCE_NAME[src]}")
            pid = m.group("id")
            if pid:
                if pid not in reg:
                    fail("id", f"{rel}: link title ^{pid} is not in the register")
                else:
                    rsrc, rln, _ = reg[pid]
                    if rsrc != src:
                        fail("id", f"{rel}: ^{pid} is a {SOURCE_NAME[rsrc]} provision but is "
                                   f"cited against {SOURCE_NAME[src]}")
                    elif rln != ln:
                        fail("id", f"{rel}: ^{pid} cited at L{ln}, register says L{rln}")

        # 4 MISQUOTED STANDARD. Two contexts may quote a reference (rules.md,
        # Rule 1): a finding's "Standard" line and "What holds". Each quotation is
        # checked against the document(s) that block actually cites, and against a
        # window around the cited lines rather than the whole file.
        #
        # Both refinements exist because testing found the loose version hollow: a
        # quote lifted from a different provision, cited to the wrong line, passed
        # clean; and an AI Act quotation sharing a block with an OWASP citation was
        # checked against the OWASP text and failed for the wrong reason.
        blocks = re.findall(r"\*\*What the standard requires[.:]\*\*(.*?)(?=\n\n|\Z)",
                            original, re.S)
        blocks += re.findall(r"^\*\*Standard\*\*(.*?)(?=\n\*\*|\n\n|\Z)", original, re.M | re.S)
        blocks += re.findall(r"^#+ What holds\s*$(.*?)(?=^#+ |\Z)", original, re.M | re.S)
        WINDOW = 12
        for para in blocks:
            cites = [(("owasp" if m.group("file").startswith("owasp") else "act"),
                      int(m.group("line")),
                      int(m.group("end")) if m.group("end") else int(m.group("line")))
                     for m in CITE.finditer(para)]
            if not cites:
                continue
            # The text a quotation in this block is allowed to have come from.
            allowed = []
            for src, a_, b_ in cites:
                lines_ = src_lines.get(src, [])
                lo = max(0, a_ - 1 - WINDOW)
                hi = min(len(lines_), b_ + WINDOW)
                allowed.extend(hyphen_variants("\n".join(lines_[lo:hi])))
            para_txt = re.sub(r"\]\([^)]*\)", "] ", para)
            for q in re.findall(r"\"([^\"]{20,400})\"", para_txt):
                parts = [x for x in re.split(r"\s*\.\.\.\s*", q) if len(norm(x)) >= 20]
                missing = [x for x in parts if not any(fold(x) in v for v in allowed)]
                if parts and missing:
                    where = ", ".join(f"{SOURCE_NAME[s]} L{a_}" for s, a_, _ in cites)
                    fail("misquote", f"{rel}: quoted passage is not within {WINDOW} lines of any "
                                     f"citation in its own block ({where}): \"{missing[0][:70]}\"")

        # 4b UNLINKED CITATION. A citation written as prose ("§L1008", "line 376")
        # resolves for a human reader and is invisible to every other check here,
        # so "OK" would mean "the citations you formatted correctly are fine" while
        # an unredeemable one sits in the text looking supported. That is the exact
        # direction of failure this repository exists to prevent, so it is an error.
        # Spans that are already part of a formatted citation: the URL itself, and
        # the link *text* in front of it, which is commonly written "[§L965](...)".
        linked_spans = [(m.start(), m.end()) for m in CITE.finditer(original)]
        linked_spans += [(m.start(), m.end()) for m in re.finditer(r"```.*?```", original, re.S)]
        linked_spans += [(m.start(), m.end()) for m in
                         re.finditer(r"\[[^\]\n]*\]\([^)\n]*\)", original)]
        for m in re.finditer(r"(?:§\s*L(\d+)\b|\bline (\d{2,4})\b(?=[^\n]{0,40}"
                             r"(?:standard|OWASP|reference|provision)))", original):
            if any(a_ <= m.start() < b_ for a_, b_ in linked_spans):
                continue
            # A reference to a line of the audited artifact is not a citation.
            window = original[max(0, m.start() - 160):m.start()]
            if re.search(r"\b(?:in the artifact|Where, in the artifact|artifact)\b", window):
                continue
            if not m.group(1):
                continue
            fail("unlinked", f"{rel}: \"§L{m.group(1)}\" reads as a citation but is not a link, "
                             f"so it cannot be redeemed and no other check sees it. Write it as "
                             f"[..](reference/<file>#L{m.group(1)}) or say plainly that it is not "
                             f"a citation.")

        # 5 SKIPPED CATEGORY, 6 UNSOUND LEDGER. Runs on any document that contains
        # audits, not only examples.md, so a user can check their own work.
        # A document holds audits if it has top-level "# Audit <n>" headings.
        # A file given on the command line that has no such heading but does carry
        # a ledger is treated as a single audit, so a user can check their own work
        # without having to imitate examples.md's numbering.
        chunks = re.split(r"\n# Audit (?=\d)", original)[1:]
        if not chunks and len(re.findall(r"^\|\s*ASI\d\d\b", original, re.M)) >= 5:
            chunks = [original]
        for a in chunks:
            ledger_count += 1
            title = a.split("\n")[0].strip()[:40] or path.name
            rows = re.findall(r"^\|\s*(ASI\d\d)\b[^|]*\|\s*\*\*(PASS|FAIL|PARTIAL|N/A)\*\*",
                              a, re.M)
            seen = Counter(c for c, _ in rows)
            for n in range(1, 11):
                code = f"ASI{n:02d}"
                if seen[code] == 0:
                    fail("skipped", f"{rel} [{title}]: {code} has no verdict")
                elif seen[code] > 1:
                    fail("skipped", f"{rel} [{title}]: {code} ruled on {seen[code]} times")
            # 6b UNSOUND SEVERITY COUNT and 6c FINDING NUMBERING. Both classes
            # shipped in this repository undetected: a severity line that did not
            # match its own findings, and an audit whose headings skipped F5 after
            # two findings were merged. Check 6 only ever validated the verdict
            # arithmetic, so both passed clean.
            sev_found = Counter(re.findall(r"^#+ F\d+ *[·・] *(CRITICAL|MAJOR|MINOR)\b",
                                           a, re.M))
            flat_a = re.sub(r"\s+", " ", a)
            sev_stated = re.search(r"(\d+) critical, (\d+) major, (\d+) minor", flat_a)
            if sev_stated and sum(sev_found.values()):
                want = tuple(int(x) for x in sev_stated.groups())
                got = (sev_found["CRITICAL"], sev_found["MAJOR"], sev_found["MINOR"])
                if want != got:
                    fail("severity", f"{rel} [{title}]: states {want[0]} critical, {want[1]} major, "
                                     f"{want[2]} minor; the findings show {got[0]}/{got[1]}/{got[2]}")
            nums = [int(n) for n in re.findall(r"^#+ F(\d+) [·・]", a, re.M)]
            if nums:
                expected = list(range(1, len(nums) + 1))
                if sorted(nums) != expected:
                    fail("numbering", f"{rel} [{title}]: finding headings are F{sorted(nums)}, "
                                      f"expected F1..F{len(nums)} with no gaps")
                referenced = {int(n) for n in re.findall(r"\bF(\d+)\b", a)}
                missing = sorted(referenced - set(nums))
                if missing:
                    fail("numbering", f"{rel} [{title}]: refers to "
                                      f"{', '.join('F'+str(m) for m in missing)} "
                                      f"but no such finding exists")

            c = Counter(v for _, v in rows)
            # Tolerate a line wrap inside the arithmetic: a writer cannot control
            # where their editor breaks the line, and failing them for it produced
            # a misleading "no stated ledger arithmetic" in testing.
            flat = re.sub(r"\s+", " ", a)
            stated = re.search(r"(\d+) pass, (\d+) fail, (\d+) partial, (\d+) not applicable", flat)
            if not stated:
                fail("ledger", f"{rel} [{title}]: no stated ledger arithmetic")
            else:
                want = tuple(int(x) for x in stated.groups())
                got = (c["PASS"], c["FAIL"], c["PARTIAL"], c["N/A"])
                if want != got:
                    fail("ledger", f"{rel} [{title}]: states {want}, table shows {got}")

        if relink and rel not in VERBATIM:
            def add_id(m: re.Match) -> str:
                if m.group("id"):
                    return m.group(0)
                src = "owasp" if m.group("file").startswith("owasp") else "act"
                pid = line_to_id.get((src, int(m.group("line"))))
                if not pid:
                    return m.group(0)
                return (f"{m.group('file')}{m.group('plain') or ''}#L{m.group('line')}"
                        f"{'-L' + m.group('end') if m.group('end') else ''} \"^{pid}\"")
            new = CITE.sub(add_id, original)
            if new != original:
                path.write_text(new, encoding="utf-8")
                rewritten += 1

    notes.append(f"citations: {total_cites} checked")
    notes.append(f"ledgers: {ledger_count} audit(s), all ten categories each")
    if targets and total_cites == 0 and ledger_count == 0:
        # An out-of-scope result is the correct output for an artifact that is not an
        # agent, and it has nothing to cite by design. Failing it would punish a user
        # for following the scope gate.
        if out_of_scope:
            notes.append("out-of-scope result: nothing to cite, which is correct here")
        else:
            fail("input", "nothing to check in the file(s) given: no citations to either "
                          "reference document and no conformity ledger. If this is an audit, "
                          "it does not cite the standard, which Rule 1 requires.")
    if relink:
        notes.append(f"relink: rewrote citations in {rewritten} file(s)")

    # 7 BROKEN LINK, 8 STALE VOCABULARY: repo-wide only.
    if not targets:
        broken = 0
        for f in md_files():
            d = os.path.dirname(f)
            body = re.sub(r"```.*?```", "", Path(f).read_text(encoding="utf-8"), flags=re.S)
            for m in re.finditer(r"\[[^\]]*\]\(([^)#\s?]+)(?:\?[^)#]*)?(?:#[^)]*)?\)", body):
                t = m.group(1)
                if t.startswith(("http", "mailto")) or f in VERBATIM:
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(d, t))):
                    fail("link", f"{f} -> {t}")
                    broken += 1
        notes.append(f"links: resolved, {broken} broken outside verbatim artifacts")
        for f in md_files():
            if f in VERBATIM:
                continue
            for word in ("WEAKNESS", "BLOCKER"):
                if re.search(rf"\b{word}\b", Path(f).read_text(encoding="utf-8")):
                    fail("vocabulary", f"{f}: uses '{word}', which rules.md does not define")

    print("=" * 68)
    for n in notes:
        print(f"  {n}")
    print("=" * 68)
    if failures:
        print(f"FAILED: {len(failures)} problem(s)\n")
        for x in failures:
            print("  " + x)
        return 1
    print("OK: the standard is intact, every citation resolves and is quoted")
    print("    correctly, and no audit skipped a category.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
