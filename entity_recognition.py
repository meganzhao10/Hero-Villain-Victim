'''
Potential concerns and possible features to implement in the future
-Exclude the location tag at the beginning of the article
-Dealing with positions (the witness...)
'''
# TODO remove all print statements once done testing

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
    name = ""
    normalized_name = ""
    count = 0
    locations = {}
    headline_locations = []
    headline = False
    name_forms = []
    role = ""

    def __init__(self, name, normalized_name, sentence_number=None, index_list=None, headline=False, headline_index_list=None):
        self.name = name
        self.normalized_name = normalized_name
        self.count = 1
        if sentence_number is not None and index_list is not None:
            self.locations = {sentence_number: index_list}
        if headline:
            self.headline = True
        if headline_index_list is not None:
            self.headline_locations
        self.name_forms = [name]

    def __repr__(self):
        return ('(Name: {name}, Count: {count}, Headline: {headline}, '
                'Headline Locations: {headline_locs}, Text Locations: {locations})'
                .format(name=self.name, count=self.count, headline=self.headline,
                        locations=self.locations, headline_locs=self.headline_locations,
                        )
                )


def get_locations(name, tokens, locations_found):
    '''
    Returns a list of indeces of the locations of name in the given tokenized
    set of words. Location is represented as the first and last index of each
    occurence of name. Updates locations_found dictionary accordingly.
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
                index_list += [j, j + length - 1]
            break
    return index_list


def extract_entities_article(tokenized_article):
    '''
    Returns a tuple where the first item is a list of (unmerged) entities from
    the article and the second item is the number of sentences in the article.

    Each entity is a tuple (entity name, sentence number, locations in sentence)
    '''
    named_entities = []
    num_sentences = len(tokenized_article)
    for i in range(num_sentences):
        sentence = tokenized_article[i]
        tokens = word_tokenize(sentence)
        tagged_sentence = pos_tag(tokens)
        chunked_entities = ne_chunk(tagged_sentence)

        locations_found = {}
        for tree in chunked_entities:
            if hasattr(tree, 'label') and tree.label() in RECOGNIZED_TYPES:
                # TODO: Currently checking entity type before merging, but adding type to entity to check after merging?
                entity = {}
                entity_name = ' '.join(c[0] for c in tree.leaves())
                sentence_number = i
                index_list = get_locations(entity_name, tokens, locations_found)
                entity = (entity_name, sentence_number, index_list)
                named_entities.append(entity)
    return (named_entities, num_sentences)


def merge_entities(temp_entities):
    '''
    Merges the list of temporary entity tuples into a list of Entity objects.
    Basis of merging algorithm from Function from NU Infolab News Context Project
    (https://github.com/NUinfolab/context).
    '''
    merged_entities = []
    for temp_entity in temp_entities:
        name, sentence_number, index_list = temp_entity
        normalized_name = normalize_name(name)
        matches = []
        for entity in merged_entities:
            if normalized_name == entity.normalized_name:
                matches = [entity]
                break
            if normalized_name in entity.normalized_name:
                matches.append(entity)

        # if name is substring of one existing entity, merge it
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
        # otherwise make new entity
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
    # when input text is unicode encoded in utf-8
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
    score += entity.count / (num_sentences * first_location)
    return score


def select_high_score_entities(alpha, entity_list, num_sentences):
    '''
    Returns a list of the three entities with highest relevance score.
    '''
    first, second, third = -1, -1, -1
    result = [None, None, None]
    for entity in entity_list:
        score = relevance_score(alpha, entity, num_sentences)
        if score > first:
            third = second
            second = first
            first = score
            result[2] = result[1]
            result[1] = result[0]
            result[0] = entity
        elif score > second:
            third = second
            second = score
            result[2] = result[1]
            result[1] = entity
        elif score > third:
            third = score
            result[2] = entity
    return [x for x in result if x is not None]


def get_headline_entities(headline, merged_entities):
    '''
    Extracts the entities from the headline and updates merged_entities accordingly.
    '''
    # print("HEADLINE ENTITIES:")  # TODO remove after testing
    locations_found = {}
    tokens = word_tokenize(headline)
    for entity in merged_entities:
        for name in entity.name_forms:
            index_list = get_locations(name, tokens, locations_found)
            if index_list:
                count = len(index_list) // len(name.split())
                for i in index_list:
                    tokens[i] = ''  # replace to avoid double counting but maintain indeces
                # print(name, '- Count:', count, '- Locations:', index_list)  # TODO remove after testing
                entity.count += count
                entity.headline = True
                if entity.headline_locations:
                    entity.headline_locations += index_list
                else:
                    entity.headline_locations = index_list
    # print('---------------')  # TODO remove after testing


def get_top_entities(headline, tokenized_article):
    # url = input("Enter a website to extract the URL's from: ")
    # print('Headline: ', headline)
    temp_entities, num_sentences = extract_entities_article(tokenized_article)
    merged_entities_ = merge_entities(temp_entities)

    # Filter out images (entity recognizer thinks images are entities)
    merged_entities = []
    for entity in merged_entities_:
        if "image" not in entity.name.lower():
            merged_entities.append(entity)

    get_headline_entities(headline, merged_entities)

    '''
    print('Merged Entities:')
    for e in merged_entities:
        print(e)
    print('------------------------')
    '''

    highest_score_entities = select_high_score_entities(0.5, merged_entities, num_sentences)
    headline_entities = [e for e in merged_entities if e.headline and e not in highest_score_entities]
    top_entities = highest_score_entities + headline_entities
    '''
    print("Top Entities")
    for e in top_entities:
        print(e)
    '''
    return top_entities
