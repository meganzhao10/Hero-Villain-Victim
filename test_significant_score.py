from role_assignment import similarity_to_role
from role_dictionaries import HERO_DICT, VILLAIN_DICT, VICTIM_DICT

# Constants to represent roles
HERO = 0
VILLAIN = 1
VICTIM = 2

HERO_DICT = {'gentle', 'preserving', 'leadership', 'amazing', 'devoted', 'humble', 'warned', 'surprised', 'humanity', 'brave', 'evacuate', 'redemption', 'smile', 'honor', 'revolutionize', 'leader', 'advocate', 'savior', 'charity', 'sympathies', 'kindness', 'good', 'protect', 'teach', 'reputation', 'respected', 'welfare', 'glory', 'victory', 'winner', 'well', 'contained', 'restoration', 'commitment', 'ability', 'efforts', 'inspire', 'safety', 'allies', 'health', 'strength', 'empowered', 'passion', 'encouraging', 'warm', 'vision', 'scored', 'authorities', 'justice', 'grand', 'admire', 'reshape', 'communities', 'response', 'strengthen', 'bolster', 'intervened', 'motivated', 'reconstruct', 'freedom', 'duty', 'aided', 'conquer', 'smart', 'bravery', 'improve', 'donate', 'wise', 'ingenuity', 'milestone', 'protections', 'expand', 'hero', 'pursuit', 'invent', 'containment', 'achievement', 'supporters'}
VILLAIN_DICT = {'contaminate', 'dirty', 'abduct', 'terror', 'worsen', 'crisis', 'lambast', 'abandonment', 'harass', 'subvert', 'virus', 'crime', 'provoke', 'kidnap', 'manipulate', 'alleged', 'refusal', 'trafficking', 'marginalize', 'conformity', 'clampdown', 'villain', 'disparaged', 'cold', 'exacerbate', 'alienate', 'commit', 'trial', 'violence', 'denounced', 'stripped', 'undermine', 'seize', 'persecuted', 'opposing', 'intimidate', 'jailed', 'fool', 'investigation', 'imprisoned', 'bias', 'deception', 'gunshots', 'threaten', 'hoax', 'engulfed', 'blame', 'eruption', 'offensive', 'contempt', 'suggested', 'coercion', 'erase', 'catastrophe', 'rumors', 'weaken', 'pointed', 'treason', 'evil', 'abused', 'sentenced', 'bullet', 'warn', 'devastate', 'convicted', 'rebuke', 'reveal', 'bully', 'collude'}
VICTIM_DICT = {'setback', 'injured', 'traumatized', 'prevented', 'healing', 'buried', 'stuck', 'anguished', 'flee', 'suffer', 'casualty', 'trampled', 'forsaken', 'harassed', 'harassment', 'hardship', 'deported', 'howling', 'shocked', 'violence', 'depressed', 'danger', 'mute', 'stripped', 'terrified', 'distrust', 'assassinated', 'shivering', 'sick', 'complain', 'abducted', 'huddled', 'victimized', 'persecuted', 'barricaded', 'devastated', 'kidnapped', 'seized', 'justified', 'evacuated', 'surrendered', 'diagnosed', 'imprisoned', 'independence', 'slave', 'deceased', 'rebuffed', 'target', 'trapped', 'screamed', 'loss', 'trafficked', 'humiliated', 'impairment', 'wounded', 'discriminated', 'disadvantaged', 'blood', 'offended', 'accuses', 'saddens', 'threatened', 'disaster', 'devastation', 'overshadowed', 'tortured', 'abused', 'remonstrated', 'jeopardizing', 'stabbed', 'prey', 'sentenced', 'challenged', 'renounced', 'scared', 'humiliation', 'deaths', 'rescued', 'bleeding'}

zero_score_words = []

# count zero score word? but only for full dictionary
def calculate_score(dict, role):
	# print('---------')
	total_score = 0
	for word in dict:
		total_score += similarity_to_role(word, role)
		# if cur == 0:
		# 	print(word)
	return total_score / len(dict)


print("HERO - HERO: " + str(calculate_score(HERO_DICT, HERO)))
print("VILLAIN - VILLAIN: " + str(calculate_score(VILLAIN_DICT, VILLAIN)))
print("VICTIM - VICTIM: " + str(calculate_score(VICTIM_DICT, VICTIM)))

print("----------------------------------------")
print("HERO - VILLAIN: " + str(calculate_score(HERO_DICT, VILLAIN)))
print("VILLAIN - HERO: " + str(calculate_score(VILLAIN_DICT, HERO)))
print("VICTIM - HERO: " + str(calculate_score(VICTIM_DICT, HERO)))
print("HERO - VICTIM: " + str(calculate_score(HERO_DICT, VICTIM)))



'''
keep changing standardization

Full dictionary 10k
HERO - HERO: 0.3885007342571777
VILLAIN - VILLAIN: 0.3619389318436508
VICTIM - VICTIM: 0.37071405514580114
----------------------------------------
HERO - VILLAIN: 0.36950972278918304
VILLAIN - HERO: 0.34851948691706597
VICTIM - HERO: 0.3584091258067737
HERO - VICTIM: 0.3645483468613141

Full dictionary 100k
HERO - HERO: 0.4189179774460293
VILLAIN - VILLAIN: 0.42354920964061926
VICTIM - VICTIM: 0.3967688362094374
----------------------------------------
HERO - VILLAIN: 0.39993499538744576
VILLAIN - HERO: 0.41310307922828327
VICTIM - HERO: 0.38705036994904607
HERO - VICTIM: 0.39449081820336535

Filtered 10k
HERO - HERO: 0.21899435832908964
VILLAIN - VILLAIN: 0.2913825463399934
VICTIM - VICTIM: 0.4146205376653103
----------------------------------------
HERO - VILLAIN: 0.19371338720301848
VILLAIN - HERO: -0.09617151620820986
VICTIM - HERO: -0.10662036598042332
HERO - VICTIM: 0.1646791386903146

Filtered 100k
HERO - HERO: 0.8302747246712505
VILLAIN - VILLAIN: 0.869050013303774
VICTIM - VICTIM: 0.9367848968832265
----------------------------------------
HERO - VILLAIN: 0.7936012155642856
VILLAIN - HERO: 0.5990784437051674
VICTIM - HERO: 0.5914134793074337
HERO - VICTIM: 0.74802459936

'''