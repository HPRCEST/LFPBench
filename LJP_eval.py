import json

with open("LJP_with_fact_evi2_claude.json", mode='r', encoding='utf-8') as f:
    data = json.load(f)

with open("extraction_annoted.json", mode='r', encoding='utf-8') as f:
    labels = json.load(f)

tsum, csum, usum = 0, 0, 0
data1 = []

for i, d in enumerate(data):
    if d == "":
        data1.append([])
    else:
        d = d.replace("[判决列表]", "").replace("[诉求列表]", "")
        beg, end = d.find("["), d.find("]")
        s, t = d[beg:end+1], ""
        for c in s:
            if c in ["0", "-", "1", "[", "]", ","]:
                t += c
        try:
            data1.append(json.loads(t))
        except:
            print(i)
assert len(data) == len(data1)

for i, l in enumerate(labels):
    tsum += len(l["判决列表"])
    #if len(l["判决列表"]) == len(data1[i]):
    for j, label in enumerate(l["判决列表"]):
        try:
            if label == data1[i][j]:
                csum += 1
        except:
            pass

print(tsum)
print(csum)
print(csum / tsum)

reasons = ['婚约财产纠纷', '房屋租赁纠纷', '生命权身体权健康权纠纷', '继承纠纷', '追索劳动报酬', '侵权责任纠纷', '商品房预售合同纠纷', '买卖合同纠纷', '返还原物纠纷', '不当得利纠纷']
rr = {r:[0, 0] for r in reasons}
for i, l in enumerate(labels):
    rr[l["案件类型"]][0] += len(l["判决列表"])
    for j, label in enumerate(l["判决列表"]):
        try:
            if label == data1[i][j]:
                rr[l["案件类型"]][1] += 1
        except:
            pass

for r in rr:
    print(f"{r}: {rr[r][1] / rr[r][0]}")
