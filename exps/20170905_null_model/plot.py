import pickle
import matplotlib.pyplot as plt

di = pickle.load( open( "null_model_tfidf_allave.pkl", "rb" ) )	
label = sorted(di.keys())
x = [i for i in range(0, len(label))]
y = [di[k] for k in label]

plt.figure(figsize = (10, 7))
plt.plot(x, y)
plt.xticks(x, label,  rotation=70)
plt.xlabel("Random text length")
plt.ylabel("Average cosine similarity of 100 samples")
plt.ylim(0,1)
plt.tight_layout()
plt.savefig("null_model_tfidf_allave.png", format = "png")