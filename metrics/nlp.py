from functools import lru_cache as cache
import spacy
from spacy_syllables import SpacySyllables  # noqa: F401 pylint: disable=unused-import
from spacy_lefff import LefffLemmatizer
from spacy.language import Language


@Language.factory("french_lemmatizer")
def create_french_lemmatizer(nlp, name):  # pylint: disable=unused-argument
    return LefffLemmatizer()


@cache
def nlp_pipe(language):
    by_language = {
        "de": "de_core_news_lg",
        "en": "en_core_web_lg",
        "fr": "fr_core_news_lg",
        "nl": "nl_core_news_sm",
    }

    nlp = spacy.load(by_language[language])
    if language == "fr":
        nlp.add_pipe("french_lemmatizer", name="tagger")
    nlp.add_pipe("syllables", after="tagger")
    return nlp
