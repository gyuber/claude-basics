#!/usr/bin/env bash
# Render the mock scenes and save PNGs to images/scenes/.
# usage: _tools/scenes/shoot.sh   (WSL with Windows Chrome; set CHROME to override)
set -euo pipefail
cd "$(dirname "$0")/../.."
CH="${CHROME:-/mnt/c/Program Files/Google/Chrome/Application/chrome.exe}"
WT=$(cmd.exe /c 'echo %TEMP%' 2>/dev/null | tr -d '\r'); WD="$WT\\claude-scenes"; LD=$(wslpath -u "$WD")
rm -rf "$LD"; mkdir -p "$LD" images/scenes
python3 -I _tools/scenes/make_scenes.py "$LD" >/dev/null
for f in "$LD"/*.html; do
  n=$(basename "$f" .html)
  "$CH" --headless=new --user-data-dir="$WD\\prof" --no-first-run --hide-scrollbars --window-size=1280,760 \
    --virtual-time-budget=3000 --screenshot="$WD\\$n.png" "file:///$(echo "$WD\\$n.html" | sed 's#\\#/#g')" >/dev/null 2>&1
  cp "$LD/$n.png" "images/scenes/$n.png"; echo "images/scenes/$n.png"
done
