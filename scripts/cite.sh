#!/usr/bin/env bash
# cite.sh — resolve a citation and print the provision it points at.
#
# Why this exists. An auditor's whole claim is that its findings can be checked
# against the standard. Without a tool, a citation is only a promise: the reader
# has to open a 1,695-line file, find a line number, and read around a hard wrap
# to see where the sentence ends. On github.com they cannot even do that, because
# rendered markdown has no line numbers. This script makes a citation redeemable
# from the terminal, in one command, with no editor and no browser.
#
#   bash scripts/cite.sh ASI04-PIN                 # by register id (OWASP)
#   bash scripts/cite.sh AIA-50-1                  # by register id (AI Act)
#   bash scripts/cite.sh owasp:589                 # by line, source named
#   bash scripts/cite.sh act:741                   # by line, source named
#   bash scripts/cite.sh 589                       # by line; source inferred, or refused
#   bash scripts/cite.sh --from examples.md        # every citation in a document
#   bash scripts/cite.sh --from <file> --list      # just the list, no text
#   bash scripts/cite.sh --list                    # the whole register
#
# This repository holds TWO reference documents. A bare line number is therefore
# ambiguous, and the script refuses to guess: it resolves one only if exactly one
# document has a registered provision there. Silently reading the wrong document
# would be the worst failure available to a tool whose job is verification.
set -uo pipefail
cd "$(dirname "$0")/.."

OWASP="reference/owasp-top-10-agentic-applications-2026.md"
ACT="reference/eu-ai-act-2024-1689-excerpts.md"
REG="provisions.md"

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
dim()  { printf '\033[2m%s\033[0m\n' "$1"; }

for f in "$OWASP" "$ACT" "$REG"; do
  [ -f "$f" ] || { echo "missing $f (run from the repo root, and clone it fully)"; exit 2; }
done

path_for_src() { case "$1" in owasp) printf '%s' "$OWASP";; act) printf '%s' "$ACT";; *) return 1;; esac; }
label_for_src() { case "$1" in owasp) printf 'OWASP';; act) printf 'AI Act';; esac; }

# Register lookup. Columns: | `id` | source | line | text | purpose |
# Emits "src line" for an id.
lookup_id() {
  awk -F'|' -v want="$1" '
    /^\| `/ {
      id=$2; gsub(/[ \t`]/, "", id)
      if (id != want) next
      src=$3; gsub(/^[ \t]+|[ \t]+$/, "", src)
      ln=$4;  gsub(/[ \t]/, "", ln)
      print (src ~ /^OWASP/ ? "owasp" : "act"), ln
      exit
    }' "$REG"
}

# Which sources have a registered provision at this line? Emits zero or more names.
sources_at_line() {
  awk -F'|' -v want="$1" '
    /^\| `/ {
      src=$3; gsub(/^[ \t]+|[ \t]+$/, "", src)
      ln=$4;  gsub(/[ \t]/, "", ln)
      if (ln == want) print (src ~ /^OWASP/ ? "owasp" : "act")
    }' "$REG" | sort -u
}

id_at() {
  awk -F'|' -v ws="$1" -v wl="$2" '
    /^\| `/ {
      id=$2;  gsub(/[ \t`]/, "", id)
      src=$3; gsub(/^[ \t]+|[ \t]+$/, "", src)
      ln=$4;  gsub(/[ \t]/, "", ln)
      s = (src ~ /^OWASP/ ? "owasp" : "act")
      if (s == ws && ln == wl) { print id; exit }
    }' "$REG"
}

# Print a provision beginning at $2 in source $1. Stops at the next numbered item,
# heading or blank line, and never runs past 8 lines, so it does not spill into the
# following provision.
print_provision() {
  local src="$1" start="$2" id="${3:-}" file total
  file=$(path_for_src "$src") || { echo "  ! unknown source: $src"; return 1; }
  total=$(wc -l < "$file" | tr -d ' ')
  if ! [ "$start" -ge 1 ] 2>/dev/null || [ "$start" -gt "$total" ]; then
    printf '  ! line %s is outside %s (1..%s)\n' "$start" "$file" "$total"; return 1
  fi
  bold "── ${id:-line $start}   [$(label_for_src "$src")]   $file#L$start"
  # Where a provision ends. The text preserves the source PDF's hard wraps, so a
  # provision is a run of ~100-character lines. It ends at a blank line, the next
  # heading, or the next numbered item — except where the extraction lost the
  # paragraph break, which happens in the front matter. There a short line ending
  # in a full stop is the paragraph end, and is the only signal available.
  awk -v s="$start" 'NR>=s && NR<s+8 {
        if (NR>s && ($0 ~ /^#{1,6} / || $0 ~ /^[0-9]+\. / || $0 ~ /^$/)) exit
        printf "  %s\n", $0
        if ($0 ~ /[.!?][")\u201d]?[ \t]*$/ && length($0) < 90) exit
      }' "$file"
  dim "   (github.com: add ?plain=1 to the URL to see line numbers)"
  echo
}

resolve_bare_line() {
  local ln="$1" found n
  found=$(sources_at_line "$ln"); n=$(printf '%s' "$found" | grep -c . || true)
  if [ "$n" -eq 1 ]; then
    print_provision "$found" "$ln" "$(id_at "$found" "$ln")"
  elif [ "$n" -gt 1 ]; then
    printf '  ! line %s is registered in more than one document.\n' "$ln"
    dim "    name the source:  cite.sh owasp:$ln   |   cite.sh act:$ln"
    return 1
  else
    printf '  ! no registered provision at line %s.\n' "$ln"
    dim "    This repository holds two reference documents, so a bare line number"
    dim "    is ambiguous and is not guessed. Name the source explicitly:"
    dim "      bash scripts/cite.sh owasp:$ln"
    dim "      bash scripts/cite.sh act:$ln"
    return 1
  fi
}

# ---- --list (whole register) ----
if [ "${1:-}" = "--list" ] && [ $# -eq 1 ]; then
  bold "── register: $(grep -c '^| `' "$REG") provisions"
  awk -F'|' '/^\| `/ {
      id=$2;  gsub(/[ \t`]/,"",id)
      src=$3; gsub(/^[ \t]+|[ \t]+$/,"",src)
      ln=$4;  gsub(/[ \t]/,"",ln)
      p=$6;   gsub(/^[ \t]+|[ \t]+$/,"",p)
      printf "  %-28s %-7s L%-6s %s\n", id, src, ln, p
    }' "$REG"
  exit 0
fi

# ---- --from FILE ----
if [ "${1:-}" = "--from" ]; then
  src_file="${2:-}"
  [ -f "$src_file" ] || { echo "usage: bash scripts/cite.sh --from <file.md> [--list]"; exit 2; }
  listonly=0; [ "${3:-}" = "--list" ] && listonly=1

  refs=$(grep -oE '(owasp-top-10-agentic-applications-2026|eu-ai-act-2024-1689-excerpts)\.md(\?plain=1)?#L[0-9]+( "\^[A-Za-z0-9-]+")?' "$src_file" \
         | sed -E 's/^(owasp[^.]*|eu-ai-act[^.]*)\.md(\?plain=1)?#L([0-9]+)( "\^([A-Za-z0-9-]+)")?.*/\1 \3 \5/' \
         | sed -E 's/^owasp[^ ]*/owasp/; s/^eu-ai-act[^ ]*/act/' \
         | sort -u -k1,1 -k2,2n)
  [ -n "$refs" ] && [ "$(printf '%s' "$refs" | grep -c .)" -gt 0 ] || {
    echo "no citations to either reference document in $src_file"; exit 0; }

  bold "── $(printf '%s\n' "$refs" | grep -c .) distinct citations in $src_file"
  echo
  printf '%s\n' "$refs" | while read -r src ln id; do
    [ -n "$id" ] || id=$(id_at "$src" "$ln")
    if [ "$listonly" -eq 1 ]; then
      printf '  %-28s %-7s L%s\n' "${id:-(unregistered)}" "$(label_for_src "$src")" "$ln"
    else
      print_provision "$src" "$ln" "$id"
    fi
  done
  exit 0
fi

# ---- single argument ----
arg="${1:-}"
[ -n "$arg" ] || { sed -n '4,22p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }

case "$arg" in
  owasp:*) print_provision owasp "${arg#owasp:}" "$(id_at owasp "${arg#owasp:}")" ;;
  act:*)   print_provision act   "${arg#act:}"   "$(id_at act   "${arg#act:}")"   ;;
  *[!0-9]*)
    arg_up=$(printf '%s' "$arg" | tr '[:lower:]' '[:upper:]')
    read -r src ln <<EOF
$(lookup_id "$arg_up")
EOF
    if [ -z "${ln:-}" ]; then
      printf '  ! no provision with id %s\n\n' "$arg_up"
      dim "  known ids:  bash scripts/cite.sh --list"
      exit 1
    fi
    print_provision "$src" "$ln" "$arg_up"
    ;;
  *) resolve_bare_line "$arg" ;;
esac
