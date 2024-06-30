#!/usr/bin/env python3
from metrics.nlp import nlp_pipe


def syllables(sentence, language):
    """
    >>> syllables('Test', 'en')
    1
    >>> syllables('Computer', 'de')
    3
    >>> syllables('Also as a sentence', 'en')
    6
    >>> syllables('''
    ...    Works also on multiple sentences.
    ...    To prove, here is sentence two.
    ... ''', 'en')
    16
    """
    tokens = list(nlp_pipe(language)(sentence))

    return sum(token._.syllables_count or 0 for token in tokens)
