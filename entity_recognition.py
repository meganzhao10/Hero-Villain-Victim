'''
Recognizes the entities in a news article with a headline and determines
which of these entities are the  most relevant.
'''

import codecs
from nltk import ne_chunk, pos_tag, word_tokenize

RECOGNIZED_TYPES = ["PERSON", "ORGANIZATION", "GPE", "POSITION"]

NAME_PREFIXES = (
    'mr',
    'mrs',
    'ms',
    'miss',
    'dr',
    'doctor',
    'sgt',
    'sergeant',
    'rev',
    'reverend',
    'chief',
    'executive',
    'officer',
    'president',
)


class Entity:
    '''
    Represents an entity in the news article. Contain the entities top-level
    name, all name forms used in the article, count of occurences, and data
    about its locations within the article and headline.
    '''
    name = ""
    normalized_name = ""
    count = 0
    locations = {}
    headline_locations = []
    headline = False
    name_forms = []
    role = ""

    def __init__(self, name, normalized_name, sentence_number=None,
                 index_list=None, headline=False, headline_index_list=None,
                 ):
        '''
        Construct a new entity.
        '''
        self.name = name
        self.normalized_name = normalized_name
        self.count = 1
        if sentence_number is not None and index_list is not None:
            self.locations = {sentence_number: index_list}
        if headline:
            self.headline = True
        if headline_index_list is not None:
            self.headline_locations = headline_index_list
        self.name_forms = [name]

    def __repr__(self):
        '''
        String representation of the entity.
        '''
        return ('(Name: {name}, Count: {count}, Headline: {headline}, '
                'Headline Locations: {headline_locs}, Text Locations: {locations})'
                .format(name=self.name, count=self.count, headline=self.headline,
                        locations=self.locations, headline_locs=self.headline_locations,
                        )
                )


def get_locations(name, tokens, locations_found):
    '''
    Returns a list of indeces of the locations of name in the given tokenized
    set of words. Location are represented either as an index of the location
    (if the occurence is one word) or a tule of the first and last index of the
    entity (if the occurence is multiple words). Updates locations_found
    dictionary accordingly.
    '''
    index_list = []
    lastIndex = locations_found.get(name, 0)
    length = len(name.split())
    for j in range(lastIndex, len(tokens) - length + 1):
        if " ".join(tokens[j:j + length]) == name:
            locations_found[name] = j + length
            if length == 1:
                index_list.append(j)
            else:
                index_list.append((j, j + length - 1))
    return index_list


def extract_entities_article(tokenized_article):
    '''
    Returns a tuple where the first item is a list of (unmerged) entities from
    the article and the second item is the number of sentences in the article.

    Each entity is a tuple (entity name, sentence number, locations in sentence)
    '''
    named_entities = []
    num_sentences = len(tokenized_article)
    for sentence_number in range(num_sentences):
        sentence = tokenized_article[sentence_number]
        tokens = word_tokenize(sentence)
        tagged_sentence = pos_tag(tokens)
        chunked_entities = ne_chunk(tagged_sentence)

        locations_found = {}
        for tree in chunked_entities:
            if hasattr(tree, 'label') and tree.label() in RECOGNIZED_TYPES:
                entity_name = ' '.join(c[0] for c in tree.leaves())
                index_list = get_locations(entity_name, tokens, locations_found)
                entity = (entity_name, sentence_number, index_list)
                named_entities.append(entity)

    return (named_entities, num_sentences)


def merge_entities(temp_entities):
    '''
    Merges the list of temporary entity tuples into a list of Entity objects.
    Basis of merging algorithm from from NU Infolab News Context Project.
    (https://github.com/NUinfolab/context).
    '''
    merged_entities = []
    for temp_entity in temp_entities:
        name, sentence_number, index_list = temp_entity
        normalized_name = normalize_name(name)
        matches = []
        for entity in merged_entities:
            # Immediate match if name matches previously used name form
            if normalized_name == entity.normalized_name or normalized_name in entity.name_forms:
                matches = [entity]
                break
            # Get entities of which name is substring
            if normalized_name in entity.normalized_name:
                matches.append(entity)

        # If name matches one existing entity, merge it
        if len(matches) == 1:
            entity = matches[0]
            entity.count += 1
            if name not in entity.name_forms:
                entity.name_forms.append(name)
            locations = entity.locations
            if sentence_number in locations:
                locations[sentence_number] += index_list
            else:
                locations[sentence_number] = index_list
        # Otherwise make new entity
        else:
            entity = Entity(name, normalized_name, sentence_number=sentence_number, index_list=index_list)
            merged_entities.append(entity)

    return merged_entities


def normalize_name(name):
    '''
    Removes prefix and 's from the given name.
    Function from NU Infolab News Context Project (https://github.com/NUinfolab/context).
    '''
    name = name.split()
    for i, word in enumerate(name):
        if word.lower().strip().strip('.') not in NAME_PREFIXES:
            break
    no_prefix = name[i:]
    normalized = ' '.join(no_prefix)

    # When input text is unicode encoded in utf-8
    try:
        s = codecs.decode("’s", 'utf-8')
    except:
        s = "’s"
    if normalized.endswith("'s") or normalized.endswith(s):
        normalized = normalized[:-2]

    return normalized


def relevance_score(alpha, entity, num_sentences):
    '''
    Calculate the relevance score for the given entity.
    '''
    score = 0
    if entity.headline:
        score += alpha
    first_location = min([key for key in entity.locations]) + 1
    score += entity.count / (num_sentences * (first_location ** 0.25))
    return score


def select_high_score_entities(alpha, entity_list, num_sentences):
    '''
    Returns a list of the 4 entities with highest relevance score
    above a threshold of 0.07 (chosen after testing many articles).
    '''
    score_list = []
    for entity in entity_list:
        score = relevance_score(alpha, entity, num_sentences)
        score_list.append((entity, score))

    score_list = sorted(score_list, key=lambda x:x[1], reverse = True)
    return [x[0] for x in score_list[:4] if x[1] > 0.07]  # threshold: 0.07


def get_headline_entities(headline, merged_entities):
    '''
    Extracts the entities from the headline and updates merged_entities accordingly.
    '''
    locations_found = {}
    tokens = word_tokenize(headline)
    for entity in merged_entities:
        for name in entity.name_forms:
            index_list = get_locations(name, tokens, locations_found)
            if index_list:
                count = len(index_list)
                # Replace to avoid double counting but maintain indeces
                for i in index_list:
                    if isinstance(i, int):
                        tokens[i] = ''
                    else:
                        for j in range(i[0], i[1]+1):
                            tokens[j] = ''
                entity.count += count
                entity.headline = True
                if entity.headline_locations:
                    entity.headline_locations += index_list
                else:
                    entity.headline_locations = index_list


def get_top_entities(headline, tokenized_article):
    '''
    Returns the top entities (as entity objects) from the given headline (string)
    and the tokenized article.
    '''
    temp_entities, num_sentences = extract_entities_article(tokenized_article)
    merged_entities_ = merge_entities(temp_entities)

    # Filter out images (entity recognizer thinks images are entities)
    merged_entities = []
    for entity in merged_entities_:
        if "image" not in entity.name.lower():
            merged_entities.append(entity)

    get_headline_entities(headline, merged_entities)
    top_entities = select_high_score_entities(0.01, merged_entities, num_sentences)
    return top_entities
