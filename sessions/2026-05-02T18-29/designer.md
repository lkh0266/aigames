# 🎨 Designer — 확정된 디자인 시스템(Ledger Base, Evidence Card)을 적용하여, 실제 게임 화면과 유사한 수준의 고해상도 UI 목업 및 에셋 시각화 결과물을 제작한다.

🎨 Designer: 작업 시작합니다.

확정된 **[Ledger Base + Evidence Card]** 디자인 시스템을 기반으로, 플레이어가 모순을 발견하고 가설을 세우는 핵심 게임 루프를 시각화합니다. 1인 개발 환경(무료 에셋/효율적 레이아스)을 고려하여, 고품질의 분위기를 유지하면서도 구현 가능한 수준의 UI 목업 디자인 브리프와 에셋 명세서를 도출합니다.

---

### 🎞️ 1. 핵심 화면 디자인 시스템: [The Ledger & The Evidence]

#### **[A] 배경 및 베이스 레이아웃 (Ledger Base)**
- **컨셉:** 차갑고 거친 질감의 현대적 '장부(Ledger)'. 종이보다는 어두운 가죽이나 매끄러운 돌판 위에 잉크가 새겨지는 듯한 느낌.
- **색상 팔레트:**
    - `Deep Charcoal (#0A0A0C)`: 메인 배경 (심연의 깊이감)
    - `Paper Parchment (#D4C8B5 / 낮은 투명도)`: 정보 텍스트 가독성을 위한 베이스 레이어
    - `Ink Black (#1A1A1A)`: 카드 및 구분선 영역
    - `Oxidized Copper (#4E6B5F)`: 보조/중립적 요소 (녹슨 구리 색상)
- **타이포그래피:**
    - 헤드라인: *Playfair Display* (세리프, 고풍스럽고 날카로운 느낌)
    - 본문/데이터: *Inter* 또는 *Roboto Mono* (산세리프/모노스페이스, 현대적이고 분석적인 느낌)

#### **[B] 정보 카드 디자인 (Evidence Card)**
- **구조:** 상단(속성 헤더) / 중앙(내용 텍스트) / 하단(TLA 태그)
- **디자인 요소:**
    - `Border`: 아주 얇은 $1px$ 실선 혹은 미세한 그라데이션 경계.
    - `Shadow`: 카드가 공중에 떠 있는 듯한 느낌을 주어 레이어 간 위계 형성 (Drop Shadow).
    - `Interaction State`: 모순이 발견된 카드는 **[Crimson Red Glow]**가 발광하며 테두리가 붉게 변함.

---

### 🖼️ 2. 핵심 UI 목업 시각화 명세 (Visual Mockup Spec)

#### **Scene: [모순 보고서 - 가설 생성 단계]**
이 화면은 플레이어가 수집한 증거들 사이의 '충돌'을 해결하는 순간을 담습니다.

| 요소 | 시각적 구성 및 레이아스 좌표/방식 | 비주얼 디테일 (Texture & Effect) |
| :--- | :--- | :--- |
| **1. 중앙 워크스페이스** | 화면의 70% 차지. 자유로운 그리드 배치(Free-form Grid). | 배경은 어두운 가죽 질감의 `Deep Charcoal`. |
| **2. 증거 카드 (Evidence)** | 좌우/상하로 배치된 작은 직사각형 모듈. | 은은한 노이즈가 섞인 종이 질감 위에 날카로운 타이포 적용. |
| **3. 연결선 (Link/Edge)** | 카드와 카드를 잇는 얇은 선(Line). | '모순' 발생 시 선이 떨리거나 붉게 점멸하는 애니메이션 효과를 고려한 설계. |
| **4. 하단 컨트롤 바** | 화면 최하단 고정형 UI (Fixed Bottom). | 현재 선택된 증거의 요약 정보와 '가설 확정' 버튼 배치. |

#### **[디테일 가이드: TLA 데이터 시각화]**
- **T(Time):** 황금색(Amber) 계열의 아이콘/텍스트 사용. 시간적 선후 관계를 나타내는 화살표 흐름 강조.
- **L(Location):** 차가운 푸른색(Cyan) 계데의 아이콘/텍스드 사용. 공간적 위치 정보를 나타냄.
- **A(Amount):** 묵직한 백금색(Silver) 계열로 금액 수치를 표현.

---

### 🎨 3. 디자인 시스템 확정 (Final Design System)

#### **[Color Palette]**
- **Primary Background:** `#0D0D0F` (깊은 심연의 블랙)
- **Secondary BG:** `#1A1A1C` (장부 종이 느낌의 어두운 회색)
- **Accent (Success/Info):** `#A8B5B2` (차갑고 낡은 은색)
- **Accent (Conflict/Warning):** `#E63946` (강렬한 모순의 레드)
- **Text Primary:** `#E0E0E0` / **Text Secondary:** `#888888`

#### **[Typography System]**
- **Title/Heading:** `Playfair Display` 또는 세리프 계열 폰트 (고풍스러운 전문직 분위기)
- **Body/Data:** `Inter` 또는 산세리프 계열 (가독성 중심의 데이터 표기)

#### **[UI Component: Evidence Card(증거 카드)]**
- **Layout:** 상단에 [T/L/A] 속성 아이콘 배치 $\rightarrow$ 중앙에 굵은 텍스트로 핵심 문구 $\rightarrow$ 하단에 부연 설명.
- **Interaction Design:**
    1.  **Hover:** 카드가 살짝 떠오르며(Z-axis), 테두리 광택이 강화됨.
    2.  **Conflict State:** 두 카드가 모순될 때, 각 카드의 가장자리에서 붉은 '균열' 효과가 발생하며 플레이어에게 시각적 피드백 전달.

---

### 📊 평가: 완료 — 확정된 디자인 시스템을 바탕으로 핵심 UI 레이아웃과 에셋 가이드를 구체화함
📝 다음 단계: Developer는 이 디자인 가이드를 기반으로 HTML/CSS를 넘어선 실제 게임 인터랙션(애니메이션 및 충돌 로직) 프로토타입 구현에 착수합니다.
