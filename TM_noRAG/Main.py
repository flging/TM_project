import subprocess
import sys

# uvicorn 설치 여부 확인 및 설치
try:
    import uvicorn
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "uvicorn"])

from fastapi import FastAPI
from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
from Indextranslate import translate
import json
import requests  # requests 라이브러리 추가

app = FastAPI()

pdf_path = "TM_noRAG/2023 Integrated Report_Kor.pdf"  # 전기보고서 첨부 경로

# 외부 API 호출을 수행하는 함수
def call_external_api():
    response = requests.get("https://api.example.com/data", params={"key": "API_KEY"})
    return response.json()

@app.post("/index_list")
def show_index_list(raw_data: str):
    # 외부 API 호출
    index_list = call_external_api()
    return index_list

@app.post("/create_draft")
def create_draft(raw_data: str, index_list: list, selected_numbers: list):
    draft = []
    for number in selected_numbers:
        disclosure_num = index_list[number]['disclosure_num']
        pages = find_gri_pages(pdf_path, disclosure_num)
        if type(pages) == list:
            extracted_pages = extract_text_from_pages(pdf_path, pages)
        else:
            extracted_pages = ["no page in previous report"]
        for extracted_page in extracted_pages:
            small_draft = [pages, disclosure_num]
            small_draft.append(get_draft(extracted_page, disclosure_num, raw_data))
        draft.append(small_draft)
    return draft

@app.post("/get_gri_title")
def get_gri_title(index_list: list):
    title_list = []
    for index in index_list:
        gri = index['disclosure_num']
        GRI_title = translate(gri)
        title_list.append(GRI_title)
    return title_list

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "uvicorn", "your_script_name_here:app", "--host", "0.0.0.0", "--port", "8000"])
