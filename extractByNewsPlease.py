

#NEED TO INSTALL 
#pip3 install news-please
#requires both newspaper and beautifulsoup

from newsplease import NewsPlease

url = input("Enter a website to extract the URL's from: ")

article = NewsPlease.from_url('url')

headline = article.title
content = article.text
print(headline)
print(content)
