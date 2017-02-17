
# coding: utf-8

# In[1]:

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from time import time
import pandas as pd
import re
import sys
sys.path.append('../../util/')
import sgt
from collections import Counter
from nltk.stem.snowball import EnglishStemmer


# In[2]:

st = EnglishStemmer()


# In[3]:

# create a corpus to give to sklearn
def create_corpus_for_voc(df):
    doc = []
    for i in df.Text.tolist():
        #Remove some non-ascii characters and 'aa's
        i = re.sub(r'aA|aa', 'a', i)
        i = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', i)
        i = i.lower()
        doc.append(i)  
    return doc


# In[4]:

# Get a vocabulary using sklearn's filtering
def get_voc(corpus, ngram, mindf):
    vectorizer = CountVectorizer(stop_words='english', ngram_range=(ngram,ngram),min_df=mindf)
    f = vectorizer.fit_transform(corpus)
    return set(sorted(vectorizer.get_feature_names()))


# In[5]:

# compute unigram-frequency dict using the same preprocessing, using only words from the vocabulary
def create_unigram_freq_dict(df, voc):
    text = {}
    df_text = df.Text.tolist()
    for line in df_text:
        line_f = re.sub(r'aA|aa', 'a', line)
        line_f = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line_f).lower()
        line_f = re.findall(u'(?u)\\b\\w\\w+\\b', line_f)
        line_f = [st.stem(word) for word in line_f if word in voc]
        text[line] = dict(Counter(line_f))
    return text


# In[6]:

def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    return sorted(list(set(timelist)))


# In[7]:

def create_df_time(df, time):
    return df[df.PublishDate.str[:7] == time]


# In[8]:

# calculate unigram probabilities by simple Good Turing smoothing.
# imput: unigram-freq dict
# output: unigram-prob dict, mimic of a document-term matrix
# if unigram is in this doc, prob = the unigram prob calculated by sgt
# otherwise, prob = the probability given to "all unknown unigrams" by sgt
def calc_sgt(line_dict, voc):
    prob_line = []
    sgt_line = sgt.simpleGoodTuringProbs(line_dict)
    num_abs_words = len(voc - set(line_dict.keys()))
    for word in voc:
        if word in line_dict.keys():
            prob_line.append(sgt_line[0][word])
        else:
            prob_line.append(sgt_line[1]/float(num_abs_words))
    return prob_line


# In[9]:

def calc_kl(p, q):
    return sum([p[i]*(np.log2(p[i]/q[i])) for i in range(len(p))])


# In[13]:

def get_dist(row, di, vocab):
    return calc_sgt(di[row['Text']], vocab)


# In[44]:

# Take average of distributions of the month
def calc_monthly_std(df, month):
    df_t = create_df_time(df, month)
    sgt_array = np.asarray(df_t.Dist.tolist())
    std = np.mean(sgt_array, axis=0)
    return std


# In[56]:

# kl between a distribution and std of the month
def calc_kl2std(dist, std_month):
    return calc_kl(dist, std_month)


def date_today(cell):
    try:
        y, m, d = cell.split('-')
        return abs(date.today() - date(int(y), int(m), int(d))).days
    except:
        return 0


def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv('../../data/preprocessed_data/' + fandom+'_preprocessed.tsv', sep = '\t')

    # tune this for filtering?
    min_df = 4

    # Add a column of smoothed unigram probablities to df
    corp = create_corpus_for_voc(df)
    vocab = get_voc(corp,1,min_df)
    unigram_dict = create_unigram_freq_dict(df, vocab)
    df['Dist'] = df.apply(lambda row: get_dist(row, unigram_dict, vocab), axis=1)

    # make a dict of std to reduce calculation
    timelist = create_timelist(df)
    std_all = {}
    for time in timelist:
        std_all[time] = calc_monthly_std(df, time)

    df['KL'] = df.apply(lambda row: calc_kl2std(row['Dist'], std_all.get(str(row['PublishDate'])[:7])), axis = 1)

    df['PublishDate'] = df.apply(lambda row: date_today(row['PublishDate']), axis = 1)
    df['CompleteDate'] = df.apply(lambda row: date_today(row['CompleteDate']), axis = 1)

    df = df.fillna(0)
    
    
    df = df.groupby(['AdditionalTags', 'ArchiveWarnings', 'Author', 'Bookmarks',\
       'Category',  'Chapters', 'Characters', 'Fandoms', 'Hits', 'Kudos', 'Rating', \
        'Relationship', 'Title', 'UpdateDate', 'Words'])\
        .agg({'PublishDate': np.max, 'CompleteDate': np.min, 'Comments': np.sum, 'KL': [np.mean]}).reset_index()

    df.to_csv('../../data/' + fandom + '_processed3.tsv', index = False, sep = '\t')


fandoms = [
'shakespare_william_works',
'hamilton_miranda',
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
'sherlock(TV)'
]

for fandom in fandoms:
    main(fandom)
    break







