
# coding: utf-8

# In[1]:
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import re
from collections import Counter
from scipy import spatial
import random

# In[3]:

def get_dist(matrix, idx):
    return matrix[idx,:].todense().tolist()[0]


def compute_cosine(mat, dist):
    mat = mat.todense()
    # Compute cosine distance between each fic in the matrix and the target fic
    # Then return the average
    mat_cos = np.apply_along_axis(spatial.distance.cosine, 1, mat, dist)
    return np.average(mat_cos)

def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')
    # length between 500 - 1500 words
    df = df[df.Text.str.split().map(len) >= 500]
    df = df[df.Text.str.split().map(len) <= 1500]
    df = df.reset_index()
    
    canon = open(fandom + '_canon.txt', 'r').read()

    # create vocabulary space
    tf = TfidfVectorizer(min_df=2, stop_words='english')
    docs = df.Text.tolist()
    docs.append(canon)
    vectorizer = tf.fit(docs) 

    transformed_df = vectorizer.transform(df.Text.tolist())
    transformed_canon = vectorizer.transform([canon]).todense()

    df['Dist'] = df.apply(lambda row: get_dist(transformed_df, row.name), axis=1)
    del df['Text']
    
    df['Cos'] = df.apply(lambda row: spatial.distance.cosine(transformed_canon, row['Dist']), axis=1)
    del df['Dist']
                
    df.to_csv(fandom + '_tfidf_tocanon.tsv', index = False, sep = '\t')
    print('Done with: ', fandom)


fandoms = [
'sherlock_holmes_&_related_fandoms',
]

for fandom in fandoms:
    # try:
    main(fandom)
    # except:
    #     print('failed with: ',fandom)
    #     continue
        
# profile.run('main("shakespare_william_works")')

'''
done:

''' 

'''
'''

