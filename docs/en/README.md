# AI Prompt Studio

[**中文**](../README.md) | **English**

![](https://img.shields.io/badge/version-v1.2.0-blue)

Converts Chinese prompts (free-form scene descriptions, NSFW welcome) into English prompts. Single-file, zero dependencies, runs in the browser:

- **🎨 SDXL image**: explicit English Stable Diffusion prompts (tag flow / natural-language flow) + negative prompts
- **🎬 H3 video**: MiniMax H3 structured English prompts (T2VA / I2VA / FL2VA / L2VA / Ref2VA × drama / action / 9-grid)

## Features

- **Tag flow** (NoobAI / Pony / Manhwa): Danbooru tags + `masterpiece, best quality, newest, absurdres` quality prefix
- **Natural-language flow** (RealVis / Juggernaut): `RAW photo`-led natural-language prompt + camera/lens/lighting words
- **Prompt-library reference**: curated library (347 embedded common tags, default) / full library (167k tags, lazy-loads `prompt-db.js`, searched in browser memory only — does NOT consume model context)
- **Auto negative prompt**: both local and online models generate a matching negative in real time; falls back to a universal default on failure
- **H3 video prompts**: generation mode (T2VA text / I2VA first-frame / FL2VA first+last / L2VA last-frame / Ref2VA references) × content style (drama / action / 9-grid), outputs the official structured format (3 fields for base modes, 6 sections for Ref2VA), with built-in H3 NSFW field experience (age + face features, Asian facial features, capped soundscape, explicit out-of-frame exits, etc.)
- **NSFW directness slider** (conservative / standard / direct / very direct)
- **Built-in explicit dictionary** as knowledge base — matched words use standard English, no euphemisms
- **Multiple backends**: local llama / OpenAI / DeepSeek / custom (OpenAI-compatible); online sources show official sites + risk disclaimer
- **Responsive**: auto-scales on phone / desktop

## Quick Start

1. Download `index.html` (plus `prompt-db.js` in the same folder if you use the full library), open it in a browser
2. Pick a "model source" → fill Base URL / model / key → type a Chinese prompt → click convert
3. Switch tabs at the top: 🎨 SDXL or 🎬 H3
4. Copy the result into SD WebUI / ComfyUI / the MiniMax H3 workflow

## Backends

| Backend | Base URL | Notes |
|---------|----------|-------|
| **Local llama** | `http://127.0.0.1:4001/v1` | start an OpenAI-compatible llama-server locally (e.g. Qwen3-4B) |
| **OpenAI** | official API | get a key at https://platform.openai.com |
| **DeepSeek** | official API | get a key at https://platform.deepseek.com |
| **Custom** | any OpenAI-compatible endpoint | e.g. the opencode gateway (below) |

> ⚠️ Online sources send your prompts (including NSFW/private content) to third-party services, which may log or review them — use at your own risk. API keys are stored only in your browser (localStorage).
>
> Context suggestion: SDXL ≥8192, H3 ≥8192 (the negative prompt is also model-generated). The full library (167k tags) is searched in browser memory only — it does not consume model context.

### Using the opencode API (needs a local proxy)

The opencode gateway **`https://opencode.ai/zen/go/v1`** sends no CORS headers, so a browser page can't call it directly. Use the bundled local proxy:

```bash
# 1. open opencode_proxy.py and put your key into API_KEY = "" at the top
#    (leave it empty to auto-read the opencode auth file ~/.local/share/opencode/auth.json or the env var OPENCODE_API_KEY)
# 2. start the proxy (default port 7898)
python opencode_proxy.py
```

Then in "custom": Base URL `http://127.0.0.1:7898/v1`, model `deepseek-v4-flash`, any key.

> Reasoning models (deepseek-v4-flash, etc.) "think" first — the page disables thinking and raises the token budget automatically.

## Prompt-library reference

- **Curated (default)**: 347 embedded common tags (quality / hair / expression / figure / clothing / pose / scene / style / NSFW / realism words), works offline.
- **Full library**: 167k tags (general descriptors + series + character names, types 0/3/4 from the "AI 绘画提示词超市" full dataset). First use fetches `prompt-db.js` (~7.6MB) from the network, then searches in browser memory; each request sends only the ≤80 matched tags to the model — it does not consume model context.

## H3 video prompts

- **Generation mode** (input type): T2VA text (quick test / atmosphere clip), I2VA first-frame start, FL2VA first+last interpolation, L2VA last-frame reverse-inference, Ref2VA character consistency + voice timbre + lip-sync.
- **Content style**: drama (relationship turn / dialogue), action (high-density combat, built-in rhythm budgets), 9-grid (3×3 storyboard — first generates the storyboard image prompt, then derives the video prompt from the actual grid).
- Outputs the official structured format: 3 fields for base modes (`integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music`), 6 sections for Ref2VA, including alignment lines. Reference images are described in text — no upload needed.

## Negative prompt

- Both local and online models generate a matching negative in real time; falls back to a universal default (`easynegative, bad-hands, ...`) on failure or empty output.

## Online use

This project is hosted on GitHub Pages: **https://bfrkqsb7.github.io/sd-prompt-converter/**

- **OpenAI / DeepSeek**: work directly on the hosted page (official APIs send CORS headers)
- **Local llama / opencode / full library**: cannot be reached from the hosted page (CORS / browser private-network restrictions) — download `index.html` + `prompt-db.js` (+ `opencode_proxy.py`) and open locally for full functionality

## License

MIT
