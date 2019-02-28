'''
Calculates scores across dictionaries using standardization.
Used to verify methods since hero-hero scores should be high,
hero-victim scores should be low, etc.
Note: Will not run properly anymore
'''


from role_assignment import similarity_to_role
from role_dictionaries import HERO_DICT, VILLAIN_DICT, VICTIM_DICT

# Constants to represent roles
HERO = 0
VILLAIN = 1
VICTIM = 2

# HERO_DICT = {'gentle', 'preserving', 'leadership', 'amazing', 'devoted', 'humble', 'warned', 'surprised', 'humanity', 'brave', 'evacuate', 'redemption', 'smile', 'honor', 'revolutionize', 'leader', 'advocate', 'savior', 'charity', 'sympathies', 'kindness', 'good', 'protect', 'teach', 'reputation', 'respected', 'welfare', 'glory', 'victory', 'winner', 'well', 'contained', 'restoration', 'commitment', 'ability', 'efforts', 'inspire', 'safety', 'allies', 'health', 'strength', 'empowered', 'passion', 'encouraging', 'warm', 'vision', 'scored', 'authorities', 'justice', 'grand', 'admire', 'reshape', 'communities', 'response', 'strengthen', 'bolster', 'intervened', 'motivated', 'reconstruct', 'freedom', 'duty', 'aided', 'conquer', 'smart', 'bravery', 'improve', 'donate', 'wise', 'ingenuity', 'milestone', 'protections', 'expand', 'hero', 'pursuit', 'invent', 'containment', 'achievement', 'supporters'}
# VILLAIN_DICT = {'contaminate', 'dirty', 'abduct', 'terror', 'worsen', 'crisis', 'lambast', 'abandonment', 'harass', 'subvert', 'virus', 'crime', 'provoke', 'kidnap', 'manipulate', 'alleged', 'refusal', 'trafficking', 'marginalize', 'conformity', 'clampdown', 'villain', 'disparaged', 'cold', 'exacerbate', 'alienate', 'commit', 'trial', 'violence', 'denounced', 'stripped', 'undermine', 'seize', 'persecuted', 'opposing', 'intimidate', 'jailed', 'fool', 'investigation', 'imprisoned', 'bias', 'deception', 'gunshots', 'threaten', 'hoax', 'engulfed', 'blame', 'eruption', 'offensive', 'contempt', 'suggested', 'coercion', 'erase', 'catastrophe', 'rumors', 'weaken', 'pointed', 'treason', 'evil', 'abused', 'sentenced', 'bullet', 'warn', 'devastate', 'convicted', 'rebuke', 'reveal', 'bully', 'collude'}
# VICTIM_DICT = {'setback', 'injured', 'traumatized', 'prevented', 'healing', 'buried', 'stuck', 'anguished', 'flee', 'suffer', 'casualty', 'trampled', 'forsaken', 'harassed', 'harassment', 'hardship', 'deported', 'howling', 'shocked', 'violence', 'depressed', 'danger', 'mute', 'stripped', 'terrified', 'distrust', 'assassinated', 'shivering', 'sick', 'complain', 'abducted', 'huddled', 'victimized', 'persecuted', 'barricaded', 'devastated', 'kidnapped', 'seized', 'justified', 'evacuated', 'surrendered', 'diagnosed', 'imprisoned', 'independence', 'slave', 'deceased', 'rebuffed', 'target', 'trapped', 'screamed', 'loss', 'trafficked', 'humiliated', 'impairment', 'wounded', 'discriminated', 'disadvantaged', 'blood', 'offended', 'accuses', 'saddens', 'threatened', 'disaster', 'devastation', 'overshadowed', 'tortured', 'abused', 'remonstrated', 'jeopardizing', 'stabbed', 'prey', 'sentenced', 'challenged', 'renounced', 'scared', 'humiliation', 'deaths', 'rescued', 'bleeding'}

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
HERO - HERO: 0.43593697829454453
VILLAIN - VILLAIN: 0.45674700531749385
VICTIM - VICTIM: 0.4703535636156092
----------------------------------------
HERO - VILLAIN: 0.4246066886216203
VILLAIN - HERO: 0.3187238823521552
VICTIM - HERO: 0.27248955419349413
HERO - VICTIM: 0.43848298826863097

Full dictionary 100k
HERO - HERO: 0.9639838467566706
VILLAIN - VILLAIN: 0.9759726872820005
VICTIM - VICTIM: 0.9676917967296632
----------------------------------------
HERO - VILLAIN: 0.9521711059837578
VILLAIN - HERO: 0.8806906494929407
VICTIM - HERO: 0.8392620609487662
HERO - VICTIM: 0.9523609127801426

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
