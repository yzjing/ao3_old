
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

def sample_words(text):
    if len(text.split()) == 1000:
        return text
    else:
        text_s = []
        text = text.split()
        for i in range(1000):
            text_s.append(random.choice(text))
        return ' '.join([w for w in text_s])

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

def get_dist(matrix, idx):
    return matrix[idx,:].todense().tolist()[0]

def compute_cosine(target_df, dist):
    # Compute cosine distance between each fic and the target fic
    # Then return the average
    target_df['Cos'] = target_df.apply(lambda row: spatial.distance.cosine(row['Dist'], dist), axis=1)
    return np.average(target_df['Cos'].tolist())

def main(fandom):
    # print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')

    df = df[df.Text.str.split().map(len) >= 1000]
    df = df[df.Text.str.split().map(len) <= 1500]

    timelist = create_timelist(df)
    windows = create_timewindow(timelist, 3)

    df_all = []
    for i in range(1, len(windows)):
        df_t = create_df_time(df, windows[i])
        if len(df_t) > 100 :
            df_t = df_t.sample(100)  
            df_t = df_t.reset_index()
          
            vectorizer = TfidfVectorizer(min_df=2, stop_words='english')
            transformed_doc = vectorizer.fit_transform(df_t.Text.tolist()) 

            df_t['Dist'] = df_t.apply(lambda row: get_dist(transformed_doc, row.name), axis=1)
            del df_t['Text']

            dist_array = np.asarray(df_t.Dist.tolist())
            std = np.mean(dist_array, axis=0)
            df_t['Cos'] = df_t.apply(lambda row: compute_cosine(df_t, row['Dist']), axis=1)
            del df_t['Dist']
            df_all.append(df_t)

            
    df_all = pd.concat(df_all)
    df_all.to_csv(fandom + '_temporal_tfidf_cos_tocurr_samplew_allave.tsv', index = False, sep = '\t')

fandoms = [
'shakespare_william_works',
'homestuck',
'bishoujo_senshi_sailor_moon',
'haikyuu',
'hamilton_miranda',
'kuroko_no_basuke',
'les_miserables_all_media_types',
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

