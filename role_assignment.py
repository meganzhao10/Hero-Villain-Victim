from nltk import pos_tag, sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from entity_recognition import get_top_entities
from role_dictionaries import HERO_DICT, VILLAIN_DICT, VICTIM_DICT
from stop_words import STOP_WORDS
from functools import lru_cache

# pip3 install textblob
from textblob import TextBlob
# pip3 install news-please
# pip3 install newspaper3k
from newsplease import NewsPlease
from newspaper import Article
# pip install beautifulsoup4
# pip install lxml
# pip install html5lib
from bs4 import BeautifulSoup

IGNORE_POS = [
    "PRP",  # personal pronoun
    "PRP$",  # possessive pronoun
    "WP",  # wh-pronoun
    "WP$",  # possessive wh-pronoun
    "CC",  # coordinating conjunction
    "IN",  # preposition/subordinating conjunction
    "DT",  # determiner
    "WDT",  # wh-determiner
    "PDT",  # predeterminer
    "RP",  # particle
    "CD",  # cardinal digit
    "POS",  # possessive
    "UH",  # interjection
    "TO",  # to
    "LS",  # list marker
    "EX",  # existential there
    "FW",  # foreign word
]


def get_wn_pos(nltk_pos):
    '''
    Converts the given nltk part of speech to a word net part of speech
    '''
    if nltk_pos in ["NN", "NNS", "NNP", "NNPS"]:
        return wn.NOUN
    elif nltk_pos in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]:
        return wn.VERB
    elif nltk_pos in ["JJ", "JJR", "JJS"]:
        return wn.ADJ
    elif nltk_pos in ["RB", "RBR", "RBS", "WRB"]:
        return wn.ADV
    else:
        return None


# TODO Do we need to make words lowercase at any point in analysis???

def extract_by_newspaper(url):
    content = Article(url)
    content.download()
    content.parse()
    headline = content.title
    article = content.text
    return headline, article


def extract_by_newsplease(url):
    content = NewsPlease.from_url(url)
    headline = content.title
    article = content.text
    return headline, article


def extract_by_soup(url):
    content = BeautifulSoup(url, "lxml")
    headline = content.title.string
    articleList = list()
    for i in content.find_all("p"):
        articleList.append(i.get_text())
        # print(i.get_text())

    return headline, articleList  # TODO modify output so article is string


@lru_cache(maxsize=1000000)
def word_similarity(word1, word1_pos, word2):
    '''
    Returns the Wu-Palmer similarity between the given words.
    Values range between 0 (least similar) and 1 (most similar).
    '''
    if word1_pos is not None:
        syns_w1 = wn.synsets(word1, pos=word1_pos)
    else:
        syns_w1 = wn.synsets(word1)
    syns_w2 = wn.synsets(word2)
    score = 0
    for w1 in syns_w1:
        for w2 in syns_w2:
            cur_score = w1.wup_similarity(w2)
            if cur_score:
                score = max(score, cur_score)
    return score


def decay_function(decay_factor, entity_location, term_index):
    distance = abs(term_index - entity_location[0])
    if len(entity_location) > 1:
        distance = min(distance, abs(term_index - entity_location[1]))
    return (1 - decay_factor) ** distance


def sentiment(word):
    '''
    Returns the sentiment of the given string as a float within
    the range [-1.0, 1.0]
    '''
    # TODO deal with negations???
    word_blob = TextBlob(word)
    return word_blob.sentiment.polarity


def choose_role(word):
    '''
    Uses the sentiment score of a term to determine which dictionary is likely
    to be most useful.
    '''
    s = sentiment(word)
    if s > 0.4:  # TODO update value to expand neutral range
        return ["hero"]
    elif s < -0.4:
        return ["villain", "victim"]
    else:
        return ["hero", "villain", "victim"]


def similarity_to_role(word, word_pos, role):
    similarity_total = 0
    if role == "hero":
        dict_length = len(HERO_DICT)
        for hero_term in HERO_DICT:
            similarity_total += word_similarity(word, word_pos, hero_term)
    elif role == "villain":
        dict_length = len(VILLAIN_DICT)
        for villain_term in VILLAIN_DICT:
            similarity_total += word_similarity(word, word_pos, villain_term)
    elif role == "victim":
        dict_length = len(VICTIM_DICT)
        for victim_term in VICTIM_DICT:
            similarity_total += word_similarity(word, word_pos, victim_term)
    return similarity_total / dict_length


def skip_word(word, pos):
    '''
    Returns true if the given word should be ignored in analysis.
    '''
    # pronouns, conjunctions, particles, determiners
    if any((
        len(word) < 2,
        word.lower() in STOP_WORDS,
        pos in IGNORE_POS,
        word == "''",
        word == "``",
    )):
        return True

    return False


def role_score_by_sentence(entity, role, index, tokenized_article):
    '''
    Calculates the role score of the entity in the given sentence.
    '''
    entity_location = entity.locations[index]  # A list where the elements are the beginning and ending indices
    total_score = 0
    # article from a string to a list of sentences
    sentence = word_tokenize(tokenized_article[index])
    tagged_sentence = pos_tag(sentence)
    begin_index = entity_location[0]
    end_index = entity_location[1] if len(entity_location) > 1 else entity_location[0]
    # TODO I think if an entity appears twice in a sentence then we need to do something different with locations
    for i in range(len(sentence)):
        cur_score = 0
        if not begin_index <= i <= end_index:
            word = sentence[i]
            pos = tagged_sentence[i][1]
            if not skip_word(word, pos):
                term_role = choose_role(word)
                if role in term_role:
                    cur_score += similarity_to_role(word, get_wn_pos(word), role)
                    # cur_score += additional_score(entity, role, sentence[i])
                    cur_score *= decay_function(0.5, entity_location, i)  # TODO update f value
        total_score += cur_score
    return total_score


def entity_role_score(entity, role, article):
    '''
    Calculates the role score of the entity by averaging the
    role scores of the sentences where the entity appears.
    '''
    total_score = 0
    count = 0
    for index in entity.locations:
        total_score += role_score_by_sentence(entity, role, index, article)
        count += 1
    print(role + ": " + str(total_score/count))
    return total_score / count


def main(url):
    '''
    Retrieve the three top entities from entity_recognition.py;
    assign each entity the role with the highest role score.
    '''
    headline, article = extract_by_newsplease(url)
    tokenized_article = sent_tokenize(article)
    entities = get_top_entities(headline, tokenized_article)
    for entity in entities:
        # TODO calculate headline score ??
        role = "hero"
        score = entity_role_score(entity, "hero", tokenized_article)
        cur = entity_role_score(entity, "villain", tokenized_article)
        if cur > score:
            score = cur
            role = "villain"
        if entity_role_score(entity, "victim", tokenized_article) > score:
            role = "victim"
        entity.role = role
        print(entity)
        print(entity.role)
        # TODO assign threshold ???
    return entities


if __name__ == "__main__":
    main("https://www.bbc.com/news/world-us-canada-47047394")
