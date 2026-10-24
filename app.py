"""
FilmAura — Streamlit Application
A student-built personalized movie recommendation system.
Tagline: Your mood. Your taste. Your next movie.
"""

import streamlit as st
from recommender import FilmAuraRecommender

# Page Configuration
st.set_page_config(
    page_title="FilmAura — Personalized Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

# Application Header
st.title("🎬 FilmAura")
st.markdown("#### *Your mood. Your taste. Your next movie.*")
st.markdown(
    "Welcome to **FilmAura**, an intelligent movie recommender system built for the "
    "**Machine Learning Essentials** course. Select your current mood and preferred genre, "
    "and optionally pick a favorite anchor movie to receive personalized, explainable recommendations."
)
st.divider()

# Load Recommender Engine with caching
@st.cache_resource
def get_recommender():
    try:
        return FilmAuraRecommender(), None
    except FileNotFoundError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Unexpected error loading model artifacts: {e}"

recommender, error_msg = get_recommender()

# Check if model artifacts exist
if error_msg:
    st.error("⚠️ **Model Artifacts Not Found**")
    st.info(
        "The recommendation model has not been trained or exported yet.\n\n"
        "**To generate artifacts:**\n"
        "1. Open `notebooks/FilmAura_ML_Backend.ipynb` in Google Colab or Kaggle.\n"
        "2. Run all cells to train the hybrid recommender on MovieLens.\n"
        "3. Download the exported files from the `artifacts/` folder into your local `artifacts/` directory.\n\n"
        f"*Details: {error_msg}*"
    )
    st.stop()

# User Input Controls
st.subheader("1. What are you in the mood for?")

col1, col2 = st.columns(2)
with col1:
    moods = recommender.get_available_moods()
    selected_mood = st.selectbox(
        "Select your current mood:",
        options=moods,
        index=moods.index("Dark") if "Dark" in moods else 0,
        help="Affective mood spectrum guiding the recommendation resonance."
    )

with col2:
    genres = ["All Genres"] + recommender.get_available_genres()
    selected_genre = st.selectbox(
        "Select preferred genre:",
        options=genres,
        index=genres.index("Sci-Fi") if "Sci-Fi" in genres else 0,
        help="Filters recommendations to include your chosen genre."
    )

st.subheader("2. (Optional) Anchor with a film you cherish")
movies = recommender.get_movie_titles()
movie_options = ["None (Recommend based purely on mood & genre)"] + [m["title"] for m in movies]
selected_movie_title = st.selectbox(
    "Pick a favorite movie to match visual and narrative tone:",
    options=movie_options,
    index=0,
    help="When chosen, the model computes content and collaborative similarity to this seed film."
)

favorite_movie_id = None
if selected_movie_title != "None (Recommend based purely on mood & genre)":
    for m in movies:
        if m["title"] == selected_movie_title:
            favorite_movie_id = m["movieId"]
            break

col_top_k, col_btn = st.columns([1, 2])
with col_top_k:
    top_k = st.slider("Results to show:", min_value=3, max_value=10, value=5)

with col_btn:
    st.write("") # Spacing
    st.write("")
    recommend_clicked = st.button("✨ Recommend Movies", type="primary", use_container_width=True)

st.divider()

# Handle Recommendation Query
if recommend_clicked or "has_run" in st.session_state:
    st.session_state.has_run = True
    
    with st.spinner("Analyzing ratings, content vectors, and mood resonance..."):
        recommendations = recommender.recommend(
            mood=selected_mood,
            genre=selected_genre if selected_genre != "All Genres" else None,
            favorite_movie_id=favorite_movie_id,
            top_k=top_k
        )

    if not recommendations:
        st.warning("No movies matched all chosen criteria. Try picking 'All Genres' or choosing a different mood.")
    else:
        st.subheader(f"Top {len(recommendations)} FilmAura Recommendations")
        
        for i, film in enumerate(recommendations, 1):
            with st.container(border=True):
                c_title, c_score = st.columns([4, 1])
                with c_title:
                    st.markdown(f"### {i}. {film['title']} ({film['year']})")
                with c_score:
                    st.markdown(f"**{film['match_pct']}% Match**")

                genres_str = " • ".join(film["genres"])
                st.caption(f"🎭 **Genres:** {genres_str} &nbsp;|&nbsp; ⭐ **Rating:** {film['rating']} / 5.0 ({film['votes']:,} votes)")
                
                st.markdown(f"💡 **Why this movie?** {film['explanation']}")

# Footer
st.markdown("---")
st.caption("FilmAura • Machine Learning Essentials (MLE) Course Project • Built with Python & Streamlit")
