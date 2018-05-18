# coding: utf-8

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
from collections import Counter
from scipy import spatial
import random
import pickle





def create_random_sample(vocab, length):
    # create collection of 100 random samples
    sample_collection = []
    for i in range(100):
        sample = ' '
        for j in range(length):
            sample += random.choice(vocab) + ' '
        sample_collection.append(sample)
    return sample_collection

def sample_cos(voc, vec, size):
    # small sample collection
    sample_collection = create_random_sample(voc, size)
    sample_mat = vec.transform(sample_collection)
    std = np.mean(sample_mat, axis=0)
    cos_list_all = []
    for i in range(len(sample_collection)):
        cos_list = []
        for j in range(len(sample_collection)):
            cos_list.append(spatial.distance.cosine(sample_mat[i,:].todense().tolist()[0], sample_mat[j,:].todense().tolist()[0]))
        cos_list_all.append(np.mean(cos_list))
    print ("sample size: ", size, "mean cosine: ", np.mean(cos_list))
    return np.mean(cos_list_all)

df = pd.read_csv('../../data/shakespare_william_works_preprocessed.tsv', sep = '\t')

vectorizer = TfidfVectorizer(min_df=2, stop_words='english').fit(df.Text.tolist()) 
vocab = list(vectorizer.vocabulary_.keys())

# For analysis use a higher min df

cos_dict = {}
for val in range (1, 5000, 100):
    cos_dict[val] = sample_cos(vocab, vectorizer,val)

with open('null_model_tfidf_allave' + '.pkl', 'wb') as f:
    pickle.dump(cos_dict, f)



    