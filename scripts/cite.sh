#!/usr/bin/env bash
# cite.sh: print the provision a citation points at. Run with --help for usage.
set -uo pipefail
CALLER="$PWD"
cd "$(dirname "$0")/.."

REF="reference/owasp-top-10-agentic-applications-2026.md"
REG="provisions.md"

usage() {
  cat <<'EOF'
bash scripts/cite.sh ASI04-PIN              one provision, by register id
bash scripts/cite.sh 589                    one provision, by line
bash scripts/cite.sh --from examples.md     every citation in a document
bash scripts/cite.sh --from <file> --list   the citations only, no text
bash scripts/cite.sh --list                 the whole register
EOF
}

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
dim()  { printf '\033[2m%s\033[0m\n' "$1"; }

for f in "$REF" "$REG"; do
  [ -f "$f" ] || { echo "missing $f (clone the repository fully)"; exit 2; }
done

# Register rows: | `id` | line | text | purpose |
line_for_id() {
  awk -F'|' -v want="$1" '/^\| `/ {
      id=$2; gsub(/[ \t`]/, "", id)
      if (id == want) { ln=$3; gsub(/[ \t]/, "", ln); print ln; exit }
    }' "$REG"
}

id_at() {
  awk -F'|' -v want="$1" '/^\| `/ {
      ln=$3; gsub(/[ \t]/, "", ln)
      if (ln == want) { id=$2; gsub(/[ \t`]/, "", id); print id; exit }
    }' "$REG"
}

# A provision runs from its line to the next blank line, heading or numbered item, at most eight
# lines. Where the extraction lost a paragraph break, a short line ending in a full stop ends it.
print_provision() {
  local start="$1" id="${2:-}" total
  total=$(wc -l < "$REF" | tr -d ' ')
  if ! [ "$start" -ge 1 ] 2>/dev/null || [ "$start" -gt "$total" ]; then
    printf '  ! line %s is outside %s (1..%s)\n' "$start" "$REF" "$total"; return 1
  fi
  bold "── ${id:-line $start}   $REF#L$start"
  awk -v s="$start" 'NR>=s && NR<s+8 {
        if (NR>s && ($0 ~ /^#{1,6} / || $0 ~ /^[0-9]+\. / || $0 ~ /^$/)) exit
        printf "  %s\n", $0
        if ($0 ~ /[.!?][")”]?[ \t]*$/ && length($0) < 90) exit
      }' "$REF"
  dim "   (github.com: add ?plain=1 to the URL to see line numbers)"
  echo
}

case "${1:-}" in
  --help|-h|help) usage; exit 0 ;;
  "") usage; exit 2 ;;
esac

if [ "$1" = "--list" ] && [ $# -eq 1 ]; then
  bold "── register: $(grep -c '^| `' "$REG") provisions"
  awk -F'|' '/^\| `/ {
      id=$2; gsub(/[ \t`]/, "", id)
      ln=$3; gsub(/[ \t]/, "", ln)
      p=$5;  gsub(/^[ \t]+|[ \t]+$/, "", p)
      printf "  %-28s L%-6s %s\n", id, ln, p
    }' "$REG"
  exit 0
fi

if [ "$1" = "--from" ]; then
  src_file="${2:-}"
  case "$src_file" in
    /*|"") ;;
    *) [ -f "$src_file" ] || src_file="$CALLER/$src_file" ;;
  esac
  [ -f "$src_file" ] || { echo "usage: bash scripts/cite.sh --from <file.md> [--list]"; exit 2; }
  listonly=0; [ "${3:-}" = "--list" ] && listonly=1

  refs=$(grep -oE 'owasp-top-10-agentic-applications-2026\.md(\?plain=1)?#L[0-9]+( "\^[A-Za-z0-9-]+")?' "$src_file" \
         | sed -E 's/^[^#]*#L([0-9]+)( "\^([A-Za-z0-9-]+)")?.*/\1 \3/' \
         | sort -u -k1,1n)
  [ -n "$refs" ] || { echo "no citations to the standard in $src_file"; exit 0; }

  bold "── $(printf '%s\n' "$refs" | grep -c .) distinct citations in $src_file"
  echo
  printf '%s\n' "$refs" | while read -r ln id; do
    [ -n "${id:-}" ] || id=$(id_at "$ln")
    if [ "$listonly" -eq 1 ]; then
      printf '  %-28s L%s\n' "${id:-(unregistered)}" "$ln"
    else
      print_provision "$ln" "$id"
    fi
  done
  exit 0
fi

arg="$1"
case "$arg" in
  *[!0-9]*)
    arg_up=$(printf '%s' "$arg" | tr '[:lower:]' '[:upper:]')
    ln=$(line_for_id "$arg_up")
    if [ -z "$ln" ]; then
      printf '  ! no provision with id %s\n\n' "$arg_up"
      dim "  known ids:  bash scripts/cite.sh --list"
      exit 1
    fi
    print_provision "$ln" "$arg_up"
    ;;
  *) print_provision "$arg" "$(id_at "$arg")" ;;
esac
