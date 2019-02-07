

#NEED TO INSTALL 
#pip3 install news-please
#requires both newspaper and beautifulsoup

from newsplease import NewsPlease
import urllib.request

url = "https://www.nbcnews.com/news/religion/ungodly-abuse-lasting-torment-new-tribes-missionary-kids-n967191"


content = NewsPlease.from_url(url)




#content = NewsPlease.from_url(url)
headline = content.title
article = content.text

print(headline)
print(article)




'''
NewPlease (usually takes longer time) works for:
BBC
reuters
news.yahoo.com
huffingtonpost
https://www.latimes.com/
https://www.usatoday.com/
https://www.theguardian.com/us
https://www.washingtonpost.com/?reload=true
https://www.dailymail.co.uk/ushome/index.html
nbc

Partially works for:
NY Times partial 
CNN (read more thing)
wsj: mainly because subsribtion restriction




NOT WORK FOR:
https://abcnews.go.com/
usNEWS


Cookie handling : Some websites need cookie handling. At the moment the only work around is to use the raw_html extraction. For instance ;
'''