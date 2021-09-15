
# coding: utf-8

import pandas as pd


def main(fandom_list):
    for fandom in fandom_list:
        print('working on fandom: ', fandom)
        df = pd.read_csv(fandom + '_temporal_lda_jsd_toprev_with_dist_merged_chs_sampled.tsv', sep = '\t')
        del df['Text']
        df.to_csv(fandom + '_temporal_lda_jsd_toprev_with_dist_merged_chs_no_text.tsv', index = False, sep = '\t')


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

if __name__ == "__main__":
    main(fandoms)
        


