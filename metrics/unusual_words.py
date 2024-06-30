from metrics.nlp import nlp_pipe


def unusual_words(sentence, language):
    """
    >>> unusual_words('Test', 'en')
    []
    >>> unusual_words('Caesar osculierte die Pharaonin Cleopatra zwischen den Pyramiden affektiv.', 'de')
    [{'word': 'Pharaonin', 'frequency on wikipedia': 1}]
    >>> unusual_words('Caesar küsst Cleo zu Hause.', 'de')
    []
    >>> unusual_words('''
    ...    Ich muss zur Arbeit gehen.
    ...    Ich fahre mit meinem Auto zur Arbeit.
    ...    Ich mag Latein.
    ...    Ist heute Wochenende?
    ...    Ich esse kein Gemüse!
    ...    Wie alt bist du?
    ...    Aber Schifffahrtskapitän ist ein kompliziertes Wort.
    ... ''', 'de')
    [{'word': 'fahre', 'frequency on wikipedia': 8}, {'word': 'kompliziertes', 'frequency on wikipedia': 7}]
    >>> unusual_words("Let's guess what are complicated words in english.", 'en')  # cause "english" it needs to be upper case
    [{'word': 'english', 'frequency on wikipedia': 3}]
    """
    tokens = list(nlp_pipe(language)(sentence))

    word_frequencies = get_word_frequency(language)

    result = {token.text: word_frequencies[token.text] for token in tokens if word_frequencies.get(token.text, 1000) < 10}
    return list({"word": word, "frequency on wikipedia": frequency} for word, frequency in result.items())


def get_word_frequency(language):
    def all_words(lines):
        for line in lines:
            _idx, word, frequency = line.split("\t")

            yield word, int(frequency)

    def is_good_word(word):
        return all(c.isalpha() for c in word)

    with open(f"/wordcorpus/{language}/words.txt", "r", encoding="utf-8") as file:
        return {word: frequency for word, frequency in all_words(file.read().splitlines(keepends=False)) if is_good_word(word)}
