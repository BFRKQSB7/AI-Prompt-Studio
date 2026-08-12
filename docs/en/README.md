# SD Prompt Converter

[**中文**](../README.md) | **English**

Converts Chinese prompts (free-form scene descriptions, NSFW welcome) into **explicit English Stable Diffusion prompts**. Single-file, zero dependencies, runs in the browser.

## Features

- **Tag flow** (NoobAI / Pony / Manhwa): Danbooru tags + `masterpiece, best quality, newest, absurdres` quality prefix
- **Natural-language flow** (RealVis / Juggernaut): `RAW photo`-led natural-language prompt + camera/lens/lighting words
- **NSFW directness slider** (conservative / standard / direct / very direct)
- **Built-in explicit dictionary** as knowledge base — matched words use standard English, no euphemisms
- **Auto negative prompt**: local models fill a universal default; online models generate a matching negative in real time
- **Multiple backends**: local llama / OpenAI / DeepSeek / custom (OpenAI-compatible)

## Quick Start

1. Download `index.html`, open it in a browser (no install)
2. Pick a "model source" → fill Base URL / model / key → type a Chinese prompt → click convert
3. Copy the result into SD WebUI / ComfyUI

## Backends

| Backend | Config | Notes |
|---------|--------|-------|
| **Local llama** | Base URL `http://127.0.0.1:4001/v1` | start an OpenAI-compatible llama-server locally (e.g. Qwen3-4B) |
| **OpenAI** | official API | fill in a key |
| **DeepSeek** | official API | fill in a key |
| **Custom** | any OpenAI-compatible endpoint | e.g. the opencode gateway (below) |

### Using the opencode API (needs a local proxy)

The opencode gateway **`https://opencode.ai/zen/go/v1`** sends no CORS headers, so a browser page can't call it directly. Use the bundled local proxy:

```bash
# set a key (or use the opencode default auth file — the proxy reads it automatically)
set OPENCODE_API_KEY=sk-...
# start the proxy (default port 7898)
python opencode_proxy.py
```

Then in "custom": Base URL `http://127.0.0.1:7898/v1`, model `deepseek-v4-flash`, any key.

> Reasoning models (Qwen3-4B / deepseek-v4-flash, etc.) "think" first — the page disables thinking and raises the token budget automatically.

## Negative prompt

- **Local models** (heavy load): auto-fill a universal default negative (`easynegative, bad-hands, ...`)
- **Online models**: generate a matching negative in real time from the positive prompt

## Online use

This project is hosted on GitHub Pages: **https://bfrkqsb7.github.io/sd-prompt-converter/**

- **OpenAI / DeepSeek**: work directly on the hosted page (official APIs send CORS headers)
- **Local llama / opencode**: cannot be reached from the hosted page (CORS / browser private-network restrictions) — download `index.html` (+ `opencode_proxy.py`) and open locally for full functionality

## License

MIT
