import pdfplumber
import re

def find_gri_pages(pdf_path, gri_value):
    
    pages_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages_text += page.extract_text() + "\n"
    
    pattern = rf"{gri_value}.*?((?:(?!1|2|3\b)\d+(?:(?:~|, )\d+)*)|해당사항 없음)"
    match = re.search(pattern, pages_text, re.DOTALL)

    if match:
        matched_text = match.group(1)
        if "해당사항 없음" in matched_text:
            return "해당사항 없음"
        else:
            parts = matched_text.split(',')
            numbers = []

            for part in parts:
                # Trim spaces and check if the part represents a range
                part = part.strip()
                if '~' in part:
                    # If part is a range, split it by '~' and convert both ends to integers
                    start, end = map(int, part.split('~'))
                    # Add all numbers in the range to the list, including both ends
                    numbers.extend(range(start, end + 1))
                else:
                    # If part is a single number, convert it to integer and add to the list
                    numbers.append(int(part))

            return numbers
    else:
        return "GRI 값에 해당하는 페이지를 찾을 수 없습니다."
        
    input_string = page_str(pdf_path, gri_value)
    # Split the input string by commas to process each part separately
    



# # 함수 사용 예제
# pdf_path = "TM/2023 Integrated Report_Kor.pdf"  
# gri_value = "GRI 305-1"  
# print(find_gri_pages(pdf_path, gri_value))
