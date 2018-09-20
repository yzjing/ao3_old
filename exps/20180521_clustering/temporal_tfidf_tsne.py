
# coding: utf-8

# In[1]:
import numpy as np
import pandas as pd
import random
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


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


def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')

    # length between 500 - 1500 words
    df = df[df.Text.str.split().map(len) >= 500]
    df = df[df.Text.str.split().map(len) <= 1500]

    timelist = create_timelist(df)
    windows = create_timewindow(timelist, 6)
    tsne_dict = {}

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

            tsne = TSNE(n_components=2).fit_transform(vectorized_prev.todense())
            tsne_dict[windows[i-1]] = tsne
    pickle.dump(tsne_dict, open(fandom + 'temporal_tsne.p', 'wb'))
    print('Done with: ', fandom)


fandoms = [
'shakespare_william_works',
'hetalia_axis_powers',
'marvel',
]


for fandom in fandoms:
    # try:
    # cProfile.run('main(fandom)')
    main(fandom)
    
    
    # except:
    #     print('failed with: ',fandom)
    #     continue
        
'''

'''

