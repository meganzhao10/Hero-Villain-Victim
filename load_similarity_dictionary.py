import json
# from top_words import TOP_WORDS
from role_assignment import word_similarity, skip_word, HERO, VILLAIN, VICTIM
from role_dictionaries import HERO_DICT, VILLAIN_DICT, VICTIM_DICT


# 10k file: 'google-10000-english-usa.txt'
# 100k file: 'wiki-100k.txt'
with open('google-10000-english-usa.txt') as input_file:

    dic = {}
    i = 0
    for line in input_file:
        word = line.strip()
        # Skip comments and words ignored for analysis
        if word[0] != '#' and not skip_word(word, None):
            scores = [0, 0, 0]
            dict_length = len(HERO_DICT)
            for hero_term in HERO_DICT:
                scores[HERO] += word_similarity(word, hero_term)
            scores[HERO] /= len(HERO_DICT)
            for victim_term in VICTIM_DICT:
                scores[VICTIM] += word_similarity(word, victim_term)
            scores[VICTIM] /= len(VICTIM_DICT)
            for villain_term in VILLAIN_DICT:
                scores[VILLAIN] += word_similarity(word, villain_term)
            scores[VILLAIN] /= len(VILLAIN_DICT)

            dic[word] = scores
        # Print progress
        i += 1
        if i % 250 == 0:
            print(i, "words read...")


with open('similarity_dictionary.py', 'w') as output_file:
    output_file.truncate()
    output_file.write('SIM_DIC = ')
    json.dump(dic, output_file)

print("DONE")
