
# coding: utf-8

# In[1]:
import numpy as np
import pandas as pd
import random
from sklearn.manifold import TSNE


def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')

    # May only use single chapter works
    # length between 500 - 1500 words
    # df = df[df.Chapters == 1]
    df = df.sample(1000)
    df = df.reset_index()
    tf = TfidfVectorizer(min_df=2, stop_words='english')
    vectorized = tf.fit_transform(df.Text.tolist()) 
    tsne = TSNE(n_components=2).fit_transform(vectorized)
    print(tsne.shape)
    # df['pc1'] = df.apply(lambda row: svd[row.name,0], axis=1)
    # df['pc2'] = df.apply(lambda row: svd[row.name,1], axis=1)
    # df.to_csv(fandom + '_tfidf_svd.tsv', index = False, sep = '\t')
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
        
'''

'''

