#!/usr/bin/env python3
"""Parse PROMPTS.md into prompts.json with auto category (kanban column) + tags."""
import re, json

txt = open("PROMPTS.md", encoding="utf-8").read()
blocks = re.findall(r'## (.+?)\n\n```(?:md)?\n(.*?)\n```', txt, re.S)

# Ordered category rules -> first match wins. (column label, [keywords])
CATEGORY_RULES = [
    ("Development & Code", ["developer","code","javascript","python","sql","css","html","regex","git","terminal","console","api","programm","debug","software engineer","devops","docker","kubernetes","linux","compiler","framework","react","backend","frontend","stack overflow","solidity","smart contract"]),
    ("Data & AI", ["prompt","machine learning","data scien","dataset","neural","llm","gpt","midjourney","stable diffusion","ai ","artificial intelligence","analytics","statistic"]),
    ("Language & Translation", ["translat","pronunciation","language","english teacher","spoken","accent","synonym","etymolog","linguist"]),
    ("Career & Interview", ["interview","recruiter","resume","cv","career","cover letter","hiring","job "]),
    ("Business & Marketing", ["marketing","advertis","seo","sales","startup","business","brand","product manager","investor","pitch","ecommerce","social media","copywriter","ceo","consultant"]),
    ("Writing & Content", ["writer","write","story","poet","essay","novel","screenwriter","journalist","blog","editor","proofread","content","author","script","narrat"]),
    ("Education & Learning", ["teacher","tutor","instructor","explain","student","math","physics","chemistry","history","professor","educat","exam","study","learn"]),
    ("Health & Lifestyle", ["doctor","therap","diet","nutrition","fitness","mental","psycholog","health","medical","yoga","wellness","coach","trainer","remedy","fashion","chef","recipe","travel"]),
    ("Roleplay & Fun", ["act as a character","roleplay","game","dungeon","rapper","comedian","magician","santa","fun","joke","meme","astrolog","wizard","fictional"]),
    ("Productivity & Tools", ["assistant","planner","schedule","note","email","spreadsheet","excel","calculator","converter","organiz","productiv","summar"]),
]

# tag keyword map: keyword substring -> tag label
TAG_MAP = {
    "python":"python","javascript":"javascript","typescript":"typescript","sql":"sql","css":"css","html":"html",
    "react":"react","regex":"regex","git":"git","docker":"docker","kubernetes":"kubernetes","linux":"linux",
    "terminal":"terminal","api":"api","code":"coding","developer":"coding","debug":"debugging","solidity":"blockchain",
    "smart contract":"blockchain","data scien":"data-science","machine learning":"ml","neural":"ml","analytics":"analytics",
    "statistic":"statistics","midjourney":"image-gen","stable diffusion":"image-gen","prompt":"prompt-eng",
    "translat":"translation","language":"language","pronunciation":"pronunciation","english":"english",
    "interview":"interview","resume":"career","cv":"career","career":"career","cover letter":"career","recruiter":"hiring",
    "marketing":"marketing","seo":"seo","sales":"sales","startup":"startup","business":"business","brand":"branding",
    "advertis":"advertising","social media":"social-media","copywriter":"copywriting","investor":"finance","pitch":"pitch",
    "writer":"writing","write":"writing","story":"storytelling","poet":"poetry","essay":"essay","novel":"fiction",
    "screenwriter":"screenwriting","journalist":"journalism","blog":"blogging","editor":"editing","proofread":"editing",
    "teacher":"teaching","tutor":"teaching","explain":"explainer","math":"math","physics":"physics","chemistry":"chemistry",
    "history":"history","exam":"exam","study":"study",
    "doctor":"health","therap":"therapy","diet":"nutrition","nutrition":"nutrition","fitness":"fitness","mental":"mental-health",
    "psycholog":"psychology","medical":"medical","chef":"cooking","recipe":"cooking","travel":"travel","fashion":"fashion",
    "game":"games","roleplay":"roleplay","comedian":"comedy","joke":"comedy","astrolog":"astrology",
    "assistant":"assistant","email":"email","excel":"spreadsheet","spreadsheet":"spreadsheet","schedule":"planning",
    "summar":"summary","productiv":"productivity","legal":"legal","law":"legal","finance":"finance","accountant":"finance",
    "music":"music","song":"music","art":"art","design":"design","ux":"design","ui":"design",
}

def categorize(title, body):
    t = (title + " " + body).lower()
    for label, kws in CATEGORY_RULES:
        if any(k in t for k in kws):
            return label
    return "Other"

TAG_RE = {kw: re.compile(r'\b' + re.escape(kw) + r'', re.I) for kw in TAG_MAP}

def tag(title, body):
    t = title + " " + body
    tags = set()
    for kw, lab in TAG_MAP.items():
        if TAG_RE[kw].search(t):
            tags.add(lab)
    return sorted(tags)

items = []
seen = set()
for title, body in blocks:
    title = title.strip()
    key = title.lower()
    if key in seen:      # dedupe repeated titles
        continue
    seen.add(key)
    items.append({
        "title": title,
        "prompt": body.strip(),
        "category": categorize(title, body),
        "tags": tag(title, body),
    })

# column order
COLS = [c for c, _ in CATEGORY_RULES] + ["Other"]
data = {"columns": COLS, "count": len(items), "prompts": items}
json.dump(data, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False)
# also emit data.js so index.html works offline via double-click (file:// blocks fetch)
with open("data.js", "w", encoding="utf-8") as f:
    f.write("window.PROMPTS_DATA=")
    json.dump(data, f, ensure_ascii=False)
    f.write(";")

from collections import Counter
print("total cards:", len(items))
print("by column:")
c = Counter(i["category"] for i in items)
for col in COLS:
    print(f"  {col}: {c.get(col,0)}")
alltags = Counter(t for i in items for t in i["tags"])
print("distinct tags:", len(alltags))
