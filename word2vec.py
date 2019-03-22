from __future__ import print_function
#from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
#from nltk import word_tokenize
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import pairwise_distances
from sklearn.metrics import silhouette_score
from kmeansplots import kmeans_plot, silhouette_plot

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
window = 10
#documents = [TaggedDocument(synopsis_name.split('||')[1].strip(), [i]) for i, synopsis_name in enumerate(filtered_synopses)]
documents = [TaggedDocument(synopsis_name.split('||')[1].strip().split(), [synopsis_name.split('||')[0].strip()]) for synopsis_name in filtered_synopses]
model = Doc2Vec(documents, vector_size = 500, window=window, min_count=5, workers=4, epochs=20)

#print(documents[0])


#print(filtered_synopses[493].split('||')[0])
#for item in model.docvecs.most_similar(positive = model.docvecs['الورشة']):
#    print(item, '\n')
#print(model.docvecs['الورشة'])
#print(model.docvecs)

vectors = []

for i in range(len(filtered_synopses)):
    vectors.append(model.docvecs[filtered_synopses[i].split('||')[0].strip()])


kmeans = KMeans(n_clusters=4, random_state=0).fit(vectors)

#print('Labels:  ', kmeans.labels_)#array([1, 1, 1, 0, 0, 0], dtype=int)
#x = kmeans.predict([model.docvecs['قلب المرأة']])
#print(x)

m = metrics.silhouette_score(vectors, kmeans.labels_, metric='euclidean')
print(m, '   ', window)



from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples

import matplotlib.cm as cm

print(__doc__)

# Generating the sample data from make_blobs
# This particular setting has one distinct cluster and 3 clusters placed close
# together.
'''X, y = make_blobs(n_samples=2045,
                  n_features=2,
                  centers=4,
                  cluster_std=1,
                  center_box=(-10.0, 10.0),
                  shuffle=True,
                  random_state=1)  # For reproducibility
'''
range_n_clusters = [2, 3, 4, 5, 6]

for n_clusters in range_n_clusters:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)

    ax1.set_xlim([-0.1, 1])
    
    ax1.set_ylim([0, len(vectors) + (n_clusters + 1) * 10])


    clusterer = KMeans(n_clusters=n_clusters, random_state=10)
    cluster_labels = clusterer.fit_predict(vectors)

    
    silhouette_avg = silhouette_score(vectors, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    
    sample_silhouette_values = silhouette_samples(vectors, cluster_labels)

    y_lower = 10
    for i in range(n_clusters):
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        y_lower = y_upper + 10

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    #colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
    #ax2.scatter(vectors[:], vectors[:], marker='.', s=30, lw=0, alpha=0.7,
    #            c=colors, edgecolor='k')

    #centers = clusterer.cluster_centers_
    #ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
    #            c="white", alpha=1, s=200, edgecolor='k')

    #for i, c in enumerate(centers):
    #    ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
    #                s=50, edgecolor='k')

    #ax2.set_title("The visualization of the clustered data.")
    #ax2.set_xlabel("Feature space for the 1st feature")
    #ax2.set_ylabel("Feature space for the 2nd feature")

    plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                  "with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')

plt.show()

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
