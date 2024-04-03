from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
import json



pdf_path = "TM_noRAG/2023 Integrated Report_Kor.pdf"  #전기보고서 첨부 경로
raw_data = """
직원 복지: 새로운 웰빙 프로그램을 도입하여 직원 만족도 점수가 20% 증가.
""" #유저가 입력


def make_draft(pdf_path, raw_data):
    draft = []
    index_list=json.loads(get_index(raw_data))
    for index in index_list:
        disclosure_num = index['disclosure_num']
        pages = find_gri_pages(pdf_path,disclosure_num)
        if type(pages) == list:
            extracted_pages = extract_text_from_pages(pdf_path, pages)
        else:
            extracted_pages = ["no page in previous report"]
        
        for extrated_page in extracted_pages:
            small_draft = [pages, disclosure_num]
            small_draft.append(get_draft(extrated_page,disclosure_num,raw_data)) 
        draft.append(small_draft)
        print(small_draft)
    return draft

print(make_draft(pdf_path, raw_data))




