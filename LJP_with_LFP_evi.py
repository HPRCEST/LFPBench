from openai import OpenAI
from tqdm import tqdm
import json

with open("extraction_annoted.json", mode='r', encoding='utf-8') as f:
    data = json.load(f)

with open("LFP_claude_evi2.json", mode='r', encoding='utf-8') as f:
    data1 = json.load(f)

with open("extraction_evidence_washed2.json", mode='r', encoding='utf-8') as f:
    evidences = json.load(f)

OpenAI.api_key = "sk-agEcX3Su78Bu09c2F49978C6Ba424977B936C8710fAb42E0"

client = OpenAI(api_key = "sk-agEcX3Su78Bu09c2F49978C6Ba424977B936C8710fAb42E0")

query = '''
你需要参考[证据列表]中各方提出的证据和[参考事实]中模型提供的参考事实，预测法院对原告[诉求列表]的判决结果，并形成一个一一对应的判决列表。
[判决列表]是一个由（0,1,-1）三种数字组成的列表，如果你认为法院会完全支持这条诉求，结果就为1，如果部分支持，结果为0，驳回诉求则填入-1。
你只需要输出格式化的判决列表，不要添加任何注释。
'''

responses = []

for i, d in enumerate(tqdm(data)):
    if d["事实确认"] == "":
        fact = d["本院查明"]
    else:
        fact = d["事实确认"]
    prompt = query + "[案件类型]\n" + d["案件类型"] + "\n[当事人]\n" + d["当事人"]
    prompt += "[参考事实]\n" + data1[str(i)]
    #prompt += "[参考事实]\n" + fact
    prompt += "\n[证据列表]\n"
    e_list = evidences[i][:-1]
    e_list.reverse()
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

with open("LJP_with_LFP_evi2_claude_reverse.json", mode='w', encoding='utf-8') as f:
    json.dump(responses, f, ensure_ascii=False, indent=4)
    