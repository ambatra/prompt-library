# Prompt Library

> **⚠️ Disclaimer:** This is a **personal clone and aggregation** of prompts collected from various open-source repositories and community resources. **I do not claim ownership of any of the prompts** in this collection. All credit belongs to the original creators and communities listed below.

A personal, searchable collection of AI prompts — aggregated from open-source prompt libraries, restructured for easy retrieval via a Kanban-style board.

## 🙏 Credits & Sources

This library is built entirely from the work of others. Full attribution below:

| Source | Creator | What was used | License |
|--------|---------|---------------|---------|
| [AI Visual Prompt Cookbook](https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook) | [@VigoCreativeAI](https://x.com/VigoCreativeAI) | 99 structured visual/image prompt styles with preview images | MIT |
| Community prompt collections | Various contributors | ~2,148 text prompts across coding, writing, business, and more | Various / Public |

> If you are the creator of any prompt included here and would like it removed or attributed differently, please [open an issue](https://github.com/ambatra/prompt-library/issues).

## What This Repo Does

- **Aggregates** prompts from multiple open-source repos into one place
- **Restructures** them into searchable, categorized cards
- **Adds a Kanban board** (`index.html`) for visual browsing with search, tags, and copy-to-clipboard
- **Does not modify** the original prompts — only reorganizes and presents them

## 🖥️ Kanban Board

Open **`index.html`** or browse live at **[ambatra.github.io/prompt-library](https://ambatra.github.io/prompt-library/)** (if GitHub Pages is enabled):

- **2,247 prompts** — 2,148 text + 99 visual styles
- Kanban columns grouped by category
- 🎨 Image prompt cards show thumbnail previews
- Live search across titles, prompt text, and tags
- Click any tag chip to filter; click a card to expand
- **Copy** button on every card
- Toggle between Kanban and Grid views
- Filter by Text / Image / All

## Files

| File | Purpose |
|------|---------|
| `index.html` | Kanban board viewer (self-contained, dark mode) |
| `prompts.json` | All prompts as structured JSON |
| `data.js` | Same data as JS module for offline use |
| `PROMPTS.md` | Text prompts in markdown (source of truth) |
| `images/` | 99 thumbnail previews for visual styles (from AI Visual Prompt Cookbook) |
| `build.py` | Regenerate text prompts from `PROMPTS.md` |
| `build_image_prompts.py` | Merge image prompts from AI Visual Prompt Cookbook |

## License

This repo itself is for personal use. Individual prompts retain the licenses of their original sources:

- **AI Visual Prompt Cookbook** — [MIT License](https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook/blob/main/LICENSE)
- **Text prompts** — sourced from publicly available community collections

---

*This is a living collection. New prompt sources will be added and credited over time.*
