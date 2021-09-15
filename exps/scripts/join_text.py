
# coding: utf-8

import pandas as pd


def main(fandom_list, novelty_df):
    df_text_all = []
    for fandom in fandom_list:
        print('working on fandom: ', fandom)
        df_text = pd.read_csv('../' + fandom + '_preprocessed2.tsv', sep = '\t')
        merged = pd.merge(novelty_df, df_text, on=['AdditionalTags', 'ArchiveWarnings', 'Author', 'Category',\
 'ChapterIndex', 'Chapters' ,'Characters' ,'CompleteDate',\
 'Fandoms',  'Language', 'Notes' ,'PublishDate' ,'Rating',\
 'Summary' ,'Title' ,'URL' ,'UpdateDate' ,'Words'], how='inner')
        df_text_all.append(merged)
    df_text_all = pd.concat(df_text_all)        
    df_text_all.to_csv('top_topic_novelty_text.tsv', index = False, sep = '\t')


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
    novelty_df = pd.read_csv('top_topic_novelty_to_join_text.tsv', sep='\t')
    main(fandoms, novelty_df)
        


