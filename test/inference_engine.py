import json
import re
from typing import Dict, List, Any, Tuple, Optional

class CoreInferenceEngine:
    """
    추론 엔진 핵심 모듈 (MVP)
    데이터 파싱, 규칙 기반 모순점 검출, 증거물 생성
    """
    
    def __init__(self, rules: Dict[str, Dict[str, Any]]):
        self.rules = rules
        self.nodes = []
        self.edges = []
        self.contradictions = []
    
    def parse_事件文件(self, data: Dict[str, Any]) -> bool:
        """
        사건 파일(JSON) 파싱 및 그래프 구조 생성
        """
        try:
            # 1. 사건 정보 노드
            self.nodes.append({
                "id": "event_info",
                "type": "event",
                "label": f"{data.get('사건명', '사건')} 정보",
                "data": {
                    "date": data.get('사건발생일자'),
                    "location": data.get('발생장소')
                }
            })
            
            # 2. 인물 노드 생성
            for i, person in enumerate(data.get('인물', [])):
                node_id = f"person_{i}"
                self.nodes.append({
                    "id": node_id,
                    "type": "person",
                    "label": person.get('이름', f'인물{i+1}'),
                    "data": {
                        "role": person.get('역할'),
                        "motive": person.get('동기')
                    }
                })
                
                # 사건 정보와 인물 연결
                self.edges.append({
                    "id": f"edge_event_person_{i}",
                    "source": "event_info",
                    "target": node_id,
                    "type": "participated_in",
                    "weight": 1
                })
            
            # 3. 핵심 사실(Key Facts) 노드
            if "핵심_사실" in data:
                for i, fact in enumerate(data["핵심_사실"]):
                    fact_id = f"fact_{i}"
                    self.nodes.append({
                        "id": fact_id,
                        "type": "fact",
                        "label": fact.get('사실명', f'사실{i+1}'),
                        "data": {
                            "statement": fact.get('내용'),
                            "veracity": fact.get('진위', 'UNKNOWN')
                        }
                    })
                    
                    # 인물과 사실 연결
                    for j, person in enumerate(data.get('인물', [])):
                        if fact.get('관련인물_index', -1) == j:
                            self.edges.append({
                                "id": f"edge_person_fact_{i}_{j}",
                                "source": f"person_{j}",
                                "target": fact_id,
                                "type": "has_knowledge",
                                "weight": 0.8
                            })
            
            print(f"✅ 데이터 파싱 성공: {len(self.nodes)}개 노드, {len(self.edges)}개 엣지 생성")
            return True
        except Exception as e:
            print(f"❌ 파싱 오류: {e}")
            return False
    
    def detect_contradictions(self) -> List[Dict[str, Any]]:
        """
        사전에 정의된 규칙을 기반으로 모순점 검출
        """
        self.contradictions = []
        
        # 규칙 1: 날짜 불일치 검사
        event_date = None
        for node in self.nodes:
            if node["id"] == "event_info":
                event_date = node["data"].get("date")
                break
        
        if event_date:
            for i, fact in enumerate(self.nodes):
                if fact["type"] == "fact" and fact["data"].get("statement"):
                    # 간단한 날짜 키워드 매칭 (실제로는 정규식 필요)
                    if "yesterday" in fact["data"]["statement"].lower() or 
                       "previous day" in fact["data"]["statement"].lower():
                        self.contradictions.append({
                            "id": f"contradiction_{len(self.contradictions)}",
                            "rule": "date_mismatch",
                            "description": "'어제'라는 언급이 사건 발생일자와 불일치합니다.",
                            "affected_nodes": [fact["id"], "event_info"],
                            "evidence": {
                                "type": "statement_comparison",
                                "fact_statement": fact["data"]["statement"],
                                "event_date": event_date
                            }
                        })
        
        # 규칙 2: 자금 규모 불일치 (예: 1억 vs 10만)
        large_amount_rule = {
            "description": "금액 단위가 일반적이지 않습니다.",
            "patterns": [
                r"1억", r"100,000,000",
                r"1 billion", r"1,000,000,000"
            ]
        }
        
        for i, fact in enumerate(self.nodes):
            if fact["type"] == "fact" and fact["data"].get("statement"):
                for pattern in large_amount_rule["patterns"]:
                    if re.search(pattern, fact["data"]["statement"], re.IGNORECASE):
                        self.contradictions.append({
                            "id": f"contradiction_{len(self.contradictions)}",
                            "rule": "amount_inconsistency",
                            "description": large_amount_rule["description"],
                            "affected_nodes": [fact["id"]],
                            "evidence": {
                                "type": "numeric_analysis",
                                "matched_pattern": pattern,
                                "context": fact["data"]["statement"]
                            }
                        })
                        break
        
        return self.contradictions
    
    def get_logical_evidence(self, contradiction_id: str) -> Dict[str, Any]:
        """
        모순점을 클릭했을 때 상세한 논리적 증거물 제공
        """
        for contradiction in self.contradictions:
            if contradiction["id"] == contradiction_id:
                rule_type = contradiction["rule"]
                
                if rule_type == "date_mismatch":
                    return {
                        "title": "시간적 모순",
                        "analysis": "사건 발생일은 '2026년 5월 1일'로 명시되어 있으나, 증인 A는 '어제'라고 진술했습니다. 만약 오늘이 5월 2일이라면 진술은 맞지만, 사건이 발생한 시점(5월 1일)을 기준으로 한다면 명백한 시간적 불일치입니다.",
                        "evidence_items": [
                            {
                                "label": "사건 발생일",
                                "value": contradiction["evidence"]["event_date"],
                                "source": "사건 기록",
                                "is_fact": True
                            },
                            {
                                "label": "증인 A 진술",
                                "value": contradiction["evidence"]["fact_statement"],
                                "source": "증인 A",
                                "is_fact": False
                            }
                        ],
                        "logical_chain": [
                            "사건 발생일 (5/1) !== 증인 진술 ('어제', 5/1 기준) => 논리적 모순",
                            "가설: 증인이 시간을 착각했거나, 사건 기록 날짜가 잘못되었거나, 혹은 사건이 5/1 이전(4/30)에 발생했음"
                        ]
                    }
                
                elif rule_type == "amount_inconsistency":
                    return
