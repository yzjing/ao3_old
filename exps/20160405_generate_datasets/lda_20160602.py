# coding: utf-8

import pandas as pd
from gensim import corpora, models, similarities
import re
import multiprocessing

def preprocess(df):
    #pre-processing
    #input: a slice of the original df  
    #output: a list of lists each containing cleaned words from a work
    df = df.astype(str)
    text = df[['Text']]
    text = text.drop_duplicates().Text.str.lower().str.split()
    text_cleaned = []
    for line in text:
        line = [re.sub(r'[^A-Za-z0-9]+', '', str(word)) for word in line]
        line = [word for word in line if len(word) > 1 and not word.isdigit()]
        text_cleaned.append(line)
    return text_cleaned


def run_lda(file_name):
    f = file_name + '_preprocessed.tsv'
    print 'reading from:', f
    df = pd.read_csv(f, sep = '\t', error_bad_lines=False)
    print 'dataframe created'
    text = preprocess(df)
    print 'preprocessing finished'
    id2word = corpora.dictionary.Dictionary(text)
    corpus = [id2word.doc2bow(t) for t in text]
    print 'start running lda'
    lda = models.LdaMulticore(corpus=corpus,id2word=id2word,num_topics=40)
    lda.save(file_name)
    print 'lda finished'

fandoms = [
]

'''
done:
'sherlock_holmes_&_related_fandoms'
'sherlock(TV)'
'hamilton_miranda'
'buffy_the_vampire_slayer'，
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
'hetalia_axis_powers',
'homestuck',
'internet_personalities',
'k_pop',
'kuroko_no_basuke',
'les_miserables_all_media_types',
'les_miserables_schonberg_boublil',
'ms_paint_adventures',
'music_rpf',
'naruto',
'one_direction',
'original_work',
'rock_music_rpf',
'shakespare_william_works',
'star_wars_all_media_types',
'the_walking_dead_&_related_fandoms',
'tolkien_j_r_r_works_&_related_fandoms'
'video_blogging_rpf'
'''


'''
not able to run:
'harry_potter',
'marvel',
'marvel_movies',
'marvel_cinematic_universe',
'supernatural',
'real_person_fiction',
'the_avengers_all_media_types',
'the_avengers_ambiguous_fandom',
'''

if __name__ == "__main__":
    for fandom in fandoms:
        run_lda(fandom)




