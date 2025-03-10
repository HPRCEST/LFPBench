from openai import OpenAI
from tqdm import tqdm
import json

with open("extraction_annoted.json", mode='r', encoding='utf-8') as f:
    data = json.load(f)

with open("extraction_evidence_washed2.json", mode='r', encoding='utf-8') as f:
    evidences = json.load(f)

OpenAI.api_key = "api_key"

client = OpenAI(api_key = "api_key")

query = '''
[案件类型]
（略）
[当事人]
（略）
[证据列表]
（1）（略）
（2）（略）
（3）（略）
[诉求列表]
（1）（略）
（2）（略）
（3）（略）
[判决列表]
[
    0,
    1,
    -1
]
上面提供了输入的格式示例，现在你需要根据[证据列表]中各方提交的证据，预测对原告[诉求列表]的判决结果，并形成一个一一对应的判决列表。
[判决列表]是一个由（0,1,-1）三种数字组成的列表，如果你认为法院会完全支持这条诉求，结果就为1，如果部分支持，结果为0，驳回诉求则填入-1。
你只需要输出格式化的判决列表，不要添加任何注释。
'''

query2 = '''
[案件类型]
（略）
[当事人]
（略）
[证据列表]
（1）（略）
（2）（略）
（3）（略）
[诉求列表]
（1）（略）
（2）（略）
（3）（略）
[判决列表]
[
    0,
    1,
    -1
]
上面提供了输入的格式示例，现在你需要根据[证据列表]中各方提交的证据，预测对原告[诉求列表]的判决结果，并形成一个一一对应的判决列表。
[判决列表]是一个由（0,1,-1）三种数字组成的列表，如果你认为法院会完全支持这条诉求，结果就为1，如果部分支持，结果为0，驳回诉求则填入-1。
请你一步步描述你的思考过程，理清思路，并在最后输出一个像上面这样的判决列表。
'''

responses = []

for i, d in enumerate(tqdm(data)):
    if d["事实确认"] == "":
        fact = d["本院查明"]
    else:
        fact = d["事实确认"]
    prompt = query + "[案件类型]\n" + d["案件类型"] + "\n[当事人]\n" + d["当事人"]
    prompt += "[证据列表]\n"
    e_list = evidences[i][:-1]
    for i,e in enumerate(e_list):
        #prompt += f"（{i+1}）\n证据提交方：{e['证据提交方']}\n证据名称：{e['证据名称']}\n具体内容：{e['具体内容']}\n证明目的：{e['证明目的']}\n"
        prompt += f"（{i+1}）\n证据提交方：{e['证据提交方']}\n证据内容：{e['证据内容']}\n"
    prompt += "[诉求列表]\n[\n    " + "\n    ".join(d["诉求列表"]) + "\n]\n[判决列表]\n"
    completion = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=[
            {"role": "system", "content": "你是一个中国大陆的法学专家，你会熟练地按当地法律处理相关文本。"},
            {"role": "user", "content": prompt}
        ]
    )
    responses.append(completion.choices[0].message.content)

with open("LJP_with_evi2_claude.json", mode='w', encoding='utf-8') as f:
    json.dump(responses, f, ensure_ascii=False, indent=4)
