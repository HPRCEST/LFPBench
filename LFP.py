from openai import OpenAI
from tqdm import tqdm
import json

with open("extraction_evidence_washed2.json", mode='r', encoding='utf-8') as f:
    evidences = json.load(f)

with open("extraction_annoted.json", mode='r', encoding='utf-8') as f:
    data = json.load(f)

assert len(evidences) == len(data)

OpenAI.api_key = "api_key"

client = OpenAI(api_key = "api_key")

query = '''
请分析上面案件的原告诉求和证据列表，输出站在法庭立场上对案件基本事实的忠实描述；
只输出事实认定结果，不要添加任何推理过程和解释：
'''

query2 = '''
你是一名具备丰富法律知识和丰富审判经验的法官，请你遵循以下4个步骤，根据我提供的信息，最终输出一个5行、2列的表格：

提供的信息：
[原告诉求]
[案件当事人]
[证据列表]

你应当遵循的步骤如下：
步骤1：根据[原告诉求]中的内容，确定原告应当对哪些事实负担举证责任。
步骤2：分析[证据列表]中提到的证据，确定双方提出的每个证据属于：当事人陈述、书证、物证、视听资料、电子数据、证人证言、鉴定意见、勘验笔录中的哪一种，并明确提出证据的是原告还是被告。
步骤3：根据[原告诉求]中的内容，以一个中立的、具备法律知识和丰富审判经验的法官的视角，从真实性、合法性和关联性三个维度，评价原告、被告提出的证据能否被采信。你可以从证据是否是虚构、或者伪造的，来判断证据的真实性；你可以从证据是否是偷拍、透露、威胁胁迫的所形成的，来判断证据的合法性；你可以从证据是否与待证明的事实有关，来判断证据的关联性。如果某一证据不具有合法性或者真实性之一，则可以直接否定这一证据，但是关联性只涉及证明力大小的问题。
步骤4：结合证据真实性、合法性、关联性三个维度，如果证据足以证明待证事实的存在具有“高度可能性”的，就可以认定该事实存在。

输出的表格请遵循以下形式：
第一行的两列分别是：“待证事实”，和，依据步骤一得到的具体待证事实
第二行的两列分别是：“证据种类”，和，依据步骤二得到的每个证据具体的种类
第三行的两列分别是：“证据三性”，和，依据步骤三得到的对每个证据三性的逐一进行判断，明确每个证据是否真实、是否合法、是否有关联。
第四行的两列分别是：“案件事实”，和，依据步骤四得到的每个证据证明的内容，不具有真实性或者合法性的证据也要写明“排除”。
第五行：根据被证明的事实，输出详细的事实认定结果。事实认定结果应当包含：案件的时间、人物、时间和结果等作用于案件判决的信息。
'''

query3 = '''
上面提供了一个案件在庭审前提交的原告诉求和证据列表，请你输出站在法庭立场上对案件基本事实的忠实描述；
你要一步步描述你的思考过程，理清思路，仔细分析原、被告提交的证据及其证明目的，以评估原告的诉求是否可以得到支持；
注意，你的任务是辅助法官作出最后的判决，所以请提供你的分析而不是给出最终结果。
'''

query4 = '''
请分析上面案件的原告诉求和证据列表，输出站在法庭立场上对案件基本事实的忠实描述；
请你一步步描述你的思考过程，理清思路，并在最后认定一个客观的事实，但不要作出具体的判决。
认定的事实中如有主观推测的部分，需要加以说明。
'''

answers = {}

for e in tqdm(evidences):
    number = e[-1]
    e_list = e[:-1]
    prompt = "[原告诉求]\n"
    for i,a in enumerate(data[number]["诉求列表"]):
        prompt += f"（{i+1}）{a}\n"
    prompt += "[案件当事人]\n"
    prompt += data[number]["当事人"]
    prompt += "[证据列表]\n"
    #e_list.reverse()
    for i,e in enumerate(e_list):
        #prompt += f"（{i+1}）\n证据提交方：{e['证据提交方']}\n证据名称：{e['证据名称']}\n具体内容：{e['具体内容']}\n证明目的：{e['证明目的']}\n"
        prompt += f"（{i+1}）\n证据提交方：{e['证据提交方']}\n证据内容：{e['证据内容']}\n"
    prompt += query
    #print(prompt)
    #break
    messages=[
        {"role": "system", "content": "你是一个中国大陆的法官，你会综合原、被告提交的证据和原告的诉求客观公正地认定案件事实。"},
        {"role": "user", "content": prompt}
    ]
    try:
        completion = client.chat.completions.create(
            model="claude-3-5-sonnet-20241022",
            messages=messages
        )
        answers[number] = completion.choices[0].message.content
    except:
        break

with open("LFP_claude_evi2.json", mode='w', encoding='utf-8') as f:
    json.dump(answers, f, ensure_ascii=False, indent=4)
