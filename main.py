from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import shutil
import os

# Initialize FastAPI app
app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Function to save uploaded PDF file
def save_pdf(pdf: UploadFile):
    with open(f"temp/{pdf.filename}", "wb") as buffer:
        shutil.copyfileobj(pdf.file, buffer)

# Function to read raw data from text file
def read_raw_data(raw_data: UploadFile):
    content = raw_data.file.read()
    return content.decode("utf-8")

# Function to extract basic information from raw data
def process_raw_data(raw_data: str):
    # Example: parse raw data and extract interviewee and data name
    interviewee = "Example Interviewee"
    data_name = "Example Data"
    return interviewee, data_name

# Function to extract GRI titles from index list
def extract_gri_titles(index_list):
    gri_titles = [index['disclosure_num'] for index in index_list]  # Assuming 'disclosure_num' is the key for GRI titles
    return gri_titles[:5]  # Extract first 5 GRI titles

# Function to render PDF upload page
@app.get("/")
def read_root():
    return templates.TemplateResponse("upload_pdf.html", {"request": "request"})

# Endpoint to handle PDF upload
@app.post("/upload_pdf/")
async def upload_pdf(pdf: UploadFile = File(...)):
    save_pdf(pdf)
    return {"filename": pdf.filename}

# Endpoint to render raw data input page
@app.get("/input_raw_data/")
def read_raw_data_form():
    return templates.TemplateResponse("input_raw_data.html", {"request": "request"})

# Endpoint to handle raw data input
@app.post("/input_raw_data/")
async def input_raw_data(raw_data: UploadFile = File(...)):
    content = read_raw_data(raw_data)
    return {"raw_data_content": content}

# Endpoint to render raw data info input page
@app.get("/input_raw_data_info/")
def read_raw_data_info_form():
    return templates.TemplateResponse("input_raw_data_info.html", {"request": "request"})

# Endpoint to handle raw data info input
@app.post("/input_raw_data_info/")
async def input_raw_data_info(interviewee: str = Form(...), data_name: str = Form(...)):
    return {"interviewee": interviewee, "data_name": data_name}

# Endpoint to render GRI title selection page
@app.get("/select_gri_titles/")
def read_gri_titles(interviewee: str, data_name: str):
    # Mock index list, replace with actual data
    index_list = [{'disclosure_num': 'GRI1'}, {'disclosure_num': 'GRI2'}, {'disclosure_num': 'GRI3'}, {'disclosure_num': 'GRI4'}, {'disclosure_num': 'GRI5'}]
    gri_titles = extract_gri_titles(index_list)
    return templates.TemplateResponse("select_gri_titles.html", {"request": "request", "gri_titles": gri_titles})

# Endpoint to handle selected GRI titles
@app.post("/select_gri_titles/")
async def select_gri_titles(selected_titles: List[str]):
    return {"selected_titles": selected_titles}

# Endpoint to render text editing page
@app.get("/edit_text/")
def read_text_edit():
    # Mock text content, replace with actual data
    text_content = "Example text content"
    return templates.TemplateResponse("edit_text.html", {"request": "request", "text_content": text_content})

# Endpoint to handle edited text
@app.post("/edit_text/")
async def edit_text(text_content: str = Form(...)):
    return {"edited_text_content": text_content}

# Endpoint to render draft creation page
@app.get("/create_draft/")
def read_create_draft(selected_titles: List[str], interviewee: str, data_name: str):
    # Mock index list, replace with actual data
    index_list = [{'disclosure_num': 'GRI1'}, {'disclosure_num': 'GRI2'}, {'disclosure_num': 'GRI3'}, {'disclosure_num': 'GRI4'}, {'disclosure_num': 'GRI5'}]
    draft_data = []  # Replace with actual data
    return templates.TemplateResponse("create_draft.html", {"request": "request", "selected_titles": selected_titles, "interviewee": interviewee, "data_name": data_name, "index_list": index_list, "draft_data": draft_data})

# Endpoint to handle draft creation
@app.post("/create_draft/")
async def create_draft(selected_titles: List[str], interviewee: str, data_name: str, index_list: List[dict], draft_data: List[dict]):
    # Generate draft using selected GRI titles, interviewee, data name, index list, and draft data
    return {"draft_generated": True}

# Endpoint to render draft display page
@app.get("/display_draft/")
def read_display_draft():
    # Mock draft, replace with actual data
    draft = "Example draft"
    return templates.TemplateResponse("display_draft.html", {"request": "request", "draft": draft})
