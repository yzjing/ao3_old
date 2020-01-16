
# coding: utf-8

# In[1]:
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import re
from collections import Counter
from scipy import spatial
import random
import cProfile
from sklearn.cluster import KMeans


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
    return matrix[idx,:]

def compute_cosine(row, std):
    return spatial.distance.cosine(row, std)


def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')

    # May only use single chapter works
    # length between 500 - 1500 words
    # df = df[df.Chapters == 1]
    df = df[df.Text.str.split().map(len) >= 500]
    df = df[df.Text.str.split().map(len) <= 1500]

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

            tf = TfidfVectorizer(min_df=2, stop_words='english')
            vectorizer = tf.fit(df_two.Text.tolist()) 

            vectorized_prev = vectorizer.transform(df_t_prev.Text.tolist())
            kmeans = KMeans(n_clusters=3).fit(vectorized_prev)
            vectorized_curr = vectorizer.transform(df_t_curr.Text.tolist())
            c_label = kmeans.predict(vectorized_curr)
            centroids = kmeans.cluster_centers_
            print(centroids)


    #         for index, row in df.iterrows():
    #             print(row.name)
    #         df['cluster_id'] = df.apply(lambda row: c_label[row.name], axis=1)
    #         print(df.head())


    #         prev_std = np.mean(transformed_prev, axis=0)

    #         transformed_curr = vectorizer.transform(df_t_curr.Text.tolist()).toarray()
    #         transformed_curr_dist = np.apply_along_axis(compute_cosine, 1, transformed_curr, std=prev_std)
    #         df_t_curr['Cos'] = df_t_curr.apply(lambda row: transformed_curr_dist[row.name], axis=1)
    #         del df_t_curr['Text']

    #         df_all.append(df_t_curr)
            
    # df_all = pd.concat(df_all)
    # print(len(df_all))
    # df_all.to_csv(fandom + '_temporal_tfidf_cos_toprev_conlen.tsv', index = False, sep = '\t')
    # print('Done with: ', fandom)


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
    # cProfile.run('main(fandom)')
    main(fandom)
    break
    
    # except:
    #     print('failed with: ',fandom)
    #     continue
        


