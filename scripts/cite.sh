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
#   bash scripts/cite.sh ASI04-PIN                 # by register id
#   bash scripts/cite.sh 589                       # by line number
#   bash scripts/cite.sh --from examples.md        # every citation in a document
#   bash scripts/cite.sh --from examples.md --list # just the list, no text
#   bash scripts/cite.sh --list                    # the whole register
#
# Provisions in this standard wrap across two or three lines, so a citation names
# where a provision BEGINS. This script prints from there to the end of the
# sentence or the start of the next numbered item, which is what a reader
# actually needs to see.
set -uo pipefail
cd "$(dirname "$0")/.."

REF="reference/owasp-top-10-agentic-applications-2026.md"
REG="provisions.md"

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
dim()  { printf '\033[2m%s\033[0m\n' "$1"; }

[ -f "$REF" ] || { echo "missing $REF (run from the repo, or clone it fully)"; exit 2; }
[ -f "$REG" ] || { echo "missing $REG (run: python3 scripts/build_register.py)"; exit 2; }

# id -> line, from the register table.
line_for_id() {
  awk -F'|' -v want="$1" '
    /^\| `/ {
      gsub(/[ \t]/, "", $2); gsub(/`/, "", $2)
      gsub(/[ \t]/, "", $3)
      if ($2 == want) { print $3; exit }
    }' "$REG"
}

id_for_line() {
  awk -F'|' -v want="$1" '
    /^\| `/ {
      gsub(/[ \t]/, "", $2); gsub(/`/, "", $2)
      gsub(/[ \t]/, "", $3)
      if ($3 == want) { print $2; exit }
    }' "$REG"
}

# Print a provision beginning at $1. Stops at the next numbered item, the next
# heading, or a blank line, whichever comes first, and never runs past 8 lines.
print_provision() {
  local start="$1" id="$2"
  local total; total=$(wc -l < "$REF" | tr -d ' ')
  [ "$start" -ge 1 ] 2>/dev/null && [ "$start" -le "$total" ] || {
    printf '  ! line %s is outside %s (1..%s)\n' "$start" "$REF" "$total"; return 1; }

  bold "── ${id:-line $start}   $REF#L$start"
  awk -v s="$start" 'NR>=s && NR<s+8 {
        if (NR>s && ($0 ~ /^### / || $0 ~ /^## / || $0 ~ /^[0-9]+\. / || $0 ~ /^$/)) exit
        printf "  %s\n", $0
      }' "$REF"
  dim "   (github.com: add ?plain=1 to the URL to see line numbers)"
  echo
}

# --list with no --from: dump the register.
if [ "${1:-}" = "--list" ] && [ $# -eq 1 ]; then
  bold "── register: $(grep -c '^| `' "$REG") provisions"
  awk -F'|' '/^\| `/ { gsub(/[ \t]/,"",$2); gsub(/`/,"",$2); gsub(/[ \t]/,"",$3);
                       sub(/^ +/,"",$5); sub(/ +$/,"",$5);
                       printf "  %-26s L%-6s %s\n", $2, $3, $5 }' "$REG"
  exit 0
fi

# --from FILE: resolve every citation in a document.
if [ "${1:-}" = "--from" ]; then
  src="${2:-}"; [ -f "$src" ] || { echo "usage: bash scripts/cite.sh --from <file.md> [--list]"; exit 2; }
  listonly=0; [ "${3:-}" = "--list" ] && listonly=1

  # Prefer the id in the link title; fall back to the line number.
  refs=$(grep -oE 'owasp-top-10-agentic-applications-2026\.md(\?plain=1)?#L[0-9]+( "\^[A-Za-z0-9-]+")?' "$src" \
         | sed -E 's/.*#L([0-9]+)( "\^([A-Za-z0-9-]+)")?/\1 \3/' | sort -u -k1,1n)
  [ -n "$refs" ] || { echo "no citations to the standard in $src"; exit 0; }

  count=$(printf '%s\n' "$refs" | grep -c .)
  bold "── $count distinct citations in $src"
  echo
  printf '%s\n' "$refs" | while read -r ln id; do
    [ -n "$id" ] || id=$(id_for_line "$ln")
    if [ "$listonly" -eq 1 ]; then
      printf '  %-26s L%s\n' "${id:-(unregistered)}" "$ln"
    else
      print_provision "$ln" "$id"
    fi
  done
  exit 0
fi

# Single argument: an id or a bare line number.
arg="${1:-}"
[ -n "$arg" ] || { sed -n '4,17p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }

if printf '%s' "$arg" | grep -qE '^[0-9]+$'; then
  print_provision "$arg" "$(id_for_line "$arg")"
else
  arg_up=$(printf '%s' "$arg" | tr '[:lower:]' '[:upper:]')
  ln=$(line_for_id "$arg_up")
  if [ -z "$ln" ]; then
    printf '  ! no provision with id %s\n\n' "$arg_up"
    dim "  known ids:"
    awk -F'|' '/^\| `/ { gsub(/[ \t]/,"",$2); gsub(/`/,"",$2); printf "    %s\n", $2 }' "$REG"
    exit 1
  fi
  print_provision "$ln" "$arg_up"
fi
