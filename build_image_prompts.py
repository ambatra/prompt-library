#!/usr/bin/env python3
"""
Extract image prompts from AI-Visual-Prompt-Cookbook and merge into prompts.json.
Reclusters 99 styles into ~7 intuitive, balanced groups.
Copies thumbnail images into the repo.
"""
import json, os, re, shutil
from pathlib import Path

SOURCE = Path("/tmp/ai-visual-prompt-cookbook")
STYLES = SOURCE / "styles"
COPY_PROMPTS = SOURCE / "docs" / "copy-prompts"
THUMBS = SOURCE / "assets" / "thumbs"
REPO = Path("/tmp/prompt-library")
IMG_DIR = REPO / "images"

# Better clustering — balanced, intuitive groupings
CLUSTERS = {
    "Manga & Comic": {
        "keywords": ["manga", "anime", "comic", "ink-comic", "halftone-comic"],
        "styles": []
    },
    "Doodle & Hand-Drawn": {
        "keywords": ["doodle", "scribble", "marker", "crayon", "sketch", "storyboard",
                      "naive-marker", "rough-ink", "rough-marker", "rough-animation"],
        "styles": []
    },
    "Street & Grunge": {
        "keywords": ["street", "skate", "graffiti", "y2k", "zine", "ransom",
                      "sticker", "xerox", "screenprint", "hiphop", "k-pop",
                      "streetwear", "punk"],
        "styles": []
    },
    "Editorial & Fashion": {
        "keywords": ["editorial", "fashion", "luxury", "nameplate", "supermodel",
                      "portrait", "noir", "analog", "checkerboard", "architectural",
                      "triptych"],
        "styles": []
    },
    "Bold Typography": {
        "keywords": ["megatype", "kinetic-type", "type-poster", "type-canyon",
                      "block-type", "layered-type", "shockwave-type", "bubble-letter",
                      "perspective-type", "typographic", "neon-kinetic", "folded-diamond",
                      "court-photo-type", "sunburst"],
        "styles": []
    },
    "Product & Advertising": {
        "keywords": ["product", "food", "beverage", "clearance", "ad-style",
                      "ad-system", "grocer", "sneaker", "splash", "chrome-clearance",
                      "food-card", "food-zine", "hud-macro", "newspaper-product",
                      "coastal-product"],
        "styles": []
    },
    "Photo Collage & Lifestyle": {
        "keywords": ["collage", "snapshot", "photo-hybrid", "diary", "outdoor",
                      "companion", "home-life", "bedroom", "travel", "city",
                      "transit", "subway", "metro", "urban", "gallery",
                      "mascot", "monster", "pet", "cat-doodle", "fish-doodle",
                      "avatar", "3d", "plush", "toy", "gadget",
                      "cutout-poster", "assemblage", "overlay", "festival"],
        "styles": []
    },
}

def classify(slug, summary):
    text = f"{slug} {summary}".lower()
    for name, info in CLUSTERS.items():
        for kw in info["keywords"]:
            if kw in text:
                return name
    return "Photo Collage & Lifestyle"  # catch-all

def extract_prompt(md_text):
    m = re.search(r"```text\n(.*?)```", md_text, re.DOTALL)
    return m.group(1).strip() if m else ""

def main():
    IMG_DIR.mkdir(exist_ok=True)

    # Load existing data
    with open(REPO / "prompts.json") as f:
        data = json.load(f)

    # Get existing columns
    existing_cols = data["columns"]
    image_prompts = []

    slugs = sorted(d.name for d in STYLES.iterdir() if d.is_dir() and not d.name.startswith("."))
    print(f"Processing {len(slugs)} image styles...")

    for slug in slugs:
        # Read style.json
        jpath = STYLES / slug / "style.json"
        if not jpath.exists():
            continue
        with open(jpath) as f:
            sj = json.load(f)

        # Read copy prompt
        cppath = COPY_PROMPTS / f"{slug}.md"
        prompt_text = ""
        if cppath.exists():
            with open(cppath) as f:
                prompt_text = extract_prompt(f.read())

        title = sj.get("style_name", slug.replace("-", " ").title())
        summary = sj.get("style_summary", "")
        cluster = classify(slug, summary)

        # Copy thumbnail
        thumb_src = THUMBS / f"{slug}-16x9.jpg"
        thumb_name = f"{slug}.jpg"
        if thumb_src.exists():
            shutil.copy2(thumb_src, IMG_DIR / thumb_name)

        # Build tags from style metadata
        tags = ["image-prompt"]
        cat = sj.get("visual_deconstruction", {}).get("overall_style_category", "")
        if isinstance(cat, list):
            cat = " ".join(cat)
        for word in ["poster", "editorial", "manga", "comic", "doodle", "collage",
                      "typography", "portrait", "product", "fashion", "anime",
                      "3d", "photo", "zine", "grunge", "street", "vintage",
                      "neon", "minimal", "retro", "hand-drawn", "illustration",
                      "graffiti", "sticker", "plush", "kawaii"]:
            if word in slug or word in cat.lower() or word in summary.lower():
                tags.append(word)
        tags = list(dict.fromkeys(tags))[:8]  # dedupe, max 8

        image_prompts.append({
            "title": title,
            "prompt": prompt_text if prompt_text else summary,
            "category": f"🎨 {cluster}",
            "tags": tags,
            "image": f"images/{thumb_name}" if thumb_src.exists() else None,
            "summary": summary,
            "slug": slug,
        })

    # Add new columns for image categories
    image_cols = sorted(set(p["category"] for p in image_prompts))

    # Merge: existing text prompts + new image prompts
    all_prompts = data["prompts"] + image_prompts
    all_columns = existing_cols + image_cols

    merged = {
        "columns": all_columns,
        "count": len(all_prompts),
        "prompts": all_prompts,
    }

    with open(REPO / "prompts.json", "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    # Also write data.js
    with open(REPO / "data.js", "w") as f:
        f.write("window.PROMPTS_DATA = ")
        json.dump(merged, f, ensure_ascii=False)
        f.write(";\n")

    # Stats
    cluster_counts = {}
    for p in image_prompts:
        c = p["category"]
        cluster_counts[c] = cluster_counts.get(c, 0) + 1

    print(f"\n✅ Merged {len(image_prompts)} image prompts into {data['count']} existing prompts")
    print(f"   Total: {len(all_prompts)} prompts")
    print(f"\nImage prompt clusters:")
    for c, n in sorted(cluster_counts.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")

if __name__ == "__main__":
    main()
