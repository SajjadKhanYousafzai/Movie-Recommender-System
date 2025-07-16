# Import libraries
import os
import pickle
import streamlit as st
import requests
import pandas as pd

# Set page configuration for wide layout and custom title
st.set_page_config(
    page_title="🎥 CineMatch: Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cinematic styling
st.markdown("""
<style>
    body {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .stApp {
        background: linear-gradient(to bottom, #2c3e50, #1a1a1a);
        font-family: 'Arial', sans-serif;
    }
    .main-header {
        font-size: 3.5em;
        color: #e50914;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.5em;
        color: #ffffff;
        text-align: center;
        margin-bottom: 30px;
    }
    .movie-card {
        background-color: #2c2c2c;
        border-radius: 10px;
        padding: 10px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(229, 9, 20, 0.5);
    }
    .movie-title {
        font-size: 1.2em;
        color: #e50914;
        text-align: center;
        margin-top: 10px;
    }
    .stButton>button {
        background-color: #e50914;
        color: white;
        border-radius: 25px;
        padding: 10px 20px;
        font-size: 1.2em;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff3333;
    }
    .stSelectbox {
        background-color: #2c2c2c;
        border-radius: 10px;
        padding: 10px;
    }
    .footer {
        text-align: center;
        color: #888;
        margin-top: 50px;
        font-size: 0.9em;
    }
    .loading-spinner {
        text-align: center;
        font-size: 1.5em;
        color: #e50914;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to fetch movie posters and details from TMDB API
def fetch_movie_data(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path', None)
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750.png?text=No+Image"
    overview = data.get('overview', 'No description available.')
    rating = data.get('vote_average', 'N/A')
    return full_path, overview, rating

# Function to recommend movies
def recommend(movie, sort_by='similarity'):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_overviews = []
    recommended_movie_ratings = []
    recommended_movie_similarities = []
    for i in distances[1:6]:  # Top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        poster, overview, rating = fetch_movie_data(movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(poster)
        recommended_movie_overviews.append(overview)
        recommended_movie_ratings.append(rating)
        recommended_movie_similarities.append(i[1])
    
    # Create DataFrame for sorting
    recommendations_df = pd.DataFrame({
        'name': recommended_movie_names,
        'poster': recommended_movie_posters,
        'overview': recommended_movie_overviews,
        'rating': recommended_movie_ratings,
        'similarity': recommended_movie_similarities
    })
    
    # Sort based on user preference
    if sort_by == 'rating':
        recommendations_df = recommendations_df.sort_values(by='rating', ascending=False)
    elif sort_by == 'name':
        recommendations_df = recommendations_df.sort_values(by='name')
    
    return (recommendations_df['name'].tolist(),
            recommendations_df['poster'].tolist(),
            recommendations_df['overview'].tolist(),
            recommendations_df['rating'].tolist())

# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Load pickled files
movies_path = 'movie_list.pkl'
similarity_path = 'similarity.pkl'

# Check file existence
print("Movies file exists:", os.path.exists(movies_path))
print("Similarity file exists:", os.path.exists(similarity_path))

try:
    movies = pickle.load(open(movies_path, 'rb'))
    similarity = pickle.load(open(similarity_path, 'rb'))
except FileNotFoundError as e:
    st.error(f"Error: File not found - {e}. Please ensure the model files are in the correct directory.")
    st.stop()

# Main app header
st.markdown('<div class="main-header">🎥 CineMatch: Movie Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Discover movies tailored to your taste!</div>', unsafe_allow_html=True)

# Sidebar for additional options
with st.sidebar:
    st.header("⚙️ Settings")
    sort_option = st.selectbox(
        "Sort recommendations by:",
        ["Similarity", "Rating", "Name"],
        index=0
    )
    sort_by = {'Similarity': 'similarity', 'Rating': 'rating', 'Name': 'name'}[sort_option]
    st.markdown("---")
    st.markdown("**About CineMatch**")
    st.write("CineMatch uses machine learning to recommend movies based on content similarity. Powered by TMDB API.")
    st.markdown("---")
    st.markdown("**API Key**: 8265bd1679663a7ea12ac168da84d2e8")

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🎬 Type or select a movie",
    movie_list,
    placeholder="Choose a movie...",
    help="Select a movie to get personalized recommendations."
)

# Recommendation button
if st.button('🍿 Get Recommendations', use_container_width=True):
    with st.spinner('Fetching recommendations...'):
        try:
            recommended_movie_names, recommended_movie_posters, recommended_movie_overviews, recommended_movie_ratings = recommend(selected_movie, sort_by)
            
            # Display selected movie details
            st.markdown(f"### You selected: {selected_movie}")
            selected_movie_id = movies[movies['title'] == selected_movie]['movie_id'].iloc[0]
            selected_poster, selected_overview, selected_rating = fetch_movie_data(selected_movie_id)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(selected_poster, use_container_width=True)
            with col2:
                st.write(f"**Rating**: {selected_rating}/10")
                st.write(f"**Overview**: {selected_overview}")
            
            st.markdown("---")
            st.markdown("### Recommended Movies")
            
            # Display recommendations in a grid
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    st.image(recommended_movie_posters[idx], use_container_width=True)
                    st.markdown(f'<div class="movie-title">{recommended_movie_names[idx]}</div>', unsafe_allow_html=True)
                    st.caption(f"Rating: {recommended_movie_ratings[idx]}/10")
                    with st.expander("Details"):
                        st.write(recommended_movie_overviews[idx])
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.success("Recommendations loaded successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown('<div class="footer">Made with ❤️ by CineMatch Team | Powered by Streamlit & TMDB API | © 2025</div>', unsafe_allow_html=True)
