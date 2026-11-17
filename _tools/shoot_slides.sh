#!/usr/bin/env bash
# Screenshot slides at 1440x900 and build one contact sheet to check overflow.
# usage: _tools/shoot_slides.sh [slide numbers...]   (default: all)  -> prints the sheet path
# WSL + Windows Chrome; set CHROME to override.
set -euo pipefail
cd "$(dirname "$0")/.."
CH="${CHROME:-/mnt/c/Program Files/Google/Chrome/Application/chrome.exe}"
WT=$(cmd.exe /c 'echo %TEMP%' 2>/dev/null | tr -d '\r'); WD="$WT\\claude-slides"; LD=$(wslpath -u "$WD")
rm -rf "$LD"; mkdir -p "$LD/slides" "$LD/images"; cp -r images/official images/scenes "$LD/images/"
n=$(grep -c '<section class="slide' slides/index.html)
L=("$@"); [ ${#L[@]} -eq 0 ] && L=($(seq 1 "$n"))
win(){ echo "file:///$(echo "$1" | sed 's#\\#/#g')"; }
for i in "${L[@]}"; do
  sed "s#</style>#.slide{display:none!important}.slide:nth-of-type($i){display:flex!important}</style>#" slides/index.html > "$LD/slides/one$i.html"
  "$CH" --headless=new --user-data-dir="$WD\\prof" --no-first-run --hide-scrollbars --window-size=1440,900 \
    --virtual-time-budget=8000 --screenshot="$WD\\s$i.png" "$(win "$WD\\slides\\one$i.html")" >/dev/null 2>&1
done
rows=$(( (${#L[@]} + 3) / 4 ))
{ echo '<html><body style="margin:0;background:#000;display:grid;grid-template-columns:repeat(4,720px)">'
  for i in "${L[@]}"; do echo "<img src=\"s$i.png\" style=\"width:720px;height:450px\">"; done; echo '</body></html>'; } > "$LD/sheet.html"
"$CH" --headless=new --user-data-dir="$WD\\prof" --hide-scrollbars --window-size=2880,$((rows*450)) --screenshot="$WD\\sheet.png" "$(win "$WD\\sheet.html")" >/dev/null 2>&1
echo "$LD/sheet.png"
