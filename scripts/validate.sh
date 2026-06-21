#!/usr/bin/env bash
set -euo pipefail

VENV_PY=".venv/bin/python"
if [[ ! -x "$VENV_PY" ]]; then
  echo "ERROR: .venv/bin/python not found. Create venv and install deps first."
  exit 1
fi

if ! "$VENV_PY" -m ruff --version >/dev/null 2>&1; then
  echo "Installing ruff in .venv ..."
  "$VENV_PY" -m pip install ruff==0.6.9
fi

OUT_DIR="temp/coverage"
mkdir -p "$OUT_DIR"

"$VENV_PY" -m ruff check src --config ruff.toml
"$VENV_PY" -m pytest \
  --cov=at \
  --cov-report=term-missing \
  --cov-report=html:"$OUT_DIR" \
  "$@"
