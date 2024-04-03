from openai import OpenAI
client = OpenAI()

def get_index(raw_data):
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": """ ESG보고서를 작성하기 위해 GRI에 따라 데이터 가공을 할거야.  
         다음 기준 맞춰서 데이터 가공해줘.
         1. 반드시 데이터에 가장 적합한 5개의 disclosure_number를 정해.
         2. 각 disclosure_number마다 데이터와 관련해서 해당 번호를 고른 이유 설명해. (description)
         3. disclosure_number는 반드시 숫자-숫자의 형식으로 자세히 정해야 해. (GRI Number-number)의 형식으로 반드시 'GRI'가 숫자 앞에 붙어야 해. 
         4. disclosure_number의 Number는 반드시 다음 범위 안의 숫자여야 해. 200~400 또는 1~3.
         5. 다음과 같은 형식으로만 응답을 생성해:
         [{"disclosure_num": "GRI {Number-number}", "description": description }, {"disclosure_num": "GRI {Number-number}", "description": description },...].
    """},
        {"role": "user", "content": f"raw_data:{raw_data}"}
    ],
    temperature=0
    )
    return response.choices[0].message.content

# print(get_index("""직원 복지: 새로운 웰빙 프로그램을 도입하여 직원 만족도 점수가 20% 증가.
# """))