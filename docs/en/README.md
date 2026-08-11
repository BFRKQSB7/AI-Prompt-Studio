# Realistic Prompt Generator v1.0.1

[**中文简体**](../../README.md) | **English**

A local, offline realistic-model prompt generator: **click slot phrases to auto-assemble a natural-language English prompt**. Single-file, zero-dependency, double-click to run.

## Compatible models

**RealVis XL V5.0 / Juggernaut v9** and other natural-language realistic models (they expect full sentences, not Danbooru tags). Complements the "AI Drawing Prompt Supermarket" (tag-style, for NoobAI / Manhwa).

## Related tool

Tag-based models (NoobAI / Manhwa)? Use the **AI Drawing Prompt Supermarket** (Danbooru tag point-and-assemble):

👉 [ai-prompt-supermarket](https://github.com/BFRKQSB7/ai-prompt-supermarket) · [online](https://bfrkqsb7.github.io/ai-prompt-supermarket/)

**When to go there**: your model is tag-based (NoobAI / Manhwa); this tool serves natural-language types (RealVis / Juggernaut).

## Features

- **Slot-based assembly**: 9 slots (8 positive + ⑨ negative words). Clicking phrases auto-assembles a coherent English prompt in fixed order; negatives are also clickable with sensible pre-selected defaults
- **Subcategories**: every slot has subcategory filters (e.g. clothing → dresses / tops / outerwear / nude…), easy to find
- **~500 curated phrases**: all with Chinese annotations, photography-oriented (lighting / lens / texture) to fit realistic models
- **NSFW support**: "nude / NSFW" under clothing and "seductive / NSFW" under action, for adult self-use
- **Weights**: right-click a phrase or chip to set `(phrase:1.2)` weight
- **Inspiration shuffle**: one click picks a random phrase per slot and assembles
- **Favorites**: ★ favorite phrases, persisted across sessions, with "favorites only" filter
- **Presets**: save / load favorite combinations
- **Drag reorder**: drag chips to change phrase order
- **Dark mode** + one-click copy for positive / negative (copy has a 3-tier fallback, works in any environment)

## Usage

Open `index.html`, pick a slot on the left, click phrases in the middle, and the prompt assembles at the top for one-click copy.

## Online (GitHub Pages)

**https://bfrkqsb7.github.io/realistic-prompt-generator/**

- The online version is identical to the local one (same `index.html`)
- The local version works offline (all data inlined, double-click to open)

## Changelog

### v1.1.0
- **Added**: subcategories — each slot filters by subcategory (e.g. clothing → dresses / tops / outerwear / nude…)
- **Added**: negative-words slot (⑨) — click to add to the negative box, with sensible pre-selected anti-artifact defaults
- **Added**: NSFW support — "nude / NSFW" under clothing, "seductive / NSFW" under action
- **Added**: phrase library expanded to ~500 (sharpness / texture / professions / poses and more)

### v1.0.1
- **Optimized**: dark mode by default (still toggleable to light with 🌓)
- **Optimized**: README adds a "Related tool" link (to the AI Drawing Prompt Supermarket)

### v1.0.0
- **Added**: first release — 8-slot natural-language prompt assembly + weights / shuffle / favorites / presets / dark mode / 3-tier copy fallback

## Notes

- Single-file HTML, all data inlined, works offline, ~30KB
- The phrase library covers adult-content categories; please comply with local laws and platform policies, and do not generate content involving minors
