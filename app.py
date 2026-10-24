"""
FilmAura — Main Application Entrypoint
Integrates Google Stitch UI Design with Machine Learning Essentials Recommender.
"""

import sys
import os
import streamlit as st

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from src.styles import get_custom_css
from src.components import render_top_nav
from src.data_loader import ensure_artifacts_exist
from src.recommender import FilmAuraRecommender
from src.views.landing import render_landing_view
from src.views.onboarding_mood import render_mood_onboarding_view
from src.views.onboarding_taste import render_taste_calibration_view
from src.views.results import render_results_view
from src.views.movie_detail import render_movie_detail_view
from src.views.watchlist_view import render_watchlist_view
from src.views.about_view import render_about_view

# Streamlit Page Config
st.set_page_config(
    page_title="FilmAura — ML-Powered Cinema Discovery",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Nocturne Cinema Theme CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "selected_moods" not in st.session_state:
    st.session_state.selected_moods = ["Dark", "Suspenseful"]
if "selected_genres" not in st.session_state:
    st.session_state.selected_genres = ["Sci-Fi", "Thriller"]
if "anchor_movie_ids" not in st.session_state:
    st.session_state.anchor_movie_ids = ["blade-runner-2049-2017"]
if "watchlist" not in st.session_state:
    st.session_state.watchlist = ["children-of-men-2006"]
if "watched_list" not in st.session_state:
    st.session_state.watched_list = []
if "active_movie_id" not in st.session_state:
    st.session_state.active_movie_id = "children-of-men-2006"
if "hybrid_blend" not in st.session_state:
    st.session_state.hybrid_blend = 70

# Load Recommender with Resource Caching
@st.cache_resource
def load_recommender() -> FilmAuraRecommender:
    ensure_artifacts_exist()
    return FilmAuraRecommender()

try:
    recommender = load_recommender()
except Exception as e:
    st.error(f"⚠️ Error initializing FilmAura Recommender Engine: {e}")
    st.info("Please verify Python dependencies and run artifacts generation.")
    st.stop()

# Render Top Navigation Bar
current_page = st.session_state.get("page", "landing")
watchlist_count = len(st.session_state.get("watchlist", []))
render_top_nav(active_page=current_page, watchlist_count=watchlist_count)

# Navigation Router
if current_page == "landing":
    render_landing_view()
elif current_page == "onboarding_mood":
    render_mood_onboarding_view()
elif current_page == "onboarding_taste":
    render_taste_calibration_view()
elif current_page == "results":
    render_results_view(recommender)
elif current_page == "detail":
    active_id = st.session_state.get("active_movie_id", "children-of-men-2006")
    render_movie_detail_view(recommender, active_id)
elif current_page == "watchlist":
    render_watchlist_view(recommender)
elif current_page == "methodology":
    render_about_view()
else:
    render_landing_view()
