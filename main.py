from fastapi import FastAPI, UploadFile, File, Form
from typing import List
import tempfile
import os

# Import your existing functions here
from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
from Indextranslate import translate
import json

app = FastAPI()

# Temporary storage for uploaded files
temp_pdf_storage = {}

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

@app.post("/upload_pdf/")
async def upload_pdf(pdf_file: UploadFile = File(...)):
    # Save the uploaded PDF file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        temp_pdf.write(pdf_file.file.read())
        temp_pdf_path = temp_pdf.name
    temp_pdf_storage[temp_pdf_path] = temp_pdf.name
    return {"pdf_path": temp_pdf_path}

@app.post("/enter_raw_data/")
async def enter_raw_data(raw_data: str = Form(...)):
    return {"raw_data": raw_data}

@app.post("/enter_raw_data_info/")
async def enter_raw_data_info(interviewee: str = Form(...), raw_data_name: str = Form(...)):
    return {"interviewee": interviewee, "raw_data_name": raw_data_name}

@app.post("/show_gri_titles/")
async def show_gri_titles(raw_data: List[str] = Form(...)):
    index_list = Show_indexList(raw_data)  # Assuming Show_indexList function is available
    gri_titles = get_GRI_Title(index_list)  # Assuming get_GRI_Title function is available
    return {"gri_titles": gri_titles}

@app.post("/show_extracted_text/")
async def show_extracted_text(pdf_path: str = Form(...)):
    pdf_file_path = temp_pdf_storage.get(pdf_path, None)
    if pdf_file_path:
        # Extract text from PDF
        extracted_text = extract_text_from_pages(pdf_file_path)  # You need to implement this function
        return {"extracted_text": extracted_text}
    else:
        return {"error": "PDF file not found"}

@app.post("/edit_extracted_text/")
async def edit_extracted_text(text: str = Form(...)):
    return {"edited_text": text}

@app.post("/create_draft/")
async def create_draft(selected_titles: List[str] = Form(...), edited_text: str = Form(...), raw_data: List[str] = Form(...)):
    index_list = Show_indexList(raw_data)  # Assuming Show_indexList function is available
    selected_numbers = [index_list.index(title) for title in selected_titles]
    draft = Create_Draft(raw_data, index_list, selected_numbers, edited_text)  # Assuming Create_Draft function is available
    return {"draft": draft}

# Assuming you will have a similar function to show the final draft
