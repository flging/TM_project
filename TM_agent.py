from openai import OpenAI

client = OpenAI()

def get_draft(extracted_text,index,raw_data):
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": """
        To create an ESG report, you will provide text from a previous report and current data. Based on these, along with referencing the appropriate GRI index, please draft an ESG report.
Please Write Draft In Korean. 
        """},
        {"role": "user", "content": f''' 
previous report:{extracted_text}, GRI index:{index}, raw_data:{raw_data}
'''}
    ]
    )
    return response.choices[0].message.content