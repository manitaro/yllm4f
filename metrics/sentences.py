from metrics.nlp import nlp_pipe


def sentences(sentence, language):
    """
    >>> sentences('Test', 'en')
    1
    >>> sentences('Computer', 'de')
    1
    >>> sentences('Also as a sentence', 'en')
    1
    >>> sentences('''
    ...    Works also on multiple sentences.
    ...    To prove, here is sentence two.
    ... ''', 'en')
    1
    >>> sentences('''
    ...    Could work with commas, points, ... . Does not count every dot as new sentence.
    ... ''', 'en')
    2
    >>> sentences('''
    ...    Works with normal sentences.
    ...    Does it work with question?
    ...    It should work with exclamations as well!
    ... ''', 'en')
    3
    """
    doc = nlp_pipe(language)(sentence)

    return len(list(doc.sents))
