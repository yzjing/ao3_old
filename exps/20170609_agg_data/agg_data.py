
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

	df = pd.read_csv('../../data/' + fandom + '_preprocessed.tsv', sep = '\t')
	df = df[['Author','Bookmarks','Chapters','Comments','CompleteDate','Hits','Kudos','PublishDate','Text','Title','UpdateDate','Words']]
	df['PublishDate'] = df.apply(lambda row: date_today(row['PublishDate']), axis = 1)
	df['UpdateDate'] = df.apply(lambda row: date_today(row['UpdateDate']), axis = 1)
	df['CompleteDate'] = df.apply(lambda row: date_today(row['CompleteDate']), axis = 1)

	df_agg = df.groupby(['Author','Hits','Kudos','Title','Words','Bookmarks','Chapters','Comments'])\
	                     .agg({'CompleteDate':np.min, 'PublishDate':np.max,'UpdateDate':np.max,\
	                                                'Text':lambda x: ','.join(x)}).reset_index()
	df_agg.to_csv(fandom+'_agg.tsv',index=False,sep='\t')


fandom_list = [line.strip() for line in open('../../data/fandom_filtered_list')]
for fandom in fandom_list:
	agg_data(fandom)


