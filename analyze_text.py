import sys
import argparse
import json
from language.fasttext import detect_language
from metrics.flesch_reading_ease import flesch_reading_ease
from metrics.words import words
from metrics.syllables import syllables
from metrics.sentences import sentences

from metrics.complicated_words import complicated_words
from metrics.unusual_words import unusual_words


def analyze_text(text, language, use_llm):
    fre_score, fre_grade = flesch_reading_ease(text, language=language)
    result = {
        "language": language,
        "flesch-reading-ease": {
            "score": fre_score,
            "grade": fre_grade,
        },
        "statistics": {
            "sentences": sentences(text, language=language),
            "words": words(text, language=language),
            "syllables": syllables(text, language=language),
        },
        "complicated words": complicated_words(text, language=language),
        "unusual words": unusual_words(text, language=language),
    }

    if use_llm:
        from metrics.youth_language import youth_language
        from metrics.understandability import understandability
        from metrics.conciseness import conciseness

        result["youth language"] = youth_language(text, language=language)
        result["understandability"] = understandability(text, language=language)
        result["conciseness"] = conciseness(text, language=language)
    return result


def get_most_likely_language(languages):
    """
    >>> get_most_likely_language({'de': 0.89})
    'de'
    >>> get_most_likely_language({'de': 0.89, 'en': 0.5})
    'de'
    >>> get_most_likely_language({'de': 0.89, 'en': 0.92})
    'en'
    >>> get_most_likely_language({'de': 0.1, 'en': 0.2, 'fr': 0.3})
    'fr'
    """
    for language, _probability in sorted(list(languages.items()), key=lambda a: -a[1]):
        return language
    assert False, "no language found"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Text Analyzer",
        description="Check how readable your text is - especially for young people",
    )

    parser.add_argument("--language", type=str, default=None, help="the language the text is written in. If not provided language is determined.")
    parser.add_argument("--output", type=str, default="json", choices=["json", "text"], help="FOO!")
    parser.add_argument("--enable-llm", action="store_const", default=False, const=True, help="use an LLM to analyze the text")

    arguments = parser.parse_args()

    user_text = sys.stdin.read()
    analysis = analyze_text(
        text=user_text,
        language=arguments.language or get_most_likely_language(languages=detect_language(user_text)),
        use_llm=arguments.enable_llm,
    )

    if arguments.output == "json":
        print(json.dumps(analysis, indent=2, sort_keys=True))
    elif arguments.output == "text":

        def format_value(value, indent=0):
            if isinstance(value, dict):
                return "\n".join(
                    " " * indent + ("{:<" + str(30 - indent) + "}").format(k) + ("\n" if isinstance(v, (dict, list)) else ": ") + str(format_value(v, indent=indent + 2)) for k, v in value.items()
                )
            if isinstance(value, float):
                return f"{value:.2f}"
            if isinstance(value, list):

                def short_format(v):
                    def time_or_times(frequency):
                        if frequency == 1:
                            return f"{frequency} time on wikipedia"
                        return f"{frequency} times on wikipedia"

                    if isinstance(v, dict):
                        return f'{v["word"]} ({time_or_times(v["frequency on wikipedia"])})'
                    return str(v)

                return " " * indent + "- " + (("\n" + " " * indent + "- ").join(short_format(v) for v in value))
            return value

        print(format_value(analysis))
    else:
        assert False, f"unexpected output format ({arguments.output})"
