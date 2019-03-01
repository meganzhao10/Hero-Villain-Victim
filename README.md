# Hero-Villain-Victim
A Google Chrome extension to detect roles of hero, villain, and victim in news articles using natural language techniques. 

## Getting Started

### Prerequisites
Newspaper 
```
pip3 install newspaper3k
```
NLTK
```
###
```

TextBlob
```
pip3 install textblob
```
Spacy
```
pip install -U spacy
python3 -m spacy download xx
```
### Installing
Open the Extension Management page by navigating to chrome://extensions.

Click the LOAD UNPACKED button and select the extension directory.


## Built With
* [Newspaper](https://github.com/codelucas/newspaper) - scrape articles from news sites
* [NLTK](https://www.nltk.org/) - recognize entities
* [WordNet](https://wordnet.princeton.edu/) - compute similarity of two word (we probably don't need to include this)
* [TextBlob](https://textblob.readthedocs.io/en/dev/) - analyze sentiment of words
* [Spacy](https://spacy.io/) - recognize active/passive sentences


## Authors: 
* **Tianna Avery** - [tiannaavery](https://github.com/tiannaavery)
* **Quinn Mayville** - [mayvilleq](https://github.com/mayvilleq)
* **Yingying Wang** - [yingyingww](https://github.com/yingyingww)
* **Megan Zhao** - [meganzhao](https://github.com/meganzhao)

## Acknowledgments

* Inspired by the paper: Who is the Hero, the Villain, and the Victim?: Detection of Roles in News Articles using Natural Language Techniques (https://dl.acm.org/citation.cfm?id=3172993)
* Advised by David Musicant

