import pandas as pd 
from scipy import spatial
import numpy as np

# def get_cos(dist, std):
#     return spatial.distance.cosine(dist, std)

def add_cos(fandom):
    df = pd.read_csv(fandom + '_agg_unigram_sgt_dist.tsv', sep = '\t')

    # print(df.columns.values)
    # need to eval? the Dist
    dist_array = df.Dist.tolist()
    dist_array = np.asarray([eval(i) for i in dist_array])
    std = np.mean(dist_array, axis=0)

    df['Cos'] = df.apply(lambda row: spatial.distance.cosine(eval(row['Dist']), std), axis=1)
    del df['Dist']
    df.to_csv(fandom + '_agg_cos.tsv', index = False, sep = '\t')
    

fandoms = [
'homestuck',
'bishoujo_senshi_sailor_moon',
'haikyuu',
'hamilton_miranda',
'kuroko_no_basuke',
'les_miserables_all_media_types',
'shakespare_william_works',
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

if __name__ == '__main__':
	for fandom in fandoms:
	    add_cos(fandom)
