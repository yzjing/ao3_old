
# coding: utf-8

# In[5]:


import matplotlib.pyplot as plt
import pickle
import numpy as np

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)


fig, ax = plt.subplots(1,2,figsize = (15,6))

idx = np.arange(24)

data = pickle.load(open('data.p', 'rb'))
labels = pickle.load(open('labels.p', 'rb'))
ax[0].barh(idx, data)
ax[0].set_yticks(range(0,24))
ax[0].set_yticklabels(labels)

for tick in ax[0].yaxis.get_major_ticks():
    tick.label.set_fontsize(13)
    tick.label.set_horizontalalignment('right')
    
# find the maximum width of the label on the major ticks
# yax = ax[0].get_yaxis()
# yax.set_tick_params(pad=pad)

# for tick in ax[0].xaxis.get_major_ticks():
#     tick.label.set_fontsize(13)
    
ax[0].set_ylim(-0.5, 23.5)
ax[0].set_ylabel("Fandom", fontsize = 15)
ax[0].set_xlabel("Number of fanfictions", fontsize = 15)
ax[0].set_title('(a): Size of Fandoms', fontsize = 15)


# time_labels_f =[l for l in time_labels if time_labels.index(l)%5==0]
# ax[1].scatter(0, agg)
# ax[1].plot(x, y)
# ax[1].set_xticks(np.arange(0, len(time_labels), 5))
# ax[1].set_xticklabels(time_labels_f)
# for tick in ax[1].xaxis.get_major_ticks():
#     tick.label.set_fontsize(13)
#     tick.label.set_rotation(90)
# for tick in ax[1].yaxis.get_major_ticks():
#     tick.label.set_fontsize(13)

# ax[1].set_xlabel("Time", fontsize=15)
# ax[1].set_ylabel("Number of fanfictions published",fontsize=15)
# ax[1].set_title('(b): Volume of Fanfictions', fontsize = 15)

# ax[1].text(0.08, 0.4, "Pre-2009", fontsize=14, transform=ax[1].transAxes)
# # plt.xlim(-1,90)
# # start_idx = labels.index('2010-01')
# # end_idx = labels.index('2016-05')

plt.tight_layout()

plt.savefig("fic_time_fandom_size_dist.pdf", format="pdf")


