
#This could be useful for us to get the infinitive 
#form of the verb (not supper precise)
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
#print(stemmer.stem('killed'))


'''This software spacy works pretty well for non-p'''
#To instiall:
#pip install -U spacy
#python3 -m spacy download xx
import spacy
nlp = spacy.load('en')
sent = "In the morning, John shot an elephant"
sent1 = "The jury returned a verdict of manslaughter"
sent2 = "Before assembling the guns, you read these instructions carefully"
doc=nlp(sent2)

sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
obj_toks = [tok for tok in doc if (tok.dep_ == "dobj") ]

print("subject is ",sub_toks) 
print("object is ",obj_toks)