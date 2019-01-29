
'''This software spacy works pretty well for non-passive sentences'''
#To instiall:
#pip install -U spacy
#python3 -m spacy download xx
import spacy
nlp = spacy.load('en')
sent = "In the morning, John shot an elephant"
sent1 = "The jury returned a verdict of manslaughter"
sent2 = "Since then, negotiations have been taking place between the UK and the other EU countries."
sent3 = "In this chapter, we will adopt the formal framework of 'generative grammar'"
sent4="The EU is a political and economic union of 28 countries which trade with each other and allow citizens to move easily between the countries to live and work"
sent5="Carleton was founded by me"
#passive sent returns nothing
doc=nlp(sent5)

sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
dobj_toks = [tok for tok in doc if (tok.dep_ == "dobj") ]
#Looks like we mostly have direct object
#iobj_toks = [tok for tok in doc if (tok.dep_ == "iobj") ]

print("subject is ",sub_toks) 
print("direct object is ",dobj_toks)
#print("indirect object is ",iobj_toks)



#This could be useful for us to get the infinitive 
#form of the verb (not supper precise)
#from nltk.stem import PorterStemmer
#stemmer = PorterStemmer()
#print(stemmer.stem('killed'))
