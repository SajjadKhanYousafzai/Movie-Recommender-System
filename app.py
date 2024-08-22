import pickle
import pandas as pd
import streamlit as st

def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]  # Find the index of the selected movie using pandas
    print(f"Movie Index: {movie_index}")  # Debugging: Check if movie_index is valid
    
    # Print shape of similarity matrix
    print(f"Similarity Matrix Shape: {similarity.shape}")  # Debugging: Check the shape of the similarity matrix
    
    distances = similarity[movie_index]  # Use square brackets to index the similarity matrix
    print(f"Distances: {distances}")  # Debugging: Check if distances are correctly extracted
    
    movies_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # Get top 5 recommendations

    recommend_movies = []
    for i in movies_indices:
        recommend_movies.append(movies_list.iloc[i[0]]['title'])  # Use .iloc to access the movie title by index
    return recommend_movies

# Load the movies list and similarity matrix
movies_list = pickle.load(open("movies.pkl", "rb"))
movies_list = pd.DataFrame(movies_list)  # Ensure movies_list is a DataFrame

similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit application
st.title("Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie you like:",
    movies_list["title"].values  # Extract the titles from the DataFrame for selection
)

if st.button("Recommend"):
    recommendation = recommend(selected_movie)
    for i in recommendation:
        st.write(i)
