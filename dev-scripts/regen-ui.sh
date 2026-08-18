#!/usr/bin/env bash
#
# Regenerate Ui_*.py from a .ui file (or every .ui file in pycirkuit/ui/ if
# none is given), fixing the "import resources_rc" line pyside6-uic doesn't
# qualify on its own (no flag produces it - see CONTRIBUTING.md), then
# formatting the result with black.
#
# Usage:
#   dev-scripts/regen-ui.sh                 # regenerate every .ui file
#   dev-scripts/regen-ui.sh mainwindow.ui    # just this one

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
UIC="$REPO_ROOT/.venv/bin/pyside6-uic"
BLACK="$REPO_ROOT/.venv/bin/black"

if [[ ! -x "$UIC" || ! -x "$BLACK" ]]; then
    echo "error: pyside6-uic/black not found in $REPO_ROOT/.venv - see CONTRIBUTING.md to set up the venv" >&2
    exit 1
fi

if [[ $# -gt 0 ]]; then
    ui_files=("$@")
else
    mapfile -t ui_files < <(find "$REPO_ROOT/pycirkuit/ui" -maxdepth 1 -name '*.ui' | sort)
fi

for ui_file in "${ui_files[@]}"; do
    dir="$(dirname "$ui_file")"
    base="$(basename "$ui_file" .ui)"
    out="$dir/Ui_${base}.py"

    echo "Regenerating $out from $ui_file"
    "$UIC" "$ui_file" -o "$out"
    sed -i 's/^import resources_rc$/from pycirkuit.resources import resources_rc/' "$out"
    "$BLACK" -q "$out"
done
