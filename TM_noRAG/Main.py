from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
from Indextranslate import translate
import json



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


# print(Create_Draft(raw_data, Show_indexList(raw_data),[0,1,2],pdf_path))


