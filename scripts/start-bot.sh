#!/bin/bash
set -e
read -p "Do you want to connect your account? (yes/no): " choice

if [[ "$choice" == "yes" || "$choice" == "y" ]]; then
    echo "Running login_once.py..."
    python src/login_once.py
else
    echo "Skipping userbot setup."
fi

echo "Starting main bot..."
exec python src/main.py