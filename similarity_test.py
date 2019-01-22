from nltk.corpus import wordnet
import sys

list_w1 = wordnet.synsets(sys.argv[1])
list_w2 = wordnet.synsets(sys.argv[2])
score = 0
for w1 in list_w1:
    for w2 in list_w2:
        cur_score = w1.wup_similarity(w2)
        if cur_score:
            score = max(score, cur_score)
print(score)
