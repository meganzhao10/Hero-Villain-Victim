from nltk import pos_tag, sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from entity_recognition import get_top_entities
from role_dictionaries import HERO_DICT, VILLAIN_DICT, VICTIM_DICT
from stop_words import STOP_WORDS
from functools import lru_cache
from similarity_dictionary import SIM_DIC

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


# Parts of speech that are invalid in WordNet similarity function
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

# Constants to represent roles
HERO = 0
VILLAIN = 1
VICTIM = 2


def role_to_string(role):
    '''
    Converts a given role to a string.
    '''
    if role == HERO:
        return "hero"
    elif role == VILLAIN:
        return "villain"
    elif role == VICTIM:
        return "victim"
    else:
        return None


def get_wn_pos(nltk_pos):
    '''
    Converts the given nltk part of speech to a word net part of speech.
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
def word_similarity(word1, word2, word1_pos=None):
    '''
    Returns the Wu-Palmer similarity between the given words.
    Values range between 0 (least similar) and 1 (most similar).
    Optional part of speech argument for word1 limits WordNet synsets.
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
    '''
    Accounts for decay in score based on distance between words.
    '''
    distance = abs(term_index - entity_location[0])
    if len(entity_location) > 1:
        distance = min(distance, abs(term_index - entity_location[1]))
    return (1 - decay_factor) ** distance


def sentiment(word):
    '''
    Returns the sentiment of the given string as a float within
    the range [-1.0, 1.0].
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
    if s > 0.15:  # TODO consider updating value to adjust neutral range
        return [HERO]
    elif s < -0.15:
        return [VILLAIN, VICTIM]
    else:
        return [HERO, VILLAIN, VICTIM]


def similarity_to_role(word, role, word_pos=None):
    '''
    Returns the similarity of the word to the role. Optional part of speech
    argument to be passed along to WordNet.
    '''
    similarity_total = 0
    scores = SIM_DIC.get(word)

    if role == HERO:
        if scores is None:
            dict_length = len(HERO_DICT)
            for hero_term in HERO_DICT:
                similarity_total += word_similarity(word, hero_term, word1_pos=word_pos)
        else:
            return scores[HERO]

    elif role == VILLAIN:
        if scores is None:
            dict_length = len(VILLAIN_DICT)
            for villain_term in VILLAIN_DICT:
                similarity_total += word_similarity(word, villain_term, word1_pos=word_pos)
        else:
            return scores[VILLAIN]

    elif role == VICTIM:
        if scores is None:
            dict_length = len(VICTIM_DICT)
            for victim_term in VICTIM_DICT:
                similarity_total += word_similarity(word, victim_term, word1_pos=word_pos)
        else:
            return scores[VICTIM]

    return similarity_total / dict_length


def skip_word(word, pos):
    '''
    Returns true if the given word should be ignored in analysis.
    '''
    # pronouns, conjunctions, particles, determiners
    if any((
        len(word) < 3,
        word.lower() in STOP_WORDS,
        pos in IGNORE_POS,
        word == "''",
        word == "``",
        word == '"',
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
                    cur_score += similarity_to_role(word, role, word_pos=get_wn_pos(pos))
                    # cur_score += additional_score(entity, role, word)
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
    print(role_to_string(role) + ": " + str(total_score/count))
    return total_score / count


def main(url):
    '''
    Retrieve the three top entities from entity_recognition.py;
    assign each entity the role with the highest role score.
    '''
    headline, article = extract_by_newspaper(url)
    tokenized_article = sent_tokenize(article)
    entities = get_top_entities(headline, tokenized_article)
    for entity in entities:
        # TODO calculate headline score ??
        role = HERO
        score = entity_role_score(entity, HERO, tokenized_article)
        cur = entity_role_score(entity, VILLAIN, tokenized_article)
        if cur > score:
            score = cur
            role = VILLAIN
        if entity_role_score(entity, VICTIM, tokenized_article) > score:
            role = VICTIM
        entity.role = role_to_string(role)
        print(entity)
        print(entity.role)
        # TODO assign threshold ???
    return entities


def is_word_part_of_entity(entities_in_sent, sentence_index, word_index):
    for entity in entities_in_sent:
        entity_location = entity.locations[sentence_index]
        begin_index = entity_location[0]
        end_index = entity_location[1] if len(entity_location) > 1 else entity_location[0]
        # TODO I think if an entity appears twice in a sentence then we need to do something different with locations
        if begin_index <= word_index <= end_index:
            return True
    return False


def get_top_words(word_dic):
    '''
    Returns a list of the top three (word, score) pairs in the dictionary.
    '''
    result = []
    for i, word in enumerate(sorted(word_dic, key=word_dic.get, reverse=True)):
        if i > 2:
            break
        result.append((word, word_dic[word]))
    return result


def main2(url):
    headline, article = extract_by_newspaper(url)
    tokenized_article = sent_tokenize(article)
    entities = get_top_entities(headline, tokenized_article)

    # Initialize scores, counts, top words (indexed by entities)
    hero_scores, villain_scores, victim_scores = [], [], []
    top_hero_words, top_villain_words, top_victim_words = [], [], []
    counts = []
    for i in range(len(entities)):
        hero_scores.append(0)
        villain_scores.append(0)
        victim_scores.append(0)
        top_hero_words.append({})
        top_villain_words.append({})
        top_victim_words.append({})
        counts.append(0)

    # Loop through each sentence
    for sentence_index in range(len(tokenized_article)):

        # Find which entities in sentence and update counts
        entities_in_sent = []
        for i, entity in enumerate(entities):
            if sentence_index in entity.locations:
                counts[i] += 1
                entities_in_sent.append(entity)

        # Skip sentence if no entities in it
        if not entities_in_sent:
            continue

        # Loop through words in sentence
        sentence = word_tokenize(tokenized_article[sentence_index])
        for i in range(len(sentence)):

            # Skip word if it is part of an entity
            if is_word_part_of_entity(entities_in_sent, sentence_index, i):
                continue

            # Check if word is a skip word (stop words, invalid POS, punctuation)
            tagged_sentence = pos_tag(sentence)
            word = sentence[i]
            pos = tagged_sentence[i][1]
            if skip_word(word, pos):
                continue

            # Update scores for corresponding roles
            term_role = choose_role(word)
            scores = {}
            for role in term_role:
                scores[role] = similarity_to_role(word, role, word_pos=get_wn_pos(pos))
            for entity in entities_in_sent:
                entity_index = entities.index(entity)
                for role in term_role:
                    cur_score = scores[role]
                    # cur_score += additional_score(entity, role, word)
                    cur_score *= decay_function(0.5, entity.locations[sentence_index], i)  # TODO update f value
                    if role == HERO:
                        hero_scores[entity_index] += cur_score
                        if word in top_hero_words[entity_index]:
                            top_hero_words[entity_index][word] += cur_score
                        else:
                            top_hero_words[entity_index][word] = cur_score

                    elif role == VILLAIN:
                        villain_scores[entity_index] += cur_score
                        if word in top_villain_words[entity_index]:
                            top_villain_words[entity_index][word] += cur_score
                        else:
                            top_villain_words[entity_index][word] = cur_score

                    elif role == VICTIM:
                        victim_scores[entity_index] += cur_score
                        if word in top_victim_words[entity_index]:
                            top_victim_words[entity_index][word] += cur_score
                        else:
                            top_victim_words[entity_index][word] = cur_score

    # Compute total scores
    for i, entity in enumerate(entities):
        hero_score = hero_scores[i] / counts[i]
        villain_score = villain_scores[i] / counts[i]
        victim_score = victim_scores[i] / counts[i]

        print(entity)
        print("HERO:", hero_score)
        print("HERO TOP WORDS:", get_top_words(top_hero_words[i]))
        print("VILLAIN:", villain_score)
        print("VILLAIN TOP WORDS:", get_top_words(top_villain_words[i]))
        print("VICTIM:", victim_score)
        print("VICTIM TOP WORDS:", get_top_words(top_victim_words[i]))

        # entity.role = role_to_string(role)
        # print(entity)
        # print(entity.role)


if __name__ == "__main__":
    main2("https://us.cnn.com/2019/02/07/politics/adam-schiff-trump-white-house-staffers/index.html")
