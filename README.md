# Hero-Villain-Victim
A Google Chrome extension to detect roles of hero, villain, and victim in news articles using natural language techniques. 

## Getting Started

### Prerequisites
NLTK

TextBlob
```
pip3 install textblob
```
spacy
```
pip install -U spacy
python3 -m spacy download xx
```
#### newspaper 
```
pip3 install newspaper3k
```
### Installing
Open the Extension Management page by navigating to chrome://extensions.

Click the LOAD UNPACKED button and select the extension directory.


## Built With
* [Newspaper](https://github.com/codelucas/newspaper) - to scrape articles from news sites
* [NLTK](https://www.nltk.org/) - to recognize entities
* [WordNet](https://wordnet.princeton.edu/) - to compute similarity of two word (we probably don't need to include this)
* [TextBlob](https://textblob.readthedocs.io/en/dev/) - to analyze sentiment of words
* [Spacy](https://spacy.io/) - to recognize active/passive sentences


## Authors: 
* **Tianna Avery** - [tiannaavery](https://github.com/tiannaavery)
* **Quinn Mayville** - [mayvilleq](https://github.com/mayvilleq)
* **Yingying Wang** - [yingyingww](https://github.com/yingyingww)
* **Megan Zhao** - [meganzhao](https://github.com/meganzhao)

## Acknowledgments

* Inspired by the paper: Who is the Hero, the Villain, and the Victim?: Detection of Roles in News Articles using Natural Language Techniques (https://dl.acm.org/citation.cfm?id=3172993)
* Advised by David Musicant

