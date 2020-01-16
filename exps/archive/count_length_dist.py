
# coding: utf-8

# In[1]:
import pandas as pd

def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv('../' + fandom + '_preprocessed_merged_chs.tsv', sep = '\t')
    lens = df.Words.tolist()
    with open('length_dist.txt', 'a') as g:
    	for number in lens:
    		g.write(str(number))
    		g.write('\n')

    


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

