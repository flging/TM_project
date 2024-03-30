# Parsing the given JSON string and selecting one of the `disclosure_num` values for each data entry
# Then adding the data to a dictionary under the selected `disclosure_num` as a key

import json

# Given JSON string
json_str = '''
[
    {"data":"DX의 업무 범위 : 홈페이지 내 소개자료 확인 / (ESG팀_자료요청) 홈페이지 링크", "disclosure_num":["102-1", "102-2", "102-7"]},
    {"data":"조직도", "disclosure_num":["102-18"]},
    {"data":"현장에서 발생하는 비효율적인 업무들을 개선하는 업무를 진행 중, 스프린트로 2/3개월 마디", "disclosure_num":["102-15", "103-2", "103-3"]},
    {"data":"119운영위원회 -리스크 관리 위원회 산하 (CEO/CFO 산하)", "disclosure_num":["102-18", "102-26", "102-30"]},
    {"data":"Dash-board 구축은 전사시스템 개편 진행시 포함될 예정", "disclosure_num":["102-9", "103-2"]},
    {"data":"안전 조회 번역 웹", "disclosure_num":["103-2", "403-1"]},
    {"data":"AI 자재 관리 어시스턴트", "disclosure_num":["103-2", "301-2"]},
    {"data":"현장에서 자재공급승인원을 제작하는 부분을 자동화하는 기능", "disclosure_num":["103-2", "301-2", "302-4"]},
    {"data":"DX/CX 관련 교육 진행", "disclosure_num":["103-2", "404-2"]}
]
'''

# Converting JSON string into Python object
data_list = json.loads(json_str)

# Dictionary to hold the processed data
diction = {}

# Iterating over the list to process each entry
for entry in data_list:
    # Selecting the first `disclosure_num` for simplicity
    selected_disclosure_num = entry["disclosure_num"][0]
    
    # Simplifying the disclosure_num to a more readable format, e.g., "102-1" becomes "2-1"
    simplified_key = selected_disclosure_num.split("-")[1] + "-" + selected_disclosure_num.split("-")[0]
    
    # Adding the data to the dictionary
    if simplified_key not in diction:
        diction[simplified_key] = [entry["data"]]
    else:
        diction[simplified_key].append(entry["data"])

print(diction)
