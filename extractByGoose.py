import urllib.request

from newspaper import Article, Source

#from newsplease import NewsPlease


url = "https://us.cnn.com/2019/02/07/politics/adam-schiff-trump-white-house-staffers/index.html"
#



f = urllib.request.urlopen(url)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
response = opener.open(url)
raw_html = response.read()
#import requests
#import newspaper
#resp = requests.get(url)
#print(newspaper.fulltext(resp.text))
#
content = Article(url)
content.download(input_html=response.body)
content.parse()
headline = content.title
article = content.text
#
print(headline)
print(article)


#print (raw_html)


#content = NewsPlease.from_url(raw_html)

#content = NewsPlease.from_html(raw_html, url=url) 

##content = NewsPlease.from_url(url)
#headline = content.title
#article = content.text

#
#f= open("text.txt","w+")
#f.write(article)
#print(headline)
#print(article)
#
#print("I worked")



#>>> import urllib2
#>>> import goose
#>>> url = > a = g.extract(raw_html=raw_html)

#"http://www.nytimes.com/2013/08/18/world/middleeast/pressure-by-us-failed-to-sway-egypts-leaders.html?hp"
#>>> opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
#>>> response = opener.open(url)
#>>> raw_html = response.read()