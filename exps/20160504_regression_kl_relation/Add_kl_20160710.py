
# coding: utf-8

import pandas as pd
import numpy as np
import ast
from datetime import date

def calc_kl(p, q):
    return sum([p[i]*(np.log2(p[i]/q[i])) for i in range(len(p))])

def create_df_time(df, time):
    return df[df.PublishDate.str[:7] == time]

def calc_monthly_std(df):
    gammas = []
    dis = df.TopicDistribution.tolist()
    for i in dis:
        gammas.append(ast.literal_eval(i))
        
    gammas_flat = []
    for gamma in gammas:
#         gamma = ast.literal_eval(gamma)
        for elem in gamma:
            gammas_flat.append(elem)
    ave = {}
    for n in range(40):
        t = []
        for i in gammas_flat:
            if i[0] == n:
                t.append(i[1])
        ave[n] = sum(t)/float(len(df))
    return ave.values()

def calc_ind_kl(td, std_month):
    try:
        return calc_kl(td, std_month)
    except:
        return float('nan')


def date_today(cell):
    try:
        y, m, d = cell.split('-')
        return abs(date.today() - date(int(y), int(m), int(d))).days
    except:
        return 0


def add_kl(fn):
    print 'reading csv: ', fn
    df = pd.read_csv(fn + '_processed.tsv', sep = '\t')
    df = df.fillna(0)

    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    timelist = sorted(list(set(timelist)))

    print 'calculating std gammas'
    std_gammas = {}
    for time in timelist:
        df_t = create_df_time(df, time)
        std_gammas[time] = calc_monthly_std(df_t)

    print 'adding kl'
    df['KL'] = df.apply(lambda row:calc_ind_kl([i[1] for i in ast.literal_eval(row['TopicDistribution'])], std_gammas.get(str(row['PublishDate'])[:7])), axis = 1)

    df['PublishDate'] = df.apply(lambda row: date_today(row['PublishDate']), axis = 1)
    df['CompleteDate'] = df.apply(lambda row: date_today(row['CompleteDate']), axis = 1)

    print 'grouping'
    df = df.groupby(['AdditionalTags', 'ArchiveWarnings', 'Author', 'Bookmarks', 'Category', 'Chapters', 'Characters', 'Fandoms', 'Hits', 'Kudos', 'Rating', 'Relationship', 'Title', 'UpdateDate', 'Words']).agg({'PublishDate': np.max, 'CompleteDate': np.min, 'Comments': np.sum, 'KL': [np.mean]}).reset_index()

    df.to_csv(fn + '_processed2.tsv', index = False, sep = '\t')
    print 'process finished'
    
fandoms = [
'sherlock_holmes_&_related_fandoms',
'sherlock(TV)'
]

for f in fandoms:
    add_kl(f)

'''
done:
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
'''


