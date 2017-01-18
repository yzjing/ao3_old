import multiprocessing

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
def create_unigram_freq_dict(doc, voc):
    text = []
    for line in doc:
        line = re.findall(u'(?u)\\b\\w\\w+\\b', line)
        line = [st.stem(word) for word in line if word in voc]
        text.append(dict(Counter(line)))
    return text


# In[6]:

def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    return sorted(list(set(timelist)))


# In[7]:

def create_df_time(df, time):
    return df[df.PublishDate.str[:7] == time]


# In[49]:

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

def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv('../../data/preprocessed_data/' + fandom+'_preprocessed.tsv', sep = '\t')
    kl_all = []
    t0 = time()
    min_df = 2
        
    timelist = create_timelist(df)

    for t in timelist:
        sgt_list = []
        df_t = create_df_time(df, t)
        
        # len(df_t) must > min_df
        # tune this for filtering?
        if len(df_t) > min_df*10:
            
            # output of the following pipeline:
            # a list of lists, each list containing sgt word probablity
            # word order is supposed to be the same
            corp = create_corpus_for_voc(df_t)
            vocab = get_voc(corp,1,min_df)
            unigram_dict = create_unigram_freq_dict(corp, vocab)
            for i in unigram_dict:
                sgt_list.append(calc_sgt(i, vocab))
            
            # calculate kl.
            # std: "standard work", average of the numpy matrix
            # calculate kl of each work - std work in each month
            # then use the average as kl of the month
            sgt_array = np.asarray(sgt_list)
            std = np.mean(sgt_array, axis=0)
            kl_month = []
            for row in sgt_array:
                kl = calc_kl(std, row)
                kl_month.append(kl)
            kl_all.append(np.average([i for i in kl_month if not np.isinf(i)]))
    with open(fandom, 'w') as g:
        for i in kl_all:
            g.write(str(i))
            g.write('\n')
    print("done in %0.3fs." % (time() - t0))


fandoms = [
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

jobs = []
for fandom in fandoms:
    p = multiprocessing.Process(target=main, args=(fandom,))
    jobs.append(p)
    p.start()





