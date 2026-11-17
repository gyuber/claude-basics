# 00. Claude Code란

## 한 줄 정의
Claude 데스크톱 앱의 **Code 탭**이에요. **내 PC 폴더 안의 파일을 직접 읽고, 고치고, 새로 만드는** Claude입니다.
원래 개발자용이지만 판결문, 계약서, 거래내역 같은 **사건 기록 작업**에 그대로 쓸 수 있어요.

## 앱에서 Code 탭 찾기
Claude 데스크톱 앱에는 **Chat, Cowork, Code** 세 가지 방식이 있어요.

![데스크톱 앱의 세 가지 모드](../images/official/app-three-modes.png)
*출처: Claude Academy, [Navigating the Claude desktop app](https://claude.com/resources/tutorials/navigating-the-claude-desktop-app)*

앱 왼쪽 위의 **`</>` 버튼**이 Code예요. 말풍선 버튼은 일반 대화(Chat)입니다.

![앱 사이드바와 Code 전환 버튼](../images/official/app-sidebar-code-button.jpg)
*출처: Claude 공식 유튜브, [Getting started with Claude Code Projects](https://www.youtube.com/watch?v=omihvjf0A2k)*

## 일반 대화와 무엇이 다른가
```mermaid
flowchart LR
  subgraph Chat["💬 일반 대화"]
    A1["기록 첨부"] --> A2["답변 (글)"] --> A3["복사해서<br/>서면에 붙여넣기"]
  end
  subgraph Code["🗂️ Code 탭"]
    B1["일 맡기기"] --> B2["사건 폴더<br/>기록 읽기"] --> B3["Word·엑셀 파일로<br/>바로 저장"]
  end
```

| | 일반 대화 | Code 탭 |
|---|---|---|
| 기록 | 파일을 하나씩 첨부 | **사건 폴더째로** 읽고 저장 |
| 지침 | 매번 "우리는 원고 측이야" 설명 | `CLAUDE.md`에 한 번 써 두면 **자동으로 읽음** (07편) |
| 반복 업무 | 매번 다시 설명 | 내용증명, 판결문 요약을 **스킬**로 재사용 (08편) |

## 예시: 송금 내역 정리를 한 마디로
**할 일**: 계좌 거래내역 312건 중 피고에게 보낸 돈만 골라 엑셀로 정리하기

![Code 탭에 한 마디로 시키면 결과물 폴더에 엑셀 파일이 생겨요](../images/scenes/00-code-tab.png)
*재현 그림: Code 탭에 한 마디로 시키면 결과물 폴더에 엑셀 파일이 생겨요*

> **🙋 나** `@자료/거래내역.xlsx` 에서 피고 B에게 보낸 돈만 날짜순으로 정리해서 `결과물/`에 엑셀로 저장해줘
>
> **🤖 Claude** 피고 B 명의 계좌로 송금된 거래 17건, 합계 48,300,000원을 날짜순으로 정리했어요. 같은 날 나눠 보낸 거래 3건은 따로 표시했어요. `결과물/송금내역정리.xlsx`

일반 대화였다면 엑셀을 첨부하고, 답으로 나온 표를 복사해서, 새 엑셀에 붙여넣고 저장까지 직접 해야 해요.

*💬 예시 대화와 재현 그림은 이해를 돕기 위해 만든 것이에요. 사건, 이름, 숫자는 모두 가상이고 실제 답은 조금 다를 수 있어요.*

## 기억할 것
- 코딩은 몰라도 돼요. **평소 말로** 시키면 됩니다.
- Claude는 **빠르고 성실한 신입 어쏘**예요. 맥락을 잘 주고, 결과는 꼭 검토하세요.

📖 공식: [데스크톱 앱의 Claude Code](https://code.claude.com/docs/en/desktop)
