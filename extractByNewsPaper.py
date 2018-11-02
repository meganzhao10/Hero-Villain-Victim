#NEED TO INSTALL 
#pip3 install newspaper3k


from newspaper import Article
import nltk
## my device runs into error when trying to download punkt
#nltk.download('punkt')

#import requests




def test():

    
    url = input("Enter a website to extract the URL's from: ")
    content = Article(url)
    content.download()
    content.parse()

    headline =content.title
    article = content.text

    print('Headline: ', headline)
    temp_entities, num_sentences = extract_entities_article(article)
    merged_entities = merge_entities(temp_entities)
    get_headline_entities(headline, merged_entities)
    print('Merged Entities:')
    for e in merged_entities:
        print(e)
    print('------------------------')
    highest_score_entities = select_high_score_entities(0.5, merged_entities, num_sentences)
    
    headline_entities = [e for e in merged_entities if e.headline and e not in highest_score_entities]
    top_entities = highest_score_entities + headline_entities
    print("------------------------------------------")
    print("Top Entities")
    for e in top_entities:
        print(e)


test()
