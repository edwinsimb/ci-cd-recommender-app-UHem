import numpy as np
import pandas as pd
import ast

movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

movies = movies.merge(credits, on='title')
movies.dropna(inplace=True)

movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter += 1

    return L

movies['cast'] = movies['cast'].apply(convert3)

movies['cast'] = movies['cast'].apply(lambda x: x[0:3])

def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L

movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x: x.split())

def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(' ', ''))
    
    return L1

movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new = movies.drop(columns=['overview', 'genres', 'keywords', 'cast', 'crew'])

new['tags'] = new['tags'].apply(lambda x: ''.join(x))







from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cv = CountVectorizer(max_features=500, stop_words='english')

vector = cv.fit_transform(new['tags']).toarray()

similarity = cosine_similarity(vector)

def recommend(movie):
    index = new[new['title'] == movie].index[0]

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    for i in distances[1:6]:
        print(new.iloc[i[0]].title)





import pickle

pickle.dump(new, open('app/movie_list.pkl', 'wb'))
pickle.dump(similarity, open('app/similarity.pkl', 'wb'))