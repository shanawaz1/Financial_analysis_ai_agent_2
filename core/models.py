from functools import lru_cache


@lru_cache(maxsize=1)
def get_nlp():
    import spacy
    import transformers

    transformers.logging.set_verbosity_error()
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("sentencizer")
    return nlp


@lru_cache(maxsize=1)
def get_summarizer():
    from transformers import pipeline

    return pipeline("summarization", model="knkarthick/MEETING_SUMMARY")


@lru_cache(maxsize=1)
def get_fin_model():
    from transformers import pipeline

    return pipeline(
        "sentiment-analysis",
        model="yiyanghkust/finbert-tone",
        tokenizer="yiyanghkust/finbert-tone",
    )


@lru_cache(maxsize=1)
def get_fls_model():
    from transformers import pipeline

    return pipeline(
        "text-classification",
        model="yiyanghkust/finbert-fls",
        tokenizer="yiyanghkust/finbert-fls",
    )