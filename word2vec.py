#from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
#from nltk import word_tokenize

file = open('synopses.txt', 'r', encoding = 'utf-8')
s = file.read()
file.close()

synopses = s.split('\n')

synopses = list(filter(None, synopses))
#print(synopses)

#print(synopses[0].split('||'))
i = 0
filtered_synopses = []
for synopsis in synopses:
    if(len(synopsis.split('||')) == 2):
        filtered_synopses.append(synopsis)

#print(filtered_synopses[0].split('||')[0])

documents = [TaggedDocument(synopsis_name.split('||')[1].strip(), [i]) for i, synopsis_name in enumerate(filtered_synopses)]
model = Doc2Vec(documents, vector_size=1, window=1, min_count=1, workers=4)

#print(documents[0], '\n', documents[1])
print(model.docvecs.most_similar(positive = [493]))
with open('SampleDoc2VecOutput.txt', 'w', encoding='utf-8') as file:
    for item in model.docvecs.most_similar(positive=[493]):
        file.write(model.docvecs.__getitem__(item[0]))
        file.write('     ')
        file.write(filtered_synopses[item[0]].split('||')[0])
        file.write('\n')
    

'''for synopsis in synopses:
    list_of_sentences.append(word_tokenize(synopsis))

with open('word2vecInput.txt', 'w', encoding='utf-8') as file:
    for sentence in list_of_sentences:
        for item in sentence:
            file.write('%s ' % item)
        file.write('\n')
model = Word2Vec(list_of_sentences, min_count=1)

#print(model.wv.most_similar('الخواجه'))
print(model.wv.__getitem__('الخواجه'))

model.save('model')
'''
