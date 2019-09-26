
# coding: utf-8

# In[54]:

import pandas as pd
from gensim import corpora, models, similarities
import re


# In[55]:

f = 'sherlock_current_wtext.csv'


# In[56]:

def preprocess(df, st):
    #pre-processing
    #input: a slice of the original df
    #output: a list of lists each containing cleaned words from a work
    df = df.astype(str)
    df = df.groupby(['Additional_Tags', 'Archive_Warnings', 'Author', 'Bookmarks',               'Category', 'Chapters', 'Characters', 'Comments', 'CompleteDate',               'Fandoms', 'Hits', 'Kudos', 'Language', 'PublishDate',                 'Rating', 'Relationship', 'Summary', 'Title', 'Words'])['Text'].apply(','.join).reset_index()
    text = df[['Text']]
    text['Text'] = text['Text'].str.replace('A', '')
    text = text.drop_duplicates().Text.str.lower().str.split()
    text_cleaned = []
    for line in text:
        line = [re.sub(r'[^A-Za-z0-9]+', '', str(word)) for word in line]
        line = [word for word in line if len(word) > 1 and not word.isdigit() and word not in st]
        text_cleaned.append(line)
    return text_cleaned


# In[57]:

def filter_length(text, word_limit):
    return [line for line in text if len(line) > word_limit]


# In[58]:

def create_df_time(df, time):
    return df[df.PublishDate.str[:7] == time]


# In[ ]:

df = pd.read_csv(f)


# In[ ]:

df = df[df.PublishDate.str[:7] == df.CompleteDate.str[:7]]


# In[ ]:

timelist = df.PublishDate.drop_duplicates().tolist()
timelist = [str(i)[:7] for i in timelist]
timelist = sorted(list(set(timelist)))


# In[ ]:

st = [line.strip() for line in open('nltk_stopwords', 'r') ]


# In[ ]:

text = preprocess(df, st)
text = filter_length(text, 500)
id2word = corpora.dictionary.Dictionary(text)
corpus = [id2word.doc2bow(t) for t in text]
lda = models.LdaModel(corpus=corpus,id2word=id2word,num_topics=40)


# In[52]:

for month in timelist:
    df_ts = create_df_time(df,month)
    text = preprocess(df_ts, st)
    text = filter_length(text, 500)
    with open('lda_results/topic40/lda_topic40_%s' %month, 'w') as g:
        for i in range(len(text)):
            g.write(str(lda.get_document_topics(id2word.doc2bow(text[i]), minimum_probability = 0)))
            g.write('\n')


# In[ ]:


