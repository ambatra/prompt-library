# Prompt Library

A private, curated library of **2,247 reusable AI prompts** — text prompts *and* visual style prompts — kept for easy access, search, and continuous improvement.

## 🖥️ Live Board

**→ [Browse the Kanban board](https://ambatra.github.io/prompt-library/)**

A self-contained dark-mode Kanban board with:
- **Kanban & Grid views** — toggle between column layout and card grid
- **Text / Image / All filters** — switch between 2,148 text prompts and 99 visual style prompts
- **Live search** across titles, prompt text, tags, and categories
- **Tag chips** — click to filter; supports multi-tag intersection
- **Copy button** on every card — one click to clipboard
- **Image cards** — visual prompt styles show a 16:9 thumbnail preview
- **Expand modal** — click an image to see the full prompt, preview, and tags

## Collections

| Collection | Count | Source |
|-----------|-------|--------|
| 📝 Text Prompts | 2,148 | Curated from various prompt engineering resources |
| 🎨 Image Prompts | 99 | [AI Visual Prompt Cookbook](https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook) |

### Image Prompt Categories

| Category | Styles | Description |
|----------|--------|-------------|
| 🎨 Manga & Comic | 24 | Anime, manga dossiers, comic halftone, ink styles |
| 🎨 Doodle & Hand-Drawn | 24 | Marker, crayon, scribble, sketch, naive styles |
| 🎨 Editorial & Fashion | 22 | Luxury editorial, portraits, architectural, analog |
| 🎨 Street & Grunge | 12 | Y2K, streetwear, graffiti, zine, skate punk |
| 🎨 Product & Advertising | 7 | Food ads, product shots, beverage splash, sneaker tech |
| 🎨 Photo Collage & Lifestyle | 6 | Travel diaries, mascots, 3D avatars, photo overlays |
| 🎨 Bold Typography | 4 | Megatype, kinetic type, perspective lettering |

## Files

| File | Purpose |
|------|---------|
| `index.html` | Kanban board viewer (self-contained, dark mode) |
| `prompts.json` | All prompts as structured JSON (title, prompt, category, tags, image) |
| `data.js` | Same data as JS module for offline/local use |
| `PROMPTS.md` | Original text prompts in markdown |
| `images/` | 99 thumbnail previews for visual styles |
| `build.py` | Regenerate text prompts from `PROMPTS.md` |
| `build_image_prompts.py` | Merge image prompts from AI Visual Prompt Cookbook |

## How to Add Prompts

### Text prompts
1. Edit `PROMPTS.md` (follow the existing `<details>` pattern)
2. Run `python3 build.py` to refresh `prompts.json`

### Image prompt sources
1. Clone the source repo
2. Update `build_image_prompts.py` with new source paths
3. Run `python3 build_image_prompts.py` to merge

## Attribution

- [AI Visual Prompt Cookbook](https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook) by [@VigoCreativeAI](https://x.com/VigoCreativeAI) — MIT License
