#!/bin/bash
set -e

echo "=== Creating virtual environment ==="
python3 -m venv .venv

echo "=== Activating virtual environment ==="
source .venv/bin/activate

echo "=== Installing dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Creating data directory ==="
mkdir -p data

echo "Setup completed successfully!"
echo ""
echo "👉 To start the bot, activate your virtual environment first:"
echo "   source .venv/bin/activate"
echo "Then run:"
echo "   ./start-bot.sh"
