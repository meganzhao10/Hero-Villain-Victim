from nltk import (
     word_tokenize, pos_tag, ne_chunk, sent_tokenize,
 )
from newspaper import Article




url = input("Enter a website to extract the URL's from: ")
content = Article(url)
content.download()
content.parse()

headline = content.title
article = content.text


# from nltk.tokenize import MWETokenizer
# entity_categories = ['GPE', 'PERSON', 'ORGANIZATION']
#short_article = "Saudi Arabia was preparing an alternative explanation of the fate of a dissident journalist on Monday, saying he died at the Saudi Consulate in Istanbul two weeks ago in an interrogation gone wrong, according to a person familiar with the kingdom’s plans."

#headline = "Keith Ellison’s Campaign Overshadowed by Ex-Girlfriend’s Allegations"
# article = """
# When Keith Ellison started his bid to become Minnesota’s next attorney general, Keith Ellison had formidable advantages.

# An outspoken progressive who had served in Congress for more than a decade, Mr. Ellison was one of the most recognizable politicians in the state. As deputy chairman of the Democratic National Committee, he had a national profile that has helped him raise nearly twice as much money as his Republican challenger, Doug Wardlow, a lawyer. On top of that, there was history: Minnesota has not elected a Republican attorney general since 1966 in Minnesota.

# But in recent weeks, Mr. Ellison’s edge appears to be evaporating, amid claims by his ex-girlfriend, Karen Monahan, that he mistreated her during their long-term relationship. Ms. Monahan has accused him of causing emotional pain through infidelity and dishonesty when they were a couple and said he had once tried to drag her off a bed after an argument while screaming obscenities at her.


# Recent polls show that Mr. Wardlow, a little-known conservative, is now in a tight race with Mr. Ellison. One poll has them deadlocked, while another has the congressman with a slim lead, with 41 percent of voters supporting Mr. Ellison and 36 percent supporting Mr. Wardlow.

# A loss by Mr. Ellison, the first Muslim elected to Congress, would be a stunning blow to a leader of the ascendant progressive wing of the Democratic Party. Mr. Wardlow has pounced on the allegations, releasing an ad that portrayed Mr. Ellison as a perpetrator of domestic violence. Mr. Ellison, a champion of feminist causes, now finds himself struggling to respond amid a contentious national debate over the #MeToo movement, roiled even further after the accusations against Justice Brett M. Kavanaugh of the Supreme Court.

# Mr. Ellison denies the allegations, including those of infidelity, and said in an extensive interview that he had been conflicted about how to react. He said he wanted to clear his name but did not want to demonize Ms. Monahan, 44, an environmental activist with whom he had a long-term relationship.

# “The #MeToo movement is a justice movement, and I don’t ever want to be counted among those who in some way tried to dissuade victims from coming forward,” he said. “But I think the #MeToo movement has room for due process. Every social justice movement must.”

# As allegations against politicians emerge, voters are grappling with what behavior constitutes abuse and when it should be disqualifying. In Mr. Ellison’s case, the claims are not about unwanted sexual advances, but emotional pain and a fight that Ms. Monahan said became physical when he grabbed her leg. In Minnesota, a majority of voters — 57 percent — said they were unsure what to think about the accusations against Mr. Ellison, according to a Star Tribune/MPR News poll.

# Ms. Monahan claims to have taken a cellphone video of Mr. Ellison pulling her across the bed, her sole allegation of physical abuse, but has refused to show it to anyone. An investigation commissioned by Minnesota’s Democratic-Farmer-Labor Party, which has endorsed Mr. Ellison, recently concluded that Ms. Monahan’s allegations of physical abuse were unsubstantiated.

# “An allegation standing alone is not necessarily sufficient to conclude that the conduct occurred, particularly where the accusing party declines to produce supporting evidence that she herself asserts exists,” wrote the investigator, Susan Ellingstad, who heads the employment law department of the firm Lockridge Grindal Nauen.

# Mr. Wardlow has called the investigation against Mr. Ellison “a sham,” noting that the law firm where Ms. Ellingstad works had donated to Mr. Ellison’s campaigns.

# In recent days, Mr. Wardlow has championed Ms. Monahan’s cause on conservative news media outlets, highlighting what he called a double standard for Democrats who have rallied around Mr. Kavanaugh’s accusers while ignoring Ms. Monahan. Sarah Huckabee Sanders, the White House spokeswoman, and the conservative talk show hosts Tucker Carlson and Glenn Beck made similar remarks.

# Ms. Monahan, a well-known progressive organizer in Minneapolis, recently retained Andrew Parker, a lawyer who is Mr. Wardlow’s former boss, to represent her. Ms. Monahan declined to comment and referred all questions to Mr. Parker.

# “The fact that she has a video and people are bullying and requiring her to show it” amounted to revictimizing her, said Mr. Parker, who amergeded that he also had not seen the video. “She will not do that.”

# Mr. Parker amergeded that there was “more than enough evidence” to corroborate Ms. Monahan’s claims, including her accounts of the abuse to friends and doctors.

# The race presents voters with a stark choice. Mr. Ellison, a supporter of transgender and reproductive rights, has vowed to challenge the Trump administration as attorney general by protecting the Affordable Care Act and being an advocate for immigrants. Mr. Wardlow once served as legal counsel for the conservative Christian group Alliance Defending Freedom and has promised to crack down on sanctuary cities and voter fraud.

# But Mr. Ellison’s campaign has been consumed with Ms. Monahan’s allegations.

# Mr. Ellison said the final stages of the relationship had been marked by frequent arguments but said he was stunned by Ms. Monahan’s abuse allegations and her recent emergence as a cause célèbre of the Republican Party. “I think the question to be asked is, ‘What is her ultimate goal?’” he said. “If her goal is to frustrate my political future, maybe she’ll ally with anyone who can help her achieve that.”

# Ms. Monahan has said on Twitter, “I didn’t #WalkAwayFromDemocrats, they #WalkedAway from me.”

# Mr. Ellison’s inner circle has been divided over how to respond to allegations, which Ms. Monahan has been alluding to on Twitter and Facebook — without naming him — since the couple’s tumultuous breakup. Some advocated a vigorous defense, while others saw nothing to be gained by talking about her claims.

# Friends of the couple have described the relationship as rocky, with Ms. Monahan often accusing Mr. Ellison of infidelity. Even after they separated and she moved out of his house, Ms. Monahan continued trying to prove that he had been unfaithful to her, he said.

# Ms. Monahan visited him in January 2017 and searched his phone without his permission, obtaining screenshots of text messages that he had sent to two other women. She also left a handwritten journal at his house that insulted one of the women he had started dating, calling her “old.” Ms. Monahan later wrote the woman a letter accusing the woman of stealing Mr. Ellison’s affections.

# Mr. Ellison said he had tried to strike a conciliatory tone with Ms. Monahan. She sent him videos, articles and texts about “narcissist abuse,” a nonmedical term that has gained popularity online to describe the pain experienced by partners of pathologically self-centered people. And she asked him to discuss the articles with her, saying that she wanted to help him and that she also wanted “restorative justice.”

# “She wanted to meet and talk about the relationship and try to process the issues,” he said.

# He watched one of the videos but told Ms. Monahan he did not agree with her assessment.

# “I think I’m fairly well adjusted,” he said in an interview. “I’m not saying I don’t go through the normal ups and downs of life. But I didn’t see this thing about my needing help.”

# Mr. Ellison said that the last time he saw Ms. Monahan, at a coffee shop in June, he asked her why she kept writing on Twitter about him. “She said she had a right to tell her story,” he said.

# He said he assumed that she was going to continue her “cryptic-sounding tweets” but was shocked when she and her son accused him of physical abuse by name on social media days before the Democratic primary.

# “I never thought she was going to do this,” he said. “I knew she could not possibly produce a tape of what she described.”

# Ms. Monahan told Ms. Ellingstad, the investigator, that Mr. Ellison’s decision to run for attorney general “screamed entitlement” and had convinced her to go public.

# Ever since, Mr. Ellison has been trying to dispel the cloud that has hovered over his campaign. The Minneapolis Star Tribune and Alpha News, a right-leaning news site, have sued to unseal Mr. Ellison’s divorce records. His ex-wife, Kim Ellison, has said he was never abusive during their 25-year marriage.

# Ms. Ellingstad’s report has been forwarded to local law enforcement officials, who have declined to take up the matter. Mr. Ellison has asked the House Ethics Committee to look into the allegations as well.

# A group of progressive women, including a former Minneapolis mayor, Betsy Hodges, recently released a letter explaining why they continue to support Mr. Ellison.

# Abena Abraham, 22, who signed and helped craft the letter, said that disposing of Mr. Ellison and electing his Republican rival would not end violence against women or promote the cause of women’s rights.

# “We should elect him and then hold him accountable,” she said.

# Many liberals in the state continue to express bitterness that another progressive star, Senator Al Franken, was forced to resign without an investigation after he was accused of groping a sleeping woman for a photograph and of trying to kiss a Senate aide.

# But Billy Grant, Mr. Wardlow’s campaign manager, predicted that the allegations against Mr. Ellison would cause many progressives either to vote for the third-party candidate, from the Grassroots-Legalize Cannabis Party, or to leave that part of the ballot blank.

# “The court of public opinion is all we’re going to have before the election,” he said.

# That may be the only thing that Mr. Ellison and Mr. Wardlow agree on. Asked how the allegations were affecting his race, Mr. Ellison said, “We won’t really know until the evening of November 6th.”

# """


class Entity:
    name = ""
    count = 0
    locations = {}
    headline = False

    def __init__(self, name, sentence_number=None, index_list=None, headline=False):
        self.name = name
        self.count = 1
        if sentence_number is not None and index_list is not None:
            self.locations = {sentence_number: index_list}
        if headline:
            self.headline = True

    def __repr__(self):
        return f'(Name: {self.name}, Count: {self.count}, Headline: {self.headline}, Locations: {self.locations})'


def extract_entities_article(article):
    '''
    Returns a list of (unmerged) entities from the article.

    Each entity is a tuple (entity name, sentence number)
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


def extract_entities_headline(headline):
    '''
    Returns a list of (unmerged) entities from the article.

    Each entity is a tuple (entity name, "HEADLINE")
    '''
    named_entities = []
    tokens = word_tokenize(headline)
    tagged_sentences = pos_tag(tokens)
    chunked_entities = ne_chunk(tagged_sentences)

    for tree in chunked_entities:
        if hasattr(tree, 'label'):
            entity = {}
            entity_name = ' '.join(c[0] for c in tree.leaves())
            entity = (entity_name, "HEADLINE", [])
            named_entities.append(entity)

    return named_entities


def merge_entities(entities):
    merged_entities = []
    for temp_entity in entities:
        name, sentence_number, index_list = temp_entity
        entity_updated = False
        for entity in merged_entities:
            if entity.name == name:  # TODO replace this line with actual merging
                entity.count += 1
                if sentence_number == "HEADLINE":
                    entity.headline = True
                else:
                    locations = entity.locations
                    if sentence_number in locations:
                        locations[sentence_number] += index_list
                    else:
                        locations[sentence_number] = index_list
                entity_updated = True
                break
        if not entity_updated:  # create new entity if no update happened
            if sentence_number == "HEADLINE":
                entity = Entity(name, headline=True)
            else:
                entity = Entity(name, sentence_number=sentence_number, index_list=index_list)
            merged_entities.append(entity)
    return merged_entities


# TESTING
h = extract_entities_headline(headline)  # TODO this results in weird output, headline may need to be treated differently
a = extract_entities_article(article)
for e in merge_entities(a):
    print(e)


# parameters: alpha/headline weight, entity object, total number of sentences
def relevanceScore(alpha, entity, numOfSentences):
    '''
    Calculate the relevance score for each of the merged entity in the
    input and return the three entities with the highest relevance score.

    Assume entities is a dictionary of key: entity and value: list of sentence
    indices
    '''
    score = 0
    if entity.headline:
        score += alpha
    firstLocation = min([key for key in entity.locations]) + 1
    score += entity.count / (numOfSentences * firstLocation)
    return score


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
