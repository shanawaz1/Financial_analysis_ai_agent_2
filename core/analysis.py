import os
from functools import lru_cache

import numpy as np
import requests

from core.config import FLS_KEYWORDS
from core.models import get_fls_model, get_fin_model, get_nlp, get_summarizer


@lru_cache(maxsize=128)
def split_in_sentences(text):
    doc = get_nlp()(text)
    return [str(sent).strip() for sent in doc.sents]


def make_spans(text, results):
    results_list = [r["label"] for r in results]
    return list(zip(split_in_sentences(text), results_list))


def speech_to_text(audio_path):
    if audio_path is None:
        return "Please upload an audio file first."
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "GROQ_API_KEY is not set. Add it in your environment variables."
    try:
        with open(audio_path, "rb") as f:
            resp = requests.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {api_key}"},
                data={"model": "whisper-large-v3", "response_format": "json"},
                files={"file": (os.path.basename(audio_path), f)},
                timeout=120,
            )
        if resp.status_code != 200:
            return f"Transcription error ({resp.status_code}): {resp.text[:300]}"
        return resp.json().get("text", "")
    except Exception as e:
        return f"Error processing audio: {e}"


def summarize_text(text):
    if not text or not text.strip():
        return "No text provided."
    try:
        max_l = 1024
        truncated = text[:max_l] if len(text) > max_l else text
        resp = get_summarizer()(truncated)
        return resp[0]["summary_text"]
    except Exception as e:
        return f"Error during summarization: {e}"


def text_to_sentiment(text):
    if not text or not text.strip():
        return "No text provided."
    try:
        return get_fin_model()(text)[0]["label"]
    except Exception as e:
        return f"Error during sentiment analysis: {e}"


def fin_ext(text):
    if not text or not text.strip():
        return []
    try:
        results = get_fin_model()(split_in_sentences(text))
        return make_spans(text, results)
    except Exception as e:
        return [("Error analyzing text", None)]


def fls(text):
    if not text or not text.strip():
        return []
    try:
        results = get_fls_model()(split_in_sentences(text))
        return make_spans(text, results)
    except Exception as e:
        return [("Error analyzing text", None)]


def fin_ner(text):
    if not text or not text.strip():
        return []
    try:
        doc = get_nlp()(text)
        entities = []
        for ent in doc.ents:
            if ent.label_ == "ORG" and len(ent.text) > 2:
                entities.append((ent.start_char, ent.end_char, "COMPANY"))
            elif ent.label_ in ("GPE", "LOC"):
                entities.append((ent.start_char, ent.end_char, "LOCATION"))

        output = []
        last_end = 0
        for start, end, label in sorted(entities, key=lambda x: x[0]):
            if start > last_end:
                output.append((text[last_end:start], None))
            output.append((text[start:end], label))
            last_end = end
        if last_end < len(text):
            output.append((text[last_end:], None))
        return output
    except Exception as e:
        return [(f"Error extracting entities: {e}", None)]


def keyword_boost(text, probs, mode="fls"):
    if not any(kw in text.lower() for kw in FLS_KEYWORDS):
        return probs
    if mode == "fls":
        fls_prob = probs[1]
        if fls_prob < 0.5:
            boosted = np.array(probs, dtype=float)
            boosted[1] = min(fls_prob + 0.3, 1.0)
            boosted[0] = max(probs[0] - 0.3, 0.0)
            return boosted.tolist()
        return probs
    pos_prob = probs[0]
    if pos_prob < 0.5 and len(probs) >= 2:
        boosted = np.array(probs, dtype=float)
        boosted[0] = min(pos_prob + 0.3, 1.0)
        boosted[1] = max(probs[1] - 0.3, 0.0)
        return boosted.tolist()
    return probs
