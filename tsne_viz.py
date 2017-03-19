import pandas as pd
import numpy as np
import sklearn.manifold
hackathon_vectors = pd.read_json('database.json')
hack_vectors = []

for hackathon_vector in hackathon_vectors['hack_vector']:
    hack_vectors.append(hackathon_vector)
    
X = np.array(hack_vectors).reshape(1131, 100)
tsne = sklearn.manifold.TSNE(n_components=2, n_iter=500, random_state=0, verbose=2)
all_word_vectors_matrix_2d = tsne.fit_transform(X)
df=pd.DataFrame(all_word_vectors_matrix_2d,columns=['X','Y'])
df.head(10)

df.reset_index(drop=True, inplace=True)
hackathon_vectors.reset_index(drop=True, inplace=True)

two_dimensional_hackathons = pd.concat([hackathon_vectors, df], axis=1)

two_dimensional_hackathons.to_csv('tsneviz.csv')