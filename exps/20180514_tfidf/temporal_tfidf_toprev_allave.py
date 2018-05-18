
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
    print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')

    
    timelist = create_timelist(df)
    windows = create_timewindow(timelist, 3)
    prev_std = []

    df_all = []
    for i in range(1, len(windows)):
        df_t_a = create_df_time(df, windows[i])
        df_t_b = create_df_time(df, windows[i-1])
        if len(df_t_a) > 100 and len(df_t_b) > 100:
            df_t_a = df_t_a.sample(100)  
            df_t_a['Text'] = df_t_a.apply(lambda row:sample_words(row['Text']), axis=1)
            df_t_a = df_t_a.reset_index()
            df_t_b = df_t_b.sample(100)
            df_t_b['Text'] = df_t_b.apply(lambda row:sample_words(row['Text']), axis=1)
            df_t_b = df_t_b.reset_index()
            df_two = pd.concat([df_t_a, df_t_b])

            tf = TfidfVectorizer(min_df=2, stop_words='english')
            vectorizer = tf.fit(df_two.Text.tolist()) 

            transformed_a = vectorizer.transform(df_t_a.Text.tolist())
            df_t_a['Dist'] = df_t_a.apply(lambda row: get_dist(transformed_a, row.name), axis=1)
            del df_t_a['Text']

            transformed_b = vectorizer.transform(df_t_b.Text.tolist())
            df_t_b['Dist'] = df_t_b.apply(lambda row: get_dist(transformed_b, row.name), axis=1)
            del df_t_b['Text']

            dist_array = np.asarray(df_t_a.Dist.tolist())
            prev_std = np.mean(dist_array, axis=0)

            df_t_b['Cos'] = df_t_b.apply(lambda row: compute_cosine(df_t, row['Dist']), axis=1)
            del df_t['Dist']
            df_all.append(df_t)
            
    df_all = pd.concat(df_all)
    df_all.to_csv(fandom + '_temporal_tfidf_cos_toprev_samplew.tsv', index = False, sep = '\t')
    print('Done with: ', fandom)


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

