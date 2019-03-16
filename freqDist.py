import itertools
from nltk import FreqDist
from fuzzywuzzy import fuzz

file = open('names.txt', 'r', encoding = 'utf-8')
s = file.read()
file.close()

s = s.split('\n')
s = list(filter(None, s))
for i in range(len(s)):
    s[i] = s[i].strip()
names = FreqDist(s)

#print(names.most_common())

corrections = {}

for name1, name2 in itertools.combinations(names.items(), 2):
    out = fuzz.ratio(name1[0], name2[0])
    if out > 90 and out < 100:
        print(name1[0], ': ', name1[1],'   ', name2[0], ': ', name2[1])
        if((not name1[1] == name2[1]) and min([name1[1], name2[1]]) < 10):
            corrected_name = ''
            syllables = []
            if(name1[1] == min([name1[1], name2[1]])):
                corrected_name = name2[0]
                syllables = name2[0].split()
            else:
                corrected_name = name1[0]
                syllables = name1[0].split()
                
            if('عبد' in syllables):
                for i in range(len(syllables)):
                    if(syllables[i] == 'عبد' and i < len(syllables) - 1):
                        corrected_name = ''
                        for part in syllables:
                            if (not part == 'عبد'):
                                corrected_name += part + ' '
                            else:
                                corrected_name += part
                        corrected_name = corrected_name.strip()
                corrections[name1[0]] = corrected_name
                corrections[name2[0]] = corrected_name
            elif(name1[1] == min([name1[1], name2[1]])):                
                corrections[name1[0]] = corrected_name
            else:
                corrections[name2[0]] = corrected_name

with open('testFix.txt', 'w', encoding='utf-8') as file:
    for key, value in corrections.items():
        file.write('old: ' + key + ':\t\t new: ' + value + '\n')
                
            
'''
for name1 in names.items():
    for name2 in names.items():
        out = fuzz.ratio(name1, name2[0])
        if out > 95 and out < 100:
            print(name1, ': ', names[name1],'   ', name2[0], ': ', names[name2[0]])
'''


'''d = {1:2, 2:3, 3:4, 4:7, 5:6}
print(type(d.items()))'''

'''
for name in names:
    for name_iter in names:
        out = fuzz.ratio(name_iter, name)
        if out > 90 and out < 100:
            print(out, name)
'''

#print('name type: ', type(name1))
#print('name[0] type: ', type(name1[0]))
#print('name[1] type: ', type(name1[1]))
#print('name1: ', name1)
#print('names[name[0]]', names[name1[0]])
#break