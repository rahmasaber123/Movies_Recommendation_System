import streamlit as st
import pickle
import pandas as pd
import requests

# ================= Styling =================
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0F0529;
        color: #ffffff;
    }
    /* Title styling with purple hover glow */
    h1 {
        font-size: 42px !important;
        color: #f3ccff !important;
        text-align: center;
        font-weight: 900 !important;
        transition: all 0.3s ease-in-out;
    }
    h1:hover {
        color: #d580ff !important;
        text-shadow: 0 0 10px #d580ff,
                     0 0 20px #b84dff,
                     0 0 40px #8000ff,
                     0 0 80px #cc66ff;
        transform: scale(1.05);
    }
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #6a0dad, #a64dff);
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #a64dff, #6a0dad);
        transform: scale(1.05);
        transition: 0.2s ease-in-out;
    }
    /* Movie poster cards */
    .stImage img {
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.6);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stImage img:hover {
        transform: scale(1.08);
        box-shadow: 0px 6px 25px rgba(166,77,255,0.9);
    }
    /* Movie titles */
    .movie-title {
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        color: #e0b3ff;
        transition: 0.3s;
    }
    .movie-title:hover {
        color: #ffffff;
        text-shadow: 0 0 5px #a64dff, 0 0 10px #d580ff;
    }
    </style>
""", unsafe_allow_html=True)

# ================= Functions =================
def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=0e85d2ff4d5a7ca71e7148ef6012eb00&language=en-US"
    )
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return ""

def recommend(movie):
    # get index of the selected movie
    movie_index = movies[movies['title'] == movie].index[0]

    # fetch only the Top-K neighbors (already stored as indices)
    neighbors = similarity[movie_index]

    recommended_movie = []
    recommended_movie_poster = []

    # take top 5 neighbors
    for i in neighbors[:5]:
        movie_id = movies.iloc[i].movie_id
        recommended_movie.append(movies.iloc[i].title)
        recommended_movie_poster.append(fetch_poster(movie_id))

    return recommended_movie, recommended_movie_poster

# ================= Data =================
movie_data = pickle.load(open("movie_dict.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))  # expected as dict or list of lists
movies = pd.DataFrame(movie_data)

# ================= UI =================
st.title(' Movie Recommender System 🎬')

# Add a placeholder option
movie_list = ["-- Select a movie --"] + list(movies['title'].values)
selected_movie_name = st.selectbox("🎥 Select your Movie", movie_list)

if st.button(" Recommend A Movie"):
    if selected_movie_name != "-- Select a movie --":  # prevent running on placeholder
        names, posters = recommend(selected_movie_name)

        cols = st.columns(min(len(names), 5))
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.markdown(f"<p class='movie-title'>{name}</p>", unsafe_allow_html=True)
                if poster:
                    st.image(poster)
    else:
        st.warning("⚠️ Please select a movie before getting recommendations.")





