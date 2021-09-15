import pandas as pd


fandoms = [
'shakespare_william_works',
'sherlock_holmes_&_related_fandoms',
'star_wars_all_media_types',
'les_miserables_all_media_types',
'bishoujo_senshi_sailor_moon',
'haikyuu',
'hamilton_miranda',
'kuroko_no_basuke',
'the_walking_dead_&_related_fandoms',
'hetalia_axis_powers',
'naruto',
'buffy_the_vampire_slayer',
'arthurian_mythology_&_related_fandoms',
'ms_paint_adventures',
'one_direction',
'attack_on_titan',
'doctor_who_&_related_fandoms',
'tolkien_j_r_r_works_&_related_fandoms',
'dcu',
'dragon_age_all_media_types',
'harry_potter',
'marvel',
'supernatural'

]

for fandom in fandoms:
    print('working on fandom: ', fandom)
    df = pd.read_csv( fandom + '_temporal_lda_perp.tsv', sep = '\t')
    del df['Processed_text']
    df.to_csv(fandom + '_temporal_lda_perp_rm_text.tsv', index = False, sep = '\t')
