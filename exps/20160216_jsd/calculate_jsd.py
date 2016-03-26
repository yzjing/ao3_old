import numpy as  
import pandas as pd
import re
from collections import Counter
import random

data = pd.read_csv('sherlock_current_wtext.csv')

def preprocess(df):
    #pre-processing
    #input: a slice of the original df
    #output: a list of lists each containing cleaned words from a work
    df = df.astype(str)
    df = df.groupby(['Additional_Tags', 'Archive_Warnings', 'Author', 'Bookmarks',\
               'Category', 'Chapters', 'Characters', 'Comments', 'CompleteDate',\
               'Fandoms', 'Hits', 'Kudos', 'Language', 'PublishDate',\
                 'Rating', 'Relationship', 'Summary', 'Title', 'Words'])['Text'].apply(','.join).reset_index()
    text = df[['Text']]
    text['Text'] = text['Text'].str.replace('A', '')
    text = text.drop_duplicates().Text.str.lower().str.split()
    text_cleaned = []
    for line in text:
        line = [re.sub(r'[^A-Za-z0-9]+', '', str(word)) for word in line]
        line = [word for word in line if len(word) > 1 and not word.isdigit()]
        text_cleaned.append(line)
    return text_cleaned

def filter_top_words(text, top_number):
    corpus = [word for line in text for word in line]
    c = Counter(corpus)
    top = [i[0] for i in c.most_common(top_number)]
    text_intop = []
    for line in text:
        line = [word for word in line if word in top]
        text_intop.append(line)
    return text_intop

def filter_length(text, word_limit):
    return [line for line in text if len(line) > word_limit]

def calculate_prob_matrix(text_list):
    #vectorize the words and turn each work into a list of word frequences over the whole vocalburary.
    #input: a list of list of words.
    #output: np array.
    vocabulary = list(set([word for text in text_list for word in text]))
    text_prob_matrix = []
    freq_dict = {}
    for text in text_list:
        c = Counter(text)
        for word in vocabulary:
            if word in text:
                freq_dict[word] = c[word]
            else:
                freq_dict[word] = 0
        s = float(sum(freq_dict.values()))
        if s != 0:
            text_prob = [freq_dict[word]/s for word in sorted(freq_dict.keys())]
            text_prob_matrix.append(text_prob)
    text_prob_matrix = np.asarray(text_prob_matrix)
    return text_prob_matrix

def calculate_pairwise_jsd(p, q):
    #input: two lists of probablity distributions
    #output: jsd value
    m = [(p[i]+q[i])/2 for i in range(len(p)) ]
    kl_pm = [p[i]*(np.log2(p[i]/m[i])) for i in range(len(p))]
    kl_pm = sum([v for v in kl_pm if not np.isnan(v)])
    kl_qm = [q[i]*(np.log2(q[i]/m[i])) for i in range(len(q))]
    kl_qm = sum([u for u in kl_qm if not np.isnan(u)])
    kl = kl_pm/2 + kl_qm/2
    return kl

def calculate_monthly_jsd(matrix):
    jsds = []
    for i in range(matrix.shape[0]):
        for j in range(i+1, matrix.shape[0]):
            jsds.append(calculate_pairwise_jsd(matrix[i], matrix[j]))
    return jsds

def bootstrap_resample(jsd_list):
    ave_original = np.average(jsd_list)
    aves = []
    for i in range(10000):
        sample = []
        for i in range(len(jsd_list)):
            sample.append(random.choice(jsd_list))
        aves.append(np.average(sample))
    tail = sorted(aves)[249]
    head = sorted(aves)[9750]
    return (ave_original, tail, head)

def create_df_time(df, time):
    return df[df.PublishDate.str[:7] == time]

def calculate_overall_jsd():
    jsds_timerange = []
    work_count = []
    for month in timelist:
        df_ts = create_df_time(data, month)

        text = preprocess(df_ts)
        text = filter_length(text, 500)

        work_count.append(len(text))

        text = filter_top_words(text, 1000)
        matrix = calculate_prob_matrix(text)
        monthly_jsds = calculate_monthly_jsd(matrix)
        monthly_ave_resampled_jsds = bootstrap_resample(monthly_jsds)
        jsds_timerange.append(monthly_ave_resampled_jsds)
        print "Finished calculation for: ", month, 'jsd = ', monthly_ave_resampled_jsds
    return jsds_timerange, work_count


timelist = data.PublishDate.drop_duplicates().tolist()
timelist = [str(i)[:7] for i in timelist]
timelist = sorted(list(set(timelist)))[3:]

jsds_timerange, work_count= calculate_overall_jsd()
print jsds_timerange


