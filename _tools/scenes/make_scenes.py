"""Render illustrative "Code tab" mock screens for the lessons.

These are teaching illustrations (재현 그림), not real screenshots: every image
carries a "재현 그림" tag. Output: one HTML file per scene in <out_dir>; screenshot
them with _tools/scenes/shoot.sh.

usage: python3 _tools/scenes/make_scenes.py <out_dir>
"""
import html
import os
import sys

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { width: 1280px; height: 760px; font-family: "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
  background: #E9E6DD; color: #2B2A27; font-size: 15px; }
.win { position: absolute; inset: 18px; border-radius: 12px; overflow: hidden; background: #FAF9F5;
  box-shadow: 0 10px 30px rgba(40,35,25,.18); display: grid; grid-template-columns: 250px 1fr; }
.win.full { grid-template-columns: 1fr; }
.side { background: #F0EEE6; border-right: 1px solid #E2DED2; padding: 14px 12px; display: flex; flex-direction: column; gap: 6px; }
.dots { display: flex; gap: 7px; margin-bottom: 10px; }
.dots i { width: 11px; height: 11px; border-radius: 50%; background: #D9D5C9; }
.icons { display: flex; gap: 12px; align-items: center; color: #77736A; font-size: 15px; margin-bottom: 12px; }
.icons .mode { margin-left: auto; display: flex; gap: 2px; background: #E6E3D9; border-radius: 8px; padding: 2px; font-weight: 400; }
.icons .mode i { font-style: normal; padding: 3px 9px; border-radius: 6px; font-size: 13px; }
.icons .mode i.on { background: #FFFFFF; color: #2B2A27; font-weight: 700; }
.menu { font-size: 14px; padding: 7px 10px; border-radius: 8px; color: #3D3A34; }
.menu.on { background: #E6E3D9; }
.acct { margin-top: auto; font-size: 13px; color: #6B675E; border-top: 1px solid #E2DED2; padding-top: 10px; }
.ph-row { display: flex; gap: 12px; align-items: center; }
.plus { color: #6B675E; font-size: 18px; }
.tabs { display: flex; gap: 4px; background: #E6E3D9; border-radius: 8px; padding: 3px; margin-bottom: 8px; }
.tabs span { flex: 1; text-align: center; font-size: 13px; padding: 5px 0; border-radius: 6px; color: #77736A; }
.tabs span.on { background: #FFFFFF; color: #2B2A27; font-weight: 700; box-shadow: 0 1px 2px rgba(0,0,0,.08); }
.new { font-size: 14px; padding: 8px 10px; border-radius: 8px; color: #3D3A34; }
.sec { font-size: 12px; color: #9A958A; margin: 10px 4px 2px; }
.sess { font-size: 14px; padding: 9px 10px; border-radius: 8px; color: #3D3A34; display: flex; justify-content: space-between; align-items: center; gap: 6px; }
.sess.on { background: #FFFFFF; box-shadow: 0 1px 2px rgba(0,0,0,.06); font-weight: 700; }
.badge { font-size: 11px; padding: 2px 7px; border-radius: 10px; white-space: nowrap; }
.badge.run { background: #FCE9DF; color: #B4532E; }
.badge.done { background: #E3F1E4; color: #2F7A3A; }
.badge.wait { background: #FFF3CC; color: #8A6A00; }
.tree { margin-top: 6px; font-size: 13px; color: #55524A; line-height: 1.75; font-family: Consolas, monospace; }
.tree b { color: #B4532E; }
.main { display: flex; flex-direction: column; min-width: 0; }
.top { height: 44px; border-bottom: 1px solid #ECE9E0; display: flex; align-items: center; padding: 0 22px; font-size: 14px; color: #6B675E; gap: 10px; }
.top b { color: #2B2A27; }
.msgs { flex: 1; padding: 20px 34px; display: flex; flex-direction: column; gap: 14px; overflow: hidden; }
.me { align-self: flex-end; max-width: 72%; background: #EFEBE1; border-radius: 14px; padding: 11px 16px; line-height: 1.6; }
.ai { max-width: 86%; line-height: 1.7; }
.ai .who, .me .who { font-size: 12px; color: #9A958A; display: block; margin-bottom: 2px; }
.chip { display: inline-block; font-family: Consolas, monospace; font-size: 13px; background: #FFFFFF; border: 1px solid #DDD8CB; border-radius: 6px; padding: 0 6px; color: #B4532E; }
.tool { font-family: Consolas, monospace; font-size: 13px; color: #6B675E; background: #F3F1EA; border-radius: 8px; padding: 7px 12px; }
.tool b { color: #2F7A3A; }
.file { display: inline-flex; gap: 8px; align-items: center; border: 1px solid #DDD8CB; background: #FFFFFF; border-radius: 10px; padding: 8px 12px; font-size: 14px; }
.file i { font-style: normal; font-size: 18px; }
.card { border: 1px solid #E0DBCE; background: #FFFFFF; border-radius: 12px; padding: 14px 16px; }
.card h4 { font-size: 14px; margin-bottom: 8px; }
.perm { border: 2px solid #E8A87C; background: #FFF8F2; border-radius: 12px; padding: 14px 16px; }
.perm .cmd { font-family: Consolas, monospace; background: #FFFFFF; border: 1px solid #EAD7C6; border-radius: 6px; padding: 6px 10px; margin: 8px 0 10px; }
.btns { display: flex; gap: 8px; }
.btn { font-size: 13px; padding: 6px 14px; border-radius: 8px; border: 1px solid #D5D0C3; background: #FFFFFF; }
.btn.ok { background: #2B2A27; color: #FFFFFF; border-color: #2B2A27; }
table { border-collapse: collapse; font-size: 13.5px; width: 100%; }
th, td { border: 1px solid #E4E0D5; padding: 6px 10px; text-align: left; }
th { background: #F3F1EA; }
td.n { text-align: right; font-family: Consolas, monospace; }
.warn { color: #B4532E; font-weight: 700; }
.input { margin: 0 26px 6px; border: 1px solid #DDD8CB; background: #FFFFFF; border-radius: 14px; padding: 12px 16px 8px; }
.input .ph { color: #2B2A27; min-height: 22px; }
.input .ph.empty { color: #A9A497; }
.bar { display: flex; gap: 14px; margin: 0 40px 10px; font-size: 13px; color: #55524A; align-items: center; }
.bar span { padding: 2px 4px; }
.bar .chk { color: #8A867B; }
.bar .model { margin-left: auto; }
.pop { position: absolute; background: #FFFFFF; border: 1px solid #DDD8CB; border-radius: 10px; box-shadow: 0 8px 24px rgba(0,0,0,.14); padding: 6px; font-size: 14px; min-width: 300px; }
.pop div { padding: 7px 10px; border-radius: 6px; display: flex; justify-content: space-between; gap: 16px; }
.pop div.on { background: #F3F1EA; }
.pop small { color: #9A958A; }
.toast { position: absolute; right: 30px; bottom: 30px; width: 330px; background: #2B2A27; color: #FAF9F5; border-radius: 12px; padding: 12px 16px; font-size: 14px; line-height: 1.5; box-shadow: 0 10px 24px rgba(0,0,0,.25); }
.toast small { color: #C9C4B8; display: block; }
.call { position: absolute; background: #D97757; color: #FFFFFF; font-weight: 700; font-size: 14px; border-radius: 14px; padding: 4px 11px; box-shadow: 0 2px 6px rgba(0,0,0,.2); }
.tag { position: absolute; right: 28px; top: 26px; font-size: 12px; color: #FFFFFF; background: rgba(43,42,39,.55); border-radius: 6px; padding: 3px 8px; z-index: 5; }
.doc { background: #FFFFFF; border: 1px solid #E0DBCE; border-radius: 10px; padding: 16px 20px; line-height: 1.8; font-size: 14.5px; }
.doc mark { background: #FCE2D6; }
.doc .ok { background: #E3F1E4; }
.split { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.code { font-family: Consolas, monospace; font-size: 13.5px; white-space: pre; line-height: 1.65; background: #FFFFFF; border: 1px solid #E0DBCE; border-radius: 10px; padding: 12px 16px; }
.code .add { background: #E3F1E4; display: block; }
"""


def esc(s):
    return html.escape(s, quote=False)


def side(sessions, active=0, tree=None, groups=None):
    """Sidebar like the real app: icon row, Korean menu, sessions grouped under a folder heading."""
    out = ['<div class="side"><div class="icons"><span>☰</span><span>▢</span><span>‹</span><span>›</span>'
           '<b class="mode"><i>💬</i><i class="on">&lt;/&gt;</i></b></div>',
           '<div class="menu on">＋ 새로 만들기</div><div class="menu">⌕ 검색</div>'
           '<div class="menu">⧉ 아티팩트</div><div class="menu">▭ 사용자 지정</div><div class="menu">··· 더 보기</div>']
    if groups is None:
        groups = [('사건폴더', sessions, active)]
    for title, sess, act in groups:
        out.append(f'<div class="sec">{title} ⌄</div>')
        for i, item in enumerate(sess):
            name, badge = (item if isinstance(item, tuple) else (item, None))
            b = ''
            if badge:
                cls, txt = badge
                b = f'<span class="badge {cls}">{txt}</span>'
            out.append(f'<div class="sess{" on" if i == act else ""}"><span>{name}</span>{b}</div>')
    if tree:
        out.append('<div class="sec">폴더 내용</div><div class="tree">' + tree + '</div>')
    out.append('<div class="acct">한 · 사용자 · Pro</div></div>')
    return ''.join(out)


def bar(mode='자동', folder='사건폴더', text='', empty=True, env='로컬'):
    """Prompt box and the row under it: environment, folder, worktree / model, effort, permission mode."""
    ph = f'<div class="ph{" empty" if empty else ""}">{text or "작업을 설명하거나 질문하세요"}</div>'
    return (f'<div class="input"><div class="ph-row"><span class="plus">＋</span>{ph}</div></div>'
            f'<div class="bar"><span>⌨ {env} ⌄</span><span>📁 {folder} ⌄</span><span class="chk">☐ 워크트리</span>'
            f'<span class="model">기본 모델 · 중간</span><span>{mode}</span></div>')


def me(t):
    return f'<div class="me"><span class="who">나</span>{t}</div>'


def ai(t):
    return f'<div class="ai"><span class="who">Claude</span>{t}</div>'


def page(body, extra=''):
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="tag">재현 그림 · 실제 화면과 다를 수 있어요</div>{body}{extra}</body></html>')


TREE = ('📁 자료<br>&nbsp;&nbsp;판결문.pdf<br>&nbsp;&nbsp;계약서_v1.docx<br>&nbsp;&nbsp;계약서_v2.docx<br>'
        '&nbsp;&nbsp;거래내역.xlsx<br>📁 결과물<br>📄 CLAUDE.md')

S = {}

# 00: one sentence -> a file appears
S['00-code-tab'] = page(
    '<div class="win">' + side(['송금내역 정리', '판결문 요약'], 0,
                               TREE + '<br>&nbsp;&nbsp;<b>송금내역정리.xlsx ← 새로 생김</b>') +
    '<div class="main"><div class="top"><b>송금내역 정리</b> · 사건폴더</div><div class="msgs">' +
    me('<span class="chip">@자료/거래내역.xlsx</span> 에서 피고 B에게 보낸 돈만 날짜순으로 정리해서 '
       '<span class="chip">결과물/</span>에 엑셀로 저장해줘') +
    '<div class="tool">✓ 읽음 자료/거래내역.xlsx (거래 312건)</div>' +
    '<div class="tool">✓ <b>만듦</b> 결과물/송금내역정리.xlsx</div>' +
    ai('피고 B 명의 계좌로 송금된 거래 <b>17건, 합계 48,300,000원</b>을 날짜순으로 정리했어요. '
       '같은 날 여러 번 나눠 보낸 거래 3건은 따로 표시해 뒀어요.<br>'
       '<span class="file"><i>📊</i>결과물/송금내역정리.xlsx</span>') +
    '</div>' + bar() + '</div></div>')

# 01: first conversation
S['01-first-chat'] = page(
    '<div class="win">' + side(['기록 살펴보기'], 0, TREE) +
    '<div class="main"><div class="top"><b>기록 살펴보기</b> · 사건폴더</div><div class="msgs">' +
    me('이 폴더에 뭐가 있는지 알려줘') +
    ai('이 폴더에는 이런 파일이 있어요.<br>'
       '• <span class="chip">자료/판결문.pdf</span> 1심 판결문 (23쪽)<br>'
       '• <span class="chip">자료/계약서_v1.docx</span>, <span class="chip">계약서_v2.docx</span> 같은 계약서의 두 버전<br>'
       '• <span class="chip">자료/거래내역.xlsx</span> 계좌 거래내역 312건<br>'
       '• <span class="chip">결과물/</span> 비어 있음<br><br>'
       '계약서 두 버전에서 바뀐 조항을 먼저 비교해 드릴까요?') +
    me('응, 바뀐 조항만 표로 보여줘') +
    '</div>' + bar() + '</div></div>')

# 02: bottom bar with callouts and @ picker
S['02-screen'] = page(
    '<div class="win">' + side(['판결문 요약'], 0, TREE) +
    '<div class="main"><div class="top"><b>판결문 요약</b> · 사건폴더</div><div class="msgs">' +
    ai('판결문을 읽었어요. 어떤 형식으로 요약할까요?') +
    '</div>' + bar(text='<span class="chip">@판</span>', empty=False) + '</div></div>',
    '<div class="pop" style="left:300px;top:505px"><div class="on"><span>📄 자료/판결문.pdf</span><small>23쪽</small></div>'
    '<div><span>📄 자료/판결문_2심.pdf</span><small>18쪽</small></div></div>'
    '<div class="call" style="left:300px;top:470px">@ 치면 파일 목록</div>'
    '<div class="call" style="left:300px;top:732px">① 환경</div>'
    '<div class="call" style="left:390px;top:732px">② 사건 폴더</div>'
    '<div class="call" style="left:1010px;top:732px">③ 모델</div>'
    '<div class="call" style="left:1150px;top:732px">④ 권한 모드</div>')

# 03: permission prompt
S['03-permission'] = page(
    '<div class="win">' + side(['증거목록 만들기'], 0, TREE) +
    '<div class="main"><div class="top"><b>증거목록 만들기</b> · 사건폴더 · 수동</div><div class="msgs">' +
    me('<span class="chip">자료/</span> PDF들로 증거목록 만들어줘') +
    '<div class="tool">✓ 읽음 자료/ (PDF 20개)</div>' +
    '<div class="perm"><b>이 명령을 실행할까요?</b><div class="cmd">rm 자료/계약서_v1.docx</div>'
    '<div style="font-size:13px;color:#6B675E;margin-bottom:10px">자료 폴더의 파일을 <b class="warn">삭제</b>하는 명령이에요.</div>'
    '<div class="btns"><span class="btn">허락</span><span class="btn ok">거절</span></div></div>' +
    '</div>' + bar(mode='수동') + '</div></div>',
    '<div class="call" style="left:760px;top:330px">지우라고 한 적 없으면 → 거절</div>')

# 03b: plan mode
S['03-plan'] = page(
    '<div class="win">' + side(['증거목록 만들기'], 0, TREE) +
    '<div class="main"><div class="top"><b>증거목록 만들기</b> · 사건폴더 · 계획</div><div class="msgs">' +
    me('<span class="chip">자료/</span> 폴더 PDF 20개로 증거목록을 엑셀로 만들어줘') +
    '<div class="card"><h4>📝 계획</h4>'
    '1. PDF 20개를 하나씩 읽기<br>2. 파일마다 작성일, 작성자, 내용 한 줄 뽑기<br>'
    '3. 날짜순으로 갑 제1호증부터 번호 붙이기<br>4. <span class="chip">결과물/증거목록.xlsx</span>로 저장<br>'
    '5. 날짜를 못 찾은 파일은 맨 아래 따로 표시</div>' +
    ai('이대로 진행할까요? 고칠 부분이 있으면 말씀해 주세요.') +
    '</div>' + bar(mode='계획') + '</div></div>',
    '<div class="call" style="left:930px;top:734px">↑ 권한 모드 "계획": 계획만, 아무것도 안 바꿈</div>')

# 04: good instruction
S['04-instruction'] = page(
    '<div class="win">' + side(['계약서 검토'], 0, TREE) +
    '<div class="main"><div class="top"><b>계약서 검토</b> · 사건폴더</div><div class="msgs">' +
    me('우리는 <b>매수인 측</b>이야. <span class="chip">@자료/계약서_v2.docx</span> 에서 '
       '<b>매수인에게 불리한 조항</b>을 찾아서 조항 번호, 문제점, 수정 문구를 <b>표로</b> 정리하고 '
       '<span class="chip">결과물/</span>에 Word로 저장해줘') +
    ai('매수인에게 불리한 조항 4개를 찾았어요.<br>'
       '<table><tr><th>조항</th><th>문제점</th><th>수정 문구 제안</th></tr>'
       '<tr><td>5조</td><td>잔금 지급 기한이 일방적으로 짧음</td><td>"인도일로부터 30일 이내"</td></tr>'
       '<tr><td>9조</td><td>매도인만 해제권 보유</td><td>"각 당사자는 ... 해제할 수 있다"</td></tr>'
       '<tr><td>12조</td><td>하자담보책임 배제</td><td>"인도 후 6개월간 하자담보책임을 진다"</td></tr></table>'
       '<br><span class="file"><i>📄</i>결과물/계약서검토_매수인.docx</span>') +
    '</div>' + bar() + '</div></div>')

# 05: refine
S['05-refine'] = page(
    '<div class="win">' + side(['판결문 요약'], 0, TREE) +
    '<div class="main"><div class="top"><b>판결문 요약</b> · 사건폴더</div><div class="msgs">' +
    me('<span class="chip">@자료/판결문.pdf</span> 요약해줘') +
    ai('<span style="color:#9A958A">(A4 두 장 분량의 요약)</span>') +
    me('너무 길어. 쟁점, 원고 주장, 법원 판단으로 나눠서 세 줄씩') +
    ai('<b>쟁점</b> 매매대금 잔금 지급 지연이 계약 해제 사유인지<br>'
       '<b>원고 주장</b> 30일 넘게 지연돼 해제가 정당하다<br>'
       '<b>법원 판단</b> 지연은 인정되나 최고 절차가 없어 해제는 무효 (판결문 14쪽)') +
    me('좋아. 의뢰인 설명용으로 쉬운 말 버전도 만들어서 Word로 저장해줘') +
    '</div>' + bar() + '</div></div>')

# 06: result table preview (evidence list)
S['06-result'] = page(
    '<div class="win full"><div class="main"><div class="top">📊 <b>결과물/증거목록.xlsx</b> 미리 보기</div>'
    '<div class="msgs"><table><tr><th>번호</th><th>증거</th><th>작성일</th><th>작성자</th><th>입증 취지</th></tr>'
    '<tr><td>갑 제1호증</td><td>부동산 매매계약서</td><td>2026-03-02</td><td>원고, 피고</td><td>매매계약 체결 사실</td></tr>'
    '<tr><td>갑 제2호증</td><td>계좌이체 확인증</td><td>2026-03-02</td><td>원고</td><td>계약금 지급 사실</td></tr>'
    '<tr><td>갑 제3호증</td><td>내용증명</td><td>2026-05-10</td><td>원고</td><td>잔금 지급 최고</td></tr>'
    '<tr><td>갑 제4호증</td><td>문자메시지 캡처</td><td>2026-05-21</td><td>피고</td><td>지급 거절 의사</td></tr>'
    '<tr><td>갑 제5호증</td><td>등기사항전부증명서</td><td><span class="warn">확인 필요</span></td><td>등기소</td><td>소유권 현황</td></tr>'
    '</table><div class="tool">✓ PDF 20개 중 5개를 증거로 분류, 날짜를 못 찾은 1건은 "확인 필요"로 표시</div>'
    '</div></div></div>')

# 07: CLAUDE.md with added rule
S['07-claude-md'] = page(
    '<div class="win">' + side(['내용증명 초안'], 0, TREE) +
    '<div class="main"><div class="top"><b>내용증명 초안</b> · 사건폴더</div><div class="msgs">' +
    me('앞으로 판례 번호나 조문을 쓰면 꼭 "원문 확인 필요"라고 표시해줘. CLAUDE.md에도 적어줘') +
    '<div class="tool">✓ <b>고침</b> CLAUDE.md</div>' +
    '<div class="code"># 사건폴더 규칙\n- 답은 쉬운 한국어로, 서면은 경어체로.\n- 자료/ 는 읽기만, 결과는 결과물/ 에 Word 로.\n'
    '- 의뢰인 이름은 A, 상대방은 B 로 쓴다.\n<span class="add">+ 판례 번호, 조문, 이율, 기한은 "원문 확인 필요"라고 표시한다.</span></div>' +
    ai('CLAUDE.md에 한 줄 추가했어요. 다음 작업부터 판례와 조문 옆에 "원문 확인 필요"를 붙일게요.') +
    '</div>' + bar() + '</div></div>')

# 08: slash menu with skills
S['08-skills'] = page(
    '<div class="win">' + side(['내용증명 초안', '판결문 요약'], 0,
                               TREE + '<br>📁 .claude/skills<br>&nbsp;&nbsp;내용증명/<br>&nbsp;&nbsp;판결문-요약/') +
    '<div class="main"><div class="top"><b>내용증명 초안</b> · 사건폴더</div><div class="msgs">' +
    ai('<span class="tool">✓ 스킬 사용: 내용증명</span><br>내용증명 스킬대로 썼어요. 요구사항, 사실관계, 기한, 법적 근거 순서예요.<br>'
       '<span class="file"><i>📄</i>결과물/2026-12-01 내용증명_B.docx</span>') +
    '</div>' + bar(text='/', empty=False) + '</div></div>',
    '<div class="pop" style="left:300px;top:470px">'
    '<div class="on"><span>/내용증명</span><small>내용증명 초안 작성</small></div>'
    '<div><span>/판결문-요약</span><small>쟁점·주장·판단으로 요약</small></div>'
    '<div><span>/증거목록</span><small>PDF를 갑호증 목록으로</small></div></div>'
    '<div class="call" style="left:300px;top:428px">/ 치면 스킬 목록</div>')

# 09: github
S['09-github'] = page(
    '<div class="win">' + side(['규칙 정리'], 0, TREE + '<br>📄 .gitignore') +
    '<div class="main"><div class="top"><b>규칙 정리</b> · 사건폴더</div><div class="msgs">' +
    me('오늘 고친 규칙이랑 스킬 GitHub에 올려줘') +
    '<div class="tool">✓ git add CLAUDE.md .claude/skills/내용증명<br>✓ git commit -m "내용증명 스킬에 기한 규칙 추가"<br>✓ <b>git push</b></div>' +
    ai('2개 파일을 올렸어요.<br>• CLAUDE.md (원문 확인 규칙)<br>• .claude/skills/내용증명/SKILL.md (기한 규칙)<br><br>'
       '<span class="chip">자료/</span>, <span class="chip">결과물/</span>은 .gitignore에 있어서 <b>올리지 않았어요</b>.') +
    '</div>' + bar() + '</div></div>')

# 10: anonymize before/after
S['10-anonymize'] = page(
    '<div class="win full"><div class="main"><div class="top">📄 <b>자료/진술서.docx</b> → <b>자료/진술서_비식별.docx</b></div>'
    '<div class="msgs"><div class="split">'
    '<div class="doc"><b>원본</b><br>진술인 <mark>홍길동(900101-1234567)</mark>은 2026. 3. 2. '
    '<mark>주식회사 한빛상사</mark> 대표 <mark>김철수</mark>와 매매계약을 체결하였고, 연락은 '
    '<mark>010-1234-5678</mark>로 하였다.</div>'
    '<div class="doc"><b>비식별</b><br>진술인 <span class="ok">A</span>는 2026. 3. 2. '
    '<span class="ok">甲사</span> 대표 <span class="ok">B</span>와 매매계약을 체결하였고, 연락은 '
    '<span class="ok">(삭제)</span>로 하였다.</div></div>'
    '<div class="doc" style="margin-top:6px">대금 지급 기한은 인도일로부터 30일입니다 '
    '<span class="warn">(원문 확인 필요: 계약서 5조)</span>. 지연손해금 이율은 '
    '<span class="warn">(원문 확인 필요: 근거 조문)</span>에 따릅니다.</div>'
    '</div></div></div>')

# 11: parallel sessions
S['11-parallel'] = page(
    '<div class="win">' + side([], groups=[('2026가합1234 매매대금', [('판결문 요약', ('done', '완료')), ('송금내역 정리', ('run', '진행 중'))], 1),
                              ('2026가단5678 임대차', [('내용증명 초안', ('run', '진행 중'))], -1)]) +
    '<div class="main"><div class="top"><b>송금내역 정리</b> · 사건폴더</div><div class="msgs">' +
    me('<span class="chip">@자료/거래내역.xlsx</span> 피고 B에게 보낸 돈만 <span class="chip">결과물/송금내역.xlsx</span>로') +
    '<div class="tool">… 거래 312건 읽는 중</div>' +
    '</div>' + bar() + '</div></div>',
    '<div class="toast"><b>판결문 요약</b> 작업이 끝났어요<small>결과물/판결문요약.docx</small></div>'
    '<div class="call" style="left:60px;top:58px">＋ 새로 만들기 (Ctrl+N)</div>')

# 07b: which rules and skills are loaded (root vs project)
S['07-scope'] = page(
    '<div class="win">' + side(['하자담보 정리'], 0,
        '💻 C:\\Users\\나\\.claude<br>&nbsp;&nbsp;📄 <b>CLAUDE.md</b> (공통)<br>&nbsp;&nbsp;📁 skills<br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;내용증명/<br>&nbsp;&nbsp;&nbsp;&nbsp;판결문-요약/<br><br>'
        '📁 사건\\2026가합1234<br>&nbsp;&nbsp;📄 <b>CLAUDE.md</b> (이 사건)<br>&nbsp;&nbsp;📁 .claude\\skills<br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;하자담보-정리/<br>&nbsp;&nbsp;📁 자료 · 결과물') +
    '<div class="main"><div class="top"><b>하자담보 정리</b> · 2026가합1234</div><div class="msgs">' +
    me('지금 어떤 규칙이랑 스킬을 읽고 있어?') +
    ai('<table><tr><th>종류</th><th>어디서</th><th>내용</th></tr>'
       '<tr><td>📜 규칙</td><td>공통 (C:\\Users\\나\\.claude\\CLAUDE.md)</td><td>경어체, 의뢰인은 A, 원문 확인 표시</td></tr>'
       '<tr><td>📜 규칙</td><td>이 사건 (사건폴더\\CLAUDE.md)</td><td>우리는 원고(매수인), 쟁점은 하자담보책임</td></tr>'
       '<tr><td>🧩 스킬</td><td>공통</td><td>/내용증명, /판결문-요약</td></tr>'
       '<tr><td>🧩 스킬</td><td>이 사건</td><td>/하자담보-정리</td></tr></table>'
       '<br>두 CLAUDE.md는 <b>둘 다</b> 읽어요. 공통 규칙 다음에 사건 규칙을 읽어요.') +
    '</div>' + bar(folder='2026가합1234') + '</div></div>')

# 11b: sessions grouped by case folder, and adding a folder to one session
S['11-folders'] = page(
    '<div class="win">' + side([], groups=[
        ('2026가합1234 매매대금', [('판결문 요약', ('done', '완료')), ('항소이유서 초안', ('run', '진행 중'))], 1),
        ('2026가단5678 임대차', [('내용증명 초안', ('done', '완료'))], -1),
        ('폴더 없음', ['질문 메모'], -1)]) +
    '<div class="main"><div class="top"><b>항소이유서 초안</b> · 2026가합1234 매매대금 + 1심기록</div><div class="msgs">' +
    me('1심 기록 폴더도 같이 보면서 항소이유를 정리해줘') +
    '<div class="tool">✓ 폴더 추가: 사건\\2026가합1234_1심기록</div>' +
    ai('두 폴더를 같이 보고 있어요.<br>• <span class="chip">2026가합1234 매매대금/</span> 항소심 폴더<br>'
       '• <span class="chip">2026가합1234_1심기록/</span> 1심 판결문, 준비서면, 증거<br><br>'
       '1심 판결의 사실인정과 법리 판단에서 다툴 만한 부분 4곳을 찾았어요.') +
    '</div>' + bar(folder='2026가합1234 매매대금') + '</div></div>',
    '<div class="pop" style="left:296px;top:520px">'
    '<div><span>📎 파일 또는 사진 추가</span></div>'
    '<div class="on"><span>📁 폴더 추가</span><small>이 작업에 폴더 하나 더</small></div>'
    '<div><span>/ 슬래시 명령</span></div></div>'
    '<div class="call" style="left:296px;top:478px">＋ › 폴더 추가</div>'
    '<div class="call" style="left:22px;top:560px">↑ 사이드바는 사건 폴더별로 묶여요</div>')


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, doc in S.items():
        with open(os.path.join(out, name + '.html'), 'w') as f:
            f.write(doc)
    print('\n'.join(S))


if __name__ == '__main__':
    main()
