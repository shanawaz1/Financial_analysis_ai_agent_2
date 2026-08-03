# CONTEXT — Financial Analyst AI Agent Deployment

This document records what this repo is, what we changed while getting it deployed, and why.

## What this project is

An AI agent (Gradio app) that analyzes financial audio and text:

- **Speech Recognition** — transcribes financial audio to text.
- **Summarization & Tone** — summarizes text and classifies financial sentiment.
- **In-depth Analysis** — financial tone spans, forward-looking statement (FLS) detection, named-entity recognition (companies/locations).
- **FLS Decision Plot / Global SHAP Summary** — SHAP-based explainability views.

Core stack: Gradio 3.50, Hugging Face `transformers`/`torch`, spaCy, shap, matplotlib.

## Why this repo exists (what we did)

The upstream repo (`shanawaz1/Financial_analysis_ai_agent`) ran only locally. We cloned it into a new repo (`Financial_analysis_ai_agent_2`) and made targeted changes to get it deployed on Render's **free tier**, without rewriting the app.

### 1. Deployment attempts
- **Vercel — failed.** Vercel only runs serverless functions (short-lived, no persistent server). Gradio needs a long-running web server, and the ML deps (torch/transformers) exceed Vercel's limits. Wrong platform for this app.
- **Hugging Face Spaces — free tier not available.** HF now requires PRO for Gradio/Docker Spaces on the free `cpu-basic` plan.
- **Render (free) — chosen.** Long-running Python web service. First attempts failed at startup; fixed below.

### 2. Fix: lazy-load heavy ML imports
Original `core/models.py` imported `spacy`/`transformers` (and transitively `torch`) at module import time, and `core/shap_utils.py` imported `shap`/`matplotlib` at import time. On Render's free tier (0.1 CPU, 512 MB), Gradio could not bind a port inside Render's startup scan window.

Change: moved all heavy imports **inside functions** so the Gradio server binds in seconds and torch/shap load only on first request.
- `core/models.py` — imports moved into `get_*()` functions.
- `core/shap_utils.py` — `shap`/`matplotlib` imported lazily inside functions.

### 3. Fix: pin the dependency stack Gradio 3.50.2 was built for
Render defaults to bleeding-edge Python/packages that broke Gradio 3.50.2:
- `altair 5.5.0` + Python 3.14 → `TypedDict` `closed=True` crash. Fixed by pinning `PYTHON_VERSION=3.12.9`.
- `starlette 1.3.1` / `jinja2 3.1.6` → `TypeError: unhashable type: 'dict'` on page render.
- `pydantic 2.13` → `AttributeError: 'FieldInfo' object has no attribute 'in_'` in fastapi 0.103.

Pinned in `requirements.txt` (versions compatible with Gradio 3.50.2):
```
fastapi==0.103.2
starlette==0.27.0
jinja2==3.1.2
uvicorn==0.23.2
pydantic==2.4.2
```
Also added `requests>=2.31.0` (used by the ASR API call) and removed `librosa`/`soundfile` (only the local whisper pipeline needed them).

### 4. Fix: ASR via Groq API instead of downloading whisper-large-v3
The original Speech Recognition downloaded `openai/whisper-large-v3` (~3 GB). On Render free (512 MB) it OOM-killed the app.

Change: `core/analysis.py` `speech_to_text()` now calls Groq's hosted `whisper-large-v3` API. Result: **full large-model accuracy with zero local RAM/disk cost**, works on free tier. Requires a free `GROQ_API_KEY` (set as a Secret env var in Render).

### 5. Fix: entrypoint
Added `run.py` — launches Gradio on `0.0.0.0` on Render's `PORT`. Render Start Command: `python run.py`.

### 6. UI polish
Replaced the broken light theme with a dark professional financial look (`ui/css.py`): navy gradient background, emerald buttons, styled tabs/inputs/scrollbar, and a proper logo in the page header (plain `<img>`, no Gradio download UI).

## Current status

- **Deployed & live:** https://financial-analysis-ai-agent-2.onrender.com (Render free tier).
- Auto-deploys on push to `main`.

## Known limits (free tier)

- Free instances spin down after inactivity; first load can take 1–2 min (cold start).
- Text-analysis tabs load finbert on first use (~400 MB) — borderline on 512 MB, may OOM under heavy use.
- Groq free tier is rate-limited (fine for demos).
- **Privacy:** audio is uploaded to Groq's servers — avoid sensitive financial recordings if that matters.

## Render configuration recap

| Setting | Value |
|---------|-------|
| Start Command | `python run.py` |
| Build Command | `pip install -r requirements.txt` |
| Env: `PYTHON_VERSION` | `3.12.9` |
| Env: `GROQ_API_KEY` | (Secret) free key from console.groq.com |

## Deploying to a fresh Render service

1. New Web Service → connect `shanawaz1/Financial_analysis_ai_agent_2`.
2. Set Start Command `python run.py`, Env `PYTHON_VERSION=3.12.9`, Secret `GROQ_API_KEY`.
3. Deploy (Clear build cache & deploy on first setup).
4. Open the service URL.
