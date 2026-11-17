# 슬라이드 원본

- `template.html`: 칠판 테마 템플릿 (gyuber/dotfile#2), 스타일과 그리기 스크립트
- `sections.html`: 슬라이드 내용. **슬라이드를 고칠 때는 이 파일을 고친다**
- `build.py`: 두 파일을 합쳐 `slides/index.html`을 만든다. 쪽 번호는 자동

```
python3 slides/_src/build.py            # slides/index.html
python3 slides/_src/build.py <폴더>     # + <폴더>/artifact.html (Claude 페이지용)
```

강의(`기초/`)를 고치면 이 슬라이드도 같이 고친다.
