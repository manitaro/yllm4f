#!/usr/bin/env python3
from metrics.nlp import nlp_pipe


def flesch_reading_ease(sentence, language=None):
    return {"de": flesch_reading_ease_german,}.get(
        language or "en", flesch_reading_ease_english
    )(sentence)


def flesch_reading_ease_english(sentence):
    """
    >>> def test(sentence):
    ...     value, grade = flesch_reading_ease_english(sentence)
    ...
    ...     return f'{value:.2f} {grade}'
    ...
    >>> test('Test')
    '121.22 5th grade'
    >>> test('I love my cat')  # Pharaonin wird mit 3 statt 4 Silben erkannt
    '118.18 5th grade'
    >>> test('This is fairly complicated.')  # Cleo wird nur mit 1 statt 2 Silben erkannt
    '33.58 10th to 12th grade'
    >>> test('''
    ...    Let's check if it works for multiple sentences as well.
    ...    To check it we need a second sentence.
    ...    A third sentence also does not harm.
    ...    complex words with multiple syllables result in a higher reading complexity.
    ... ''')
    '67.76 7th grade'
    """
    tokens = list(nlp_pipe("en")(sentence))
    syllables = sum(token._.syllables_count for token in tokens if token._.syllables_count)
    words = max(1, len(list(token.text for token in tokens if token._.syllables_count)))
    sentences = max(1, len(list(nlp_pipe("en")(sentence).sents)))
    value = 206.835 - 1.015 * words / sentences - 84.6 * syllables / words

    return value, to_grade(value)


def flesch_reading_ease_german(sentence):
    """
    >>> def test(sentence):
    ...     value, grade = flesch_reading_ease_german(sentence)
    ...
    ...     return f'{value:.2f} {grade}'
    ...
    >>> test('Test')
    '120.50 5th grade'
    >>> test('Caesar osculierte die Pharaonin Cleopatra zwischen den Pyramiden affektiv.')  # Pharaonin wird mit 3 statt 4 Silben erkannt
    '15.00 college'
    >>> test('Caesar küsst Cleo zu Hause.')  # Cleo wird nur mit 1 statt 2 Silben erkannt
    '93.10 5th grade'
    >>> test('''
    ...    Ich muss zur Arbeit gehen.
    ...    Ich fahre mit meinem Auto zur Arbeit.
    ...    Ich mag Latein.
    ...    Ist heute Wochenende?
    ...    Ich esse kein Gemüse!
    ...    Wie alt bist du?
    ... ''')
    '86.29 5th grade'
    """
    tokens = list(nlp_pipe("de")(sentence))
    syllables = sum(token._.syllables_count for token in tokens if token._.syllables_count)
    words = max(1, len(list(token.text for token in tokens if token._.syllables_count)))
    sentences = max(1, len(list(nlp_pipe("de")(sentence).sents)))
    value = 180 - words / sentences - 58.5 * syllables / words

    return value, to_grade(value)


def to_grade(value):
    last_grade = "5th grade"
    for score, grade in {
        80: "6th grade",
        70: "7th grade",
        60: "8th & 9th grade",
        50: "10th to 12th grade",
        30: "college",
        10: "college graduate",
        0: "professional",
    }.items():
        if score <= value:
            return last_grade
        last_grade = grade
    assert False, f"negative flesch-reading-ease is not allowed ({value})"
