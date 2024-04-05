from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
from Indextranslate import translate
import json

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_path = "TM_noRAG/2023 Integrated Report_Kor.pdf"  # 전기보고서 첨부 경로

@app.post("/index_list")
async def show_index_list(raw_data: str):
    index_list = json.loads(get_index(raw_data))
    return JSONResponse(content=index_list)

@app.post("/create_draft")
async def create_draft(raw_data: str, selected_numbers: list):
    index_list = json.loads(get_index(raw_data))
    draft = []
    for number in selected_numbers:
        disclosure_num = index_list[number]['disclosure_num']
        pages = find_gri_pages(pdf_path, disclosure_num)
        if isinstance(pages, list):
            extracted_pages = extract_text_from_pages(pdf_path, pages)
        else:
            extracted_pages = ["no page in previous report"]
        for extracted_page in extracted_pages:
            small_draft = {"pages": pages, "disclosure_num": disclosure_num}
            small_draft["draft"] = get_draft(extracted_page, disclosure_num, raw_data)
            draft.append(small_draft)
    return JSONResponse(content=draft)

@app.post("/get_gri_title")
async def get_gri_title(raw_data: str):
    index_list = json.loads(get_index(raw_data))
    title_list = [translate(index['disclosure_num']) for index in index_list]
    return JSONResponse(content=title_list)