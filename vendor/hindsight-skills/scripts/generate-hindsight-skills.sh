#!/usr/bin/env bash
# Generate SKILL.md files from .tmpl templates by replacing {{PREAMBLE}} and {{VERSION}} placeholders.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PREAMBLE_FILE="$REPO_ROOT/skills/shared/preamble.md"
SKILLS_DIR="$REPO_ROOT/skills"
VERSION_FILE="$REPO_ROOT/VERSION"

if [ ! -f "$PREAMBLE_FILE" ]; then
  echo "Error: preamble not found at $PREAMBLE_FILE" >&2
  exit 1
fi

if [ ! -f "$VERSION_FILE" ]; then
  echo "Error: VERSION not found at $VERSION_FILE" >&2
  exit 1
fi

VERSION=$(tr -d '[:space:]' < "$VERSION_FILE")

# ─── Copy VERSION and CHANGELOG into hindsight-upgrade skill ─
UPGRADE_DIR="$SKILLS_DIR/hindsight-upgrade"
if [ -d "$UPGRADE_DIR" ]; then
  cp "$VERSION_FILE" "$UPGRADE_DIR/VERSION"
  [ -f "$REPO_ROOT/CHANGELOG.md" ] && cp "$REPO_ROOT/CHANGELOG.md" "$UPGRADE_DIR/CHANGELOG.md"
  echo "Copied VERSION and CHANGELOG.md into $UPGRADE_DIR"
fi

# ─── Generate SKILL.md from templates ─────────────────────────

count=0

for tmpl in "$SKILLS_DIR"/*/SKILL.md.tmpl; do
  [ -f "$tmpl" ] || continue
  skill_dir=$(dirname "$tmpl")
  output="$skill_dir/SKILL.md"

  # Split template at {{PREAMBLE}} and concatenate with preamble content
  # Get line number of the placeholder
  placeholder_line=$(grep -n '{{PREAMBLE}}' "$tmpl" | head -1 | cut -d: -f1 || true)

  if [ -z "$placeholder_line" ]; then
    # No placeholder, just copy
    cp "$tmpl" "$output"
  else
    # Lines before placeholder + preamble content + lines after placeholder
    head -n $((placeholder_line - 1)) "$tmpl" > "$output"
    cat "$PREAMBLE_FILE" >> "$output"
    tail -n +$((placeholder_line + 1)) "$tmpl" >> "$output"
  fi

  # Replace {{VERSION}} with actual version
  if grep -q '{{VERSION}}' "$output"; then
    sed "s/{{VERSION}}/$VERSION/g" "$output" > "$output.tmp"
    mv "$output.tmp" "$output"
  fi

  echo "Generated: $output"
  count=$((count + 1))
done

echo "Done. Generated $count skill(s)."
