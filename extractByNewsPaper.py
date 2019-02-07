#NEED TO INSTALL 
#pip3 install newspaper3k


from newspaper import Article
## my device runs into error when trying to download punkt
#nltk.download('punkt')

url = "https://www.nbcnews.com/news/religion/ungodly-abuse-lasting-torment-new-tribes-missionary-kids-n967191"


content = Article(url)
content.download()
content.parse()
headline = content.title
article = content.text

print(headline)
print(article)



'''
NewsPaper works for:
BBC
reuters
news.yahoo.com
huffingtonpost
https://www.latimes.com/
https://www.usatoday.com/
usnews
https://www.theguardian.com/us
https://www.washingtonpost.com/?reload=true
https://www.dailymail.co.uk/ushome/index.html
nbc



Partially works for:
NY Times partial 
CNN (read more thing) - show part of the content, and then "Read More"...
wsj: mainly because subsribtion restriction





NOT WORKING:
https://abcnews.go.com/


'''