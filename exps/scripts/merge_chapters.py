
# coding: utf-8

# In[1]:
import pandas as pd
import numpy as np
from datetime import date


def earlist_date(cell):
    cell = cell.values
    y, m, d = cell[0].split('-')
    min_date = date.today()
    conv_date = date(int(y), int(m), int(d))
    if conv_date < min_date:
        min_date = conv_date
    return min_date
    
def latest_date(cell):
    cell = cell.values
    try:
        y, m, d = cell[0].split('-')
        max_date = date(2000, 1, 1)
        conv_date = date(int(y), int(m), int(d))
        if conv_date > max_date:
            max_date = conv_date
        return max_date
    except:
        return float('nan')
    

def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_preprocessed_filter_en_20210915.tsv', sep = '\t')
    df = df.replace([np.inf, -np.inf], np.nan)
    df['Hits'].fillna(0, inplace=True)
    df['Kudos'].fillna(0, inplace=True)
    df['Bookmarks'].fillna(0, inplace=True)
    df['Comments'].fillna(0, inplace=True)
    grp = df.groupby(['AdditionalTags', 'ArchiveWarnings', 'Author', 'Bookmarks', 'Category',
					'Chapters', 'Characters', 'Fandoms', 'Hits', 'Kudos', 'Language', 
					'Rating', 'Relationship', 'Title', 'Words'], dropna=False)\
			.agg({'Text':' '.join, 'PublishDate': lambda x: earlist_date(x), \
    		 'UpdateDate': lambda x: latest_date(x), 'CompleteDate': lambda x: latest_date(x),\
   			  'Comments': sum, 'URL': np.random.choice})\
			.reset_index()
    # print(len(grp[grp.Kudos == 0]))
    grp.to_csv(fandom + '_preprocessed_filter_en_merged_chs_20210915.tsv', sep='\t', index=False)
    


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

"""


"""

for fandom in fandoms:
    # try:
    main(fandom)
    # except:
    #     print('failed with: ',fandom)
    #     continue
        
# profile.run('main("shakespare_william_works")')

'''
done:

''' 

'''
'''

