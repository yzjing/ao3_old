
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import re
from gensim import corpora, models, similarities


# In[2]:

f = '../../data/sherlock_current_wtext.csv'


# In[3]:

data = pd.read_csv(f)


# In[4]:

df = data


# In[5]:

# df = df.head(100)


# In[6]:

# df = df.fillna(0)


# In[7]:

# df = df.astype(str)


# In[8]:

df.columns.values


# In[9]:

def bookmarks_values(bms, pubdate):
    if bms != 0:
        pubdate = pubdate[:7]
        v = re.findall(': ([0-9]+)', cell)
        return sum([int(i) for i in v])


# In[10]:

df.AdditionalTags = df.AdditionalTags.str.strip()


# In[11]:

df.ArchiveWarnings = df.ArchiveWarnings.str.strip()


# In[12]:

# df.Bookmarks = df.apply(lambda row:bookmarks_values(row['Bookmarks']),axis = 1)


# In[13]:

def ch_values(cell):
    return cell.split('/')[0]


# In[14]:

df.Chapters = df.apply(lambda row:ch_values(row['Chapters']),axis = 1)


# In[15]:

df.Characters = df.Characters.str.strip()


# In[16]:

def comments_values(cell):
    if cell != 0:
        v = re.findall(': ([0-9]+)', cell)
        return sum([int(i) for i in v])


# In[17]:

# df.Comments = df.apply(lambda row:comments_values(row['Comments']),axis = 1)


# In[18]:

df.Rating = df.Rating.str.strip()


# In[19]:

df.Relationship = df.Relationship.str.strip()


# In[20]:

df['FullLength'] = df['Words']


# In[21]:

df['ChapterLength'] = len(df.Text.str.split()[0])


# In[22]:

lda = models.LdaModel.load('../20160225_lda/sherlock_40topics')


# In[23]:

def get_gamma(text, id2word):
    #pre-processing
    #input: a slice of the original df
    #output: a list of lists each containing cleaned words from a work
    text = text.lower().split()
    text = [re.sub(r'[^A-Za-z0-9]+', '', str(word)) for word in text]
    text = [word for word in text if len(word) > 1 and not word.isdigit()]
    gamma = lda.get_document_topics(id2word.doc2bow(text), minimum_probability = 0)
    return gamma


# In[24]:

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


# In[25]:

text_all = preprocess(df)
print len(text_all)
id2word = corpora.dictionary.Dictionary(text_all)


# In[27]:

import cPickle as pickle
id2word = pickle.load(open('../../id2word.p'))


# In[28]:

id2word[10]


# In[29]:

df['TopicDistribution'] = df.apply(lambda row:get_gamma(row['Text'], id2word), axis=1)


# In[30]:

df.head()


# In[31]:

df2 = df[['AdditionalTags', 'ArchiveWarnings', 'Author', 'Bookmarks', 'Category', 'Chapters', 'Characters', 'Comments',       'CompleteDate', 'Fandoms', 'Hits', 'Kudos', 'PublishDate', 'Rating', 'Relationship', 'TopicDistribution', 'FullLength', 'ChapterLength']]


# In[32]:

df2.head(1)


# In[34]:

df2.to_csv('../../data/sherlock_processed.tsv', index = False, sep = '\t')


# In[ ]:



