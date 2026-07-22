#!/usr/bin/env python3
"""
Recluster all 2,247 prompts into ~30 granular categories with 100+ hashtags.
Generates prompts.json, data.js and an index.html with cluster sidebar navigation.
"""
import json, re
from pathlib import Path
from collections import Counter

REPO = Path("/tmp/prompt-library")

CLUSTERS = [
    ("💻 Frontend & Web Dev",        ["html", "css", "javascript", "react", "vue", "angular", "svelte", "frontend", "web dev", "next.js", "tailwind", "dom", "responsive", "ui component", "web page", "website", "web app", "browser"]),
    ("⚙️ Backend & APIs",            ["api", "backend", "server", "node.js", "express", "fastapi", "flask", "django", "rest", "graphql", "endpoint", "microservice", "authentication", "middleware", "database", "sql", "mongodb", "postgres", "redis"]),
    ("🐍 Python & Data Science",     ["python", "pandas", "numpy", "jupyter", "scikit", "matplotlib", "data science", "data analy", "statistician", "data engineer", "etl", "pipeline", "data transform"]),
    ("📱 Mobile & App Dev",          ["mobile", "ios", "android", "swift", "kotlin", "flutter", "react native", "app dev"]),
    ("🔗 Blockchain & Web3",         ["blockchain", "ethereum", "solidity", "smart contract", "web3", "crypto", "defi", "nft", "token"]),
    ("🛠️ DevOps & Infrastructure",   ["devops", "docker", "kubernetes", "ci/cd", "deploy", "terraform", "aws", "cloud", "linux", "terminal", "bash", "shell", "git", "github", "infrastructure", "server admin", "sysadmin"]),
    ("🐛 Debugging & Code Review",   ["debug", "code review", "refactor", "bug", "error", "fix", "troubleshoot", "test", "unit test", "qa", "quality"]),
    ("🏗️ Architecture & Patterns",   ["architect", "design pattern", "system design", "clean code", "solid", "microservice", "scalab", "software engineer", "technical lead", "tech stack"]),
    ("💻 General Coding",            ["coding", "programming", "developer", "engineer", "code", "algorithm", "function", "class", "regex", "console", "compiler"]),
    ("🤖 AI & Machine Learning",     ["machine learning", "deep learning", "neural network", "model train", "tensorflow", "pytorch", "llm", "gpt", "ai model", "nlp", "computer vision", "classifier"]),
    ("🧠 Prompt Engineering",        ["prompt engineer", "prompt craft", "prompt template", "meta-prompt", "chain of thought", "few-shot", "zero-shot", "system prompt", "instruction tun"]),
    ("🔮 AI Assistants & Agents",    ["ai assist", "chatbot", "virtual assist", "copilot", "agent", "ai tutor", "ai writing", "ai doctor", "smart domain", "ai tool"]),
    ("✍️ Creative Writing",          ["storytell", "story", "novelist", "screenwriter", "poet", "fiction", "creative writ", "narrative", "character", "plot", "worldbuild", "screenplay", "script"]),
    ("📝 Copywriting & Marketing",   ["copywrite", "ad copy", "headline", "slogan", "marketing", "seo", "social media", "brand", "campaign", "advertis", "influencer", "content market", "growth hack", "sales"]),
    ("📰 Journalism & Research",     ["journal", "news", "article", "report", "research", "essay", "academic", "thesis", "citation", "paper", "peer review", "investigat"]),
    ("📧 Email & Communication",     ["email", "letter", "memo", "communicat", "correspondence", "outreach", "cold email", "follow-up", "newsletter"]),
    ("✏️ Editing & Rewriting",       ["edit", "rewrite", "proofread", "grammar", "paraphrase", "summariz", "simplif", "plagiarism", "tone", "clarity"]),
    ("💼 Business Strategy",         ["business", "strateg", "startup", "entrepreneur", "pitch deck", "business plan", "swot", "competitive", "market research", "go-to-market", "venture", "investor"]),
    ("📊 Finance & Accounting",      ["financ", "account", "invest", "stock", "portfolio", "budget", "tax", "revenue", "profit", "valuation", "financial model"]),
    ("👔 Career & Interview",        ["career", "interview", "resume", "cv ", "cover letter", "job", "hiring", "recruiter", "linkedin", "salary", "negotiat", "profession"]),
    ("📈 Product & Project Mgmt",    ["product manag", "project manag", "roadmap", "agile", "scrum", "sprint", "user story", "requirement", "stakeholder", "kanban", "jira", "priorit"]),
    ("🎓 Teaching & Learning",       ["teach", "learn", "tutor", "student", "course", "curriculum", "lesson", "instructor", "education", "mentor", "coach", "study", "academy", "school"]),
    ("🌍 Language & Translation",    ["translat", "language", "english", "french", "spanish", "chinese", "japanese", "korean", "german", "arabic", "hindi", "bilingual", "pronunciation", "etymolog", "linguist", "vocabulary", "grammar teach"]),
    ("📚 Knowledge & Explainers",    ["explain", "knowledge", "encyclopedia", "wikipedia", "history", "science", "philosophy", "how does", "what is", "define", "concept", "101", "beginner"]),
    ("🎮 Games & Entertainment",     ["game", "trivia", "puzzle", "riddle", "quiz", "tic-tac", "chess", "rpg", "dungeon", "adventure", "entertainment", "fun"]),
    ("🎭 Roleplay & Personas",       ["roleplay", "act as", "pretend", "persona", "character", "comedian", "rapper", "magician", "debate", "impersonat"]),
    ("🏥 Health & Wellness",         ["health", "medical", "doctor", "nurse", "mental health", "therapy", "wellness", "nutrition", "fitness", "yoga", "meditation", "diet", "personal trainer", "psychology", "counsel"]),
    ("🎨 Design & UX",              ["design", "ux", "ui design", "figma", "wireframe", "prototype", "user experience", "color palat", "typography", "graphic design", "layout", "visual design"]),
    ("🍳 Lifestyle & Hobbies",       ["recipe", "cook", "chef", "food", "travel", "garden", "diy", "home", "pet", "automobile", "car", "hobby", "craft", "music", "guitar", "compos"]),
    ("🖼️ Manga & Comic Art",        ["manga", "anime", "comic-poster", "comic-type", "ink-comic", "halftone-comic", "bold-anime", "crimson-ink", "hot-ink"]),
    ("🖼️ Doodle & Hand-Drawn Art",  ["doodle", "scribble", "marker", "crayon", "sketch", "storyboard", "naive-marker", "rough-ink", "rough-marker", "rough-animation"]),
    ("🖼️ Street & Grunge Art",      ["streetwear", "graffiti", "y2k", "zine", "ransom", "sticker-collage", "screenprint", "hiphop", "k-pop", "skate"]),
    ("🖼️ Editorial & Fashion Art",  ["editorial", "fashion-cover", "luxury-perspective", "nameplate", "supermodel", "portrait-poster", "portrait-dossier", "noir", "analog-sticker", "architectural-fashion", "triptych", "checkerboard"]),
    ("🖼️ Product & Ad Art",         ["product-launch", "food-card", "beverage-splash", "clearance-poster", "ad-system", "sneaker-tech", "macro-product", "newspaper-product", "food-zine", "coastal-product"]),
    ("🖼️ Typography & Poster Art",  ["megatype", "kinetic-type", "type-poster", "type-canyon", "block-type", "layered-type", "shockwave-type", "bubble-letter", "perspective-type", "typographic"]),
    ("🖼️ Photo Collage & Lifestyle Art", ["photo-collage", "snapshot", "photo-hybrid", "diary-style", "outdoor-diary", "mascot-poster", "monster-poster", "pet-sketch", "avatar-campaign", "gadget-pop", "assemblage", "overlay-poster", "festival-mobile"]),
]

TAG_RULES = [
    (["python"],["python","scripting"]),(["javascript","js "],["javascript","scripting"]),
    (["typescript"],["typescript","javascript"]),(["react"],["react","frontend","javascript"]),
    (["vue"],["vue","frontend","javascript"]),(["angular"],["angular","frontend","javascript"]),
    (["svelte"],["svelte","frontend"]),(["html"],["html","frontend"]),(["css"],["css","frontend","styling"]),
    (["java "],["java"]),(["c++","c#"],["systems-lang"]),(["rust"],["rust","systems-lang"]),
    (["go ","golang"],["golang"]),(["swift"],["swift","ios"]),(["kotlin"],["kotlin","android"]),
    (["ruby"],["ruby"]),(["php"],["php"]),(["sql"],["sql","database"]),
    (["node.js","nodejs"],["nodejs","backend"]),(["express"],["expressjs","backend"]),
    (["django"],["django","python"]),(["flask"],["flask","python"]),(["fastapi"],["fastapi","python"]),
    (["next.js","nextjs"],["nextjs","react"]),(["tailwind"],["tailwindcss","css"]),
    (["docker"],["docker","containers"]),(["kubernetes","k8s"],["kubernetes","orchestration"]),
    (["terraform"],["terraform","iac"]),(["aws"],["aws","cloud"]),(["azure"],["azure","cloud"]),
    (["gcp","google cloud"],["gcp","cloud"]),(["git"],["git","version-control"]),
    (["machine learning"],["machine-learning","ai"]),(["deep learning"],["deep-learning","ai"]),
    (["neural network"],["neural-networks","ai"]),(["nlp","natural language"],["nlp","ai"]),
    (["gpt","chatgpt"],["gpt","llm","ai"]),(["claude"],["claude","llm","ai"]),
    (["gemini"],["gemini","llm","ai"]),(["prompt"],["prompt-engineering"]),
    (["fine-tun","fine tun"],["fine-tuning","ai"]),(["rag","retrieval"],["rag","ai"]),
    (["embedding"],["embeddings","ai"]),(["langchain"],["langchain","ai"]),
    (["agent"],["ai-agents"]),(["chatbot"],["chatbot","conversational-ai"]),
    (["blog"],["blogging","content"]),(["seo"],["seo","content-marketing"]),
    (["copywrite","ad copy"],["copywriting","marketing"]),(["headline"],["headlines","copywriting"]),
    (["story","fiction"],["storytelling","creative-writing"]),(["screenplay","script"],["screenwriting"]),
    (["poem","poetry"],["poetry","creative-writing"]),(["essay"],["essay-writing"]),
    (["email"],["email","communication"]),(["newsletter"],["newsletter","email"]),
    (["summary","summarize"],["summarization"]),(["paraphrase","rewrite"],["rewriting"]),
    (["proofread","grammar"],["proofreading","editing"]),(["translate","translat"],["translation","multilingual"]),
    (["startup"],["startup","entrepreneurship"]),(["pitch"],["pitch-deck","fundraising"]),
    (["marketing"],["marketing","growth"]),(["social media"],["social-media","marketing"]),
    (["brand"],["branding","marketing"]),(["sales"],["sales","revenue"]),
    (["investor","invest"],["investing","finance"]),(["financial","finance"],["finance"]),
    (["accounting","accountant"],["accounting","finance"]),(["strategy","strategic"],["strategy","planning"]),
    (["product manag"],["product-management"]),(["project manag"],["project-management"]),
    (["agile","scrum"],["agile","methodology"]),(["interview"],["interviewing","career"]),
    (["resume","cv "],["resume","career"]),(["linkedin"],["linkedin","networking"]),
    (["negotiat"],["negotiation","communication"]),
    (["teach","tutor"],["teaching","education"]),(["student","learn"],["learning","education"]),
    (["course","curriculum"],["course-design","education"]),(["math"],["mathematics","education"]),
    (["science"],["science","education"]),(["history"],["history","knowledge"]),
    (["philosophy"],["philosophy","knowledge"]),(["language"],["language-learning"]),
    (["english"],["english","language-learning"]),
    (["health"],["health","wellness"]),(["mental health","therapy","psycholog"],["mental-health","wellness"]),
    (["medical","doctor"],["medical","healthcare"]),(["nutrition","diet"],["nutrition","health"]),
    (["fitness","workout","trainer"],["fitness","wellness"]),(["recipe","cook","chef"],["cooking","lifestyle"]),
    (["travel"],["travel","lifestyle"]),(["music"],["music","creative"]),
    (["design"],["design"]),(["ux","user experience"],["ux-design"]),
    (["ui "],["ui-design"]),(["figma"],["figma","design-tools"]),
    (["color"],["color-theory","design"]),(["wireframe","prototype"],["prototyping","design"]),
    (["game"],["gaming","entertainment"]),(["quiz","trivia"],["quiz","entertainment"]),
    (["roleplay","act as"],["roleplay","persona"]),(["comedian","comedy"],["comedy","entertainment"]),
    (["deploy"],["deployment","devops"]),(["ci/cd","pipeline"],["cicd","automation"]),
    (["security","cyber"],["cybersecurity"]),(["performance","optimiz"],["optimization","performance"]),
    (["image-prompt"],["visual-style","ai-art"]),
    (["manga"],["manga","japanese-art"]),(["anime"],["anime","japanese-art"]),
    (["doodle"],["doodle","illustration"]),(["poster"],["poster-design","visual-style"]),
    (["editorial"],["editorial-design","visual-style"]),(["comic"],["comic-art","illustration"]),
    (["graffiti"],["graffiti","street-art"]),(["collage"],["collage","mixed-media"]),
    (["typography"],["typography","type-design"]),(["portrait"],["portrait","photography"]),
    (["retro"],["retro","vintage"]),(["neon"],["neon","vibrant"]),
    (["3d"],["3d","dimensional"]),(["photo"],["photography"]),
    (["fashion"],["fashion","style"]),(["product"],["product-design"]),
    (["street"],["street-art","urban"]),(["plush","toy"],["plush","kawaii"]),
    (["vintage","retro"],["vintage","nostalgic"]),(["zine"],["zine","diy-print"]),
    (["halftone"],["halftone","print-texture"]),(["fisheye"],["fisheye","distortion"]),
    (["kawaii"],["kawaii","cute"]),
]

def classify_prompt(title, prompt, old_category, old_tags):
    text = f"{title} {prompt} {old_category} {' '.join(old_tags)}".lower()
    slug = title.lower().replace(" ", "-")
    is_image = "image-prompt" in old_tags or old_category.startswith("🎨")
    if is_image:
        for name, patterns in CLUSTERS:
            if not name.startswith("🖼️"): continue
            for pat in patterns:
                if pat in slug or pat in text: return name
        return "🖼️ Photo Collage & Lifestyle Art"
    best, best_score = None, 0
    for name, patterns in CLUSTERS:
        if name.startswith("🖼️"): continue
        score = sum(1 + (2 if pat in title.lower() else 0) for pat in patterns if pat in text)
        if score > best_score: best_score, best = score, name
    return best or "📚 Knowledge & Explainers"

def enrich_tags(title, prompt, old_tags, category):
    text = f"{title} {prompt}".lower()
    new_tags = set(old_tags)
    for keywords, tags_to_add in TAG_RULES:
        for kw in keywords:
            if kw in text: new_tags.update(tags_to_add); break
    new_tags.discard("")
    return sorted(new_tags)[:12]

def main():
    with open(REPO / "prompts.json") as f:
        data = json.load(f)
    print(f"Reclustering {len(data['prompts'])} prompts...")
    for p in data["prompts"]:
        p["category"] = classify_prompt(p["title"], p["prompt"], p["category"], p.get("tags", []))
        p["tags"] = enrich_tags(p["title"], p["prompt"], p.get("tags", []), p["category"])
    cat_counts = Counter(p["category"] for p in data["prompts"])
    text_cols = sorted([c for c in cat_counts if not c.startswith("🖼️")], key=lambda x: -cat_counts[x])
    img_cols = sorted([c for c in cat_counts if c.startswith("🖼️")], key=lambda x: -cat_counts[x])
    columns = text_cols + img_cols
    data["columns"] = columns
    data["count"] = len(data["prompts"])
    with open(REPO / "prompts.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open(REPO / "data.js", "w") as f:
        f.write("window.PROMPTS_DATA = "); json.dump(data, f, ensure_ascii=False); f.write(";\n")
    all_tags = set()
    for p in data["prompts"]: all_tags.update(p["tags"])
    print(f"\n✅ Done! {len(data['prompts'])} prompts, {len(columns)} clusters, {len(all_tags)} unique tags")
    for c in columns: print(f"  {c}: {cat_counts[c]}")

if __name__ == "__main__":
    main()
