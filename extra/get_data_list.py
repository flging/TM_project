from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

def extract_text_with_location(pdf_path, page_numbers):
    for page_number, page_layout in zip(page_numbers, extract_pages(pdf_path, page_numbers=page_numbers)):
        print(f"Processing Page: {page_number + 1}")  # 페이지 번호는 1부터 시작하는 것으로 표시
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = element.get_text().replace('\n', '')  # 개행 문자 제거
                bbox_int = tuple(int(coord) for coord in element.bbox)  # 위치 정보 정수 변환
                font_name = font_size = font_color = "Unknown"  # 초기값 설정
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            font_name = character.fontname
                            font_size = round(character.size, 2)  # 소수점 두 자리로 폰트 크기 반올림
                            font_color = character.graphicstate.ncolor if character.graphicstate else "Unknown"
                            break  # 첫 글자의 정보만을 사용
                    break  # 첫 텍스트 라인의 첫 글자에서 정보를 얻음

                print(f"Text: {text}")
                print(f"Location: {bbox_int}")
                print(f"Font: {font_name}, Size: {font_size}")
                print(f"Color: {font_color}")

pdf_path = '2023 Integrated Report_Kor.pdf'  # PDF 파일 경로를 여기에 입력하세요
page_numbers = [5, 5]  # 정보를 추출하고자 하는 페이지 번호
extract_text_with_location(pdf_path, page_numbers)
