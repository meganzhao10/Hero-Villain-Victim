from nltk.corpus import wordnet
import sys
from role_dictionaries import *


#scripts for command line argument 
list_w1 = wordnet.synsets(sys.argv[1])
list_w2 = wordnet.synsets(sys.argv[2])
score = 0
for w1 in list_w1:
    for w2 in list_w2:
        cur_score = w1.wup_similarity(w2)
        if cur_score:
            score = max(score, cur_score)
print(score)
'''
result = []
for word1 in VILLAIN_DICT:
    for word2 in VILLAIN_DICT:
        if word1 != word2:
            list_w1 = wordnet.synsets(word1)
            list_w2 = wordnet.synsets(word2)
            score = 0
            for w1 in list_w1:
                for w2 in list_w2:
                    cur_score = w1.wup_similarity(w2)
                    if cur_score:
                        if cur_score == 1:
                            score = cur_score
                            break
                        else:
                            score = max(score, cur_score)
            if score == 1:
                result.append((word1, word2))
print(result)
'''
