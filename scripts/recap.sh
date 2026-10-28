#!/usr/bin/env bash
# Print session recap from learner/journal/PROGRESS.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROGRESS="$ROOT/learner/journal/PROGRESS.md"

echo "═══════════════════════════════════════════"
echo "  Farnodes AI Lab — session recap"
echo "═══════════════════════════════════════════"
echo ""

if [[ ! -f "$PROGRESS" ]]; then
  echo "Missing $PROGRESS"
  echo "Start with OPEN.md and Day 1 in DAILY_30MIN.md"
  exit 1
fi

extract_field() {
  local label="$1"
  grep -F "**${label}**" "$PROGRESS" | head -1 | awk -F'|' '{gsub(/^ +| +$/,"",$3); print $3}'
}

last=$(extract_field "Last completed")
phase=$(extract_field "Phase")
next=$(extract_field "Next up")

echo "Last completed: $last"
echo "Phase:          $phase"
echo "Next:           $next"
echo ""
echo "--- Quick recall ---"
awk '/^### Quick recall/,/^### Today/{if ($0 !~ /^###/) print}' "$PROGRESS" | sed '/^$/d'
echo ""
echo "--- Today's one-liner ---"
awk '/^### Today/,/^---/{if ($0 !~ /^###/ && $0 !~ /^---/) print}' "$PROGRESS" | sed '/^$/d'
echo ""
echo "Chapters: docs/revision/  |  Tasks: docs/guides/DAILY_30MIN.md  |  Entry: OPEN.md"
