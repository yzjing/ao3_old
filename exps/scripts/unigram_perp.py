
# coding: utf-8

# In[1]:
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import re
import sgt_opt as sgt
from collections import Counter
from scipy import stats

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

# Get a vocabulary using sklearn's filtering
def get_voc(corpus, ngram, mindf):
    vectorizer = CountVectorizer(stop_words='english', ngram_range=(ngram,ngram),min_df=mindf)
    f = vectorizer.fit_transform(corpus)
    return set(sorted(vectorizer.get_feature_names()))


# compute unigram-frequency dict using the same preprocessing, using only words from the vocabulary
def create_unigram_freq_dict(df, voc):
    text = {}
    df_text = df.Text.tolist()
    for line in df_text:
        line_f = re.sub(r'aA|aa', 'a', line)
        line_f = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line_f).lower()
        line_f = re.findall(u'(?u)\\b\\w\\w+\\b', line_f)
        line_f = [word for word in line_f if word in voc]
        text[line] = dict(Counter(line_f))
    return text

def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    timelist = [item for item in timelist if int(item[0:4]) >= 2009]
    return sorted(list(set(timelist)))

def create_df_time(df, time_window):
    dfs = []
    for time in time_window:
        dfs.append(df[df.PublishDate.str[:7] == time])
    return pd.concat(dfs)

# calculate unigram probabilities by simple Good Turing smoothing.
# imput: unigram-freq dict
# output: unigram-prob dict, mimic of a document-term matrix
# if unigram is in this doc, prob = the unigram prob calculated by sgt
# otherwise, prob = the probability given to "all unknown unigrams" by sgt
# def calc_sgt(line_dict, voc):
#     prob_line = []
#     sgt_line = sgt.simpleGoodTuringProbs(line_dict)
#     num_abs_words = len(voc - set(line_dict.keys()))
#     for word in voc:
#         if word in line_dict.keys():
#             prob_line.append(sgt_line[0][word])
#         else:
#             prob_line.append(sgt_line[1]/float(num_abs_words))
#     gc.collect()
#     return prob_line


# # In[13]:
# def get_dist(text, di, vocab):
#     return calc_sgt(di[text], vocab)

def get_dist(text, di, vocab):
    prob_line = []
    try:
        sgt_line = sgt.simpleGoodTuringProbs(di[text])
        num_abs_words = len(vocab - set(di[text].keys()))
        for word in vocab:
            if word in di[text].keys():
                prob_line.append(sgt_line[0][word])
            else:
                prob_line.append(sgt_line[1]/float(num_abs_words))
        return prob_line
    except:
        return [0]

def calc_perp(prob_line):
    ent = stats.entropy(prob_line)
    return np.power(2, ent)

def run_all(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv('../' + fandom + '_preprocessed2.tsv', sep = '\t')
    # length between 500 - 1500 words
    df = df[df.Text.str.split().map(len) >= 500]

    min_df = 4

    timelist = create_timelist(df)
    df_all = []
    for time in timelist[6:]:
        # use the current month and the past 6 months
        # df_t_curr = create_df_time(df, time)
        df_t = create_df_time(df, timelist[timelist.index(time)-6:timelist.index(time)])
        df_t = df_t.reset_index()
    
        # df_t = df_t.sample(50,replace=True)

        # Add a column of smoothed unigram probablities to df
        corp = create_corpus_for_voc(df_t)
        vocab = get_voc(corp,1,min_df)
        unigram_dict = create_unigram_freq_dict(df_t, vocab)
        df_t['Dist'] = df_t['Text'].map(lambda x: get_dist(x, unigram_dict, vocab))
        df_t['Perplexity'] = df_t['Dist'].map(lambda x: calc_perp(x))
        del df_t['Text']
        del df_t['Dist']
        df_all.append(df_t)

    df_all = pd.concat(df_all)
    df_all.to_csv(fandom + '_unigram_perplexity.tsv', index = False, sep = '\t')
    print('Done with: ', fandom)




if __name__ == "__main__":
    fandoms = [
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
    'marvel',
    ]

    for fandom in fandoms:
        run_all(fandom)

# jobs = []
# for fandom in fandoms:
#     p = multiprocessing.Process(target=main, args=(fandom,))
#     jobs.append(p)
#     p.start()



# profile.run('main("shakespare_william_works")')

# main("shakespare_william_works")

'''
done:
'bishoujo_senshi_sailor_moon',
'haikyuu',
''' 

