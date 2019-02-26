from nltk import pos_tag, sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from entity_recognition import get_top_entities
from role_dictionaries import HERO_DICT, VILLAIN_DICT, VICTIM_DICT
from stop_words import STOP_WORDS
from functools import lru_cache
# from similarity_dictionary import SIM_DIC
import re

# pip install -U spacy
# python3 -m spacy download xx
import spacy

# pip3 install textblob
from textblob import TextBlob
# pip3 install news-please
# pip3 install newspaper3k
# from newsplease import NewsPlease
from newspaper import Article
# pip install beautifulsoup4
# pip install lxml
# pip install html5lib
# from bs4 import BeautifulSoup


''' UNCOMMENT CHUNK BELOW TO USE FILTERED DICTIONARIES '''
from similarity_dictionary_filtered import SIM_DIC
HERO_DICT = {'gentle', 'preserving', 'leadership', 'amazing', 'devoted', 'humble', 'warned', 'surprised', 'humanity', 'brave', 'evacuate', 'redemption', 'smile', 'honor', 'revolutionize', 'leader', 'advocate', 'savior', 'charity', 'sympathies', 'kindness', 'good', 'protect', 'teach', 'reputation', 'respected', 'welfare', 'glory', 'victory', 'winner', 'well', 'contained', 'restoration', 'commitment', 'ability', 'efforts', 'inspire', 'safety', 'allies', 'health', 'strength', 'empowered', 'passion', 'encouraging', 'warm', 'vision', 'scored', 'authorities', 'justice', 'grand', 'admire', 'reshape', 'communities', 'response', 'strengthen', 'bolster', 'intervened', 'motivated', 'reconstruct', 'freedom', 'duty', 'aided', 'conquer', 'smart', 'bravery', 'improve', 'donate', 'wise', 'ingenuity', 'milestone', 'protections', 'expand', 'hero', 'pursuit', 'invent', 'containment', 'achievement', 'supporters'}
VILLAIN_DICT = {'contaminate', 'dirty', 'abduct', 'terror', 'worsen', 'crisis', 'lambast', 'abandonment', 'harass', 'subvert', 'virus', 'crime', 'provoke', 'kidnap', 'manipulate', 'alleged', 'refusal', 'trafficking', 'marginalize', 'conformity', 'clampdown', 'villain', 'disparaged', 'cold', 'exacerbate', 'alienate', 'commit', 'trial', 'violence', 'denounced', 'stripped', 'undermine', 'seize', 'persecuted', 'opposing', 'intimidate', 'jailed', 'fool', 'investigation', 'imprisoned', 'bias', 'deception', 'gunshots', 'threaten', 'hoax', 'engulfed', 'blame', 'eruption', 'offensive', 'contempt', 'suggested', 'coercion', 'erase', 'catastrophe', 'rumors', 'weaken', 'pointed', 'treason', 'evil', 'abused', 'sentenced', 'bullet', 'warn', 'devastate', 'convicted', 'rebuke', 'reveal', 'bully', 'collude'}
VICTIM_DICT = {'setback', 'injured', 'traumatized', 'prevented', 'healing', 'buried', 'stuck', 'anguished', 'flee', 'suffer', 'casualty', 'trampled', 'forsaken', 'harassed', 'harassment', 'hardship', 'deported', 'howling', 'shocked', 'violence', 'depressed', 'danger', 'mute', 'stripped', 'terrified', 'distrust', 'assassinated', 'shivering', 'sick', 'complain', 'abducted', 'huddled', 'victimized', 'persecuted', 'barricaded', 'devastated', 'kidnapped', 'seized', 'justified', 'evacuated', 'surrendered', 'diagnosed', 'imprisoned', 'independence', 'slave', 'deceased', 'rebuffed', 'target', 'trapped', 'screamed', 'loss', 'trafficked', 'humiliated', 'impairment', 'wounded', 'discriminated', 'disadvantaged', 'blood', 'offended', 'accuses', 'saddens', 'threatened', 'disaster', 'devastation', 'overshadowed', 'tortured', 'abused', 'remonstrated', 'jeopardizing', 'stabbed', 'prey', 'sentenced', 'challenged', 'renounced', 'scared', 'humiliation', 'deaths', 'rescued', 'bleeding'}


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

nlp = spacy.load('en')


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


# def extract_by_newsplease(url):
#    content = NewsPlease.from_url(url)
#    headline = content.title
#    article = content.text
#    return headline, article


# def extract_by_soup(url):
#    content = BeautifulSoup(url, "lxml")
#    headline = content.title.string
#    articleList = list()
#    for i in content.find_all("p"):
#        articleList.append(i.get_text())
#        print(i.get_text())

#    return headline, articleList  # TODO modify output so article is string

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


@lru_cache(maxsize=1000000)
def similarity_to_role(word, role):
    '''
    Returns the similarity of the word to the role. Optional part of speech
    argument to be passed along to WordNet.
    '''
    similarity_total = 0
    scores = SIM_DIC.get(word)
    count_zero = 0

    if scores:
        score = scores[role]

    else:
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
            return 0  # TODO do we want to do something else here?

        score = similarity_total / (dict_length - count_zero)  # Do we want to shift this to 0,1 interval??

    #full dictionary 10k
    # if role == HERO:
    #     avg = 0.3398
    #     std = 0.1271
    # elif role == VILLAIN:
    #     avg = 0.3239
    #     std = 0.1259
    # else:
    #     avg = 0.3180
    #     std = 0.1238

    # full dictionary 100k
    # if role == HERO:
    #     avg = 0.2228
    #     std = 0.1782
    # elif role == VILLAIN:
    #     avg = 0.2128
    #     std = 0.1722
    # else:
    #     avg = 0.2099
    #     std = 0.1699

    # filtered dictionary 10k
    if role == HERO:
        avg = 0.3230
        std = 0.1239
    elif role == VILLAIN:
        avg = 0.2878
        std = 0.1202
    else:
        avg = 0.2901
        std = 0.1194

    # filtered dictionary 100k
    # if role == HERO:
    #     avg = 0.2099
    #     std = 0.1689
    # elif role == VILLAIN:
    #     avg = 0.1876
    #     std = 0.1556
    # else:
    #     avg = 0.1915
    #     std = 0.1581

    #return score

    return (score - avg) / std


def skip_word(word, pos):
    '''
    Returns true if the given word should be ignored in analysis.
    '''
    # pronouns, conjunctions, particles, determiners
    for stop in STOP_WORDS:
        if any((
            len(word) < 3,
            re.fullmatch(stop, word.lower()),
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
                    cur_score += similarity_to_role(word, role)
                    cur_score += additional_score(entity, role, word)
                    cur_score *= decay_function(0.2, entity_location, i)  # TODO update f value
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


def active_passive_role(entity_string, aSentence):
    '''
    Determine whether the entity is an active or passive role
    depending on if it's subject or object in a sentence
    Active roles = subject or passive object
    Passive roles = object or passive subject
    '''
    aSent = nlp(aSentence)
    isActive = False
    for tok in aSent:
        if (tok.dep_ == "nsubj"):
            isActive = True
        if (str(tok) == entity_string):
            # print(str(tok) + ": " + str(tok.dep_))
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
        if sentence_index == "H":
            entity_location = entity.headline_locations
        else:
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


def additional_score(act_pas, role, score):
    if act_pas == "active" and (role == HERO or role == VILLAIN):
        return score
    if act_pas == "passive" and role == VICTIM:
        return score
    return 0


def main2(url, add_score, decay_factor):
    headline, article = extract_by_newspaper(url)
#    print(headline)
#    print(article)
    tokenized_article = sent_tokenize(article)
    entities = get_top_entities(headline, tokenized_article)

    # Initialize scores, counts, top words (indexed by entities) for headline
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

    # Process headline
#    entities_in_headline = []
#    for i, entity in enumerate(entities):
#        if entity.headline:
#            counts[i] += 1
#            entities_in_headline.append(entity)
#
#    if entities_in_headline:
#        headline_tokens = word_tokenize(headline)
#        for i, word in enumerate(headline_tokens):
#            if skip_word(word, None) or is_word_part_of_entity(entities_in_headline, "H", i):
#                continue
#
#            term_role = choose_role(word)
#            scores = {}
#            for role in term_role:
#                scores[role] = similarity_to_role(word, role)
#            for entity in entities_in_headline:
#                entity_index = entities.index(entity)
#                for role in term_role:
#                    cur_score = scores[role]
#                    # cur_score += additional_score(entity, role, word)
#                    cur_score *= decay_function(0.5, entity.headline_locations, i)  # TODO update f value
#                    if role == HERO:
#                        hero_scores[entity_index] += cur_score
#                        if word in top_hero_words[entity_index]:
#                            top_hero_words[entity_index][word] += cur_score
#                        else:
#                            top_hero_words[entity_index][word] = cur_score
#
#                    elif role == VILLAIN:
#                        villain_scores[entity_index] += cur_score
#                        if word in top_villain_words[entity_index]:
#                            top_villain_words[entity_index][word] += cur_score
#                        else:
#                            top_villain_words[entity_index][word] = cur_score
#
#                    elif role == VICTIM:
#                        victim_scores[entity_index] += cur_score
#                        if word in top_victim_words[entity_index]:
#                            top_victim_words[entity_index][word] += cur_score
#                        else:
#                            top_victim_words[entity_index][word] = cur_score

    # Compute total headline scores
    # TODO incorporate this headline code into actual assignment
    # print("HEADLINE:")
    # for i, entity in enumerate(entities):
    #     if counts[i] != 0:
    #         hero_score = hero_scores[i] / counts[i]
    #         villain_score = villain_scores[i] / counts[i]
    #         victim_score = victim_scores[i] / counts[i]
    #     else:
    #         hero_score, villain_score, victim_score = 0, 0, 0
    #
    #     print(entity)
    #     print("HERO:", hero_score)
    #     print("HERO TOP WORDS:", get_top_words(top_hero_words[i]))
    #     print("VILLAIN:", villain_score)
    #     print("VILLAIN TOP WORDS:", get_top_words(top_villain_words[i]))
    #     print("VICTIM:", victim_score)
    #     print("VICTIM TOP WORDS:", get_top_words(top_victim_words[i]))
    #
    #     # entity.role = role_to_string(role)
    #     # print(entity)
    #     # print(entity.role)
    #
    #     print("------------------------")

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
            loc = entity.locations[sentence_index]
            entity_string = tokenized_sentence[loc[-1]]  # Use last index of entity
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
    entities_names_scores = [None, None, None]
    top_words = [None, None, None]
    for i, entity in enumerate(entities):
        hero_score = hero_scores[i] / counts[i]
        villain_score = villain_scores[i] / counts[i]
        victim_score = victim_scores[i] / counts[i]

        # algorithm to determine entity roles
        entity.role = HERO
        max_score = max(hero_score, villain_score, victim_score)
        if villain_score == max_score:
            entity.role = VILLAIN
        elif victim_score == max_score:
            entity.role = VICTIM

        if not entities_names_scores[entity.role] or max_score > entities_names_scores[entity.role][1]:
            entities_names_scores[entity.role] = (entity.name, max_score)

            if entity.role == HERO:
                top_words[HERO] = [x[0] for x in get_top_words(top_hero_words[i])]
            elif entity.role == VILLAIN:
                top_words[VILLAIN] = [x[0] for x in get_top_words(top_villain_words[i])]
            else:
                top_words[VICTIM] = [x[0] for x in get_top_words(top_victim_words[i])]

        print(entities_names_scores)
        print(top_words)

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

        print("------------------------")

    return entities_names_scores, top_words


def identifyHeroVillianVictimONErole(entity, hero_score, villian_score, victim_score):
    maxScore = max(hero_score, villian_score, victim_score)
    if maxScore == hero_score:
        role = "Hero"
    if maxScore == villian_score:
        role = "Villian"
    if maxScore == victim_score:
        role = "Victim"
    return role

#create a data structure that has dic entity name, role,  top words,


if __name__ == "__main__":
    main2(
"https://www.bbc.com/news/world-asia-india-47341941",
          0.2, 0.1,  # additional score, decay factor
          )
