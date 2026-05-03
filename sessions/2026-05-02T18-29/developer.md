# 💻 Developer — 확정된 TLA(시간, 장소, 금액) 데이터 구조를 기반으로 '모순점 검출 엔진'의 코드 로직을 구현하고, 가설 생성 UI와 증거물 카드 간의 상호작용 프로토러타입 코드를 작성한다.

💻 Developer: 작업 시작합니다.

확정된 TLA 데이터 구조를 엔진의 핵심으로 삼고, 이를 기반으로 모순(Contradiction)을 판별하는 로직과 UI 상호작용이 결합된 프로토타입 코드를 작성합니다. 기술 스택은 즉시 실행 가능한 HTML/JS/Tailwind CSS 조합을 사용하여 '웹 브라우저에서 돌아가는 게임 엔진' 형태로 구현합니다.

### 🛠️ 핵심 설계 전략
1.  **Engine (Logic):** `TLA_Analyzer` 클래스가 데이터를 순회하며 설정된 규칙(Rule-set)에 따라 모순 노드를 생성합니다.
2.  **UI (Interaction):** 가설 카드와 증거물 카드를 연결하는 인터랙티브 레이아웃을 구현합니다.
3.  **Data Structure:** 
    *   `Time`: 선후 관계 및 시간적 중첩 체크
    *   `Location`: 장소의 물리적 이동 가능성 체크
    *   `Amount`: 금액의 논리적 일치 여부 체크

---

### 💻 핵심 엔진 & 프로토타입 코드 (Single-File Solution)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Tailwind CSS for Rapid UI -->
    <script src="https://cdn.tailwindcss.com"></script>
    <title>TLA Inference Engine Prototype</title>
    <style>
        body { background-color: #0a0a0c; color: #e0e0e0; font-family: 'Inter', sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .contradiction-glow { box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); border-color: #ef4444; }
        .card-hover:hover { transform: translateY(-2px); transition: all 0.2s ease; background: rgba(255, 255, 255, 0.07); }
    </style>
</head>
<body class="p-4 md:p-10">

<div id="app" class="max-w-6xl mx-auto">
    <!-- Header -->
    <header class="mb-8 border-b border-white/10 pb-4 flex justify-between items-end">
        <div>
            <h1 class="text-2xl font-bold tracking-tighter text-white">CASE_FILE: #2026-05-02</h1>
            <p class="text-sm text-gray-400 italic">TLA Engine v1.0 - Core Logic Test</p>
        </div>
        <div class="text-right">
            <span class="text-xs font-mono bg-red-900/30 text-red-400 px-2 py-1 rounded">MOD-STATUS: ACTIVE</span>
        </div>
    </header>

    <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column: Evidence Cards (The Data) -->
        <div class="lg:col-span-2 space-y-6">
            <h2 class="text-sm font-semibold uppercase tracking-widest text-gray-500">Available Evidence (T-L-A Data)</h2>
            <div id="evidence-container" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- JS will inject cards here -->
            </div>
        </div>

        <!-- Right Column: Hypothesis & Analysis (The Output) -->
        <div class="space-y-6">
            <h2 class="text-sm font-semibold uppercase tracking-widest text-gray-500">Hypothesis Generator</h2>
            <div id="analysis-panel" class="glass p-6 rounded-lg space-y-4">
                <p class="text-xs text-gray-400 leading-relaxed">Select evidence to generate a hypothesis and check for logical contradictions.</p>
                <!-- Dynamic Analysis Content -->
            </div>
        </div>
    </main>
</div>

<script>
/** [ENGINE] TLA Logic Core **/
class TLAEngine {
    constructor(evidenceList) {
        this.evidence = evidenceList;
        this.rules = [
            { id: 'TIME_OVERLAP', msg: '시간의 모순: 동일 인물이 같은 시간에 두 곳에 있을 수 없습니다.' },
            { id: 'LOCATION_IMPOSSIBILITY', msg: '장소의 모순: 이동 시간이 부족한 물리적 불가능 상태입니다.' }
        ];
    }

    // Check for contradictions between two or more pieces of evidence
    checkContradictions(selectedIds) {
        const selected = this.evidence.filter(e => selectedIds.includes(e.id));
        let conflicts = [];

        for (let i = 0; i < selected.length; i++) {
            for (let j = i + 1; j < selected.length; j++) {
                const a = selected[i];
                const b = selected[j];

                // Rule 1: Time Overlap (Simple check)
                if (a.time === b.time && a.location !== b.location) {
                    conflicts.push(this.rules.find(r => r.id === 'TIME_OVERLAP'));
                }
                // Rule 2: Location-based logic (Placeholder for distance/travel time)
                if (a.location !== b.location && a.time === b.time) {
                    conflicts.push({ ...this.rules.find(r => r.id === 'LOCATION_IMPOSSIBILITY'), unique: true });
                }
            }
        }
        return [...new Set(conflicts)]; // Return unique conflicts
    }
}

/** [DATA] Mock Evidence Data **/
const mockEvidence = [
    { id: 'E1', time: '20:00', location: '서재', amount: 500, description: '피해자의 마지막 목격 시간' },
    { id: 'E2', time: '20:00', location: '응접실', amount: 1200, description: '알리바이 증거 - 용의자 A 위치' },
    { id: 'E3', time: '21:30', location: '정원', amount: 300, description: '발견된 사라진 시계' },
    { id: 'E4', time: '19:00', location: '서재', amount: 0, description: '사건 발생 전 상황 기록' }
];

/** [UI] Controller **/
const state = {
    selectedIds: []
};

const engine = new TLAEngine(mockEvidence);

function render() {
    const container = document.getElementById('evidence-container');
    const analysis = document.getElementById('analysis-panel');
    
    // Render Evidence Cards
    container.innerHTML = mockEvidence.map(e => `
