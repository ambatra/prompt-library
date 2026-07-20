# Prompt Library

A private, curated library of reusable AI prompts kept for easy access, search, and continuous improvement.

## Kanban board (view + search + tags)
Open **`index.html`** — a self-contained kanban board:
- One card per prompt, grouped into columns by category.
- Live search across titles, prompt text, and tags.
- Click any tag chip to filter; click a card body to expand; **copy** button per card.
- If GitHub Pages is enabled: browse it live at `https://ambatra.github.io/prompt-library/`.

## Files
- `PROMPTS.md` - full collection (source of truth), one prompt per `<details>` section.
- `prompts.json` - parsed data (title, prompt, category, tags) that powers the board.
- `build.py` - regenerates `prompts.json` from `PROMPTS.md` (auto category + tags).
- `index.html` - the kanban viewer.

## Improve
1. Edit / add prompts in `PROMPTS.md` (follow the existing `<details>` pattern).
2. Run `python3 build.py` to refresh `prompts.json`.
3. Commit. The board picks up changes automatically.

Search locally too:
```bash
grep -i -A3 "translator" PROMPTS.md
```
