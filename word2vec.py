#from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
#from nltk import word_tokenize
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

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

with open('test123.txt', 'w', encoding='utf-8') as file:
    for item in filtered_synopses:
        file.write(item.split('||')[0].strip())
        
        #print(item[0], '\t',item[1], '\n')
        #file.write('     ')
        #file.write(filtered_synopses[item[0]].split('||')[0])
        #file.write(item[0])
        file.write('\n')

#documents = [TaggedDocument(synopsis_name.split('||')[1].strip(), [i]) for i, synopsis_name in enumerate(filtered_synopses)]
documents = [TaggedDocument(synopsis_name.split('||')[1].strip().split(), [synopsis_name.split('||')[0].strip()]) for synopsis_name in filtered_synopses]
model = Doc2Vec(documents, vector_size = 300, window=25, min_count=20, workers=4, epochs=20)

#print(documents[0])


#print(filtered_synopses[493].split('||')[0])
#for item in model.docvecs.most_similar(positive = model.docvecs['الورشة']):
#    print(item, '\n')
print(model.docvecs['الورشة'])
#print(model.docvecs)

vectors = []

for i in range(len(filtered_synopses)):
    vectors.append(model.docvecs[filtered_synopses[i].split('||')[0].strip()])


kmeans = KMeans(n_clusters=5, random_state=0).fit(vectors)

print('Labels:  ', kmeans.labels_)#array([1, 1, 1, 0, 0, 0], dtype=int)
x = kmeans.predict([model.docvecs['قلب المرأة']])
print(x)
'''
fig = plt.figure()
fig.suptitle('Data PCA', fontsize=20)
plt.xlabel('xl', fontsize=18)
plt.ylabel('x2', fontsize=16)
plt.scatter(data['x1'], data['x2'])
fig.savefig('Data_PCA.png')
'''
#print(model.infer_vector('قلب المرأة'))
'''
with open('SampleDoc2VecOutput2.txt', 'w', encoding='utf-8') as file:
    for item in model.docvecs.most_similar(positive=[model.infer_vector('قلب المرأة')]):
        file.write(str(model.docvecs.__getitem__(item[0])))
        
        print(item[0], '\t',item[1], '\n')
        file.write('     ')
        #file.write(filtered_synopses[item[0]].split('||')[0])
        file.write(item[0])
        file.write('\n')
''' 

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
