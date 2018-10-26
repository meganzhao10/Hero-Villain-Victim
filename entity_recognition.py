from nltk import (
     word_tokenize, pos_tag, ne_chunk, sent_tokenize,
 )
from newspaper import Article


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
        self.name_forms.append(name)

    def __repr__(self):
        return '(Name: {name}, Count: {count}, Headline: {headline}, Locations: {locations})'.format(
            name=self.name, count=self.count, headline=self.headline, locations=self.locations
        )


def extract_entities_article(article):
    '''
    Returns a list of (unmerged) entities from the article.

    Each entity is a tuple (entity name, sentence number, locations in sentence)
    '''
    sentences = sent_tokenize(article)
    named_entities = []
    for i in range(len(sentences)):
        sentence = sentences[i]
        tokens = word_tokenize(sentence)
        tagged_sentences = pos_tag(tokens)
        chunked_entities = ne_chunk(tagged_sentences)

        locationsFound = {}

        for tree in chunked_entities:
            if hasattr(tree, 'label'):
                # TODO add check for entity type (maybe check after merging to avoid miscategorization??)
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
    return named_entities


# TODO fix this function. currently results in weird output, headline may need to be treated differently
def extract_entities_headline(headline):
    '''
    Returns a list of (unmerged) entities from the article.

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
            # TODO update name_forms
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


# TODO implement normalize name function
def normalize_name(name):
    name = name.split()
    for i, word in enumerate(name):
        if word.lower().strip().strip('.') not in NAME_PREFIXES:
            break
    no_prefix = name[i:]
    normalized = ' '.join(no_prefix)
    # try:
    #     s = codecs.decode("’s", 'utf-8')
    # except:
    #     s = "’s"
    # if normalized.endswith("'s") or normalized.endswith(s):
    #     normalized = normalized[:-2]
    if normalized.endswith("'s"):
        normalized = normalized[:-2]
    return normalized


def relevanceScore(alpha, entity, numOfSentences):
    '''
    Calculate the relevance score for the given entity.
    '''
    score = 0
    if entity.headline:
        score += alpha
    firstLocation = min([key for key in entity.locations]) + 1
    score += entity.count / (numOfSentences * firstLocation)
    return score


# TODO implement function to select three entities with highest relevance score
'''
    # pick three top
    first, second, third = -1, -1, -1
    result = [None, None, None]
    for entity,score in scores:
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
'''

# TESTING
url = input("Enter a website to extract the URL's from: ")
content = Article(url)
content.download()
content.parse()

headline = content.title
article = content.text

a = extract_entities_article(article)
print(a)
for e in merge_entities(a):
    print(e)
