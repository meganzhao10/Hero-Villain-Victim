##need to install:
# pip install beautifulsoup4
# pip install lxml
# pip install requests 
# pip install html5lib

# work to do - 
## currently can extract from a url

##I currently have the texts print to the terminal
## stored as strings in list
## I could try to make it store into csv if that's easier for other people's work
from bs4 import BeautifulSoup

import requests
import csv


url = input("Enter a website to extract the URL's from: ")

r  = requests.get(url)

data = r.text

soup = BeautifulSoup(data,"lxml")
#print( soup.prettify())
headline = soup.title.string
print("Title is",soup.title.string)
#print("title is ")
#print(soup.get_text())

#print(soup.find_all("p"))


#http://print("title is ",soup.title.string)
#for link in soup.find_all('a'):
#    print(link.get('href'))
content = soup.find_all('p')
#title = soup.find_all('h2')
#print(title)
#print(content)
l = list()
for i in soup.find_all("p"):
    l.append(i.get_text())
    print(i.get_text())
#print(l)
