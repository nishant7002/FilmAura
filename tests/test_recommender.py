"""
Essential Unit Tests for FilmAura Recommender Engine.
Validates artifact loading, top-K ranking, mood/genre filtering, and error handling.
"""

import sys
import os
from pathlib import Path
import pytest

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from recommender import FilmAuraRecommender

@pytest.fixture
def recommender():
    return FilmAuraRecommender()

def test_artifacts_loaded(recommender):
    """Verify catalogue and TF-IDF matrices are properly loaded."""
    assert recommender.is_loaded
    assert recommender.catalogue is not None
    assert len(recommender.catalogue) >= 10
    assert "display_title" in recommender.catalogue.columns
    assert "genres_list" in recommender.catalogue.columns

def test_get_available_genres(recommender):
    """Verify available genres are extracted and non-empty."""
    genres = recommender.get_available_genres()
    assert isinstance(genres, list)
    assert len(genres) > 0
    assert "Drama" in genres or "Sci-Fi" in genres or "Action" in genres

def test_get_available_moods(recommender):
    """Verify all 10 documented moods are available."""
    moods = recommender.get_available_moods()
    assert len(moods) == 10
    assert "Happy" in moods
    assert "Dark" in moods
    assert "Suspenseful" in moods

def test_recommend_cold_start(recommender):
    """Verify recommendations work when no seed film is provided (cold start)."""
    recs = recommender.recommend(mood="Happy", genre="Animation", favorite_movie_id=None, top_k=5)
    assert len(recs) <= 5
    for r in recs:
        assert "title" in r
        assert "year" in r
        assert "genres" in r
        assert "rating" in r
        assert "match_pct" in r
        assert "explanation" in r
        assert 80 <= r["match_pct"] <= 100
        # If genre filter active, verify genre match
        assert "Animation" in r["genres"]

def test_recommend_with_seed_movie(recommender):
    """Verify recommendations when a favorite seed movie is chosen."""
    # Pick first movie as seed
    sample_mid = int(recommender.catalogue.iloc[0]["movieId"])
    sample_title = recommender.catalogue.iloc[0]["display_title"]

    recs = recommender.recommend(mood="Dark", favorite_movie_id=sample_mid, top_k=5)
    assert len(recs) <= 5
    for r in recs:
        # Seed film should never recommend itself
        assert r["movieId"] != sample_mid
        assert r["title"] != sample_title
        assert "explanation" in r

def test_missing_artifacts_error(tmp_path):
    """Verify a clean FileNotFoundError is raised when artifacts directory is empty."""
    with pytest.raises(FileNotFoundError) as exc_info:
        FilmAuraRecommender(artifacts_dir=str(tmp_path))
    assert "Required model artifacts are missing" in str(exc_info.value)
