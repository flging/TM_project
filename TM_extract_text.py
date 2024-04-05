import fitz  # PyMuPDF

def extract_text_from_pages(pdf_path, page_numbers):
    """
    PDF 파일에서 지정된 여러 페이지들의 텍스트를 추출합니다.

    :param pdf_path: PDF 파일의 경로
    :param page_numbers: 텍스트를 추출할 페이지 번호들의 리스트 (0부터 시작)
    :return: 각 페이지의 텍스트를 담은 리스트
    """
    # PDF 파일 열기
    doc = fitz.open(pdf_path)
    
    # 추출된 텍스트를 저장할 리스트
    pages_text = []
    
    for page_number in page_numbers:
        # 각 페이지의 텍스트 추출하고 리스트에 추가
        page_text = doc[page_number-1].get_text()
        pages_text.append(page_text)
    
    # PDF 문서 닫기
    doc.close()
    
    return pages_text

# # 사용 예시
# pdf_path = 'TM_noRAG/2023 Integrated Report_Kor.pdf'
# page_numbers = [5, 6]  # 추출할 페이지 번호 리스트 (예: 첫 번째, 세 번째, 다섯 번째 페이지)
# texts = extract_text_from_pages(pdf_path, page_numbers)

# for i, text in enumerate(texts):
#     print(f"Page {page_numbers[i]} Text:\n{text}\n---\n")
