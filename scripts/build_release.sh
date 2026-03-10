#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python -m build
./scripts/build_binary.sh

echo "Release artifacts are in dist/"
