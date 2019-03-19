
# coding: utf-8

import pandas as pd
import re

def preprocessing(f):
    #input: original csv file
    #preprocessing: remove duplicates, empty lines, non-English data, too short texts
    #output: pandas dataframe
    df = pd.read_csv('../../data_collection/all_fandoms/' + f + '.csv', error_bad_lines=False)
    df = df.drop_duplicates()
    df = df[df.Text.notnull()]
    df = df[df.Language == 'English']
    df = df[df['Text'].astype('str').str.len() > 500]
    return df

def bookmarks_values(cell):
    if cell != 0:
        v = re.findall(': ([0-9]+)', cell)
        return sum([int(i) for i in v])

def ch_values(cell):
    return cell.split('/')[0]

def comments_values(cell):
    if cell != 0:
        v = re.findall(': ([0-9]+)', str(cell))
        return sum([int(i) for i in v])

def fix_fields(df):
    df = df.astype(str)
    df.AdditionalTags = df.AdditionalTags.str.strip()
    df.ArchiveWarnings = df.ArchiveWarnings.str.strip()
    df.Characters = df.Characters.str.strip()
    df.Rating = df.Rating.str.strip()
    df.Relationship = df.Relationship.str.strip()
    df.Chapters = df.apply(lambda row:ch_values(row['Chapters']),axis = 1)
    df.Bookmarks = df.apply(lambda row:bookmarks_values(row['Bookmarks']),axis = 1)
    df.Comments = df.apply(lambda row:comments_values(row['Comments']),axis = 1)
    df = df.fillna(0)
    return df

fandoms = [
'hamilton_miranda',
'tolkien_j_r_r_works_&_related_fandoms',
'sherlock_holmes_&_related_fandoms'
]

for f in fandoms:
    print 'processing fandom:', f
    df = preprocessing(f)
    df = fix_fields(df)
    df.to_csv(f + '_preprocessed.tsv', index = False, sep = '\t')

'''
buffy_the_vampire_slayer',
'attack_on_titan',
'bandom',
'bishoujo_senshi_sailor_moon',
'actor_rpf',
'arthurian_mythology_&_related_fandoms',
'dcu',
'doctor_who',
'doctor_who_&_related_fandoms',
'dragon_age_all_media_types',
'dragon_age_inquisition',
'dragon_age_video_games',
'haikyuu',
'harry_potter',
'hetalia_axis_powers',
'homestuck',
'internet_personalities',
'k_pop',
'kuroko_no_basuke',
'les_miserables_all_media_types',
'les_miserables_schonberg_boublil',
'marvel',
'marvel_cinematic_universe',
'marvel_movies',
'ms_paint_adventures',
'music_rpf',
'naruto',
'one_direction',
'original_work',
'real_person_fiction',
'rock_music_rpf',
'shakespare_william_works',
'sherlock(TV)',
'star_wars_all_media_types',
'supernatural',
'the_avengers_all_media_types',
'the_avengers_ambiguous_fandom',
'the_walking_dead_&_related_fandoms',
'video_blogging_rpf'
'''


