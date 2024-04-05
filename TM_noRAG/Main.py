from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
from Indextranslate import translate
import json



pdf_path = "TM_noRAG/2023 Integrated Report_Kor.pdf"  #전기보고서 첨부 경로
raw_data = """
[DX팀 인터뷰]
1.DX의 업무 범위 : 홈페이지 내 소개자료 확인 / (ESG팀_자료요청) 홈페이지 링크 
2. 조직도 : 
3. 현장에서 발생하는 비효율적인 업무들을 개선하는 업무를 진행 중, 스프린트로 2/3개월 마다 프로젝트를 진행 중,
 3-1. 주요 업무 
  a. 119운영위원회 - 리스크 관리 위원회 산하 (CEO/CFO 산하) 
  b. Dash-board 구축은 전사시스템 개편 진행시 포함될 예정
  c. 안전 조회 번역 웹 
  d. AI 자재 관리 어시스턴트
   '- 현장에서 자재공급승인원을 제작하는 부분을 자동화하는 기능 
  e. DX/CX 관련 교육 진행
.
""" #유저가 입력


def Show_indexList(raw_data):
    index_list=json.loads(get_index(raw_data))
    return index_list

def Create_Draft(raw_data, index_list, selected_numbers ,pdf_path):
    draft = []
    for number in selected_numbers:
        disclosure_num = index_list[number]['disclosure_num']
        pages = find_gri_pages(pdf_path,disclosure_num)
        if type(pages) == list:
            extracted_pages = extract_text_from_pages(pdf_path, pages)
        else:
            extracted_pages = ["no page in previous report"]
        for extrated_page in extracted_pages:
            small_draft = [pages, disclosure_num]
            # print(raw_data+ "\n\n\n"+extrated_page +"\n\n\n"+disclosure_num)
            small_draft.append(get_draft(extrated_page,disclosure_num,raw_data)) 
        draft.append(small_draft)
    return draft

def get_GRI_Title(index_list):
    Title_list = []
    for index in index_list:
        gri = index['disclosure_num']
        GRI_title = translate(gri)
        Title_list.append(GRI_title)
    return Title_list

# for_Draft_prompting = Create_Draft(raw_data, Show_indexList(raw_data), [0,1,2], pdf_path)


# print(Create_Draft(raw_data, Show_indexList(raw_data),[0,1,2],pdf_path))


