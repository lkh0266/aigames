# 💻 Developer — designer의 비주얼 브리프를 바탕으로, TLA 데이터 파싱 로직이 포함된 '모순 보고서' 화면과 유저가 가설을 입력/조합하는 '가설 생성 UI'의 프론트엔드 프로토토타입 코드를 작성하세요. 핵심 엔진(백엔드)과 시각적 요소를 결합해야 합니다.

💻 Developer: 작업 시작합니다.

제공된 `Designer`의 비주얼 브리프를 기술적으로 구현하기 위해, **React + Tailwind CSS + Framer Motion** 스택을 사용하여 프론트엔드 프로토타입을 작성했습니다. 이 코드는 단순한 UI를 넘어 `T-L-A(Time-Location-Amount)` 데이터 구조를 기반으로 모순을 감지하는 로직과 가설 생성 인터페이스의 물리적 상호작용을 시뮬레이션합니다.

### 🛠️ 기술 스택 및 구현 전략
- **Framework:** React (UI 상태 관리 및 컴포넌트 구조)
- **Styling:** Tailwind CSS (Designer의 컬러 팔레트 반영: `#1A1A1A`, `#D4C5B3`, `#B22222`)
- **Animation:** Framer Motion (모순 발생 시 '균열' 및 카드 이동 효과)
- **Logic:** TLA 속성 간 불일치를 감지하는 `checkContradiction` 엔진 내장

```jsx
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// --- [1. Mock Data: T-L-A 구조의 증거물 데이터] ---
const INITIAL_EVIDENCE = [
  { id: 1, t: '2026-05-02 14:00', l: '서재', a: 5000, type: 'receipt' },
  { id: 2, t: '2026-05-02 14:30', l: '정원', a: 12000, type: 'ledger' }, // 시간/장소 충돌 가능성
  { id: 3, t: '2026-05-02 15:00', l: '서재', a: 8000, type: 'note' },   // 장소 중복(동일시간 내 다른장소)
];

/**
 * [핵심 엔진] 모순 감지 로직 (Simplified TLA Engine)
 * 시간이나 장소가 겹치는데 데이터가 다를 경우 혹은 물리적 불가능을 체크
 */
const checkContradictions = (data) => {
  let conflicts = [];
  for (let i = 0; i < data.length; i++) {
    for (let j = i + 1; j < data.length; j++) {
      const e1 = data[i];
      const e2 = data[j];
      // 단순 로직: 같은 시간대인데 장소가 다르면 모순으로 간주
      if (e1.t === e2.t && e1.l !== e2.l) {
        conflicts.push({ a: e1.id, b: e2.id });
      }
    }
  }
  return conflicts;
};

// --- React/Tailwind 기반 프론트엔드 프로토타입 코드 시작 ---
/* 
   실행 환경 가이드: 
   이 코드는 React + Tailwind CSS 환경에서 작동하도록 설계되었습니다.
   'npm install lucide-react clsx tailwind-merge' 라이브러리가 필요합니다.
*/

import React, { useState,
