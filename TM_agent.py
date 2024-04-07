from openai import OpenAI

client = OpenAI()

def get_draft(extracted_text,index,raw_data):
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": """
        @@As an ESG report consultant, you should prepare draft of ***Raw Data-GRI Index Matching*** updates to the ***Previous Report Content***.


@@Updating Task Description
Updating Task's Main Goal is delivering aspect of Changing Degree and New Creation in the comparison of before & after of Company's GRI Index related behavior.
Therefore, you'd better focus on this main goal while making draft of ***Raw Data-GRI Index Matching*** updates to the ***Previous Report Content***.


@@While drafting, do's and don'ts are listed below. 
[Do's]
- Properly Include Quantified Contents 
- Contents Based on verifiable, objective metrics
- What the company is doing specifically to address the issue in the relevant GRI Index-related activity, how much and how it plans to do so in the future
- elaborate more on actions and add detailed contents.

[Don'ts]
- Vague Contents
- Contents Based on qualitative indicators
- Rhetorical words such as hard, committed, strategically, company-wide, etc.
- Including specific GRI Index number in the answer


@@Also, please refer to the example of a good and bad update draft below for your drafting assignment.
(Good update draft)
"Hilton Hotels is committed to doubling our investment in social impact and halving our environmental footprint by 2030 through responsible hospitality across our value chain. Doubling our investment in social impact means contributing to the development of the communities in which our hotels are located, which we do by actively collaborating with local businesses, purchasing from local companies, actively hiring local residents and providing vocational training to local students and young adults. To make this happen, we have increased our budget by more than 10 per cent each year for the past five years since 2016, and will spend more than twice as much by 2030 as we did in 2016. (middle) With the goal of reducing our environmental footprint by more than half in 2030 compared to 2016, we have increased our share of renewable energy by more than 5 per cent each year for the past five years, and reduced water use by more than 5 per cent per hotel each year. At this rate, we will be on track to achieve our goal by 2030." 

(Bad update draft)
"OOOO is committed to implementing ESG management by pooling efforts across the organisation. We have established an ESG Committee under the Board of Directors, a dedicated ESG team, and are conducting ESG management training for all employees to internalise ESG management. (Medium) In the environmental area, we are working to reduce greenhouse gas emissions and minimise waste across our business value chain, and in the social area, we are working to strengthen human and labour rights, fair operations, and consumer protection."


@@Please only provide updated drafts in your response, as well as your suggestions for narrative and photographic ideas that convey the context and background of each draft.
[Answer Format]
**Draft**
**narrative and photographic ideas**



@@Please do your best to complete the draft ESG report. You should *Answer in Korean*.
        """},
        {"role": "user", "content": f''' 
previous report:{extracted_text}, GRI index:{index}, raw_data:{raw_data}
'''}
    ], temperature=2, top_p=0
    )
    return response.choices[0].message.content