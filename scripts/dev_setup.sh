#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_PATH="${VENV_PATH:-$PROJECT_ROOT/.venv}"
REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-$PROJECT_ROOT/requirements.txt}"
ENV_FILE="$PROJECT_ROOT/.env"
ENV_EXAMPLE="$PROJECT_ROOT/.env.example"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "[!] Unable to find Python interpreter '$PYTHON_BIN'." >&2
  echo "    Provide an explicit path via PYTHON_BIN or install Python 3.11/3.12." >&2
  exit 1
fi

if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
  echo "[!] Requirements file not found at $REQUIREMENTS_FILE" >&2
  exit 1
fi

version_check="$($PYTHON_BIN -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')"
if [[ "$version_check" != 3.11 && "$version_check" != 3.12 ]]; then
  echo "[!] Python 3.11 or 3.12 is required. Current version: $version_check" >&2
  exit 1
fi

echo "[+] Using Python interpreter: $PYTHON_BIN ($version_check)"

echo "[+] Creating virtual environment at $VENV_PATH"
"$PYTHON_BIN" -m venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"

echo "[+] Upgrading pip/setuptools/wheel"
if ! pip install --upgrade pip setuptools wheel; then
  echo "[x] Failed to upgrade packaging tools. Check network connectivity or configure PIP_INDEX_URL." >&2
  exit 1
fi

echo "[+] Installing project requirements from $REQUIREMENTS_FILE"
if ! pip install -r "$REQUIREMENTS_FILE"; then
  echo "[x] Failed to install dependencies. Review the error above and resolve before re-running." >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" && -f "$ENV_EXAMPLE" ]]; then
  echo "[+] Creating .env from .env.example"
  cp "$ENV_EXAMPLE" "$ENV_FILE"
fi

export PYTHONPATH="$PROJECT_ROOT/src"

echo "[+] Bootstrapping database"
PYTHONPATH="$PYTHONPATH" python - <<'PYCODE'
import asyncio
from app.core.database import init_models

asyncio.run(init_models())
PYCODE

echo "[✓] Development environment ready"

echo "[i] Next steps:"
echo "    source $VENV_PATH/bin/activate"
echo "    export PYTHONPATH=$PROJECT_ROOT/src"
echo "    uvicorn src.main:app --reload"
