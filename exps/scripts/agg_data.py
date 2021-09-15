
# coding: utf-8

# In[101]:

import pandas as pd
from datetime import date
import numpy as np

def date_today(cell):
    if '-' in str(cell):
        y, m, d = cell.split('-')
        return abs(date.today() - date(int(y), int(m), int(d))).days

def agg_data(fandom):

	df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')
	df = df[['Author','Bookmarks','Chapters','Comments','CompleteDate','Hits','Kudos','PublishDate','Text','Title','UpdateDate','Words']]
	df['PublishDate'] = df.apply(lambda row: date_today(row['PublishDate']), axis = 1)
	df['UpdateDate'] = df.apply(lambda row: date_today(row['UpdateDate']), axis = 1)
	df['CompleteDate'] = df.apply(lambda row: date_today(row['CompleteDate']), axis = 1)

	df_agg = df.groupby(['Author','Hits','Kudos','Title','Words'])\
                     .agg({'Bookmarks':np.sum, 'Chapters':np.sum,'Comments':np.sum,\
                           'CompleteDate':np.min, 'PublishDate':np.max,'UpdateDate':np.max,\
                           'Text':lambda x: ','.join(x)}).reset_index()
	df_agg['completed_in_days'] = df_agg.PublishDate - df_agg.CompleteDate
	df_agg = df_agg.sample(1000)
	df_agg.to_csv(fandom+'_agg_1000.tsv',index=False,sep='\t')
	print('Finished with: ', fandom)


# fandom_list = [line.strip() for line in open('fandom_filtered_list')]
fandom_list = ['bishoujo_senshi_sailor_moon',
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
'homestuck',
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
'marvel']
for fandom in fandom_list:
	agg_data(fandom)


