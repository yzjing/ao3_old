
# coding: utf-8

# In[1]:
import numpy as np
import pandas as pd
import re
from collections import Counter

from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from scipy import special, spatial
import random
# from sklearn.feature_extraction import stop_words


# st =  stop_words.ENGLISH_STOP_WORDS

def create_filter_vocab(text):
    text_all = []
    for line in text:
        text_all.extend(line)
    c = Counter(text_all)
    fvocab = list(dict(c.most_common(500)).keys())
    fvocab.extend([word for word in c if c[word] == 1])
    return set(fvocab)

def filter_text(text, vocab, retrieve=False):
    if retrieve == False:
        text = [[word for word in line if word not in vocab] for line in text]
        return text
    else:
        text = [word for word in text if word not in vocab]
        return text

# create a corpus to give to sklearn
def preprocess(df):
    doc = []
    for line in df.Text.tolist():
        #Remove some non-ascii characters and 'aa's
        line = re.sub(r'aA|aa', 'a', line)
        line = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line)
        line = re.findall(u'(?u)\\b\\w\\w+\\b', line)
        line = [word.lower() for word in line] 
        doc.append(line)  
    return doc

def create_corpus(sentences):
    id2word = corpora.dictionary.Dictionary(sentences)
    corpus = [id2word.doc2bow(sentence) for sentence in sentences]
    return id2word, corpus

def get_dist(line, vocab, model, id2word):
    line = re.sub(r'aA|aa', 'a', line)
    line = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line)
    line = re.findall(u'(?u)\\b\\w\\w+\\b', line)
    line = [word.lower() for word in line] 
    line = filter_text(line, vocab, True)
    return model.get_document_topics(id2word.doc2bow(line), minimum_probability = 0)

def JSD(P, Q):
    P = np.asarray(P)
    Q = np.asarray(Q)
    M = 0.5 * (P + Q)
    return 0.5 * (sum(special.rel_entr(P, M)) + sum(special.rel_entr(Q, M)))

def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')

    canon = open(fandom + '_canon.txt', 'r').read()
    canon = re.findall(u'(?u)\\b\\w\\w+\\b', canon)
    canon = [word.lower() for word in canon]
    
    # May only use single chapter works
    # length between 500 - 1500 words
    # df = df[df.Chapters == 1]
    df = df[df.Text.str.split().map(len) >= 500]
    df = df[df.Text.str.split().map(len) <= 1500]

    sentences = preprocess(df)
    sentences.append(canon)

    vocab = create_filter_vocab(sentences)

    sentences = filter_text(sentences,vocab)
    id2word, corpus = create_corpus(sentences)
    model = models.LdaMulticore(corpus=corpus,id2word=id2word,num_topics=100,workers=30)

    df['Dist'] = df['Text'].map(lambda x: get_dist(x, vocab, model, id2word))

    canon_dist = model.get_document_topics(id2word.doc2bow(filter_text(canon, vocab, True)), minimum_probability = 0)
    canon_dist = [i[1] for i in canon_dist]
    df['Dist'] = df['Text'].map(lambda x: get_dist(x, vocab, model, id2word))
    del df['Text']

    df['JSD'] = df.apply(lambda row: JSD([i[1] for i in row['Dist']], canon_dist), axis=1)
    del df['Dist']
    df.to_csv(fandom + '_lda_tocanon.tsv', index = False, sep = '\t')
    print('Done with: ', fandom)

fandoms = [
'sherlock_holmes_&_related_fandoms',
]


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

