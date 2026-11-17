"""Insert a blank line before markdown tables (GitHub Pages/kramdown needs it).
usage: python3 _tools/fix_md_tables.py   (run from repo root)"""
import glob
files=glob.glob('기초/*.md')+glob.glob('작업방식/**/*.md',recursive=True)+['README.md']
for f in files:
    lines=open(f).read().split('\n'); out=[]; fence=False
    for l in lines:
        if l.startswith('```'): fence=not fence
        if not fence and l.startswith('|') and out and out[-1].strip() and not out[-1].startswith('|'):
            out.append('')
        out.append(l)
    open(f,'w').write('\n'.join(out))
