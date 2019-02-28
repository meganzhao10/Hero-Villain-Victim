from nltk import pos_tag, sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from entity_recognition import get_top_entities
from stop_words import STOP_WORDS
from functools import lru_cache
from similarity_dictionary import SIM_DIC
from role_dictionaries import HERO_DICT, VILLAIN_DICT, VICTIM_DICT
import re

# pip install -U spacy
# python3 -m spacy download xx
import spacy

# pip3 install textblob
from textblob import TextBlob
# pip3 install newspaper3k
from newspaper import Article

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


def extract_by_newspaper(url):
    '''
    News article extraction using newspaper
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
    Optional part of speech argument for word1 limits WordNet synsets.
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


def choose_role(word):
    '''
    Uses the sentiment score of a term to determine which dictionary is likely
    to be most useful.
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
    Returns the similarity of the word to the role. Optional part of speech
    argument to be passed along to WordNet.
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


def active_passive_role(entity_string, aSentence):
    '''
    Determine whether the entity is an active or passive role.
    Active roles = subject or passive object
    Passive roles = object or passive subject
    '''
    aSent = nlp(aSentence)
    isActive = False
    for tok in aSent:
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


def main(url, add_score, decay_factor):
    try:
        headline, article = extract_by_newspaper(url)
    except:
        return 0, 0
    if len(article) == 0:
        return 0, 0
    try:
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

            sentence = tokenized_article[sentence_index].strip()
            tokenized_sentence = word_tokenize(sentence)

            # Compute active/passive for each entity in sentence
            entities_act_pas = []
            for entity in entities_in_sent:
                last_loc = entity.locations[sentence_index][-1]  # Use last index of entity
                if isinstance(last_loc, int):
                    entity_string = tokenized_sentence[last_loc]
                else:
                    entity_string = tokenized_sentence[last_loc[1]]
                entities_act_pas.append(active_passive_role(entity_string, sentence))

            # Loop through words in sentence
            tagged_sentence = pos_tag(tokenized_sentence)
            for i in range(len(tokenized_sentence)):

                # Skip word if it is part of an entity
                if is_word_part_of_entity(entities_in_sent, sentence_index, i):
                    continue

                # Check if word is a skip word (stop words, invalid POS, punctuation)
                word = tokenized_sentence[i]
                pos = tagged_sentence[i][1]
                if skip_word(word, pos):
                    continue

                # Update scores for corresponding roles
                term_role = choose_role(word)
                scores = {}
                for role in term_role:
                    scores[role] = similarity_to_role(word, role)
                for entity in entities_in_sent:
                    entity_index = entities.index(entity)
                    for role in term_role:
                        cur_score = scores[role]
                        act_pas = entities_act_pas[entities_in_sent.index(entity)]
                        cur_score += additional_score(act_pas, role, add_score)
                        cur_score *= decay_function(decay_factor, entity.locations[sentence_index], i)  # TODO update f value
                        if role == HERO:
                            hero_scores[entity_index] += cur_score
                            if word in top_hero_words[entity_index]:
                                top_hero_words[entity_index][word.lower()] += cur_score
                            else:
                                top_hero_words[entity_index][word.lower()] = cur_score

                        elif role == VILLAIN:
                            villain_scores[entity_index] += cur_score
                            if word in top_villain_words[entity_index]:
                                top_villain_words[entity_index][word.lower()] += cur_score
                            else:
                                top_villain_words[entity_index][word.lower()] = cur_score

                        elif role == VICTIM:
                            victim_scores[entity_index] += cur_score
                            if word in top_victim_words[entity_index]:
                                top_victim_words[entity_index][word.lower()] += cur_score
                            else:
                                top_victim_words[entity_index][word.lower()] = cur_score

        # Compute total scores
        entities_names_scores = [None, None, None]
        top_words = [None, None, None]
        for i, entity in enumerate(entities):

            if counts[i] == 0:
                hero_score, villain_score, victim_score = 0, 0, 0
            else:
                hero_score = hero_scores[i] / counts[i]
                villain_score = villain_scores[i] / counts[i]
                victim_score = victim_scores[i] / counts[i]

            # Determine entity roles based on role scores of entities
            sorted_scores = sorted([hero_score, villain_score, victim_score], reverse = True)
            max_score = sorted_scores[0]
            second_score = sorted_scores[1]
            if max_score - second_score >= 0.05:
                if hero_score == max_score:
                    entity.role = HERO
                elif villain_score == max_score:
                    entity.role = VILLAIN
                elif victim_score == max_score:
                    entity.role = VICTIM

            if entity.role != "" and (not entities_names_scores[entity.role] or max_score > entities_names_scores[entity.role][1]):
                entities_names_scores[entity.role] = (entity.name, max_score)

                if entity.role == HERO:
                    top_words[HERO] = [x[0] for x in get_top_words(top_hero_words[i])]
                elif entity.role == VILLAIN:
                    top_words[VILLAIN] = [x[0] for x in get_top_words(top_villain_words[i])]
                else:
                    top_words[VICTIM] = [x[0] for x in get_top_words(top_victim_words[i])]

            print(entity)
            print("HERO:", hero_score)
            print("HERO TOP WORDS:", get_top_words(top_hero_words[i]))
            print("VILLAIN:", villain_score)
            print("VILLAIN TOP WORDS:", get_top_words(top_villain_words[i]))
            print("VICTIM:", victim_score)
            print("VICTIM TOP WORDS:", get_top_words(top_victim_words[i]))

            print("------------------------")

        return entities_names_scores, top_words

    except:
        return 1, 1


if __name__ == "__main__":
    main(
        "https://www.washingtonpost.com/local/legal-issues/paul-manafort-a-hardened-and-bold-criminal-mueller-prosecutors-tell-judge/2019/02/23/690bd33c-3542-11e9-af5b-b51b7ff322e9_story.html",
          0.2, 0.1,  # additional score, decay factor
          )
