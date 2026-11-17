#!/usr/bin/env bash
# After a push: wait for the Pages build, then compare table counts (markdown vs rendered HTML).
cd "$(dirname "$0")/.."
head=$(git rev-parse --short=7 HEAD)
for i in $(seq 1 40); do st=$(gh api repos/gyuber/claude-basics/pages/builds/latest --jq '"\(.status) \(.commit[0:7])"' 2>/dev/null); [ "$st" = "built $head" ] && break; sleep 8; done; echo "pages: $st"; sleep 15
for f in 기초/*.md 작업방식/*.md README.md; do
  u=$(python3 -c "import urllib.parse,sys;p=sys.argv[1];p=p[:-3]+'.html' if not p.endswith('README.md') else p.replace('README.md','');print(urllib.parse.quote(p))" "$f")
  html=$(curl -s "https://gyuber.github.io/claude-basics/$u?v=$RANDOM")
  a=$(grep -cE '^\|[ :]*-{3}' "$f"); b=$(echo "$html" | grep -o '<table' | wc -l); [ "$a" != "$b" ] && echo "TABLE MISMATCH $f md=$a html=$b"
done
echo "slides: $(curl -s "https://gyuber.github.io/claude-basics/slides/?v=$RANDOM" | grep -c '<section class="slide')"
