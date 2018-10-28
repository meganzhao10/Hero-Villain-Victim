import codecs
from nltk import (
     word_tokenize, pos_tag, ne_chunk, sent_tokenize,
 )
from newspaper import Article


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
    headline = False
    name_forms = []

    def __init__(self, name, normalized_name, sentence_number=None, index_list=None, headline=False):
        self.name = name
        self.normalized_name = normalized_name
        self.count = 1
        if sentence_number is not None and index_list is not None:
            self.locations = {sentence_number: index_list}
        if headline:
            self.headline = True
        self.name_forms = [name]

    def __repr__(self):
        return '(Name: {name}, Count: {count}, Headline: {headline}, Locations: {locations})'.format(
                name=self.name, count=self.count, headline=self.headline, locations=self.locations
        )


def extract_entities_article(article):
    '''
    Returns a tuple where the first item is a list of (unmerged) entities from
    the article and the second item is the number of sentences in the article.

    Each entity is a tuple (entity name, sentence number, locations in sentence)
    '''
    sentences = sent_tokenize(article)
    named_entities = []
    num_sentences = len(sentences)
    for i in range(num_sentences):
        sentence = sentences[i]
        tokens = word_tokenize(sentence)
        tagged_sentences = pos_tag(tokens)
        chunked_entities = ne_chunk(tagged_sentences)

        locationsFound = {}

        for tree in chunked_entities:
            if hasattr(tree, 'label') and tree.label() in RECOGNIZED_TYPES:
                # TODO: Currently checking entity type before merging, but adding type to entity to check after merging?
                entity = {}
                entity_name = ' '.join(c[0] for c in tree.leaves())
                sentence_number = i
                index_list = []
                lastIndex = locationsFound.get(entity_name, 0)
                length = len(entity_name.split())
                for j in range(lastIndex, len(tokens) - length):
                    if " ".join(tokens[j:j + length]) == entity_name:
                        locationsFound[entity_name] = j + length
                        if length == 1:
                            index_list.append(j)
                        else:
                            index_list += [j, j + length - 1]
                        break

                entity = (entity_name, sentence_number, index_list)
                named_entities.append(entity)
    return (named_entities, num_sentences)


# TODO fix this function. currently results in weird output, headline may need to be treated differently
def extract_entities_headline(headline):
    '''
    Returns a list of (unmerged) entities from the article headline.

    Each entity is a tuple (entity name, "HEADLINE", locations)
    '''
    named_entities = []
    tokens = word_tokenize(headline)
    tagged_sentences = pos_tag(tokens)
    chunked_entities = ne_chunk(tagged_sentences)

    for tree in chunked_entities:
        if hasattr(tree, 'label'):
            entity = {}
            entity_name = ' '.join(c[0] for c in tree.leaves())
            # TODO get locations within headline
            entity = (entity_name, "HEADLINE", [])
            named_entities.append(entity)

    return named_entities


def merge_entities(temp_entities):
    '''
    Merges the list of temporary entity tuples into a list of Entity objects.
    Basis of merging algorithm from Function from NU Infolab News Context Project (https://github.com/NUinfolab/context).
    '''
    merged_entities = []
    for temp_entity in temp_entities:
        name, sentence_number, index_list = temp_entity
        normalized_name = normalize_name(name)
        matches = []
        for entity in merged_entities:
            if normalized_name in entity.normalized_name:
                matches.append(entity)

        # if name is substring of one existing entity, merge it
        if len(matches) == 1:
            entity = matches[0]
            entity.count += 1
            if name not in entity.name_forms:
                entity.name_forms.append(name)
            if sentence_number == "HEADLINE":
                entity.headline = True
            else:
                locations = entity.locations
                if sentence_number in locations:
                    locations[sentence_number] += index_list
                else:
                    locations[sentence_number] = index_list
        # otherwise make new entity
        else:
            if sentence_number == "HEADLINE":
                entity = Entity(name, normalized_name, headline=True)
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


def relevanceScore(alpha, entity, num_sentences):
    '''
    Calculate the relevance score for the given entity.
    '''
    score = 0
    if entity.headline:
        score += alpha
    first_location = min([key for key in entity.locations]) + 1
    score += entity.count / (num_sentences * first_location)
    return score


def selectHighScoreEntities(alpha, entity_list, num_sentences):
    '''
    Returns a list of the three entities with highest relevance score.
    '''
    first, second, third = -1, -1, -1
    result = [None, None, None]
    for entity in entity_list:
        score = relevanceScore(alpha, entity, num_sentences)
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
    return result


def test():
    url = input("Enter a website to extract the URL's from: ")
    content = Article(url)
    content.download()
    content.parse()

    headline = content.title
    article = content.text

    temp_entities, num_sentences = extract_entities_article(article)
    merged_entities = merge_entities(temp_entities)
    print('Merged Entities:')
    for e in merged_entities:
        print(e)
    highest_score_entities = selectHighScoreEntities(0.5, merged_entities, num_sentences)
    # TODO add all entities in headline to role assignment list (first need to implement headline extraction)
    print("Highest Scoring Entities:")
    for e in highest_score_entities:
        print(e)


test()
