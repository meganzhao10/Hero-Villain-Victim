from role_assignment import similarity_to_role as sim
from role_assignment import HERO, VILLAIN, VICTIM
from role_dictionaries import HERO_DICT, VILLAIN_DICT, VICTIM_DICT
from role_assignment import skip_word
#from similarity_dictionary import SIM_DIC
from similarity_dictionary_filtered import SIM_DIC
import statistics

std = [0] * 3

def process_file(filename, dic):
    '''
    Processes the words in the given file and loads their scores
    into dic.
    '''
    print("Reading", filename)
    with open(filename) as input_file:
        hero = [0] * 100000
        villain = [0] * 100000
        victim = [0] * 100000

        scores = [0, 0, 0]
        i = 0
        line_number = 0
        #for line in input_file:
        for line in reversed(list(input_file)):
            word = line.strip()
            # Skip comments, words ignored for analysis, and words already in dic
            if word[0] != '#' and not skip_word(word, None):
                if word in dic:
                    hero[i] = dic[word][HERO]
                    victim[i] = dic[word][VICTIM]
                    villain[i] = dic[word][VILLAIN]
                else:
                    hero[i] = sim(word, HERO)
                    victim[i] = sim(word, VICTIM)
                    villain[i] = sim(word, VILLAIN)

                scores[HERO] += hero[i]
                scores[VICTIM] += victim[i]
                scores[VILLAIN] += villain[i]
            # Print progress
                i += 1
            # if i % 10000 == 0:
            #     print(i, "words read...")
                if i == 10000:
                    break


        print("DONE:", filename)
    for j in range(len(scores)):
        scores[j] /= i
    std[HERO] = statistics.stdev(hero[:i])
    std[VILLAIN] = statistics.stdev(villain[:i])
    std[VICTIM] = statistics.stdev(victim[:i])
    return scores


scores = process_file('google-10000-english-usa.txt', SIM_DIC)

print(scores)
print(std)


'''
10k
Full dictionary : 
[0.3170381831066183, 0.30221178162662615, 0.2967264665102774]
[0.14937172486128053, 0.14617562716266508, 0.1436711117207142]

c-Filtered dictionary: 
[0.32305452392159195, 0.28782595388590715, 0.2901647892770812]
[0.12396667686493487, 0.12025576023093629, 0.1194044117127747]

100k
Full
[0.2158274427747022, 0.20612047710130232, 0.20331524277195787]
[0.17967377106672355, 0.17359717803353836, 0.17129783040312827]

c-Filtered
[0.2099998821237115, 0.18763032197617394, 0.19157541508044423]
[0.16899479954978153, 0.15569504624569536, 0.15818891990967748]
'''
