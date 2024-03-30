import pdfplumber
import re

def find_gri_pages(pdf_path, gri_value):
    pages_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages_text += page.extract_text() + "\n"
    
    pattern = rf"{gri_value}.*?(\d+~\d+|\d+|해당사항 없음)"
    match = re.search(pattern, pages_text, re.DOTALL)

    if match:
        matched_text = match.group(1)
        if "해당사항 없음" in matched_text:
            return "해당사항 없음"
        else:
            return matched_text 
    else:
        return "GRI 값에 해당하는 페이지를 찾을 수 없습니다."

# # 함수 사용 예제
# pdf_path = "TM/2023 Integrated Report_Kor.pdf"  
# gri_value = "GRI 2-1"  
# print(find_gri_pages(pdf_path, gri_value))
