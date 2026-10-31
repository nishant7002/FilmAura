"""
FilmAura — Minimal Recommender Inference Engine
Loads trained model artifacts from artifacts/ and provides fast, explainable recommendations.
"""

import os
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity

# Default Mood Taxonomy mapped to heuristic descriptors
SUPPORTED_MOODS = [
    "Happy", "Relaxed", "Emotional", "Romantic", "Dark",
    "Suspenseful", "Adventurous", "Funny", "Thoughtful", "Motivational"
]

class FilmAuraRecommender:
    """
    Inference-only recommender module for the FilmAura application.
    Loads pre-trained artifacts from the artifacts/ directory.
    """

    def __init__(self, artifacts_dir: Optional[str] = None):
        self.artifacts_dir = Path(artifacts_dir) if artifacts_dir else Path(__file__).resolve().parent / "artifacts"
        self.is_loaded = False
        
        self.catalogue: Optional[pd.DataFrame] = None
        self.vectorizer = None
        self.tfidf_matrix = None
        self.svd_components: Optional[np.ndarray] = None
        self.config: Dict[str, Any] = {}
        
        self.movie_id_to_idx: Dict[int, int] = {}
        self.idx_to_movie_id: Dict[int, int] = {}

        self._load_artifacts()

    def _load_artifacts(self):
        """Loads serialized artifacts with clear error reporting if missing."""
        required_files = {
            "catalogue": self.artifacts_dir / "movies_catalogue.csv",
            "tfidf_vec": self.artifacts_dir / "tfidf_vectorizer.pkl",
            "tfidf_mat": self.artifacts_dir / "tfidf_matrix.npz",
            "config": self.artifacts_dir / "config.json"
        }

        missing = [f"{name} ({path.name})" for name, path in required_files.items() if not path.exists()]
        if missing:
            raise FileNotFoundError(
                f"Required model artifacts are missing in '{self.artifacts_dir}': {', '.join(missing)}.\n"
                f"Please run the Jupyter notebook ('notebooks/FilmAura_ML_Backend.ipynb') to train and export artifacts."
            )

        # 1. Load Catalogue
        df = pd.read_csv(required_files["catalogue"])
        
        # Parse JSON fields safely if saved as strings
        if "genres_json" in df.columns:
            df["genres_list"] = df["genres_json"].apply(lambda x: json.loads(x) if isinstance(x, str) else [])
        elif "genres" in df.columns:
            df["genres_list"] = df["genres"].apply(lambda g: [x.strip() for x in str(g).split("|") if x.strip()] if pd.notnull(g) else [])

        if "tags_json" in df.columns:
            df["tags_list"] = df["tags_json"].apply(lambda x: json.loads(x) if isinstance(x, str) else [])
        elif "tags_list" not in df.columns:
            df["tags_list"] = [[] for _ in range(len(df))]

        if "moods_json" in df.columns:
            df["moods"] = df["moods_json"].apply(lambda x: json.loads(x) if isinstance(x, str) else {})
        elif "moods" not in df.columns:
            df["moods"] = [{} for _ in range(len(df))]

        # Clean display columns
        df["display_title"] = df["clean_title"] if "clean_title" in df.columns else df["title"]
        df["year"] = df["year"].fillna(2000).astype(int)
        df["rating_mean"] = df["rating_mean"].fillna(3.5).round(1)
        df["rating_count"] = df["rating_count"].fillna(10).astype(int)

        self.catalogue = df.reset_index(drop=True)

        mids = self.catalogue["movieId"].astype(int).tolist()
        self.movie_id_to_idx = {mid: idx for idx, mid in enumerate(mids)}
        self.idx_to_movie_id = {idx: mid for idx, mid in enumerate(mids)}

        # 2. Load TF-IDF Models
        with open(required_files["tfidf_vec"], "rb") as f:
            self.vectorizer = pickle.load(f)
        self.tfidf_matrix = load_npz(required_files["tfidf_mat"])

        # 3. Load SVD Components if available
        svd_path = self.artifacts_dir / "svd_components.npy"
        if svd_path.exists():
            self.svd_components = np.load(svd_path)

        # 4. Load Config
        with open(required_files["config"], "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.is_loaded = True

    def get_available_genres(self) -> List[str]:
        """Returns sorted list of unique genres present in the catalogue."""
        if self.catalogue is None:
            return []
        all_genres = set()
        for g_list in self.catalogue["genres_list"]:
            all_genres.update(g_list)
        all_genres.discard("(no genres listed)")
        return sorted(list(all_genres))

    def get_available_moods(self) -> List[str]:
        """Returns list of supported mood categories."""
        return SUPPORTED_MOODS

    def get_movie_titles(self, limit: Optional[int] = 1000) -> List[Dict[str, Any]]:
        """Returns list of popular movies formatted for selection dropdowns."""
        if self.catalogue is None:
            return []
        cache_key = f"_cached_movies_{limit}"
        if hasattr(self, cache_key) and getattr(self, cache_key) is not None:
            return getattr(self, cache_key)

        if limit and limit < len(self.catalogue):
            df_subset = self.catalogue.sort_values(by="rating_count", ascending=False).head(limit)
        else:
            df_subset = self.catalogue

        titles = (df_subset["display_title"].fillna("Untitled").astype(str) + " (" + df_subset["year"].astype(str) + ")").tolist()
        mids = df_subset["movieId"].astype(int).tolist()
        movies = [{"movieId": m, "title": t} for m, t in zip(mids, titles)]
        movies.sort(key=lambda x: str(x["title"]))
        setattr(self, cache_key, movies)
        return movies

    def recommend(
        self,
        mood: Optional[str] = None,
        genre: Optional[str] = None,
        favorite_movie_id: Optional[int] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generates top-K recommendations blending content similarity,
        affective mood score, and Bayesian rating shrinkage.
        """
        if not self.is_loaded or self.catalogue is None:
            raise RuntimeError("Recommender artifacts not loaded.")

        is_cold_start = favorite_movie_id is None or favorite_movie_id not in self.movie_id_to_idx

        # 1. Content Similarity Vector
        if not is_cold_start:
            fav_idx = self.movie_id_to_idx[favorite_movie_id]
            content_sims = cosine_similarity(self.tfidf_matrix[fav_idx], self.tfidf_matrix)[0]
        else:
            content_sims = np.full(len(self.catalogue), 0.5)

        # 2. Bayesian Shrinkage Prior Parameters (Vectorized)
        C = float(self.catalogue["rating_mean"].mean())
        m = max(1.0, float(self.catalogue["rating_count"].quantile(0.25)))
        v = self.catalogue["rating_count"].values
        R = self.catalogue["rating_mean"].values
        wr = (v / (v + m)) * R + (m / (v + m)) * C
        s_pop = np.clip((wr - 0.5) / 4.5, 0.0, 1.0)

        # 3. Dynamic Hybrid Weights
        if is_cold_start:
            w_content, w_mood, w_pop = 0.15, 0.45, 0.40
        else:
            w_content, w_mood, w_pop = 0.45, 0.35, 0.20

        # 4. Mood Scores Vectorized
        target_mood = mood.lower() if mood else None
        if target_mood:
            s_mood = np.array([m.get(target_mood, 0.35) if isinstance(m, dict) else 0.50 for m in self.catalogue["moods"]])
        else:
            s_mood = np.full(len(self.catalogue), 0.50)

        # 5. Composite Hybrid Score (Vectorized in NumPy)
        composite = (w_content * content_sims) + (w_mood * s_mood) + (w_pop * s_pop)

        # 6. Apply Filtering Mask
        mask = np.ones(len(self.catalogue), dtype=bool)
        if favorite_movie_id and favorite_movie_id in self.movie_id_to_idx:
            mask[self.movie_id_to_idx[favorite_movie_id]] = False

        if genre and genre != "All Genres":
            genre_match = np.array([genre in g for g in self.catalogue["genres_list"]], dtype=bool)
            mask &= genre_match

        composite[~mask] = -999.0

        # 7. Select Top-K Candidate Indices
        top_indices = np.argsort(composite)[::-1][:top_k]

        fav_title = None
        if not is_cold_start:
            fav_row = self.catalogue[self.catalogue["movieId"] == favorite_movie_id]
            if not fav_row.empty:
                fav_title = fav_row.iloc[0]["display_title"]

        results = []
        for idx in top_indices:
            score = float(composite[idx])
            if score < -100.0:
                continue

            row = self.catalogue.iloc[idx]
            mid = int(row["movieId"])
            match_pct = int(np.clip(80 + (score * 20), 82, 99))

            # Natural Language Explanation
            reasons = []
            if mood:
                reasons.append(f"Resonates with your **{mood}** mood")
            if fav_title:
                reasons.append(f"Shares narrative and thematic depth with **{fav_title}**")
            elif genre and genre != "All Genres":
                reasons.append(f"Highly praised by **{genre}** viewers")
            else:
                top_g = row["genres_list"][0] if row["genres_list"] else "Cinema"
                reasons.append(f"Popular consensus pick among **{top_g}** cinephiles")

            explanation = " • ".join(reasons) + "."

            results.append({
                "movieId": mid,
                "title": row["display_title"],
                "year": int(row["year"]),
                "genres": row["genres_list"],
                "rating": float(row["rating_mean"]),
                "votes": int(row["rating_count"]),
                "match_pct": match_pct,
                "composite_score": score,
                "explanation": explanation
            })

        return results
