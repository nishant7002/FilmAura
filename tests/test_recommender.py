"""
Unit tests for FilmAura Recommender Engine.
"""

import sys
import os
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender import FilmAuraRecommender
from src.data_loader import get_movies_dataframe

@pytest.fixture
def recommender():
    return FilmAuraRecommender()

def test_dataframe_loaded(recommender):
    df = recommender.df
    assert not df.empty
    assert "title" in df.columns
    assert "genres" in df.columns
    assert "moods" in df.columns
    assert len(df) >= 10

def test_tfidf_cosine_similarity(recommender):
    assert recommender.tfidf_matrix is not None
    assert recommender.cosine_sim.shape == (len(recommender.df), len(recommender.df))
    # Self similarity should be 1.0 (or very close)
    for i in range(len(recommender.df)):
        assert abs(recommender.cosine_sim[i, i] - 1.0) < 1e-4

def test_recommendations_structure(recommender):
    recs = recommender.recommend(
        primary_mood="Dark",
        secondary_mood="Suspenseful",
        anchor_movie_ids=["blade-runner-2049-2017"],
        top_n=5
    )
    assert len(recs) > 0
    assert len(recs) <= 5
    for r in recs:
        assert "id" in r
        assert "title" in r
        assert "aura_match_pct" in r
        assert "rationale" in r
        assert "breakdown" in r
        assert 80 <= r["aura_match_pct"] <= 100
        # Seed movie should not recommend itself
        assert r["id"] != "blade-runner-2049-2017"

def test_genre_filtering(recommender):
    recs = recommender.recommend(
        primary_mood="Dark",
        selected_genres=["War"],
        top_n=5
    )
    for r in recs:
        assert "War" in r["genres"]

def test_runtime_filtering(recommender):
    recs = recommender.recommend(
        primary_mood="Dark",
        filter_under_2h=True,
        top_n=5
    )
    for r in recs:
        assert r["runtime"] <= 120

def test_sorting_by_rating(recommender):
    recs = recommender.recommend(
        sort_by="Highest Rating",
        top_n=5
    )
    ratings = [r["rating"] for r in recs]
    assert ratings == sorted(ratings, reverse=True)

def test_get_movie_by_id(recommender):
    movie = recommender.get_movie_by_id("children-of-men-2006")
    assert movie is not None
    assert movie["title"] == "Children of Men"
    assert movie["director"] == "Alfonso Cuarón"

def test_get_invalid_movie_by_id(recommender):
    movie = recommender.get_movie_by_id("non-existent-id-9999")
    assert movie is None
