
# coding: utf-8

# In[1]:
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import re
from collections import Counter
from scipy import spatial

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


#

def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    return sorted(list(set(timelist)))

def create_timewindow(timelist, window_len, step):
    idx = 0
    window_all = []
    while idx <= len(timelist) - window_len:
        time_window = []
        for i in range(0, window_len):
            time_window.append(timelist[idx + i])
        idx += 3
        window_all.append(time_window)
    return window_all

def create_df_time(df, time_window):
    dfs = []
    for time in time_window:
        dfs.append(df[df.PublishDate.str[:7] == time])
    return pd.concat(dfs)

def main(fandom):
    # print('working on fandom: ', fandom)
    # df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')

    # # exclude works with less than 500 words
    # df = df[df.Text.str.split().map(len) >= 500]

    # timelist = create_timelist(df)
    # windows = create_timewindow(timelist, 6, 3)
    # prev_std = []
    # df_all = []
    # for window in windows:
    #     df_t = create_df_time(df, window)

    test_doc = ['cat dog dog', 'dog sheep bird', 'cat bird dog']
    vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
    transformed_doc = vectorizer.fit_transform(test_doc) 
    print(vectorizer.vocabulary_)
    for i in range(3):
        print(transformed_doc[i,:].todense())
    
    #         df_t['Dist'] = df_t['Text'].map(lambda x: get_dist(x, sgt_di, vocab_fil))
    #         del df_t['Text']

    #         if len(prev_std) > 1:
    #             df_t['Cos'] = df_t.apply(lambda row: spatial.distance.cosine(row['Dist'], prev_std), axis=1)
    #             del df_t['Dist']
    #             df_all.append(df_t)

    #         dist_array = np.asarray(df_t.Dist.tolist())
    #         prev_std = np.mean(dist_array, axis=0)

    # df_all = pd.concat(df_all)
    # df_all.to_csv(fandom + '_temporal_cos_toprev.tsv', index = False, sep = '\t')
    # print('Done with: ', fandom)

fandoms = [
'shakespare_william_works',
]
'''
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
'''

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

