from flask import Flask, request, jsonify
from TM_find_page import find_gri_pages
from TM_agent_getindex import get_index
from TM_extract_text import extract_text_from_pages
from TM_agent import get_draft
from Indextranslate import translate
import json

app = Flask(__name__)

pdf_path = "TM_noRAG/2023 Integrated Report_Kor.pdf"  # 전기보고서 첨부 경로


@app.route('/create_draft', methods=['POST'])
def create_draft():
    raw_data = request.json['raw_data']
    selected_numbers = request.json['selected_numbers']

    index_list = show_index_list(raw_data)
    draft = create_draft_from_raw_data(raw_data, index_list, selected_numbers, pdf_path)

    return jsonify({"draft": draft})


def show_index_list(raw_data):
    index_list = json.loads(get_index(raw_data))
    return index_list


def create_draft_from_raw_data(raw_data, index_list, selected_numbers, pdf_path):
    draft = []
    for number in selected_numbers:
        disclosure_num = index_list[number]['disclosure_num']
        pages = find_gri_pages(pdf_path, disclosure_num)
        if type(pages) == list:
            extracted_pages = extract_text_from_pages(pdf_path, pages)
        else:
            extracted_pages = ["no page in previous report"]
        for extracted_page in extracted_pages:
            small_draft = [pages, disclosure_num]
            small_draft.append(get_draft(extracted_page, disclosure_num, raw_data))
        draft.append(small_draft)
    return draft


@app.route('/get_gri_titles', methods=['POST'])
def get_gri_titles():
    raw_data = request.json['raw_data']
    index_list = show_index_list(raw_data)
    title_list = get_gri_title(index_list)
    return jsonify({"titles": title_list})


def get_gri_title(index_list):
    title_list = []
    for index in index_list:
        gri = index['disclosure_num']
        gri_title = translate(gri)
        title_list.append(gri_title)
    return title_list


if __name__ == '__main__':
    app.run(debug=True)
