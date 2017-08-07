# import csv

with open('hamilton_miranda_unigram_dist.tsv') as f:
	text = f.readlines()
for i in range(1, 10):
	print(len(set(text[i])))