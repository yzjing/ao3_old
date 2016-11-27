
# coding: utf-8

# In[38]:

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import re
from scipy import sparse

# In[60]:

def get_distribution_matrix(corpus, ngram):
    vectorizer = CountVectorizer(stop_words='english', ngram_range = (ngram,ngram))
    f = vectorizer.fit_transform(corpus)
    l = len(vectorizer.get_feature_names())
    return np.divide(f, l)

# In[21]:

def calc_kl(p, q):
    return sum([p[i]*(np.log2(p[i]/q[i])) for i in range(len(p))])

# In[32]:

def create_df_time(df, time):
    return df[df.PublishDate.str[:7] == time]

# In[34]:

def calc_kl_fd(fn):
    df = pd.read_csv(fn, sep = '\t')

    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    timelist = sorted(list(set(timelist)))

    kl_all = []
    for t in timelist:
        df_t = create_df_time(df, t)
        doc = []
        for i in df_t.Text.tolist():
            #Remove some non-ascii characters and 'aa's
            i = re.sub(r'aA|aa', 'a', i)
            i = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', i)
            doc.append(i)  
        m = get_distribution_matrix(doc,2)
        std = sparse.csr_matrix.mean(m, axis=0)
        std = np.asarray(std)[0]+1
        kl_month = []
        for row in m.toarray():
            kl = calc_kl(row+1, std)
            if not np.isnan(kl):
                kl_month.append(kl)
        kl_all.append(np.average(kl_month))

fandoms = [
'sherlock_holmes_&_related_fandoms',
'sherlock(TV)',
'hamilton_miranda',
'shakespare_william_works',
'les_miserables_schonberg_boublil',
'bishoujo_senshi_sailor_moon',
'kuroko_no_basuke',
'les_miserables_all_media_types',
'the_walking_dead_&_related_fandoms',
'original_work',
'haikyuu',
'hetalia_axis_powers',
'naruto',
'video_blogging_rpf',
'internet_personalities',
'star_wars_all_media_types',
'rock_music_rpf',
'buffy_the_vampire_slayer',
'arthurian_mythology_&_related_fandoms',
'dragon_age_inquisition',
'bandom',
'music_rpf',
'k_pop',
'ms_paint_adventures',
'doctor_who',
'homestuck',
'one_direction',
'attack_on_titan',
'doctor_who_&_related_fandoms',
'actor_rpf',
'tolkien_j_r_r_works_&_related_fandoms',
'dragon_age_video_games',
'dcu',
'dragon_age_all_media_types',
]

for f in fandoms:
    add_kl(f)

'''
done:
'''

kl_all_fds = {}
for fandom in fandoms:
    kl_all_fds[fandom] = calc_kl_fd(fandom)


import pickle
pickle.dump(kl_all_fds, open('2gram-kl-dict', 'wb'))


