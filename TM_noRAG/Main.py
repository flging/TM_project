from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
import json



pdf_path = "TM_noRAG/2023 Integrated Report_Kor.pdf"  #전기보고서 첨부 경로
raw_data = """
ESG 보고를 위한 현재 데이터 예시
환경적 영향
탄소 배출: 전년 대비 탄소 배출량 15% 감소, 총 50,000톤의 CO2 상당량 달성.
에너지 소비: 전년 대비 에너지 소비량 10% 감소, 에너지 효율 개선 조치로 인해 총 5백만 kWh 사용.
폐기물 관리: 재활용률을 전년 대비 60%에서 75%로 증가, 총 1,000톤의 폐기물 재활용.
사회적 책임
직원 복지: 새로운 웰빙 프로그램을 도입하여 직원 만족도 점수가 20% 증가.
지역사회 참여: 교육 및 건강에 중점을 둔 지역사회 프로젝트에 50만 달러 투자.
다양성 및 포용성: 리더십 포지션에서 성비 균형을 50/50으로 달성하고 전체 직원 다양성을 15% 증가.
거버넌스 관행
윤리적 조달: 현재 90%의 자재가 우리의 윤리적 조달 정책을 준수하는 공급업체로부터 조달되며, 이는 80%에서 증가한 수치입니다.
이사회 다양성: 이사회 내 소수 집단의 대표성을 40%까지 증가.
준법 교육: 윤리 및 반부패에 중점을 둔 새로운 준법 교육을 모든 직원이 완료.
이 예시는 회사가 환경 지속 가능성, 사회적 책임, 강력한 거버넌스에 대한 그들의 헌신을 보여주기 위해 ESG 보고서에서 보고할 수 있는 다양한 지표 및 이니셔티브를 포괄합니다.
""" #유저가 입력


def make_draft(pdf_path, raw_data):
    draft = []
    index_list=json.loads(get_index(raw_data))
    for index in index_list:
        disclosure_num = index['disclosure_num']
        pages = find_gri_pages(pdf_path,disclosure_num)
        extracted_pages = extract_text_from_pages(pdf_path, pages)
        
        for extrated_page in extracted_pages:
            small_draft = [pages, disclosure_num]
            small_draft.append(get_draft(extrated_page,disclosure_num,raw_data)) 
        draft.append(small_draft)
        print(small_draft)
    return draft

print(make_draft(pdf_path, raw_data))




