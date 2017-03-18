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
from sklearn.feature_extraction.text import TfidfVectorizer

start = time.time()

hackathons = pd.read_json("scrapers/projects.json", encoding='utf-8')

text_corpus = []
for each in hackathons['project_description']:
    words = re.sub("[^a-zA-Z]", " ", each)
    words = words.lower().split()
    text_corpus.append(words)
    

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

stemmer = PorterStemmer()
def to_words(content):
    letters_only = re.sub("[^a-zA-Z]", " ", content)
    words = letters_only.lower().split()
    stops = set(stopwords.words("english"))
    meaningful_words = [w for w in words if not w in stops]
    array = []
    array.append(" ".join(meaningful_words))
    return array 

'''def text_preprocessing(description):
    description = re.sub("[^a-zA-Z.,]", " ", description)
    for project in range(len(description)):
        tokens = nltk.word_tokenize(description)
        singles = [stemmer.stem(token) for token in tokens]
        singles = ' '.join(singles)
        #description[project] = ''.join(singles)
    array = []
    array.append(singles)
    return array'''

def extractKeywords(description):
    #processed_text = text_preprocessing(description)
    #print ("Processed text: " + processed_text)
    vectorizer = TfidfVectorizer(analyzer='word')
    result = vectorizer.fit_transform(description)

    feature_array = np.array(vectorizer.get_feature_names())
    tfidf_sorting = np.argsort(result.toarray()).flatten()[::-1]

    n = 20

    top_keywords = feature_array[tfidf_sorting][:n]
    print (top_keywords)
    return top_keywords 

def keywords(row):
    try:
        return ','.join(extractKeywords(to_words(row['project_description'])))
    except:
        pass

hackathons['keywords'] = hackathons.apply(keywords, axis=1)     
hackathons.reset_index().to_json('data.json', orient='records')

end = time.time() - start

print (str(end)+" seconds")