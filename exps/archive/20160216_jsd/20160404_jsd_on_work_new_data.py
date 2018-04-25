
# coding: utf-8

# In[2]:

import numpy as np
import pandas as pd
import re
from collections import Counter
from scipy import special
# import matplotlib.pyplot as plt
# %matplotlib inline 
import random

# In[5]:

data = pd.read_csv('../../data/sherlock_current_wtext.csv')

# In[6]:

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


# In[7]:

def filter_length(text, word_limit):
    return [line for line in text if len(line) > word_limit]


# In[8]:

def filter_top_words(text, top_number):
    corpus = [word for line in text for word in line]
    c = Counter(corpus)
    top = [i[0] for i in c.most_common(top_number)]
    text_intop = []
    for line in text:
        line = [word for word in line if word in top]
        text_intop.append(line)
    return text_intop


# In[9]:

def calculate_prob_matrix(text_list):
    #vectorize the words and turn each work into a list of word frequences over the whole vocalburary.
    #input: a list of list of words.
    #output: np array.
    vocabulary = list(set([word for text in text_list for word in text]))
    text_prob_matrix = []
    for text in text_list:
        freq_list = []
        c = Counter(text)
        for word in vocabulary:
            if word in text:
                freq_list.append(c[word])
            else:
                freq_list.append(0)
        s = float(sum(freq_list))
        if s != 0:
            text_prob = [freq/s for freq in freq_list]
            text_prob_matrix.append(text_prob)
    text_prob_matrix = np.asarray(text_prob_matrix)
    return text_prob_matrix


# In[11]:

def JSD(P, Q):
    M = 0.5 * (P + Q)
    return 0.5 * (sum(special.rel_entr(P, M)) + sum(special.rel_entr(Q, M)))


# In[12]:

def calculate_monthly_jsd(matrix):
    jsds = []
    for i in range(matrix.shape[0]):
        for j in range(i+1, matrix.shape[0]):
            jsds.append(JSD(matrix[i], matrix[j]))
    return jsds


# In[13]:

def calculate_monthly_jsd_sampled(matrix):
    jsds = []
    l = matrix.shape[0]
    for n in range(1000):
        i = random.randrange(1, l)
        j = random.randrange(1, l)
        jsds.append(JSD(matrix[i], matrix[j]))
    return jsds


# In[14]:

def bootstrap_resample(jsd_list):
    ave_original = np.average(jsd_list)
    aves = []
    for i in range(1000):
        sample = []
        for i in range(len(jsd_list)):
            sample.append(random.choice(jsd_list))
        aves.append(np.average(sample))
    tail = sorted(aves)[24]
    head = sorted(aves)[975]
    return (ave_original, tail, head)


# In[15]:

def create_df_time(df, time):
    return df[df.PublishDate.str[:7] == time]


# In[16]:

timelist = data.PublishDate.drop_duplicates().tolist()
timelist = [str(i)[:7] for i in timelist]
timelist = sorted(list(set(timelist)))[2:]

# import warnings
# #put the following 2 lines before the nested loop code
# with warnings.catch_warnings(): 
#    warnings.simplefilter("ignore", category=RuntimeWarning)

for month in timelist[timelist.index('2014-09'):]:
    df_ts = create_df_time(data, month)
    text = preprocess(df_ts)
    work_count = (len(text))
    text = filter_top_words(text, 1000)
    if len(text) > 0:
        matrix = calculate_prob_matrix(text)
        monthly_jsds = calculate_monthly_jsd(matrix)
        monthly_ave_resampled_jsds = bootstrap_resample(monthly_jsds)
        
        with open('jsds_on_work_new_data.txt', 'a') as g:
            g.write(str(month) + '\t' + str(monthly_ave_resampled_jsds))
            g.write('\n')

        with open('work_count_new_data.txt', 'a') as g2:
            g2.write(str(work_count))
            g2.write('\n')

# # In[33]:

# y = [i[0] for i in jsd]
# x = range(len(y))

# # example error bar values that vary with x-position
# # error = 0.1 + 0.2 * x

# # error bar values w/ different -/+ errors
# lower_error = [i[0]-i[1] for i in jsd]
# upper_error = [i[2]-i[0] for i in jsd]
# asymmetric_error = [lower_error, upper_error]

# fig, ax = plt.subplots(figsize = (10, 7))

# ax.errorbar(x, y, yerr=asymmetric_error,marker='o')
# ax.set_title('Average pairwise jsd over time range')
# # ax.set_yscale('log')
# # ax.set_ylim([0.180, 0.225])
# plt.show()




