# import os
# import pickle
# import pandas as pd
# import streamlit as st

# # Set file paths
# movies_file_path = "D:/Machine Learning Projects/Movie Recommender System/movies.pkl"
# similarity_file_path = "D:/Machine Learning Projects/Movie Recommender System/similarity.pkl"

# # Check if the necessary files exist
# if not os.path.exists(movies_file_path):
#     st.error("movies.pkl file does not exist.")
#     st.stop()  # Stop the app if the file doesn't exist

# if not os.path.exists(similarity_file_path):
#     st.error("similarity.pkl file does not exist.")
#     st.stop()  # Stop the app if the file doesn't exist

# # Load the movies list and similarity matrix
# try:
#     movies_list = pickle.load(open(movies_file_path, "rb"))
#     if not isinstance(movies_list, pd.DataFrame):
#         movies_list = pd.DataFrame(movies_list)  # Ensure movies_list is a DataFrame
# except Exception as e:
#     st.error(f"Error loading movies.pkl: {e}")
#     st.stop()  # Stop the app if there’s an error loading

# try:
#     similarity = pickle.load(open(similarity_file_path, "rb"))
# except Exception as e:
#     st.error(f"Error loading similarity.pkl: {e}")
#     st.stop()  # Stop the app if there’s an error loading

# # Define the recommendation function
# def recommend(movie):
#     movie_index = movies_list[movies_list['title'] == movie].index[0]  # Find the index of the selected movie
#     distances = similarity[movie_index]
#     movies_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     recommend_movies = []
#     for i in movies_indices:
#         recommend_movies.append(movies_list.iloc[i[0]]['title'])
#     return recommend_movies

# # Streamlit application
# st.title("Movie Recommender System")

# selected_movie = st.selectbox(
#     "Select a movie you like:",
#     movies_list["title"].values
# )

# if st.button("Recommend"):
#     recommendation = recommend(selected_movie)
#     for i in recommendation:
#         st.write(i)
import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])