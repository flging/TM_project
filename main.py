from fastapi import FastAPI, UploadFile, File, Form, Query
from typing import List
import tempfile
import os
import json
import uuid
from fastapi.responses import JSONResponse
import shutil

# Import your existing functions here
from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
from Indextranslate import translate

app = FastAPI()

# Temporary storage for uploaded files
temp_pdf_storage = {}
gri_titles = {}

# def save_pdf(pdf: UploadFile = File(...)):
#     # Ensure the directory exists
#     upload_folder = "./temp/"
#     if not os.path.exists(upload_folder):
#         os.makedirs(upload_folder)
    
#     pdf.save(os.path.join(upload_folder, pdf.filename))

#     # Then save the file
#     with open(os.path.join(upload_folder, pdf.filename), "wb") as buffer:
#         shutil.copyfileobj(pdf.file, buffer)


def Show_indexList(raw_data):
    index_list = json.loads(get_index(raw_data))
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
        for extracted_page in extracted_pages:
            small_draft = [pages, disclosure_num]
            small_draft.append(get_draft(extracted_page,disclosure_num,raw_data)) 
        draft.append(small_draft)
    return draft

def get_GRI_Title(index_list):
    Title_list = []
    for index in index_list:
        gri = index['disclosure_num']
        GRI_title = translate(gri)
        Title_list.append(GRI_title)
    return Title_list

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    upload_folder = "./temp/"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    global file_path
    file_path = os.path.join(upload_folder, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "PDF uploaded successfully", "file_path": file_path}

async def enter_raw_data(raw_data: str = Form(...)):
    # 원시 데이터 처리
    gri_titles.update({"raw_data": raw_data})
    
    # Gri 타이틀 생성
    gri_title_list = get_GRI_Title(Show_indexList(raw_data))
    gri_titles.update({
        "gri_title1": gri_title_list[0],
        "gri_title2": gri_title_list[1],
        "gri_title3": gri_title_list[2],
        "gri_title4": gri_title_list[3],
        "gri_title5": gri_title_list[4]
    })
    
    # 클라이언트에게 Gri 타이틀 반환
    return JSONResponse(content=gri_titles)

@app.post("/enter_raw_data_info/")
async def enter_raw_data_info(interviewee: str = Form(...), raw_data_name: str = Form(...)):
    # Process the raw data info here (e.g., save to database)
    return {"message": "Raw data info received successfully"}


@app.get("/show_gri_titles/")
async def show_gri_titles():
    global gri_titles
    return JSONResponse(content=gri_titles)

@app.get("/show_extracted_text/")
async def show_extracted_text():
    global file_path
    if file_path:
        # Extract text from PDF
        extracted_text = extract_text_from_pages(file_path)  # You need to implement this function
        return {"extracted_text": extracted_text}
    else:
        return {"error": "PDF file not found"}

@app.post("/edit_extracted_text/")
async def edit_extracted_text(text: str = Form(...)):
    return {"edited_text": text}

@app.post("/create_draft/")
async def create_draft(selected_titles: List[str] = Form(...), edited_text: str = Form(...)):
    index_list = Show_indexList(edited_text)  # Assuming Show_indexList function is available
    selected_numbers = [index_list.index(title) for title in selected_titles]
    pdf_path = ""  # You need to provide the path to the PDF file
    draft = Create_Draft(edited_text, index_list, selected_numbers, pdf_path)  # Assuming Create_Draft function is available
    return {"draft": draft}

@app.get("/display_draft/")
async def display_draft():
    # Fetch and return the draft
    # For example: retrieve the draft from the database and return it
    draft = "Example draft"
    return JSONResponse(content={"draft": draft})