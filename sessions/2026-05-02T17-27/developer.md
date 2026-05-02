# 💻 Developer — 사건 파일 블루프린트를 기반으로 설계된 'Core Inference Engine MVP'의 전체 코드를 제공합니다. 이 코드에는 다음 기능이 포함되어야 합니다: 1) 사건 데이터 파싱 함수(Data Parsing), 2) T-L-A 세 속성 간 규칙 기반 모순점 플래깅 로직(Contradiction Flagging), 3) 상세 증거물 연결 및 분석 출력 로직. 코드는 주석과 함께 완벽히 실행 가능하도록 구성하며, 사용자가 직접 테스트할 수 있는 예제 케이스를 포함해야 합니다.

💻 Developer: 작업 시작합니다.

요청하신 'Core Inference Engine MVP'의 전체 코드를 제공합니다. 이 엔진은 사건 파일 데이터 구조를 입력받아, 증거물 파싱, 규칙 기반 모순점 플래깅, 그리고 최종 분석 보고서 생성을 담당하는 핵심 백엔드 로직입니다.

이 코드는 Python 3 환경에서 완벽하게 실행 가능하며, `InferenceEngine` 클래스를 통해 모든 기능을 통합 관리합니다.

### Core Inference Engine MVP (Python)

```python
import datetime
from typing import List, Dict, Any, Tuple

# --- 데이터 구조 정의 ---
class Evidence:
    """개별 증거물 정보를 담는 객체."""
    def __init__(self, evidence_id: str, time: str, location: str, amount: int, detail: str):
        self.evidence_id = evidence_id
        # 시간은 datetime 객체로 변환하여 비교 용이성을 높임
        try:
            self.time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
        except ValueError:
            self.time = None # 파싱 실패 대비
        self.location = location
        self.amount = amount
        self.detail = detail

    def __repr__(self):
        return (f"Evidence(ID={self.evidence_id}, T={self.time.strftime('%H:%M') if self.time else 'N/A'}, "
                f"L='{self.location}', A={self.amount}원)")

class InferenceEngine:
    """
    사건 데이터 파싱, 모순점 플래깅, 분석 보고서 생성을 담당하는 핵심 추론 엔진 MVP.
    """
    def __init__(self):
        self.evidence_list: List[Evidence] = []
        self.contradictions: List[Dict[str, Any]] = []

    # 1. 데이터 파싱 함수 (Data Parsing)
    def parse_evidence(self, raw_data: List[Dict[str, str]]) -> None:
        """
        원시 사건 파일 데이터를 순회하며 Evidence 객체 리스트로 변환합니다.
        raw_data 형식 예시: [{'id': 'E001', 'time': '2026-05-01 10:00', 'location': 'A지점', 'amount': '1000'}, ...]
        """
        print("\n[ENGINE] -> Step 1: 증거물 데이터 파싱 시작...")
        parsed_count = 0
        for item in raw_data:
            try:
                # 문자열 형태의 amount를 정수로 변환하는 과정 포함
                amount = int(item['amount'].replace(',', ''))
                evidence = Evidence(
                    evidence_id=item['id'],
                    time=item['time'],
                    location=item['location'],
                    amount=amount,
                    detail=item['detail']
                )
                self.evidence_list.append(evidence)
                parsed_count += 1
            except ValueError as e:
                print(f"[WARNING] 파싱 실패 (ID: {item.get('id', 'Unknown')}): 데이터 형식 오류 - {e}")

        print(f"[ENGINE] -> Step 1 완료: 총 {parsed_count}개의 증거물이 성공적으로 파싱되었습니다.")


    # 2. 규칙 기반 모순점 플래깅 로직 (Contradiction Flagging)
    def check_contradictions(self, time_threshold_hours: float = 3.0) -> None:
        """
        사전에 정의된 비즈니스 규칙을 기반으로 데이터 간의 모순점을 찾아 플래그를 지정합니다.

        [규칙 예시]
        1. 시간적 일관성 (Time Conflict): 두 증거물의 발생 시간이 일정 임계값(time_threshold_hours) 이상 차이 나는데, 
           두 증거물이 동일한 '결과'를 주장할 경우 모순으로 간주.
        2. 장소/시간 불일치 (Location Drift): 특정 지역에서 활동하기에 너무 빠른 시간 변화나 물리적 이동 거리가 비현실적인 경우.
        3. 금액 규모 오류 (Magnitude Error): 사건의 최종 목표(예: 100만원 미만)와 증거물의 자금 규모가 급격히 차이 날 경우.
        """
        print("\n[ENGINE] -> Step 2: 규칙 기반 모순점 검증 시작...")
        self.contradictions = []

        # --- Rule Set A: 시간적 일관성 체크 (Time Conflict Check) ---
        sorted_evidence = sorted(self.evidence_list, key=lambda e: e.time if e.time else datetime.datetime.max)
        
        for i in range(len(sorted_evidence)):
            e1 = sorted_evidence[i]
            if not e1.time: continue

            # 이전 증거물과 비교 (가장 가까운 시간의 증거물과만 비교하여 효율화)
            if i > 0 and sorted_evidence[i-1].time:
                e2 = sorted_evidence[i-1]
                
                # 시간 차이
