
# coding: utf-8

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import re
from collections import Counter
from scipy import spatial
import random
import cProfile


def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    timelist = [item for item in timelist if int(item[0:4]) >= 2009]
    return sorted(list(set(timelist)))

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
    df = pd.read_csv('../' + fandom + '_preprocessed2.tsv', sep = '\t')

    # May only use single chapter works
    # length between 500 - 1500 words
    # df = df[df.Chapters == 1]
    df = df[df.Text.str.split().map(len) >= 500]
    df = df[df.Text.str.split().map(len) <= 1500]

    timelist = create_timelist(df)

    df_all = []
    for time in timelist:
        future_window = timelist[timelist.index(time):timelist.index(time)+6]
        print(time, future_window)
        if len(future_window) > 0:
            # use the current month and the next 6 months
            df_t_curr = create_df_time(df, [time])
            df_t_future = create_df_time(df, future_window)
            if len(df_t_curr) > 20 and len(df_t_future) > 50:
                df_t_curr = df_t_curr.reset_index()
                df_t_future = df_t_future.reset_index()
                df_two = pd.concat([df_t_curr, df_t_future])

                tf = TfidfVectorizer(min_df=2, stop_words='english')
                vectorizer = tf.fit(df_two.Text.tolist()) 

                transformed_future = vectorizer.transform(df_t_future.Text.tolist())
                future_std = np.mean(transformed_future, axis=0)

                transformed_curr = vectorizer.transform(df_t_curr.Text.tolist()).toarray()
                transformed_curr_dist = np.apply_along_axis(compute_cosine, 1, transformed_curr, std=future_std)
                df_t_curr['Cos'] = df_t_curr.apply(lambda row: transformed_curr_dist[row.name], axis=1)
                del df_t_curr['Text']

                df_all.append(df_t_curr)
            
    df_all = pd.concat(df_all)
    print(len(df_all))
    df_all.to_csv(fandom + '_temporal_tfidf_cos_tofuture_conlen.tsv', index = False, sep = '\t')
    print('Done with: ', fandom)


fandoms = [
'shakespare_william_works',
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
'harry_potter',
'supernatural',
'marvel',
]


for fandom in fandoms:
    # try:
    # cProfile.run('main(fandom)')
    main(fandom)
    
    # except:
    #     print('failed with: ',fandom)
    #     continue
        


