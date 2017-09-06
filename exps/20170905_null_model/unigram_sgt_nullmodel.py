# coding: utf-8

# In[1]:
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import re
import sgt_opt as sgt
from collections import Counter
# from memory_profiler import profile
import random
from scipy import spatial
import pickle

# In[3]:

# create a corpus to give to sklearn
def create_corpus_for_voc(df):
    doc = []
    for i in df.Text.tolist():
        #Remove some non-ascii characters and 'aa's
        i = re.sub(r'aA|aa', 'a', i)
        i = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', i)
        i = i.lower()
        doc.append(i)  
    return doc


# In[4]:

# Get a vocabulary using sklearn's filtering
def get_voc(corpus, ngram, mindf):
    vectorizer = CountVectorizer(stop_words='english', ngram_range=(ngram,ngram),min_df=mindf)
    f = vectorizer.fit_transform(corpus)
    return sorted(list(set(vectorizer.get_feature_names())))


# In[5]:

# compute unigram-frequency dict using the same preprocessing, using only words from the vocabulary
def create_unigram_freq_dict(df, voc):
    text = []
    df_text = df.Text.tolist()
    for line in df_text:
        line_f = re.sub(r'aA|aa', 'a', line)
        line_f = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line_f).lower()
        line_f = re.findall(u'(?u)\\b\\w\\w+\\b', line_f)
        line_f = [word for word in line_f if word in voc]
        text.extend(line_f)
        text_dict = dict(Counter(text))
    return text_dict


def get_dist(text, sgt_di, vocab):
    text = [word for word in text if word in vocab]
    prob_line = []
    # try:
    num_abs_words = len(vocab) - len(set(text))
    for word in vocab:
        if word in text:
            prob_line.append(sgt_di[0][word])
        else:
            prob_line.append(sgt_di[1]/float(num_abs_words))
    return prob_line
    # except:
    #     return [0]


def create_random_sample(vocab, length):
    # create collection of 100 random samples
    sample_collection = []
    for i in range(100):
        sample = []
        for j in range(length):
            sample.append(random.choice(vocab))
        sample_collection.append(sample)
    return sample_collection

def sample_cos(size):
    # small sample collection
    sample_collection = create_random_sample(vocab, size)

    dist_collection = []
    for entry in sample_collection:
        dist_collection.append(get_dist(entry, sgt_di, vocab_fil))
    
    dist_collection_arr = np.asarray(dist_collection)
    std = np.mean(dist_collection_arr, axis=0)
    cos_list = []
    for entry in dist_collection:
        cos_list.append(spatial.distance.cosine(entry, std))
    # print ("sample size: ", size, "mean cosine: ", np.mean(cos_list))
    return np.mean(cos_list)

df = pd.read_csv('homestuck' + '_agg_1000.tsv', sep = '\t')
df = df.sample(200)

# Add a column of smoothed unigram probablities to df
corp = create_corpus_for_voc(df)
# For sgt estimation keep min df = 1
vocab = get_voc(corp,1,1)

# For analysis use a higher min df
vocab_fil = get_voc(corp,1, 4)
print(len(vocab), len(vocab_fil))
unigram_dict = create_unigram_freq_dict(df, vocab)
sgt_di = sgt.simpleGoodTuringProbs(unigram_dict)
print("sgt done")

cos_dict = {}
for val in range (1, 5000, 100):
    cos_dict[val] = sample_cos(val)

with open('null_model' + '.pkl', 'wb') as f:
    pickle.dump(cos_dict, f)



    