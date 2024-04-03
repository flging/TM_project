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
         4. disclosure_number의 Number는 반드시 다음 범위 안의 숫자여야 해. 200~500 또는 1~4.
         5. 다음과 같은 형식으로만 응답을 생성해:
         [{"disclosure_num": "GRI {Number-number}", "description": description }, {"disclosure_num": "GRI {Number-number}", "description": description },...].
    """},
        {"role": "user", "content": f"raw_data:{raw_data}"}
    ],
    temperature=0
    )
    return response.choices[0].message.content

# print(get_index(""" ·GS건설의 고객경험혁신(CX)팀은 데이터 기반의 브랜드 관리에 중점을 두어 자이 고객의 브랜드 인식에 대 한 깊은 인사이트를 분석하고, 이를 바탕으로 브랜드 관리 전략의 로드맵을 수립하고 있으며 이를 통해 GS그 룹 내 다른 브랜드들과의 시너지를 발굴하여 브랜드 커뮤니케이션의 기획 및 중장기 전략 제안에 기여하고 있 습니다. 또한, 2024년 '자이 (Xi Re-Ignite)' 프로젝트를 통해 자이 브랜드를 재정의하고 시장 내 부정적 이슈 를 극복하려는 목적으로, 단순한 BI 디자인 변경을 넘어 고객들이 공감하고 사랑할 수 있는 새로운 브랜드 아 이덴티티를 찾아내고자 하고 있습니다. 이를 통해 통해 자이의 새로운 아이덴티티, BI 및 브랜드 디자인을 개 발하고, 이를 고객들에게 효과적으로 알릴 수 있는 커뮤니케이션 전략을 수립하여, 내외부 고객 모두가 공감 할 수 있는, 강화된 자이 브랜드를 재정립하는 것을 목표로 하고 있으며, 이는 지속 가능한 경영을 위한 핵심적 인 부분으로, 고객 경험의 혁신을 통해 브랜드 가치를 높이고자 합니다.
# """))