import fitz  # PyMuPDF
from pdfminer.high_level import extract_text

def extract_text_if_no_graph(pdf_path, pages):
    # PyMuPDF를 사용하여 PDF 열기
    doc = fitz.open(pdf_path)
    text_pages = []

    for page_num in pages:
        # 페이지 번호는 0부터 시작하므로 조정
        page = doc.load_page(page_num - 1)
        # 페이지에서 이미지 리스트 가져오기
        img_list = page.get_images(full=True)
        # 페이지에서 드로잉 명령어(벡터 그래픽 포함) 가져오기
        drawing_commands = page.get_drawings()

        # 이미지나 드로잉 명령어가 없는 경우에만 텍스트 추출
        if not img_list and not drawing_commands:
            text = extract_text(pdf_path, page_numbers=[page_num - 1])
            text_pages.append(text)
        else:
            text_pages.append(None)

    return text_pages

# 사용 예시
pdf_path = 'TM/2023 Integrated Report_Kor.pdf'
pages = [5,6,7]  # 추출하려는 페이지 번호 목록
texts = extract_text_if_no_graph(pdf_path, pages)
print(texts)
