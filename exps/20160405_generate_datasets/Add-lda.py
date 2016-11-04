
# coding: utf-8

import pandas as pd
from gensim import corpora, models, similarities
import re

def get_gamma(text, lda, id2word):
    #pre-processing
    #input: a slice of the original df
    #output: a list of lists each containing cleaned words from a work
    text = text.lower().split()
    text = [re.sub(r'[^A-Za-z0-9]+', '', str(word)) for word in text]
    text = [word for word in text if len(word) > 1 and not word.isdigit()]
    gamma = lda.get_document_topics(id2word.doc2bow(text), minimum_probability = 0)
    return gamma

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


def add_lda(fn):
    print 'reading to csv: ', fn
    df = pd.read_csv(fn + '_preprocessed.tsv', sep = '\t')

    print 'loading lda model'
    lda = models.LdaModel.load(fn)

    print 'preprocess and create id2word'
    text_all = preprocess(df)
    id2word = corpora.dictionary.Dictionary(text_all)

    print 'getting gammas'
    df['TopicDistribution'] = df.apply(lambda row:get_gamma(row['Text'], lda, id2word), axis=1)
    df = df[['AdditionalTags', 'ArchiveWarnings', 'Author', 'Bookmarks',\
            'Category', 'ChapterIndex', 'Chapters', 'Characters', 'Comments',\
           'CompleteDate', 'Fandoms', 'Hits', 'Kudos', \
           'PublishDate', 'Rating', 'Relationship', 'Title',\
           'UpdateDate', 'Words', 'TopicDistribution']]
    df.to_csv('./processed_datasets/' + fn + '_processed.tsv', sep = '\t', index = False)

    print 'process finished'

fandoms = [
'sherlock(TV)',
]

for f in fandoms:
    add_lda(f)

'''
done:
'hamilton_miranda'
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
'sherlock_holmes_&_related_fandoms',
'''
