"""Build the chalkboard deck.
usage: python3 slides/_src/build.py [out_dir]
reads template.html + sections.html next to this file,
writes slides/index.html (for GitHub Pages) and, if out_dir is given,
out_dir/artifact.html (claude.ai artifact, images under images/)."""
import sys,os,re
src=os.path.dirname(os.path.abspath(__file__))
repo_slides=os.path.dirname(src)
art_dir=sys.argv[1] if len(sys.argv)>1 else None
d=src
t=open(os.path.join(d,'template.html')).read().split('\n')
sec=open(os.path.join(d,'sections.html')).read()
sec=sec.replace('<p class="note"><span class="mk st">description 이 제일 중요, 이걸 보고 꺼낼지 정해요</span></p>','<p class="note">description 이 제일 중요, Claude 가 이걸 보고 꺼낼지 정해요</p>')
css="""  /* official screenshots inside a chalk box */
  .shot img { display: block; width: 100%; height: auto; border-radius: 8px; margin-top: 4px; }
  .shot .cap { margin-top: 10px; font-size: 18px; color: var(--ink-3); }
  .shot.big { max-width: 780px; width: 100%; align-self: center; }
  /* example dialog: my lines on the left in white chalk, Claude's on the right in pink */
  .chat { display: grid; gap: 16px; }
  .chat > div { padding: 14px 26px 16px; max-width: 80%; font-size: 24px; line-height: 1.55; }
  .chat .me { justify-self: start; }
  .chat .ai { justify-self: end; color: var(--ink-2); }
  .chat .who { display: block; font-family: var(--hand); font-weight: 700; font-size: 24px; margin-bottom: 2px; }
  .chat .me .who { color: var(--yellow); }
  .chat .ai .who { color: var(--pink); }
  .chat .dim { color: var(--ink-3); font-size: 21px; }
  .chat code { font-family: var(--font); font-weight: 700; color: var(--blue); }
  .tbl tbody th { white-space: normal; }
  @media (max-width: 800px) { .chat > div { max-width: 100%; } }
</style>"""
head='\n'.join(t[:212]).replace('<title>dotfile 칠판 스케치</title>','<title>Claude Code 칠판 강의</title>').replace('</style>',css,1)
tail='\n'.join(t[618:])
hook="""    document.querySelectorAll('.chat > .me').forEach(el => box(el, { stroke: c.ink, strokeWidth: 2.4 }));
    document.querySelectorAll('.chat > .ai').forEach(el => box(el, { stroke: c.pink, strokeWidth: 2.8, fill: tint.pink, fillStyle: 'solid' }));
    diagram();"""
assert '    diagram();' in tail
tail=tail.replace('    diagram();',hook,1)
cloud = """  const SCRIB = {
    // sync: a cloud with an up arrow and a down arrow
    cloud(r, s, cx, cy, S) {
      const X = k => cx + S * k, Y = k => cy + S * k;
      s.appendChild(r.curve([[X(-0.5), Y(0.05)], [X(-0.52), Y(-0.15)], [X(-0.32), Y(-0.22)], [X(-0.22), Y(-0.42)], [X(0.02), Y(-0.48)], [X(0.2), Y(-0.36)], [X(0.38), Y(-0.36)], [X(0.52), Y(-0.16)], [X(0.48), Y(0.05)]], ln()));
      s.appendChild(r.line(X(-0.5), Y(0.05), X(0.48), Y(0.05), ln()));
      s.appendChild(r.line(X(-0.16), Y(0.42), X(-0.16), Y(0.12), ln({ stroke: P().yellow, strokeWidth: 2.4 })));
      s.appendChild(r.linearPath([[X(-0.26), Y(0.22)], [X(-0.16), Y(0.12)], [X(-0.06), Y(0.22)]], ln({ stroke: P().yellow, strokeWidth: 2.4 })));
      s.appendChild(r.line(X(0.16), Y(0.12), X(0.16), Y(0.42), ln({ strokeWidth: 2.2 })));
      s.appendChild(r.linearPath([[X(0.06), Y(0.32)], [X(0.16), Y(0.42)], [X(0.26), Y(0.32)]], ln({ strokeWidth: 2.2 })));
    },"""
assert '  const SCRIB = {' in tail
tail=tail.replace('  const SCRIB = {',cloud,1)
# renumber
n=[1]
def num(m):
    n[0]+=1; return f'<span>{n[0]:02d}</span></div>\n</section>'
sec=re.sub(r'<span>\d\d</span></div>\n</section>',num,sec)
for name,img,scn in [('index.html','../images/official','../images/scenes'),('artifact.html','images','scenes')]:
    full=head+'\n'+sec.replace('IMG',img).replace('SCN',scn)+'\n'+tail
    if name=='artifact.html':
        for pat in [r'<!doctype html>\s*',r'<html[^>]*>\s*',r'<head>\s*',r'<meta charset="utf-8">\s*',r'<meta name="viewport"[^>]*>\s*',r'</head>\s*',r'<body>\s*',r'</body>\s*',r'</html>\s*']:
            full=re.sub(pat,'',full,count=1,flags=re.I)
    if name=='index.html':
        open(os.path.join(repo_slides,'index.html'),'w').write(full)
    elif art_dir:
        open(os.path.join(art_dir,'artifact.html'),'w').write(full)
print('slides',n[0])
