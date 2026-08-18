#!/usr/bin/env bash
#
# Extract new/changed translatable strings into the .ts files, merging with
# whatever translations they already have (existing <translation> entries
# are preserved; strings no longer found in the source are marked obsolete,
# never deleted).
#
# Wraps pyside6-lupdate with the flags this project actually needs - see
# CONTRIBUTING.md ("Maintaining translations") for why each one matters:
#   -tr-function-alias translate+=_translate
#       required, or every `_translate(...)` call (this project's alias for
#       QCoreApplication.translate) is silently skipped.
#   every .py file under pycirkuit/, found explicitly (never a bare
#   directory - that only picks up .ui-embedded strings, silently skipping
#   every hand-written .py file), except resources_rc.py, which reliably
#   segfaults pyside6-lupdate if it's ever handed to it.
#
# Usage:
#   dev-scripts/extract-translations.sh                # updates both .ts files below
#   dev-scripts/extract-translations.sh some.ts other.ts  # updates these instead

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
LUPDATE="$REPO_ROOT/.venv/bin/pyside6-lupdate"

if [[ ! -x "$LUPDATE" ]]; then
    echo "error: pyside6-lupdate not found in $REPO_ROOT/.venv - see CONTRIBUTING.md to set up the venv" >&2
    exit 1
fi

if [[ $# -gt 0 ]]; then
    ts_files=("$@")
else
    ts_files=("$REPO_ROOT/pycirkuit/L10n/pycirkuit.ca.ts" "$REPO_ROOT/pycirkuit/L10n/pycirkuit_empty.ts")
fi

py_files=()
while IFS= read -r -d '' f; do
    py_files+=("$f")
done < <(find "$REPO_ROOT/pycirkuit" -name '*.py' -not -name 'resources_rc.py' -print0)

"$LUPDATE" -tr-function-alias translate+=_translate \
    "${py_files[@]}" -ts "${ts_files[@]}"
