#!/usr/bin/env bash
# cite.sh: resolve a citation and print the provision it points at.
#
# Why this exists. An auditor's whole claim is that its findings can be checked
# against the standard. Without a tool, a citation is only a promise: the reader
# has to open a 1,695-line file, find a line number, and read around a hard wrap
# to see where the sentence ends. On github.com they cannot even do that, because
# rendered markdown has no line numbers. This script makes a citation redeemable
# from the terminal, in one command, with no editor and no browser.
#
#   bash scripts/cite.sh ASI04-PIN                 # by register id
#   bash scripts/cite.sh 589                       # by line
#   bash scripts/cite.sh owasp:589                 # by line, source named explicitly
#   bash scripts/cite.sh --from examples.md        # every citation in a document
#   bash scripts/cite.sh --from <file> --list      # just the list, no text
#   bash scripts/cite.sh --list                    # the whole register
#
# This repository holds ONE reference document, the OWASP standard, so a bare line
# number is unambiguous and is resolved directly. The explicit `owasp:` form is
# still accepted, and a line with no registered provision is printed anyway, with
# the register id omitted rather than invented.
set -uo pipefail
cd "$(dirname "$0")/.."

OWASP="reference/owasp-top-10-agentic-applications-2026.md"
REG="provisions.md"

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
dim()  { printf '\033[2m%s\033[0m\n' "$1"; }

for f in "$OWASP" "$REG"; do
  [ -f "$f" ] || { echo "missing $f (run from the repo root, and clone it fully)"; exit 2; }
done

path_for_src() { case "$1" in owasp) printf '%s' "$OWASP";; *) return 1;; esac; }
label_for_src() { case "$1" in owasp) printf 'OWASP';; esac; }

# Register lookup. Columns: | `id` | source | line | text | purpose |
# Emits "src line" for an id.
lookup_id() {
  awk -F'|' -v want="$1" '
    /^\| `/ {
      id=$2; gsub(/[ \t`]/, "", id)
      if (id != want) next
      ln=$4;  gsub(/[ \t]/, "", ln)
      print "owasp", ln
      exit
    }' "$REG"
}

id_at() {
  awk -F'|' -v ws="$1" -v wl="$2" '
    /^\| `/ {
      id=$2;  gsub(/[ \t`]/, "", id)
      src=$3; gsub(/^[ \t]+|[ \t]+$/, "", src)
      ln=$4;  gsub(/[ \t]/, "", ln)
      if (src ~ /^OWASP/ && ws == "owasp" && ln == wl) { print id; exit }
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
  # heading, or the next numbered item, except where the extraction lost the
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

# ---- --help ----
case "${1:-}" in
  --help|-h|help)
    sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'
    exit 0 ;;
esac

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

  refs=$(grep -oE 'owasp-top-10-agentic-applications-2026\.md(\?plain=1)?#L[0-9]+( "\^[A-Za-z0-9-]+")?' "$src_file" \
         | sed -E 's/^owasp[^.]*\.md(\?plain=1)?#L([0-9]+)( "\^([A-Za-z0-9-]+)")?.*/owasp \2 \4/' \
         | sort -u -k1,1 -k2,2n)
  [ -n "$refs" ] && [ "$(printf '%s' "$refs" | grep -c .)" -gt 0 ] || {
    echo "no citations to the standard in $src_file"; exit 0; }

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
[ -n "$arg" ] || { sed -n '4,21p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }

case "$arg" in
  owasp:*) print_provision owasp "${arg#owasp:}" "$(id_at owasp "${arg#owasp:}")" ;;
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
  *) print_provision owasp "$arg" "$(id_at owasp "$arg")" ;;
esac
