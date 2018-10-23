#NEED TO INSTALL 
#pip3 install newspaper3k


from newspaper import Article
import nltk
## my device runs into error when trying to download punkt
#nltk.download('punkt')

#import requests

#url = input("Enter a website to extract the URL's from: ")
#testing url
url = "https://www.bbc.com/news/world-latin-america-45944164"

#r  = requests.get(url)

#data = r.text


article = Article(url)
article.download()
article.parse()

headline =article.title
content = article.text


print(headline)
print(content)


#one possible advantage is the keywords
#need to install nltk
#article.nlp()
#keyWords = article.keywords
#print(keyWords)
