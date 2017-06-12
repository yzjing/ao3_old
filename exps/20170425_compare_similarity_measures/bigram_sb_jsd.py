
# coding: utf-8

# In[1]:
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import re
from collections import Counter
from memory_profiler import profile
from scipy import special

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

# Get a vocabulary using sklearn's filtering. Return: unique ngrams after filtering
def get_voc(corpus, n, mindf):
    vectorizer = CountVectorizer(stop_words='english', ngram_range=(n,n),min_df=mindf)
    f = vectorizer.fit(corpus)
    return set(f.get_feature_names())

# In[5]:

# compute unigram-frequency dict using the same preprocessing, using only words from the vocabulary
def create_unigram_freq_dict(df, voc):
    text = []
    df_text = df.Text.tolist()
    for line in df_text:
        line_f = re.sub(r'aA|aa', 'a', line)
        line_f = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line_f).lower()
        line_f = re.findall(u'(?u)\\b\\w\\w+\\b', line_f)
        text.extend(line_f)
    text = map(lambda x:x if x in voc else None, text)
    text = dict(Counter(text))
    return text

def create_bigram_freq_dict(df, voc):
    text = []
    df_text = df.Text.tolist()
    for line in df_text:
        line_f = re.sub(r'aA|aa', 'a', line)
        line_f = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line_f).lower()
        line_f = re.findall(u'(?u)\\b\\w\\w+\\b', line_f)
        text.extend(line_f)
    text_bi = []
    for i in range(len(text)-1):
        text_bi.append(text[i]+' '+text[i+1]) 
    text_bi = map(lambda x:x if x in voc else None, text_bi)
    text_bi = dict(Counter(text_bi))
    return text_bi

# Stupid backoff. If bigram is in dictionary, score = freq/size.
# If not, go back to unigram, score = 0.4*unigram/size.

def calc_sb(bigram, bifreq, unifreq):
    if bifreq.get(bigram):
        return float(bifreq.get(bigram))/len(bifreq)
    else:
        uni = bigram.split(' ')[1]
        return float(0.4*unifreq.get(uni, 0))/len(unifreq)


def sb_score(bivocab, sentence, unifreq, bifreq):
    bigrams = []

    sentence = re.sub(r'aA|aa', 'a', sentence)
    sentence = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', sentence).lower()
    sentence = re.findall(u'(?u)\\b\\w\\w+\\b', sentence)
    for i in range(len(sentence)-1):
        bigrams.append(sentence[i]+' '+sentence[i+1]) 

    prob = list(map(lambda x: calc_sb(x, bifreq, unifreq) if x in bigrams else 0, bivocab))

    return prob

# In[6]:
def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    return sorted(list(set(timelist)))

# In[7]:
def create_df_time(df, time):
    return df[df.PublishDate.str[:7] == time]

def calc_kl(p, q):
    return sum([p[i]*(np.log2(p[i]/q[i])) for i in range(len(p))])

def JSD(P, Q):
    M = 0.5 * (P + Q)
    return 0.5 * (sum(special.rel_entr(P, M)) + sum(special.rel_entr(Q, M)))

# Take average of distributions of the month
def calc_monthly_std(df):
    dist_array = np.asarray(df.Dist.tolist())
    std = np.mean(dist_array, axis=0)
    return std

# In[56]:

# kl between a distribution and std of the month
def calc_kl2std(dist, std_month):
    return calc_kl(dist, std_month)

def calc_jsd2std(dist, std_month):
    return JSD(dist, std_month)

def preprocess(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv('data/' + fandom + '_preprocessed.tsv', sep = '\t')
    df = df.fillna(0)
    df = df.sample(10000, replace=True)

    try:
        df = df[['Author','ChapterIndex', 'Hits', 'Kudos', 'PublishDate', 'Summary', 'Text', 'Title', 'URL', 'Words']]    
    except:
        df = df[['Author','ChapterIndex', 'Hits', 'Kudos', 'PublishDate', 'Summary', 'Text', 'Title', 'Words']]    
    
    # exclude words that appear in less than this many works.
    min_df = 4

    #exclude works with less than 500 words
    df = df[df.Words.astype(int) > 500]

    # exclude the months with less than 10 authors or 10000 words
    tl = create_timelist(df)
    timelist = []
    for t in tl:
        df_t = create_df_time(df, t)
        try:
            df_t = df_t.drop(['ChapterIndex', 'URL', 'Text','Summary'], axis=1)
            df_t = df_t.drop_duplicates()
        except:
            df_t = df_t.drop(['ChapterIndex', 'Text','Summary'], axis=1)
            df_t = df_t.drop_duplicates()

        words = df_t.Words.sum()
        authors = len(set(df_t.Author.tolist()))
        if words > 5000 and authors > 5:
            timelist.append(t)

    df = df[df.PublishDate.str[:7].isin(timelist)]
    
    df = df[['Author', 'Hits', 'Kudos', 'PublishDate', 'Text', 'Title']]    
    return df, timelist

def add_dist(df,fandom):
    # Add a column of smoothed bigram probablities to df
    dfs = []
    for time in timelist:
        try:
            df_t = create_df_time(df, time)
            corpus = create_corpus_for_voc(df_t)
            univocab = get_voc(corpus, 1,4)
            unidict = create_unigram_freq_dict(df_t, univocab)
            bivocab = get_voc(corpus,2,4)
            bidict = create_bigram_freq_dict(df_t, bivocab)

            df_t['Dist'] = df_t['Text'].map(lambda x: sb_score(bivocab, x, unidict, bidict))
            std = calc_monthly_std(df_t)
            df_t['JSD'] = df_t.apply(lambda row: calc_jsd2std(row['Dist'], std), axis = 1)
            del df_t['Text']
            del df_t['Dist']
            dfs.append(df_t)
        except:
            continue
    df = pd.concat(dfs, ignore_index=True)
    # df = df.fillna(0)
    df = df.groupby(['Author', 'Hits', 'Kudos', 'Title']).agg({'JSD': [np.mean]}).reset_index() 
    df.to_csv(fandom + '_bigram_jsd.tsv', index = False, sep = '\t')
    print('Done with: ', fandom)


fandoms = [
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
'marvel'
]

if __name__ == '__main__':
    for fandom in fandoms:
        df,timelist = preprocess(fandom)
        add_dist(df,fandom)



# jobs = []
# for fandom in fandoms:
#     p = multiprocessing.Process(target=main, args=(fandom,))
#     jobs.append(p)
#     p.start()

# main("shakespare_william_works")

'''
done:
'bishoujo_senshi_sailor_moon',
'haikyuu',
'hamilton_miranda',
'kuroko_no_basuke',
'les_miserables_all_media_types',
'shakespare_william_works',
''' 
