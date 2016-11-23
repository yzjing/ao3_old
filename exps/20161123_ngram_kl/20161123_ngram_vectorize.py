
# coding: utf-8

# In[2]:

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from time import time
import pandas as pd
import re
from scipy import sparse

# In[10]:

def get_distribution_matrix(corpus, ngram):
    vectorizer = CountVectorizer(stop_words='english', ngram_range = (ngram,ngram))
    f = vectorizer.fit_transform(corpus)
    l = len(vectorizer.get_feature_names())
    return np.divide(f, l)


# In[6]:

df = pd.read_csv('../../data/preprocessed_data/shakespare_william_works_preprocessed.tsv', sep = '\t')


# In[7]:

doc = []
for i in df.Text.tolist():
    #Remove some non-ascii characters and 'aa's
    i = re.sub(r'aA|aa', 'a', i)
    i = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', i)
    doc.append(i)             


t0 = time()
m = get_distribution_matrix(doc, 2)
m_mean = sparse.csr_matrix.mean(m, axis = 0)
print m_mean[0]
print("done in %0.3fs." % (time() - t0))




