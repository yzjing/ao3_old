
# coding: utf-8

# In[101]:

import pandas as pd
import os
import numpy as np
from collections import Counter


# In[2]:

data_path = '../metadata/'


# In[87]:

def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    return sorted(list(set(timelist)))

def create_df_time(df, timelist):
    dfs = []
    for time in timelist:
        dfs.append(df[df.PublishDate.str[:7] == time])
    try:
        return pd.concat(dfs)
    except:
        return []


# In[20]:

def create_timelist_prev(time, timelist):
    return timelist[timelist.index(time)-6:timelist.index(time)]


# In[95]:

# "surprise" of a tag = (num of fics with tag)/(num of all fics + 1)
# novelty = -(total surprise of all tags in fic)/((num of tags))

def calc_novelty(df, row, tl):
    time = row['PublishDate'][:7]
    timelist_prev = create_timelist_prev(time, tl)
    df_t = create_df_time(df, timelist_prev)
    if len(df_t) > 0:
        tags = []
        for line in df_t['AdditionalTags'].tolist():
            tags.extend([elem.strip() for elem in line.split(',')])
        tags_c = Counter(tags)
        # Remove tags that appear only once

        tags = {t: tags_c[t] for t in tags if tags_c[t] > 1}
        tags_c = Counter(tags)

        tag_prob_all = 0
        fic_tags = [item.strip() for item in row['AdditionalTags'].split(',')]
        fic_tags = [t for t in fic_tags if t in tags]
        if len(fic_tags) > 0:
            for tag in fic_tags:
                tag_prob_all += tags_c[tag] / (len(df) + 1)
            nov_sc = -tag_prob_all/(len(fic_tags))
            return nov_sc
        else:
            return np.nan


fandoms = [
'homestuck'
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
'the_avengers_all_media_types',
'harry_potter',
'supernatural',
'marvel',
]

'''done:
'homestuck',
'''

for fandom in fandoms:
    df = pd.read_csv(os.path.join(fandom + '_preprocessed.tsv'), sep = '\t')
    df = df[df.Text.str.split().map(len) >= 500]
    df = df[df.Text.str.split().map(len) <= 1500]
    tl = create_timelist(df)
    df['AdditionalTags'] = df['AdditionalTags'].fillna('None')
    df['tag_novelty'] = df.apply(lambda row: calc_novelty(df, row, tl), axis=1)
    del df['Text']
    df.to_csv(fandom + '_tag_novelty_conlen_full.tsv', index = False, sep = '\t')
    print('Done with: ', fandom)
    break
