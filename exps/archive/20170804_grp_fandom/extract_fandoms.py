
# coding: utf-8

# In[1]:

import pandas as pd
import os


# In[2]:

data_path = '../../data/metadata/'


# In[167]:

output_path = 'fandoms_rearranged'


# In[210]:

files = os.listdir(data_path)


# In[213]:

for file in files:
    with open (os.path.join(data_path, file), 'r') as f:
        content = f.readlines()
    content = [line.split('\t') for line in content]

    for i in range(1,len(content)):
        for fandom in eval(content[i][10]):
            fname = fandom.replace(' ', '_').replace('/', '_') + '.tsv'
            if fname in os.listdir(output_path):
                with open(os.path.join(output_path, fname), 'a') as g:
                    g.write('\t'.join([field for field in content[i]]))
                    g.write('\n')
            else:
                with open(os.path.join(output_path, fname), 'a') as g:
                    g.write('\t'.join([field for field in content[0]]))
                    g.write('\t'.join([field for field in content[i]]))
                    g.write('\n')


