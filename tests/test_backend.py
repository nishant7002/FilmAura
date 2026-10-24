"""
Unit Tests for FilmAura Machine Learning Backend
Tests:
- DataLoader (dev and full mode error handling)
- MoodEngine (heuristic feature engineering)
- Popularity Recommender (Bayesian shrinkage)
- Content-Based Recommender (TF-IDF + Cosine)
- Item-Item Collaborative Filtering
- Matrix Factorization SVD
- Hybrid Recommender (Cold-Start and Seed-Based)
- Offline Evaluation Metrics
"""

import os
import sys
from pathlib import Path
import pytest
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.film_aura.data_loader import MovieLensDataLoader
from src.film_aura.mood_mapper import MoodEngine
from src.film_aura.models import (
    PopularityRecommender,
    ContentBasedRecommender,
    ItemItemKNNRecommender,
    SVDRecommender,
    HybridRecommender
)
from src.film_aura.metrics import (
    precision_at_k,
    recall_at_k,
    hit_rate_at_k,
    ndcg_at_k,
    catalog_coverage,
    novelty,
    rmse,
    mae
)

# ==========================================
# 1. DataLoader Tests
# ==========================================
def test_data_loader_dev_mode():
    loader = MovieLensDataLoader(mode="dev")
    movies, ratings, tags, links = loader.load_raw_data()
    assert not movies.empty
    assert not ratings.empty
    assert not tags.empty
    assert not links.empty
    assert "movieId" in movies.columns
    assert "title" in movies.columns
    assert "genres" in movies.columns
    assert "rating" in ratings.columns
    assert "userId" in ratings.columns

def test_data_loader_summary():
    loader = MovieLensDataLoader(mode="dev")
    summary = loader.get_dataset_summary()
    assert summary["mode"] == "dev"
    assert summary["num_movies"] >= 50
    assert summary["num_ratings"] >= 1000
    assert summary["num_users"] >= 50
    assert 0.0 <= summary["sparsity_pct"] <= 100.0

def test_data_loader_full_mode_strict_missing_error():
    """Verify that full mode never silently falls back to dev mode when 32M files are missing."""
    with pytest.raises(FileNotFoundError) as exc_info:
        MovieLensDataLoader(mode="full")
    assert "Full-data mode selected" in str(exc_info.value)
    assert "grouplens.org/datasets/movielens/32m" in str(exc_info.value)

def test_prepare_catalog():
    loader = MovieLensDataLoader(mode="dev")
    catalog = loader.prepare_catalog()
    assert "clean_title" in catalog.columns
    assert "year" in catalog.columns
    assert "genres_list" in catalog.columns
    assert "tags_list" in catalog.columns
    assert "content_text" in catalog.columns
    assert "rating_mean" in catalog.columns
    assert "rating_count" in catalog.columns

    # Check year extraction
    sample = catalog.iloc[0]
    assert isinstance(sample["year"], (int, np.integer))

def test_build_rating_matrix():
    loader = MovieLensDataLoader(mode="dev")
    matrix, u2r, r2u, m2c, c2m = loader.build_rating_matrix()
    assert isinstance(matrix, csr_matrix)
    assert matrix.shape[0] == len(u2r)
    assert matrix.shape[1] == len(m2c)
    assert matrix.nnz > 0

# ==========================================
# 2. MoodEngine Tests
# ==========================================
def test_mood_engine_scoring():
    engine = MoodEngine()
    scores = engine.score_movie(
        genres_list=["Sci-Fi", "Mystery"],
        tags_list=["cyberpunk", "philosophical", "existential"]
    )
    assert "thoughtful" in scores
    assert "dark" in scores
    assert scores["thoughtful"] > scores["happy"]

def test_mood_alignment():
    engine = MoodEngine()
    movie_moods = {"dark": 0.9, "suspenseful": 0.85, "happy": 0.1}
    composite, tags = engine.compute_alignment(
        movie_moods,
        primary_mood="Dark",
        secondary_mood="Suspenseful"
    )
    assert composite > 0.80
    assert len(tags) == 2

# ==========================================
# 3. Model Tests
# ==========================================
@pytest.fixture
def dev_data():
    loader = MovieLensDataLoader(mode="dev")
    cat = loader.prepare_catalog()
    mat, u2r, r2u, m2c, c2m = loader.build_rating_matrix()
    return cat, mat, u2r, r2u, m2c, c2m

def test_popularity_recommender(dev_data):
    cat, _, _, _, _, _ = dev_data
    pop = PopularityRecommender()
    pop.fit(cat)
    scores = pop.score_all()
    assert len(scores) == len(cat)
    assert scores.min() >= 0.0
    assert scores.max() <= 1.0

def test_content_recommender(dev_data):
    cat, _, _, _, _, _ = dev_data
    cb = ContentBasedRecommender()
    cb.fit(cat)
    assert cb.cosine_sim_matrix.shape == (len(cat), len(cat))
    # Self-similarity should be ~1.0
    for i in range(len(cat)):
        assert abs(cb.cosine_sim_matrix[i, i] - 1.0) < 1e-4

    scores = cb.score_anchors([1], len(cat))
    assert len(scores) == len(cat)

def test_item_item_knn(dev_data):
    _, mat, _, _, m2c, c2m = dev_data
    item_knn = ItemItemKNNRecommender()
    item_knn.fit(mat, m2c, c2m)
    assert item_knn.item_sim_matrix is not None
    scores = item_knn.score_anchors([1])
    assert len(scores) == len(m2c)

def test_svd_recommender(dev_data):
    _, mat, u2r, r2u, m2c, c2m = dev_data
    svd = SVDRecommender(n_components=5)
    svd.fit(mat, u2r, r2u, m2c, c2m)
    assert svd.item_embeddings.shape[0] == len(m2c)
    scores = svd.score_anchors([1])
    assert len(scores) == len(m2c)

def test_hybrid_recommender_with_seed(dev_data):
    cat, mat, u2r, r2u, m2c, c2m = dev_data
    hr = HybridRecommender()
    hr.fit(cat, mat, u2r, r2u, m2c, c2m)

    recs = hr.recommend(
        primary_mood="Dark",
        secondary_mood="Suspenseful",
        anchor_movie_ids=[1],
        top_n=5
    )
    assert len(recs) == 5
    for r in recs:
        assert r["movieId"] != 1  # Should not recommend seed itself
        assert "aura_match_pct" in r
        assert "rationale" in r
        assert "breakdown" in r
        assert 80 <= r["aura_match_pct"] <= 100

def test_hybrid_recommender_cold_start(dev_data):
    """Test cold-start when user has no anchor movie."""
    cat, mat, u2r, r2u, m2c, c2m = dev_data
    hr = HybridRecommender()
    hr.fit(cat, mat, u2r, r2u, m2c, c2m)

    # Empty anchor movie IDs
    recs = hr.recommend(
        primary_mood="Happy",
        secondary_mood=None,
        anchor_movie_ids=[],
        top_n=5
    )
    assert len(recs) == 5
    for r in recs:
        assert "aura_match_pct" in r
        assert "rationale" in r
        # Should gracefully recommend without crashing

# ==========================================
# 4. Metric Tests
# ==========================================
def test_precision_recall_hit_rate():
    rec = [1, 2, 3, 4, 5]
    rel = {2, 4, 8}
    assert precision_at_k(rec, rel, k=5) == 2 / 5
    assert recall_at_k(rec, rel, k=5) == 2 / 3
    assert hit_rate_at_k(rec, rel, k=5) == 1.0

    # No hits
    rec_miss = [10, 20, 30]
    assert hit_rate_at_k(rec_miss, rel, k=3) == 0.0

def test_ndcg_at_k():
    rec_perfect = [2, 4, 8, 1, 3]
    rel = {2, 4, 8}
    # When top 3 recommendations are all relevant, NDCG should be 1.0
    assert abs(ndcg_at_k(rec_perfect, rel, k=3) - 1.0) < 1e-4

def test_rmse_mae():
    y_true = np.array([3.0, 4.0, 5.0])
    y_pred = np.array([3.0, 3.0, 5.0])
    assert mae(y_true, y_pred) == 1.0 / 3.0
    assert abs(rmse(y_true, y_pred) - np.sqrt(1.0 / 3.0)) < 1e-4

def test_coverage_and_novelty():
    all_recs = [[1, 2], [2, 3], [4, 5]]
    assert catalog_coverage(all_recs, total_catalog_size=10) == 0.5

    pop = {1: 0.5, 2: 0.25}
    nov = novelty([1, 2], pop, k=2)
    assert nov > 0.0
