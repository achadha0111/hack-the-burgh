import numpy as np
#import nltk 
#from nltk.corpus import stopwords
#from nltk.stem.porter import *
import re 
import json
import gensim.models.word2vec as w2v
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import sklearn.manifold
import multiprocessing

df = pd.read_json("scrapers/projects.json")
df.head()

text_corpus = []
for project in df['project_description']:
    words = re.sub("[^a-zA-Z]", " ", project).lower().split()
    text_corpus.append(words)


num_features = 100

min_word_count = 1

num_workers = multiprocessing.cpu_count()

# Context window length.
context_size = 7

# Downsample setting for frequent words.
#0 - 1e-5 is good for this
downsampling = 1e-3

# Seed for the RNG, to make the results reproducible.
#random number generator
#deterministic, good for debugging
seed = 2

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
print ("Number of unique words " + str(len(hack2vec.wv.vocab)))

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
        vector_sum = vector_sum + hacks2vec[word]
    vector_sum = vector_sum.reshape(1, -1)
    normalised_vector_sum = sklearn.preprocessing.normalize(vector_sum)
    return normalised_vector_sum

df['hack_vector'] = df['project_description'].apply(hackVector)
df.reset_index().to_json("database.json",orient="records")