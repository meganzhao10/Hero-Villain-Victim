from nltk.corpus import wordnet as wn


def word_similarity(word_1, word_2):
    '''
    Returns the Wu-Palmer similarity between the given words.
    Values range between 0 (least similar) and 1 (most similar).
    '''
    a = wn.synsets(word_1)[0]
    b = wn.synsets(word_2)[0]
    return a.wup_similarity(b)
