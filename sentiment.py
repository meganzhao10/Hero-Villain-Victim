from textblob import TextBlob

def sentiment(word):
    '''
    Returns the sentiment of the given string as a float within
    the range [-1.0, 1.0]
    '''
    word_blob = TextBlob(word)
    return word_blob.sentiment.polarity

def similarity_to_role(word, role):
    similarity_total = 0
    if role == "hero":
        dict_length = len(hero_dict)
        for hero_term in hero_dict:
            similarity_total += similarity(word, hero_term) / dict_length
    else if role == "villain":
        dict_length = len(villain_dict)
        for villain_term in villain_dict:
            similarity_total += similarity(word, villain_term) / dict_length
    else if role == "victim":
        dict_length = len(victim_dict)
        for victim_term in victim_dict:
            similarity_total += similarity(word, victim_term) / dict_length
