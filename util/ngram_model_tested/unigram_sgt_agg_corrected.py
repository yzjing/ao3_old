
# coding: utf-8

# In[1]:
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import re
import sgt_opt as sgt
from collections import Counter
# from memory_profiler import profile

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
    text = re.sub(r'aA|aa', 'a', text)
    text = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', text).lower()
    text = re.findall(u'(?u)\\b\\w\\w+\\b', text)
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


def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_agg_1000.tsv', sep = '\t')
    df = df.sample(500)

    # exclude works with less than 500 words
    # df = df[df.Words >= 500]

    # df = df.sample(1000, replace=True)
          
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
    df['Dist'] = df['Text'].map(lambda x: get_dist(x, sgt_di, vocab_fil))
    del df['Text']

    df.to_csv(fandom + '_agg_unigram_sgt_dist.tsv', index = False, sep = '\t')
    print('Done with: ', fandom)

fandoms = [
'homestuck',
'bishoujo_senshi_sailor_moon',
'haikyuu',
'hamilton_miranda',
'kuroko_no_basuke',
'les_miserables_all_media_types',
'shakespare_william_works',
'the_walking_dead_&_related_fandoms',
'hetalia_axis_powers',
'naruto',
'star_wars_all_media_types',
'buffy_the_vampire_slayer',
'arthurian_mythology_&_related_fandoms',
'ms_paint_adventures',
'one_direction',
'attack_on_titan',
'doctor_who_&_related_fandoms',
'tolkien_j_r_r_works_&_related_fandoms',
'dcu',
'dragon_age_all_media_types',
'sherlock_holmes_&_related_fandoms',
'the_avengers_all_media_types',
'harry_potter',
'supernatural',
'marvel',
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

