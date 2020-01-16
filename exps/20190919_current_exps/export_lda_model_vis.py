
from gensim import corpora, models, similarities
import pyLDAvis
import pyLDAvis.gensim
import pickle

model = models.LdaMulticore.load('model')
id2word = pickle.load(open('id2word.p', 'rb'))
corpus = pickle.load(open('corpus.p', 'rb'))
vis = pyLDAvis.gensim.prepare(model, corpus, id2word)
pyLDAvis.save_html(vis, 'lda_vis.html')