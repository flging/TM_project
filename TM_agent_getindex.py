from openai import OpenAI
client = OpenAI()

def get_index(raw_data):
    response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": """ You are a GRI Standards expert. Based on your best understanding of all indicators within the GRI Standards, please identify five GRI Standards indexes to which ***company interview content*** applies. 

[form of answer].
For each GRI Index, briefly state the key content of the GRI Index in **one sentence**, followed by the key reason for presenting the GRI Index in **one sentence**.

[Notes]
1) Do not include **GRI Indexes numbered in the 100s** in your answer as they are not applicable.
2) For more specific application, treat all Index numbers like example below and address the detailed guideline content.
@@example
GRI 403-3: 직업 건강 및 안전 관리 시스템
- 조직의 직업 건강 및 안전 관리 시스템에 대한 정보를 제공합니다.
- 안전 조회 번역 웹 구축은 직원들의 안전과 건강을 위한 정보 접근성을 높이는 조치로, 직업 건강 및 안전 관리 시스템의 일환으로 볼 수 있습니다.
@@

Try your best and **Answer in Korean**."""},
        {"role": "user", "content": f"raw_data:{raw_data}"}
    ],
    temperature=0
    )
    return response.choices[0].message.content

# print(get_index("""직원 복지: 새로운 웰빙 프로그램을 도입하여 직원 만족도 점수가 20% 증가.
# """))