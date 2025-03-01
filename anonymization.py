import spacy
import json
from tqdm import tqdm
nlp = spacy.load("zh_core_web_lg")

def detect_persons(text):
    doc = nlp(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return list(set(persons))

with open("extraction_evidence_washed2.json", mode='r', encoding='utf-8') as f:
    evidences = json.load(f)

'''keys = ["案件名称", "当事人", "原告诉称", "被告辩称", "证据信息", "本院查明", "本院认为", "裁判结果", "案件类型"]
for i, l in enumerate(tqdm(labels)):
    all_str = "\n".join([l[k] for k in keys]) + "\n" + "\n".join(l["诉求列表"])
    persons, p2a = detect_persons(all_str), {}
    for j, p in enumerate(persons):
        p2a[p] = f"<person{j+1}>"
    for k in keys:
        for p in persons:
            labels[i][k] = labels[i][k].replace(p, p2a[p])
    for k, _ in enumerate(labels[i]["诉求列表"]):
        for p in persons:
            labels[i]["诉求列表"][k] = labels[i]["诉求列表"][k].replace(p, p2a[p])'''

for i, elist in enumerate(tqdm(evidences)):
    all_str = "\n".join([e["证据内容"] for e in elist[:-1]])
    persons, p2a = detect_persons(all_str), {}
    for j, p in enumerate(persons):
        p2a[p] = f"<person{j+1}>"
    for j, _ in enumerate(elist[:-1]):
        for p in persons:
            evidences[i][j]["证据内容"] = evidences[i][j]["证据内容"].replace(p, p2a[p])

with open("extraction_evidence_annoy.json", mode='w', encoding='utf-8') as f:
    json.dump(evidences, f, ensure_ascii=False, indent=4)
