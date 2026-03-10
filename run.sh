#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .venv ]; then
  . .venv/bin/activate
fi

if command -v python >/dev/null 2>&1; then
  python src/bot.py "$@"
else
  python3 src/bot.py "$@"
fi
