import json
from role_assignment import similarity_to_role, skip_word, HERO, VILLAIN, VICTIM


def process_file(filename, dic):
    '''
    Processes the words in the given file and loads their scores
    into dic.
    '''
    print("Reading", filename)
    with open(filename) as input_file:

        i = 0
        for line in input_file:
            word = line.strip()
            # Skip comments, words ignored for analysis, and words already in dic
            if word[0] != '#' and not skip_word(word, None) and word not in dic:
                scores = [0, 0, 0]
                scores[HERO] = similarity_to_role(HERO)
                scores[VILLAIN] = similarity_to_role(VILLAIN)
                scores[VICTIM] = similarity_to_role(VICTIM)
                dic[word] = scores
            # Print progress
            i += 1
            if i % 250 == 0:
                print(i, "words read...")

        print("DONE:", filename)


def write_results(output_filename, dic):
    with open(output_filename, 'w') as output_file:
        output_file.truncate()
        output_file.write('SIM_DIC = ')
        json.dump(dic, output_file)


dic = {}
# 10k file: 'google-10000-english-usa.txt'
# 100k file: 'wiki-100k.txt'
process_file('wiki-100k.txt', dic)
process_file('google-10000-english-usa.txt', dic)
write_results('similarity_dictionary.py', dic)  # CHANGE THIS FOR FILTERED DICS (AND UPDATE DICS IN ROLE ASSIGNMENT)
