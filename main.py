from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List
import shutil

# Initialize FastAPI app
app = FastAPI()

# Function to save PDF file
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

# Endpoint to handle PDF upload
@app.post("/upload_pdf/")
async def upload_pdf(pdf: UploadFile = File(...)):
    save_pdf(pdf)
    return JSONResponse(content={"message": "PDF uploaded successfully", "filename": pdf.filename})

# Endpoint to handle raw data input
@app.post("/input_raw_data/")
async def input_raw_data(raw_data: UploadFile = File(...)):
    raw_data_content = read_raw_data(raw_data)
    return JSONResponse(content={"message": "Raw data received successfully", "raw_data": raw_data_content})

# Endpoint to handle raw data info input
@app.post("/input_raw_data_info/")
async def input_raw_data_info(interviewee: str = Form(...), data_name: str = Form(...)):
    return JSONResponse(content={"message": "Raw data info received successfully", "interviewee": interviewee, "data_name": data_name})

# Endpoint to handle selected GRI titles
@app.post("/select_gri_titles/")
async def select_gri_titles(selected_titles: List[str]):
    return JSONResponse(content={"message": "Selected GRI titles received successfully", "selected_titles": selected_titles})

# Endpoint to handle edited text
@app.post("/edit_text/")
async def edit_text(text_content: str = Form(...)):
    return JSONResponse(content={"message": "Text content edited successfully", "text_content": text_content})

# Endpoint to handle draft creation
@app.post("/create_draft/")
async def create_draft(selected_titles: List[str], interviewee: str = Form(...), data_name: str = Form(...)):
    return JSONResponse(content={"message": "Draft created successfully", "selected_titles": selected_titles, "interviewee": interviewee, "data_name": data_name})

# Endpoint to display draft
@app.get("/display_draft/")
async def display_draft():
    draft = "Example draft"
    return JSONResponse(content={"draft": draft})

