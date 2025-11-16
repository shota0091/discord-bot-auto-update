#!/bin/bash
set -e

cd /home/shota/bots/discode_OdaiBot

echo "=== Pulling latest code ==="
git reset --hard
git pull origin main

echo "=== Updating venv packages (if needed) ==="
source venv/bin/activate

# requirements.txt が変わっていたら更新
pip install -r requirements.txt || true

echo "=== Restarting systemd service ==="
sudo systemctl restart odaibot

echo "=== Done ==="
