#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

pyinstaller \
  --onefile \
  --name gmail-calendar-slack-bot \
  src/bot.py

echo "Binary created at: dist/gmail-calendar-slack-bot"
