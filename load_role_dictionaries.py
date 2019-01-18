'''
Script to put words from role dictionary spreadsheet into role_dictionaries.py
as three lists called HERO_DICT, VILLAIN_DICT, and VICTIM_DICT. The methods used
in this script are a bit crude but since it's a one time thing called on a very
small file it doesn't really matter.
'''

import csv
import json

hero, villain, victim = set(), set(), set()

with open('Role dictionaries - Sheet6.csv') as csv_file:
    reader = csv.reader(csv_file)
    for i, row in enumerate(reader):
        if i != 0:
            hero.add(row[1].lower())
            villain.add(row[4].lower())
            victim.add(row[7].lower())

hero.discard('')
villain.discard('')
victim.discard('')

with open('role_dictionaries.py', 'w') as output_file:
    output_file.truncate()
    output_file.write('HERO_DICT = ')
    json.dump(list(hero), output_file)
    output_file.write('\n\nVILLAIN_DICT = ')
    json.dump(list(villain), output_file)
    output_file.write('\n\nVICTIM_DICT = ')
    json.dump(list(victim), output_file)
