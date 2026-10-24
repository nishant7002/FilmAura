"""
FilmAura — Machine Learning Recommendation Models
Implements:
1. Bayesian Shrinkage Popularity Recommender
2. TF-IDF Cosine Similarity Content-Based Recommender
3. Item-Item Collaborative Filtering (Cosine on User-Item Sparse Matrix)
4. Matrix Factorization SVD (TruncatedSVD)
5. Hybrid Recommender with Cold-Start Fallback & Rationale Generator
"""

from typing import List, Dict, Any, Optional, Tuple, Set
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

from src.film_aura.config import DEFAULT_HYBRID_WEIGHTS
from src.film_aura.mood_mapper import MoodEngine

# ==========================================
# 1. Popularity Recommender (Bayesian Shrinkage)
# ==========================================
class PopularityRecommender:
    """
    Bayesian shrinkage weighted rating model (IMDb formula):
    WR = (v / (v + m)) * R + (m / (v + m)) * C
    Guarantees robust ranking that penalizes movies with high ratings but very few votes.
    """

    def __init__(self, quantile_threshold: float = 0.25):
        self.quantile_threshold = quantile_threshold
        self.C: float = 3.5
        self.m: float = 5.0
        self.scores_: Optional[pd.Series] = None

    def fit(self, df_catalog: pd.DataFrame) -> "PopularityRecommender":
        self.C = float(df_catalog["rating_mean"].mean())
        self.m = float(df_catalog["rating_count"].quantile(self.quantile_threshold))
        self.m = max(1.0, self.m)

        v = df_catalog["rating_count"].values
        R = df_catalog["rating_mean"].values

        wr = (v / (v + self.m)) * R + (self.m / (v + self.m)) * self.C
        # Normalize to [0, 1] range based on rating scale [0.5, 5.0]
        norm_scores = (wr - 0.5) / 4.5
        norm_scores = np.clip(norm_scores, 0.0, 1.0)

        self.scores_ = pd.Series(norm_scores, index=df_catalog["movieId"])
        return self

    def score_all(self) -> pd.Series:
        if self.scores_ is None:
            raise ValueError("Model must be fitted before calling score_all().")
        return self.scores_

    def get_score(self, movie_id: int) -> float:
        if self.scores_ is None or movie_id not in self.scores_:
            return 0.5
        return float(self.scores_[movie_id])


# ==========================================
# 2. Content-Based Recommender (TF-IDF + Cosine)
# ==========================================
class ContentBasedRecommender:
    """
    NLP Content-Based model using TF-IDF representation of movie titles,
    genres, and aggregated user tags, scoring candidates with Cosine Similarity.
    """

    def __init__(self, max_features: int = 5000, ngram_range: Tuple[int, int] = (1, 2)):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=max_features,
            ngram_range=ngram_range,
            sublinear_tf=True
        )
        self.tfidf_matrix = None
        self.cosine_sim_matrix = None
        self.movie_id_to_idx: Dict[int, int] = {}
        self.idx_to_movie_id: Dict[int, int] = {}

    def fit(self, df_catalog: pd.DataFrame) -> "ContentBasedRecommender":
        corpus = df_catalog["content_text"].fillna("").tolist()
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        self.cosine_sim_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

        movie_ids = df_catalog["movieId"].tolist()
        self.movie_id_to_idx = {mid: idx for idx, mid in enumerate(movie_ids)}
        self.idx_to_movie_id = {idx: mid for idx, mid in enumerate(movie_ids)}
        return self

    def score_anchors(self, anchor_movie_ids: List[int], num_total_movies: int) -> np.ndarray:
        """Returns similarity vector for one or more anchor movies."""
        valid_indices = [
            self.movie_id_to_idx[mid]
            for mid in anchor_movie_ids
            if mid in self.movie_id_to_idx
        ]

        if not valid_indices or self.cosine_sim_matrix is None:
            return np.full(num_total_movies, 0.5, dtype=np.float32)

        if len(valid_indices) == 1:
            return self.cosine_sim_matrix[valid_indices[0]]
        else:
            return np.mean(self.cosine_sim_matrix[valid_indices], axis=0)


# ==========================================
# 3. Item-Item Collaborative Filtering
# ==========================================
class ItemItemKNNRecommender:
    """
    Item-Item Collaborative Filtering based on Cosine Similarity
    computed over the columns (items) of the user-item rating matrix.
    """

    def __init__(self):
        self.item_sim_matrix: Optional[np.ndarray] = None
        self.item_user_matrix: Optional[csr_matrix] = None
        self.movie_to_col: Dict[int, int] = {}
        self.col_to_movie: Dict[int, int] = {}
        self.num_items: int = 0

    def fit(
        self,
        rating_matrix: csr_matrix,
        movie_to_col: Dict[int, int],
        col_to_movie: Dict[int, int]
    ) -> "ItemItemKNNRecommender":
        self.movie_to_col = movie_to_col
        self.col_to_movie = col_to_movie
        self.num_items = len(movie_to_col)

        # Transpose so rows are items, columns are users
        self.item_user_matrix = rating_matrix.T.tocsr()
        
        # Precompute full pairwise similarity only if item count is reasonable (e.g. <= 3500)
        # to avoid OOM memory explosion on full MovieLens 32M
        if self.num_items <= 3500:
            self.item_sim_matrix = cosine_similarity(self.item_user_matrix, dense_output=True)
            self.item_sim_matrix = np.clip(self.item_sim_matrix, 0.0, 1.0)
        else:
            self.item_sim_matrix = None
        return self

    def score_anchors(self, anchor_movie_ids: List[int]) -> Dict[int, float]:
        """Returns collaborative similarity scores for all items given anchor movies."""
        if self.movie_to_col is None:
            return {}

        valid_cols = [
            self.movie_to_col[mid]
            for mid in anchor_movie_ids
            if mid in self.movie_to_col
        ]

        if not valid_cols:
            return {mid: 0.5 for mid in self.movie_to_col}

        # If precomputed matrix exists (dev mode / compact catalogue)
        if self.item_sim_matrix is not None:
            if len(valid_cols) == 1:
                sim_vec = self.item_sim_matrix[valid_cols[0]]
            else:
                sim_vec = np.mean(self.item_sim_matrix[valid_cols], axis=0)
        elif self.item_user_matrix is not None:
            # Scalable on-the-fly similarity for MovieLens 32M
            sim_sub = cosine_similarity(self.item_user_matrix[valid_cols], self.item_user_matrix)
            sim_sub = np.clip(sim_sub, 0.0, 1.0)
            sim_vec = np.mean(sim_sub, axis=0) if len(valid_cols) > 1 else sim_sub[0]
        else:
            return {mid: 0.5 for mid in self.movie_to_col}

        return {self.col_to_movie[col]: float(sim_vec[col]) for col in range(len(sim_vec))}


# ==========================================
# 4. Matrix Factorization (TruncatedSVD)
# ==========================================
class SVDRecommender:
    """
    Latent factor matrix factorization recommender using Scikit-Learn TruncatedSVD.
    Decomposes normalized user-item rating matrix into user and item latent embeddings.
    """

    def __init__(self, n_components: int = 15, random_state: int = 42):
        self.n_components = n_components
        self.random_state = random_state
        self.svd: Optional[TruncatedSVD] = None
        self.item_embeddings: Optional[np.ndarray] = None
        self.user_embeddings: Optional[np.ndarray] = None
        self.global_mean: float = 3.5
        self.movie_to_col: Dict[int, int] = {}
        self.col_to_movie: Dict[int, int] = {}
        self.user_to_row: Dict[int, int] = {}
        self.row_to_user: Dict[int, int] = {}

    def fit(
        self,
        rating_matrix: csr_matrix,
        user_to_row: Dict[int, int],
        row_to_user: Dict[int, int],
        movie_to_col: Dict[int, int],
        col_to_movie: Dict[int, int]
    ) -> "SVDRecommender":
        self.user_to_row = user_to_row
        self.row_to_user = row_to_user
        self.movie_to_col = movie_to_col
        self.col_to_movie = col_to_movie

        # Ensure n_components does not exceed matrix dimensions
        n_comp = min(self.n_components, min(rating_matrix.shape) - 1)
        n_comp = max(2, n_comp)

        self.svd = TruncatedSVD(n_components=n_comp, random_state=self.random_state)
        if rating_matrix.nnz > 0:
            self.global_mean = float(rating_matrix.data.mean())
        
        # Fit directly on sparse matrix - zero memory explosion, scales to 32M ratings
        self.user_embeddings = self.svd.fit_transform(rating_matrix)
        self.item_embeddings = self.svd.components_.T  # Shape: (num_movies, n_components)
        return self

    def score_anchors(self, anchor_movie_ids: List[int]) -> Dict[int, float]:
        """
        Projects anchor movies as a synthetic latent user vector and scores all candidate movies.
        """
        if self.item_embeddings is None:
            return {mid: 0.5 for mid in self.movie_to_col}

        valid_cols = [
            self.movie_to_col[mid]
            for mid in anchor_movie_ids
            if mid in self.movie_to_col
        ]

        if not valid_cols:
            return {mid: 0.5 for mid in self.movie_to_col}

        # Average latent representation of anchor movies
        synthetic_user_latent = np.mean(self.item_embeddings[valid_cols], axis=0)

        # Dot product with all item embeddings
        dot_products = np.dot(self.item_embeddings, synthetic_user_latent)
        # Normalize with sigmoid-like bounds into [0, 1]
        norm_scores = 1.0 / (1.0 + np.exp(-dot_products))

        return {self.col_to_movie[col]: float(norm_scores[col]) for col in range(len(norm_scores))}


# ==========================================
# 5. Hybrid Recommendation System
# ==========================================
class HybridRecommender:
    """
    Weighted hybrid recommendation engine unifying:
    - Content-Based NLP similarity
    - Item-Item Collaborative Filtering
    - Latent Factor SVD Matrix Factorization
    - Bayesian Shrinkage Popularity
    - Affective Mood Alignment
    
    Includes robust Cold-Start Fallbacks and Explainability Rationale Generation.
    """

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        mood_engine: Optional[MoodEngine] = None
    ):
        self.weights = weights or DEFAULT_HYBRID_WEIGHTS.copy()
        self.mood_engine = mood_engine or MoodEngine()
        
        self.popularity = PopularityRecommender()
        self.content = ContentBasedRecommender()
        self.item_knn = ItemItemKNNRecommender()
        self.svd = SVDRecommender()

        self.df_catalog: Optional[pd.DataFrame] = None
        self.is_fitted = False

    def fit(
        self,
        df_catalog: pd.DataFrame,
        rating_matrix: Optional[csr_matrix] = None,
        user_to_row: Optional[Dict[int, int]] = None,
        row_to_user: Optional[Dict[int, int]] = None,
        movie_to_col: Optional[Dict[int, int]] = None,
        col_to_movie: Optional[Dict[int, int]] = None
    ) -> "HybridRecommender":
        # 1. Augment catalogue with mood scores
        self.df_catalog = self.mood_engine.augment_catalog(df_catalog)

        # 2. Fit Popularity
        self.popularity.fit(self.df_catalog)

        # 3. Fit Content-Based
        self.content.fit(self.df_catalog)

        # 4. Fit Collaborative Models if matrix provided
        if rating_matrix is not None and movie_to_col and col_to_movie:
            self.item_knn.fit(rating_matrix, movie_to_col, col_to_movie)
            if user_to_row and row_to_user:
                self.svd.fit(rating_matrix, user_to_row, row_to_user, movie_to_col, col_to_movie)

        self.is_fitted = True
        return self

    def recommend(
        self,
        primary_mood: Optional[str] = "Dark",
        secondary_mood: Optional[str] = "Suspenseful",
        selected_genres: Optional[List[str]] = None,
        anchor_movie_ids: Optional[List[int]] = None,
        filter_under_2h: bool = False,
        exclude_seen_ids: Optional[List[int]] = None,
        custom_weights: Optional[Dict[str, float]] = None,
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Executes hybrid ranking across catalogue.
        Gracefully falls back to mood + popularity filtering when no anchor movies are chosen (cold start).
        """
        if not self.is_fitted or self.df_catalog is None:
            raise RuntimeError("HybridRecommender must be fitted before generating recommendations.")

        exclude_seen_ids = set(exclude_seen_ids or [])
        anchor_movie_ids = anchor_movie_ids or []
        selected_genres = selected_genres or []
        weights = custom_weights or self.weights

        # Determine if this is a Cold-Start user (no anchor movie)
        is_cold_start = len(anchor_movie_ids) == 0

        # Adjust weights dynamically if cold-start
        w_content = 0.15 if is_cold_start else weights.get("content", 0.40)
        w_item = 0.05 if is_cold_start else weights.get("item_knn", 0.25)
        w_svd = 0.05 if is_cold_start else weights.get("svd", 0.15)
        w_pop = 0.40 if is_cold_start else weights.get("popularity", 0.10)
        w_mood = 0.35 if is_cold_start else weights.get("mood", 0.10)

        # Normalize weights
        total_w = w_content + w_item + w_svd + w_pop + w_mood
        nw_content = w_content / total_w
        nw_item = w_item / total_w
        nw_svd = w_svd / total_w
        nw_pop = w_pop / total_w
        nw_mood = w_mood / total_w

        # Compute model scores
        num_movies = len(self.df_catalog)
        content_sim_vec = self.content.score_anchors(anchor_movie_ids, num_movies)
        item_scores = self.item_knn.score_anchors(anchor_movie_ids)
        svd_scores = self.svd.score_anchors(anchor_movie_ids)
        pop_scores = self.popularity.score_all()

        results = []
        for idx, row in self.df_catalog.iterrows():
            mid = int(row["movieId"])

            # Filters
            if mid in anchor_movie_ids or mid in exclude_seen_ids:
                continue

            # Genre filter: must contain at least one of selected genres if specified
            if selected_genres:
                genres = row.get("genres_list", [])
                if not any(g in genres for g in selected_genres):
                    continue

            # Score components
            s_content = float(content_sim_vec[idx])
            s_item = item_scores.get(mid, 0.5)
            s_svd = svd_scores.get(mid, 0.5)
            s_pop = pop_scores.get(mid, 0.5)
            s_mood, mood_tags = self.mood_engine.compute_alignment(
                row.get("moods", {}), primary_mood, secondary_mood
            )

            # Composite hybrid score [0.0, 1.0]
            composite = (
                (nw_content * s_content) +
                (nw_item * s_item) +
                (nw_svd * s_svd) +
                (nw_pop * s_pop) +
                (nw_mood * s_mood)
            )

            # Map to aura match percentage [82%, 99%] for friendly presentation
            aura_match_pct = int(np.clip(80 + (composite * 20), 82, 99))

            # Explainability: construct dynamic human-readable rationale
            rationale_parts = []
            if primary_mood or secondary_mood:
                mood_str = f"{primary_mood or ''} {'& ' + secondary_mood if secondary_mood else ''}".strip()
                rationale_parts.append(f"Resonates with your <strong>{mood_str}</strong> mood")

            if anchor_movie_ids:
                anchor_match = self.df_catalog[self.df_catalog["movieId"] == anchor_movie_ids[0]]
                if not anchor_match.empty:
                    anchor_title = anchor_match.iloc[0]["clean_title"]
                    rationale_parts.append(f"Shares thematic and visual kinship with <strong>{anchor_title}</strong>")
            else:
                top_genre = row.get("genres_list", ["Cinema"])[0]
                rationale_parts.append(f"Highest Bayesian consensus among <strong>{top_genre}</strong> viewers")

            rationale = " • ".join(rationale_parts) + "."

            results.append({
                "movieId": mid,
                "id": str(mid),
                "title": row["clean_title"],
                "full_title": row["title"],
                "year": row.get("year", 2000),
                "runtime": 115,  # Standard cinematic default
                "genres": row.get("genres_list", []),
                "rating": float(row.get("rating_mean", 4.0)),
                "votes": int(row.get("rating_count", 100)),
                "tags": row.get("tags_list", []),
                "imdbId": str(row.get("imdbId", "")),
                "tmdbId": str(row.get("tmdbId", "")),
                "aura_match_pct": aura_match_pct,
                "composite_score": round(composite, 4),
                "content_sim": round(s_content, 3),
                "item_knn_score": round(s_item, 3),
                "svd_score": round(s_svd, 3),
                "pop_score": round(s_pop, 3),
                "mood_score": round(s_mood, 3),
                "mood_tags": mood_tags,
                "dominant_moods": row.get("dominant_moods", []),
                "rationale": rationale,
                "breakdown": {
                    "content_pct": int(nw_content * 100),
                    "collab_pct": int((nw_item + nw_svd) * 100),
                    "pop_pct": int(nw_pop * 100),
                    "mood_pct": int(nw_mood * 100)
                }
            })

        # Sort by composite score descending
        results.sort(key=lambda x: (x["composite_score"], x["rating"]), reverse=True)
        return results[:top_n]

    def get_movie_by_id(self, movie_id: int) -> Optional[Dict[str, Any]]:
        if self.df_catalog is None:
            return None
        matches = self.df_catalog[self.df_catalog["movieId"] == movie_id]
        if matches.empty:
            return None
        return matches.iloc[0].to_dict()
