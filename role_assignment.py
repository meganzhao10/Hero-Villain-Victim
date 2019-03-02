'''
Assigns entities in a news article to roles of hero, villain, or victim.
'''


from functools import lru_cache
import re

import spacy
from newspaper import Article
from nltk import pos_tag, sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from textblob import TextBlob

from entity_recognition import get_top_entities
from role_dictionaries import HERO_DICT, VILLAIN_DICT, VICTIM_DICT
from stop_words import STOP_WORDS
from similarity_dictionary import SIM_DIC


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

# Spacy model for detecting active/passive entities
nlp = spacy.load('en')


# Raised when newspaper fails to extract article or headline
class NewspaperError(Exception):
    pass


def extract_by_newspaper(url):
    '''
    News article extraction from url using newspaper package.
    '''
    content = Article(url)
    content.download()
    content.parse()
    headline = content.title
    article = content.text
    return headline, article


@lru_cache(maxsize=1000000)
def word_similarity(word1, word2):
    '''
    Returns the Wu-Palmer similarity between the given words.
    Values range between 0 (least similar) and 1 (most similar).
    '''
    syns_w1 = wn.synsets(word1)
    syns_w2 = wn.synsets(word2)
    score = 0
    for w1 in syns_w1:
        for w2 in syns_w2:
            cur_score = w1.wup_similarity(w2)
            cur_score = w2.wup_similarity(w1) if not cur_score else cur_score
            if cur_score:
                score = max(score, cur_score)
    return score


def decay_function(decay_factor, entity_locations, term_index):
    '''
    Accounts for decay in score based on distance between words.
    '''
    minDist = float("inf")
    for loc in entity_locations:
        if isinstance(loc, int):
            distance = abs(term_index - loc)
        else:
            distance = min(abs(term_index - loc[0]), abs(term_index - loc[1]))
        minDist = min(distance, minDist)
    return (1 - decay_factor) ** minDist


def sentiment(word):
    '''
    Returns the sentiment of the given string as a float within
    the range [-1.0, 1.0].
    '''
    word_blob = TextBlob(word)
    return word_blob.sentiment.polarity


def choose_roles_by_sentiment(word):
    '''
    Uses the sentiment score of a term to determine which dictionaries are
    likely to be most useful. Negative sentiment maps to villain and victim
    dics, positive to hero, and neutral to all three.
    '''
    s = sentiment(word)
    if s > 0.15:
        return [HERO]
    elif s < -0.15:
        return [VILLAIN, VICTIM]
    else:
        return [HERO, VILLAIN, VICTIM]


@lru_cache(maxsize=1000000)
def similarity_to_role(word, role):
    '''
    Returns the similarity of the word to the role.
    '''
    # Check for preprocessed scores
    scores = SIM_DIC.get(word)
    if scores:
        score = scores[role]

    else:
        similarity_total, count_zero = 0, 0

        if role == HERO:
            dict_length = len(HERO_DICT)
            for hero_term in HERO_DICT:
                cur_score = word_similarity(word, hero_term)
                similarity_total += cur_score
                if cur_score == 0:
                    count_zero += 1

        elif role == VILLAIN:
            dict_length = len(VILLAIN_DICT)
            for villain_term in VILLAIN_DICT:
                cur_score = word_similarity(word, villain_term)
                similarity_total += cur_score
                if cur_score == 0:
                    count_zero += 1

        elif role == VICTIM:
            dict_length = len(VICTIM_DICT)
            for victim_term in VICTIM_DICT:
                cur_score = word_similarity(word, victim_term)
                similarity_total += cur_score
                if cur_score == 0:
                    count_zero += 1

        if dict_length - count_zero == 0:
            return 0

        score = similarity_total / (dict_length - count_zero)

    # Standardize scores (avg and sd from scores on top 10k english words)
    if role == HERO:
        avg = 0.3230
        std = 0.1239
    elif role == VILLAIN:
        avg = 0.2878
        std = 0.1202
    else:
        avg = 0.2901
        std = 0.1194

    return (score - avg) / std


def skip_word(word, pos):
    '''
    Returns true if the given word should be ignored in analysis.
    '''
    if any((
        len(word) < 3,
        pos in IGNORE_POS,
        word == "''",
        word == "``",
        word == '"',
    )):
        return True

    for stop in STOP_WORDS:
        if re.fullmatch(stop, word.lower()):
            return True

    return False


def active_passive_role(entity_string, sentence):
    '''
    Determine whether the entity is an active or passive role.
    Active roles = subject or passive object
    Passive roles = object or passive subject
    '''
    sent = nlp(sentence)
    isActive = False
    for tok in sent:
        if (tok.dep_ == "nsubj"):
            isActive = True
        if (str(tok) == entity_string):
            if (tok.dep_ == "nsubj"):
                return "active"
            if (tok.dep_ == "pobj" and not isActive):
                return "active"
            if (tok.dep_ == "pobj" and isActive):
                return "passive"
            elif (tok.dep_ == "dobj" or tok.dep_ == "nsubjpass"):
                return "passive"
            else:
                return "neutral"
    return "notInSentence"


def is_word_part_of_entity(entities_in_sent, sentence_index, word_index):
    '''
    Determine if the word at word_index is part of one of the top entities
    in the sentence.
    '''
    for entity in entities_in_sent:
        if sentence_index == "H":
            entity_locations = entity.headline_locations
        else:
            entity_locations = entity.locations[sentence_index]

        for loc in entity_locations:
            if isinstance(loc, int):
                if word_index == loc:
                    return True
            elif loc[0] <= word_index <= loc[1]:
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


def additional_score(act_pas, role, score):
    '''
    Computes an additional score if the active/passive input matches the
    given role. Active matches hero and villain. Passive matches victim.
    '''
    if act_pas == "active" and (role == HERO or role == VILLAIN):
        return score
    if act_pas == "passive" and role == VICTIM:
        return score
    return 0


def get_entities_act_pas(sentence_index, sentence, tokenized_sentence, entities_in_sent):
    '''
    Determines if each entity in the sentence is active or passive within the sentence.
    Returns the results in a list that corresponds to entities_in_sent.
    '''
    entities_act_pas = []
    for entity in entities_in_sent:
        last_loc = entity.locations[sentence_index][-1]  # Use last index of entity
        if isinstance(last_loc, int):
            entity_string = tokenized_sentence[last_loc]
        else:
            entity_string = tokenized_sentence[last_loc[1]]
        entities_act_pas.append(active_passive_role(entity_string, sentence))
    return entities_act_pas


# Global variables needed for functions below
top_entities, add_score, decay = 0, 0, 0
hero_scores, villain_scores, victim_scores, counts = [], [], [], []
top_hero_words, top_villain_words, top_victim_words = [{}], [{}], [{}]


def initialize_globals(entities, additional_score, decay_factor):
    '''
    Initialize entities, decay factor, and additional score for active/passive.
    Also set up lists for scores, counts, top words (indexed by entities).
    '''
    global top_entities, add_score, decay
    global hero_scores, villain_scores, victim_scores, counts
    global top_hero_words, top_villain_words, top_victim_words
    top_entities = entities
    add_score = additional_score
    decay = decay_factor
    n = len(entities)
    hero_scores, villain_scores, victim_scores, counts = ([0]*n for i in range(4))
    top_hero_words = [{} for _ in range(n)]
    top_villain_words = [{} for _ in range(n)]
    top_victim_words = [{} for _ in range(n)]


def get_entities_in_sent(sentence_index):
    '''
    Returns a list of entities in the sentence and updates counts.
    '''
    entities_in_sent = []
    for i, entity in enumerate(top_entities):
        if sentence_index in entity.locations:
            counts[i] += 1
            entities_in_sent.append(entity)
    return entities_in_sent


def update_total_scores(entity, role, word, word_score):
    '''
    Adds the given score to the entity's total score for the given role.
    Also updates top words for that role.
    '''
    entity_index = top_entities.index(entity)
    if role == HERO:
        hero_scores[entity_index] += word_score
        if word in top_hero_words[entity_index]:
            top_hero_words[entity_index][word.lower()] += word_score
        else:
            top_hero_words[entity_index][word.lower()] = word_score
    elif role == VILLAIN:
        villain_scores[entity_index] += word_score
        if word in top_villain_words[entity_index]:
            top_villain_words[entity_index][word.lower()] += word_score
        else:
            top_villain_words[entity_index][word.lower()] = word_score
    elif role == VICTIM:
        victim_scores[entity_index] += word_score
        if word in top_victim_words[entity_index]:
            top_victim_words[entity_index][word.lower()] += word_score
        else:
            top_victim_words[entity_index][word.lower()] = word_score


def score_word(word, word_index, sentence_index, entities_in_sent, entities_act_pas):
    '''
    Scores the word across the appropriate roles and updates totals.
    '''
    # Compute scores for roles that match word senitment
    roles_to_check = choose_roles_by_sentiment(word)
    scores = {}
    for role in roles_to_check:
        scores[role] = similarity_to_role(word, role)

    # Compute score for each entity-role pair and update totals
    for entity in entities_in_sent:
        for role in roles_to_check:
            cur_score = scores[role]
            act_pas = entities_act_pas[entities_in_sent.index(entity)]
            cur_score += additional_score(act_pas, role, add_score)
            cur_score *= decay_function(decay, entity.locations[sentence_index], word_index)
            update_total_scores(entity, role, word, cur_score)


def get_roles_and_top_words():
    entities_role_results = [(None, 0), (None, 0), (None, 0)]
    top_words = [None, None, None]
    for i, entity in enumerate(top_entities):

        # Compute final role scores
        if counts[i] == 0:
            hero_score, villain_score, victim_score = 0, 0, 0
        else:
            hero_score = hero_scores[i] / counts[i]
            villain_score = villain_scores[i] / counts[i]
            victim_score = victim_scores[i] / counts[i]

        # Add relevance to scores
        hero_score += 5*entity.relevance_score
        villain_score += 5*entity.relevance_score
        victim_score += 5*entity.relevance_score

        # Determine entity role based on max role score
        sorted_scores = sorted([hero_score, villain_score, victim_score], reverse=True)
        max_score = sorted_scores[0]
        if max_score - sorted_scores[1] >= 0.05:  # Don't assign if scores too close
            if hero_score == max_score:
                entity.role = HERO
            elif villain_score == max_score:
                entity.role = VILLAIN
            elif victim_score == max_score:
                entity.role = VICTIM

        # Assign entity to corresponding role if score is larger than current leader
        if entity.role is not None and max_score > entities_role_results[entity.role][1]:
            entities_role_results[entity.role] = (entity.name, max_score)

            # Update top words accordingly
            if entity.role == HERO:
                top_words[HERO] = [x[0] for x in get_top_words(top_hero_words[i])]
            elif entity.role == VILLAIN:
                top_words[VILLAIN] = [x[0] for x in get_top_words(top_villain_words[i])]
            else:
                top_words[VICTIM] = [x[0] for x in get_top_words(top_victim_words[i])]

    result = [x[0] for x in entities_role_results]
    return result, top_words


def assign_roles(url, add_score, decay_factor):
    # Extract article from url and tokenize
    try:
        headline, article = extract_by_newspaper(url)
    except:
        raise NewspaperError
    if len(article) == 0:
        raise NewspaperError
    tokenized_article = sent_tokenize(article)

    # Remove headline from article if it's added to first sentence (common extraction error)
    if (headline in tokenized_article[0]):
        tokenized_article[0] = tokenized_article[0].replace(headline, "")

    # Get top entities and initialize globals
    entities = get_top_entities(headline, tokenized_article)
    initialize_globals(entities, add_score, decay_factor)

    # Loop through each sentence
    for sentence_index in range(len(tokenized_article)):

        # Find entities in sentence and update counts
        entities_in_sent = get_entities_in_sent(sentence_index)

        # Skip sentence if no entities.
        if not entities_in_sent:
            continue

        # Get and tokenize sentence
        sentence = tokenized_article[sentence_index].strip()
        tokenized_sentence = word_tokenize(sentence)

        # Compute active/passive for each entity in sentence
        entities_act_pas = get_entities_act_pas(sentence_index, sentence, tokenized_sentence, entities_in_sent)

        # Loop through words in sentence
        tagged_sentence = pos_tag(tokenized_sentence)
        for word_index in range(len(tokenized_sentence)):

            # Skip word if it is part of an entity
            if is_word_part_of_entity(entities_in_sent, sentence_index, word_index):
                continue

            # Check if word is a skip word (stop words, invalid POS, punctuation)
            word = tokenized_sentence[word_index]
            pos = tagged_sentence[word_index][1]
            if skip_word(word, pos):
                continue

            # Score word and track results
            score_word(word, word_index, sentence_index, entities_in_sent, entities_act_pas)

    # Finalize assignment and top words
    return get_roles_and_top_words()
