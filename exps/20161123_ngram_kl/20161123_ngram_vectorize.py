
# coding: utf-8

# In[2]:

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from time import time
import pandas as pd
import re


# In[10]:

def get_distribution_matrix(corpus, ngram):
    vectorizer = CountVectorizer(stop_words='english', ngram_range = (ngram,ngram))
    f = vectorizer.fit_transform(corpus)
    l = len(vectorizer.get_feature_names())
    return f.toarray(), l


# In[6]:

df = pd.read_csv('../../data/shakespare_william_works_preprocessed.tsv', sep = '\t')


# In[7]:

doc = []
for i in df.Text.tolist():
    #Remove some non-ascii characters and 'aa's
    i = re.sub(r'aA|aa', 'a', i)
    i = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', i)
    doc.append(i)             


# In[8]:

# vectorizer = CountVectorizer(stop_words='english', ngram_range = (2,2))
# f = vectorizer.fit_transform(doc)
# vectorizer.get_feature_names()[0:100]


# In[11]:

t0 = time()
m, l = get_distribution_matrix(doc, 2)
print("done in %0.3fs." % (time() - t0))


# In[7]:

m.shape


# In[ ]:

m_d = np.divide(m, l)

print('process completed')



