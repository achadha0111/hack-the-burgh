import pandas as pd
import numpy as np
import gensim.models.word2vec as w2v
import multiprocessing
import os
import re
import pprint
import sklearn.manifold
import matplotlib.pyplot as plt
import time
import json

start = time.time()

hackathons = pd.read_json("scrapers/projects.json", encoding='utf-8')

text_corpus = []
for each in hackathons['project_description']:
    words = re.sub("[^a-zA-Z]", " ", each)
    words = words.lower().split()
    text_corpus.append(words)
    
num_features = 100
min_word_count = 1
num_workers = multiprocessing.cpu_count()
context_size = 7
downsampling = 1e-3
seed = 3

hack2vec = w2v.Word2Vec(
    sg=1,
    seed=seed,
    workers=num_workers,
    size=num_features,
    min_count=min_word_count,
    window=context_size,
    sample=downsampling
)

hack2vec.build_vocab(text_corpus)
#print ("Vocab size: " + str(len(hack2vec.vocab)))

hack2vec.train(text_corpus)
if not os.path.exists("trained"):
    os.makedirs("trained")
hack2vec.save(os.path.join("trained", "hack2vec.w2v"))

hacks2vec = w2v.Word2Vec.load(os.path.join("trained", "hack2vec.w2v"))

import sklearn
def hackVector(row):
    vector_sum = 0
    words = re.sub("[^a-zA-Z]", " ", row).lower().split()
    for word in words:
        vector_sum = vector_sum + hack2vec[word]
        vector_sum = vector_sum.reshape(1, -1)
        normalised_vector_sum = sklearn.preprocessing.normalize(vector_sum)
        return normalised_vector_sum
hackathons['hack_vector'] = hackathons['project_description'].apply(hackVector)

end = time.time() - start

print (str(end)+" seconds")