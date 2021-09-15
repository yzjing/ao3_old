
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
    return matrix[idx,:].todense().tolist()[0]


def compute_cosine(mat, dist):
    mat = mat.todense()
    # Compute cosine distance between each fic in the matrix and the target fic
    # Then return the average
    mat_cos = np.apply_along_axis(spatial.distance.cosine, 1, mat, dist)
    return np.average(mat_cos)

def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv('../' + fandom + '_preprocessed_merged_chs_2.tsv', sep = '\t')
    # length between 500 - 1500 words
    df = df[df.Text.str.split().map(len) >= 500]

    # if len(df) > 3000:
    #     df = df.sample(3000)
        
    timelist = create_timelist(df)

    df_all = []
    for time in timelist:
        prev_window = timelist[timelist.index(time)-6:timelist.index(time)]
        if len(prev_window) > 0:
            # use the current month and the past 6 months
            df_t_curr = create_df_time(df, [time])
            df_t_prev = create_df_time(df, prev_window)
            if len(df_t_curr) > 20 and len(df_t_prev) > 50:
                if len(df_t_curr) > 200:
                    df_t_curr = df_t_curr.sample(200)
                if len(df_t_prev) > 1200:
                    df_t_prev = df_t_prev.sample(1200)
                df_t_curr = df_t_curr.reset_index()
                df_t_prev = df_t_prev.reset_index()
                # create vocabulary space
                df_two = pd.concat([df_t_curr, df_t_prev])
                tf = TfidfVectorizer(min_df=2, stop_words='english')
                vectorizer = tf.fit(df_two.Text.tolist()) 

                transformed_prev = vectorizer.transform(df_t_prev.Text.tolist())

                transformed_curr = vectorizer.transform(df_t_curr.Text.tolist())
                df_t_curr['Dist'] = df_t_curr.apply(lambda row: get_dist(transformed_curr, row.name), axis=1)
                del df_t_curr['Text']
                
                df_t_curr['Cos'] = df_t_curr.apply(lambda row: compute_cosine(transformed_prev, row['Dist']), axis=1)
                del df_t_curr['Dist']
                df_all.append(df_t_curr)
                
    df_all = pd.concat(df_all)
    df_all.to_csv(fandom + '_temporal_tfidf_merged_chs_allave.tsv', index = False, sep = '\t')
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

