import fitz  # PyMuPDF
import re  # 정규 표현식 모듈

def find_page_number_left_of_text(pdf_path, page_number, target_text):
    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]
    
    text_instances = page.search_for(target_text)
    if not text_instances:
        return None
    
    first_instance = text_instances[0]
    x0, y0, x1, y1 = first_instance
    
    # 대상 텍스트 바로 좌측의 좁은 영역을 지정합니다.
    # 이 영역은 문서 레이아웃에 따라 조정이 필요할 수 있습니다.
    narrow_left_area = fitz.Rect(x0 - 50, y0, x0, y1)  # 예시로 좌측에 50 유닛을 설정
    
    # 지정된 영역 내의 텍스트를 추출합니다.
    left_text = page.get_text("text", clip=narrow_left_area).strip()
    
    # 숫자만 있는 텍스트를 추출하기 위한 정규 표현식
    page_number_match = re.search(r'\d+', left_text)
    
    if page_number_match:
        return page_number_match.group(0)  # 첫 번째 숫자 매칭 결과를 반환
    else:
        return None  # 숫자 텍스트를 찾지 못한 경우

# 사용 예
# pdf_path = 'TM/2023 Integrated Report_Kor.pdf'
# page_number = 3
# target_text = "GRI Standards"
# left_page_number = find_page_number_left_of_text(pdf_path, page_number, target_text)
# print(left_page_number)
