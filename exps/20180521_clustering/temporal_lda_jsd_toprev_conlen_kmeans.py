
# coding: utf-8

# In[1]:
import numpy as np
import pandas as pd
import re
from collections import Counter
from gensim import corpora, models, similarities
from scipy import special, spatial
import random
from sklearn.cluster import KMeans


def filter_text(text,retrieve=False):
    text_all = []
    for line in text:
        text_all.extend(line)
    c = Counter(text_all)
    fvocab = list(dict(c.most_common(500)).keys())
    fvocab.extend([word for word in c if c[word] == 1])
    fvocab = set(fvocab)
    if retrieve == False:
        text = [[word for word in line if word not in fvocab] for line in text]
        return text
    else:
        text = [word for word in text if word not in fvocab]
        return text

# create a corpus to give to sklearn
def preprocess(df):
    doc = []
    for line in df.Text.tolist():
        #Remove some non-ascii characters and 'aa's
        line = re.sub(r'aA|aa', 'a', line)
        line = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line)
        line = re.findall(u'(?u)\\b\\w\\w+\\b', line)
        line = [word.lower() for word in line] 
        doc.append(line)  
    return doc

def create_corpus(sentences):
    id2word = corpora.dictionary.Dictionary(sentences)
    corpus = [id2word.doc2bow(sentence) for sentence in sentences]
    return id2word, corpus

def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    return sorted(list(set(timelist)))

def create_timewindow(timelist, window_len):
    idx = 0
    window_all = []
    while idx <= len(timelist) - window_len:
        window_all.append(timelist[idx:idx+window_len])
        idx += window_len
    window_all.append(timelist[idx:])
    window_all = [w for w in window_all if len(w) > 0]
    return window_all

def create_df_time(df, time_window):
    dfs = []
    for time in time_window:
        dfs.append(df[df.PublishDate.str[:7] == time])
    return pd.concat(dfs)

def get_dist(line, model, id2word):
    line = re.sub(r'aA|aa', 'a', line)
    line = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line)
    line = re.findall(u'(?u)\\b\\w\\w+\\b', line)
    line = [word.lower() for word in line] 
    line = filter_text(line, True)
    return model.get_document_topics(id2word.doc2bow(line), minimum_probability = 0)


def JSD(P, Q):
    M = 0.5 * (P + Q)
    return 0.5 * (sum(special.rel_entr(P, M)) + sum(special.rel_entr(Q, M)))

def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')

    # # May only use single chapter works
    # # length between 500 - 1500 words
    # # df = df[df.Chapters == 1]
    # df = df[df.Text.str.split().map(len) >= 500]
    # df = df[df.Text.str.split().map(len) <= 1500]

    timelist = create_timelist(df)
    windows = create_timewindow(timelist, 6)
    df_all = []
    for i in range(1, len(windows)):
        df_t_curr = create_df_time(df, windows[i])
        df_t_prev = create_df_time(df, windows[i-1])
        if len(df_t_curr) > 50 and len(df_t_prev) > 50:
            df_t_curr = df_t_curr.reset_index()
            df_t_prev = df_t_prev.reset_index()
            df_two = pd.concat([df_t_curr, df_t_prev])
            sentences = preprocess(df_two)

            sentences = filter_text(sentences)
            id2word, corpus = create_corpus(sentences)
            model = models.LdaMulticore(corpus=corpus,id2word=id2word,num_topics=100,workers=30)

            df_t_curr['Dist'] = df_t_curr['Text'].map(lambda x: get_dist(x, model, id2word))
            del df_t_curr['Text']

            df_t_prev['Dist'] = df_t_prev['Text'].map(lambda x: get_dist(x, model, id2word))
            del df_t_prev['Text']

            prev = df_t_prev.Dist.tolist()
            prev = [[j[1] for j in i] for i in prev]
            kmeans = KMeans(n_clusters=3).fit(vectorized_prev)
            curr = df_t_curr.Dist.tolist()
            curr = [[j[1] for j in i] for i in prev]            
            centroids = kmeans.cluster_centers_

            df_t_curr['JSD'] = df_t_curr.apply(lambda row: JSD([i[1] for i in row['Dist']], \
                centroids[kmeans.predict([i[1] for i in row['Dist']])]), axis=1)
            del df_t_curr['Dist']
            df_all.append(df_t_curr)


    df_all = pd.concat(df_all)
    df_all.to_csv(fandom + '_temporal_lda_jsd_toprev_full.tsv', index = False, sep = '\t')
    print('Done with: ', fandom)

fandoms = [
'shakespare_william_works',
'les_miserables_all_media_types',
'marvel',
'bishoujo_senshi_sailor_moon',
'homestuck',
'haikyuu',
'hamilton_miranda',
'kuroko_no_basuke',
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
'harry_potter',
'supernatural',
]

for fandom in fandoms:
    # try:
    main(fandom)
    break
    # except:
    #     print('failed with: ',fandom)
    #     continue
        
# profile.run('main("shakespare_william_works")')

'''
done:

''' 

'''
'''

