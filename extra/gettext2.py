
# 엑셀 파일 경로
file_path = '(한솔홀딩스_BDO) 정성데이터(원고) 검토_작성_취합 Template_24.03.08.xlsx'

import pandas as pd

# 엑셀 파일 경로

# 특정 시트 읽기 (시트 이름으로)
# df_sheet1 = pd.read_excel(file_path, sheet_name='Sheet1')

# # 특정 시트 읽기 (시트 인덱스로)
# df_sheet2 = pd.read_excel(file_path, sheet_name=1)

# 모든 시트 읽기
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names  # 모든 시트 이름을 리스트로 가져오기
dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in sheet_names}

# # 첫 번째 시트의 내용 출력
# print(df_sheet1)

# # 두 번째 시트의 내용 출력
# print(df_sheet2)

# 모든 시트의 내용 출력
for sheet_name, df in dfs.items():
    print(f"Sheet name: {sheet_name}")
    print(df)
