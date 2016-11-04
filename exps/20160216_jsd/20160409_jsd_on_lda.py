import numpy as np
import pandas as pd
import re
from collections import Counter
from scipy import special
# import matplotlib.pyplot as plt
# %matplotlib inline
import random

# In[20]:

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# In[21]:

def read_gamma(month):
    with open('../20160225_lda/lda_topic40_%s' %month, 'r') as f:
        gamma = f.readlines()
        for i in range(len(gamma)):
            gamma[i] = gamma[i].replace(')','').replace(']','').strip()
            gamma[i] = [float(v.strip()) for v in gamma[i].split(',') if is_number(v.strip())]
    return np.asarray(gamma)


# In[24]:

def JSD(P, Q):
    M = 0.5 * (P + Q)
    return 0.5 * (sum(special.rel_entr(P, M)) + sum(special.rel_entr(Q, M)))


# In[25]:

def calculate_monthly_jsd(matrix):
    jsds = []
    for i in range(matrix.shape[0]):
        for j in range(i+1, matrix.shape[0]):
            jsds.append(JSD(matrix[i], matrix[j]))
    return jsds


# In[26]:

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


# In[27]:

timelist = [i.strip() for i in open('../timelist', 'r')]

for month in timelist[timelist.index("2014-03"):]:

    gamma = read_gamma(month)
    monthly_jsds = calculate_monthly_jsd(gamma)
    monthly_ave_resampled_jsds = bootstrap_resample(monthly_jsds)

    with open('jsd_on_lda_new_data.txt', 'a') as g:
        g.write(str(month) + '\t' + str(monthly_ave_resampled_jsds))
        g.write('\n')

# In[6]:

# y = [i[0] for i in jsds_timerange]
# x = range(len(y))

# # example error bar values that vary with x-position
# # error = 0.1 + 0.2 * x

# # error bar values w/ different -/+ errors
# lower_error = [i[0]-i[1] for i in jsds_timerange]
# upper_error = [i[2]-i[0] for i in jsds_timerange]
# asymmetric_error = [lower_error, upper_error]

# fig, ax = plt.subplots(figsize = (10, 7))

# ax.errorbar(x, y, yerr=asymmetric_error,marker='o')
# ax.set_title('Average pairwise jsd of topic disribution over time range (40 topics)')
# # ax.set_yscale('log')
# # ax.set_ylim([0.180, 0.225])
# plt.grid()
# plt.show()


# In[ ]:


