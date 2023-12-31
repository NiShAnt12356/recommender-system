import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3fb485ff2b616296258d8df602d625f2'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title_x'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) , reverse=True , key = lambda x:x[1])[1:6]
    
    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movies_id = movies.iloc[i[0]].id
        
        recommend_movies.append(movies.iloc[i[0]].title_x)
        #fetch posters from API
        recommend_movies_posters.append(fetch_poster(movies_id))
    return recommend_movies,recommend_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl' , 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title_x'].values)


if st.button("Recommend"):
    names , posters = recommend(selected_movie_name)
    
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        st.text(names[0])
        st.image(posters[0])
    with c2:
        st.text(names[1])
        st.image(posters[1])
    with c3:
        st.text(names[2])
        st.image(posters[2])
    with c4:
        st.text(names[3])
        st.image(posters[3])
    with c5:
        st.text(names[4])
        st.image(posters[4])