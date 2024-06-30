from metrics.nlp import nlp_pipe


def complicated_words(sentence, language):
    """
    >>> complicated_words('Test', 'en')
    []
    >>> complicated_words('Caesar osculierte die Pharaonin Cleopatra zwischen den Pyramiden affektiv.', 'de')
    []
    >>> complicated_words('Caesar küsst Cleo zu Hause.', 'de')
    []
    >>> complicated_words('''
    ...    Ich muss zur Arbeit gehen.
    ...    Ich fahre mit meinem Auto zur Arbeit.
    ...    Ich mag Latein.
    ...    Ist heute Wochenende?
    ...    Ich esse kein Gemüse!
    ...    Wie alt bist du?
    ...    Aber Schifffahrtskapitän ist ein kompliziertes Wort.
    ... ''', 'de')
    []
    >>> complicated_words("Let's guess what are complicated words in english.", 'en')
    ['complicated']
    """
    tokens = list(nlp_pipe(language)(sentence))
    syllabel_limit = 5 if language == "de" else 3

    return list(set(token.text for token in tokens if (token._.syllables_count or 0) > syllabel_limit))
