from TM_find_page import find_gri_pages
from TM_retrieve_RAG import retrieve_RAG
from pdfminer.high_level import extract_text

pdf_path = "TM/2023 Integrated Report_Kor.pdf"
raw_data = "단체 협약"
user_input = 0


input_list=retrieve_RAG(raw_data)
disclosure_number = input_list[user_input].split("\t")[1].split(" ")[1]
pages = find_gri_pages(pdf_path,disclosure_number)
text = extract_text(pdf_path, page_numbers=[int(page) - 1 for page in str(pages).split(",")])
print(text)
print(input_list[user_input],disclosure_number,pages)
#print(raw_data,text,input_list[user_input])
