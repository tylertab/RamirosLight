#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_PATH="${VENV_PATH:-$PROJECT_ROOT/.venv}"
REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-$PROJECT_ROOT/requirements.txt}"
ENV_FILE="$PROJECT_ROOT/.env"
ENV_EXAMPLE="$PROJECT_ROOT/.env.example"

version_check="$($PYTHON_BIN -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')"
if [[ "$version_check" != 3.11 && "$version_check" != 3.12 ]]; then
  echo "[!] Python 3.11 or 3.12 is required. Current version: $version_check" >&2
  exit 1
fi

echo "[+] Using Python interpreter: $PYTHON_BIN ($version_check)"

echo "[+] Creating virtual environment at $VENV_PATH"
"$PYTHON_BIN" -m venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"

pip install --upgrade pip setuptools wheel
pip install -r "$REQUIREMENTS_FILE"

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
