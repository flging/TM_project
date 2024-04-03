from TM_find_page import find_gri_pages
from TM_retrieve_RAG import retrieve_RAG
from pdfminer.high_level import extract_text
from TM_agent import get_draft

#input 3개
#output 2개


pdf_path = "TM/2023 Integrated Report_Kor.pdf"  #전기보고서 첨부 경로
raw_data = "단체 협약" #유저가 입력

def a(raw_data):
    index_list=retrieve_RAG(raw_data) #output - list형식, index_choice에 따라 선택
    return index_list

index_choice = 0 # 프론트에서 선택에 따라 받음 0~4

def b(index_choice, index_list, pdf_path):
    disclosure_number = index_list[index_choice].split("\t")[1].split(" ")[1]
    pages = find_gri_pages(pdf_path,disclosure_number)
    extracted_text = extract_text(pdf_path, page_numbers=[int(page) - 1 for page in str(pages).split(",")])
    draft = get_draft(raw_data,extracted_text,index_list[index_choice]) #output - 문자열 형식, 최종 초안에 해당
    return draft






