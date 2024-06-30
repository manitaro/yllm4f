#!/usr/bin/env python3
from metrics.nlp import nlp_pipe


def words(sentence, language):
    """
    >>> words('Test', 'en')
    1
    >>> words('Caesar osculierte die Pharaonin Cleopatra zwischen den Pyramiden affektiv.', 'de')
    9
    >>> words('Caesar küsst Cleo zu Hause.', 'de')
    5
    >>> words('''
    ...    Ich muss zur Arbeit gehen.
    ...    Ich fahre mit meinem Auto zur Arbeit.
    ...    Ich mag Latein.
    ...    Ist heute Wochenende?
    ...    Ich esse kein Gemüse!
    ...    Wie alt bist du?
    ... ''', 'de')
    26
    """
    tokens = list(nlp_pipe(language)(sentence))

    return len(list(token.text for token in tokens if token._.syllables_count))
