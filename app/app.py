import os
import pickle
import streamlit as st
import altair
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id)

    data =  requests.get(url)

    data = data.json()

    poster_path = data['poster_path']

    full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path

    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(list(enumerate(simitarity[index])), reverse=True, key=lambda x: x[1])

    recommend_movies_names = []
    recommend_movies_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id

        recommend_movies_posters.append(fetch_poster(movie_id))

        recommend_movies_names.append(movies.iloc[i[0]].title)

    return recommend_movies_names, recommend_movies_posters



st.header('Sistema de recomendación')
movies = pd.read_pickle('data/movie_list.pkl')
simitarity = pd.read_pickle('data/similarity.pkl')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Selecciona una película de Ia lista",
    movie_list
)

import streamlit as st
if st.button('Mostrar Recomendaciones'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    cols = st.columns(5) 
    for i, col in enumerate(cols):
        col.text(recommended_movie_names[i])
        col.image(recommended_movie_posters[i])