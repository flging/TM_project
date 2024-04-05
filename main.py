from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
from Indextranslate import translate
import json
import os

app = FastAPI()

class RawData(BaseModel):
    raw_data: str

class Draft(BaseModel):
    draft: list

class SelectedNumbers(BaseModel):
    selected_numbers: list[int]

pdf_directory = "uploaded_pdfs/"  # 업로드된 PDF 파일을 저장할 디렉토리 경로
if not os.path.exists(pdf_directory):
    os.makedirs(pdf_directory)

def show_index_list(raw_data):
    index_list = json.loads(get_index(raw_data))
    return index_list

def create_draft_from_raw_data(raw_data, index_list, selected_numbers, pdf_path):
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

def get_gri_title(index_list):
    title_list = []
    for index in index_list:
        gri = index['disclosure_num']
        gri_title = translate(gri)
        title_list.append(gri_title)
    return title_list

@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()  # 파일 내용 읽기
    filename = file.filename  # 파일 이름 가져오기

    # 업로드된 파일을 디스크에 저장
    with open(os.path.join(pdf_directory, filename), "wb") as f:
        f.write(contents)

    return {"message": "File uploaded successfully"}

@app.post('/create_draft', response_model=Draft)
def create_draft(raw_data: RawData, selected_numbers: SelectedNumbers):
    index_list = show_index_list(raw_data.raw_data)
    uploaded_pdf_path = os.path.join(pdf_directory, os.listdir(pdf_directory)[0])
    draft = create_draft_from_raw_data(raw_data.raw_data, index_list, selected_numbers.selected_numbers, uploaded_pdf_path)
    return {"draft": draft}

@app.post('/get_gri_titles', response_model=list[str])
def get_gri_titles(raw_data: RawData):
    index_list = show_index_list(raw_data.raw_data)
    uploaded_pdf_path = os.path.join(pdf_directory, os.listdir(pdf_directory)[0])
    title_list = get_gri_title(index_list)
    return {"titles": title_list}

