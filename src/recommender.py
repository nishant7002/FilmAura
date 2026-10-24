"""
FilmAura — Hybrid Recommender Engine
Blends TF-IDF Content Vector Cosine Similarity, Mood Affinity Vectors,
and Bayesian Collaborative Rating Shrinkage.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.data_loader import get_movies_dataframe

class FilmAuraRecommender:
    def __init__(self):
        self.df = get_movies_dataframe()
        self._init_models()

    def _init_models(self):
        """Builds TF-IDF matrix and precomputes pairwise content similarity."""
        # Create rich content string for each movie
        content_strings = []
        for _, row in self.df.iterrows():
            genres = " ".join(row["genres"])
            cast_names = " ".join([c["name"] for c in row["cast"]])
            text = f"{row['title']} {genres} {row['director']} {row['cinematographer']} {cast_names} {row['synopsis']} {row['keywords']}"
            content_strings.append(text)

        self.df["content_corpus"] = content_strings
        self.tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
        self.tfidf_matrix = self.tfidf.fit_transform(content_strings)
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

        # Index lookup
        self.id_to_idx = {row["id"]: idx for idx, row in self.df.iterrows()}
        self.idx_to_id = {idx: row["id"] for idx, row in self.df.iterrows()}

        # Bayesian weighted rating parameters
        # WR = (v / (v + m)) * R + (m / (v + m)) * C
        self.C = self.df["rating"].mean()
        self.m = self.df["votes"].quantile(0.35)

    def compute_bayesian_rating(self, rating: float, votes: int) -> float:
        """Calculates Bayesian weighted average rating, normalized to [0, 1]."""
        wr = (votes / (votes + self.m)) * rating + (self.m / (votes + self.m)) * self.C
        # Normalize assuming ratings span 6.0 - 10.0
        normalized = (wr - 6.0) / 4.0
        return float(np.clip(normalized, 0.0, 1.0))

    def compute_mood_alignment(self, movie_moods: Dict[str, float], primary_mood: Optional[str], secondary_mood: Optional[str]) -> Tuple[float, List[Tuple[str, float]]]:
        """Calculates mood affinity score and returns detailed component tags."""
        tags = []
        if not primary_mood and not secondary_mood:
            return 0.75, [("Balanced", 0.75)]

        score = 0.0
        weights_sum = 0.0

        if primary_mood:
            p_key = primary_mood.lower().strip()
            p_val = movie_moods.get(p_key, 0.40)
            score += 0.65 * p_val
            weights_sum += 0.65
            tags.append((f"#{primary_mood.capitalize()}", round(p_val, 2)))

        if secondary_mood:
            s_key = secondary_mood.lower().strip()
            s_val = movie_moods.get(s_key, 0.35)
            score += 0.35 * s_val
            weights_sum += 0.35
            tags.append((f"#{secondary_mood.capitalize()}", round(s_val, 2)))

        final_score = score / max(weights_sum, 0.001)
        return float(np.clip(final_score, 0.0, 1.0)), tags

    def recommend(
        self,
        primary_mood: Optional[str] = "Dark",
        secondary_mood: Optional[str] = "Suspenseful",
        selected_genres: Optional[List[str]] = None,
        anchor_movie_ids: Optional[List[str]] = None,
        filter_under_2h: bool = False,
        filter_stream_only: bool = False,
        exclude_seen_ids: Optional[List[str]] = None,
        sort_by: str = "Aura Score",
        content_weight: float = 0.45,
        mood_weight: float = 0.35,
        collab_weight: float = 0.20,
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Calculates hybrid recommendations based on content similarity,
        mood resonance vectors, and collaborative Bayesian signals.
        """
        exclude_seen_ids = exclude_seen_ids or []
        anchor_movie_ids = anchor_movie_ids or []
        selected_genres = selected_genres or []

        # 1. Content similarity vector
        if anchor_movie_ids:
            valid_indices = [self.id_to_idx[mid] for mid in anchor_movie_ids if mid in self.id_to_idx]
            if valid_indices:
                content_sim_vec = np.mean([self.cosine_sim[idx] for idx in valid_indices], axis=0)
            else:
                content_sim_vec = np.full(len(self.df), 0.5)
        else:
            # Baseline similarity across catalogue
            content_sim_vec = np.full(len(self.df), 0.6)

        results = []

        for idx, row in self.df.iterrows():
            movie_id = row["id"]

            # Exclude if anchored movie itself
            if movie_id in anchor_movie_ids:
                continue

            # Exclude seen
            if movie_id in exclude_seen_ids:
                continue

            # Filter: Under 2h (120m)
            if filter_under_2h and row["runtime"] > 120:
                continue

            # Filter: Available to stream
            if filter_stream_only and "Rent" in row["stream_provider"]:
                continue

            # Filter: Genre match (if selected, must contain at least one)
            if selected_genres:
                has_genre = any(g in row["genres"] for g in selected_genres)
                if not has_genre:
                    continue

            # Score calculations
            c_sim = float(content_sim_vec[idx])
            m_score, mood_tags = self.compute_mood_alignment(row["moods"], primary_mood, secondary_mood)
            b_rating = self.compute_bayesian_rating(row["rating"], row["votes"])

            # Normalize weights
            total_w = content_weight + mood_weight + collab_weight
            nw_c = content_weight / total_w
            nw_m = mood_weight / total_w
            nw_collab = collab_weight / total_w

            raw_composite = (nw_c * c_sim) + (nw_m * m_score) + (nw_collab * b_rating)
            
            # Map raw composite [0.35, 0.95] to realistic cinephile match percentage [85%, 99%]
            scaled_match_pct = int(np.clip(80 + (raw_composite * 20), 82, 99))

            # Dynamic natural language rationale
            rationale_parts = []
            if primary_mood or secondary_mood:
                mood_str = f"{primary_mood or ''} {'& ' + secondary_mood if secondary_mood else ''}".strip()
                rationale_parts.append(f"Matches your <strong>{mood_str}</strong> mood")

            if anchor_movie_ids:
                seed_title = self.df[self.df["id"] == anchor_movie_ids[0]]["title"].values[0]
                rationale_parts.append(f"Similar visual tone and thematic depth to <strong>{seed_title}</strong>")
            else:
                rationale_parts.append(f"High collaborative alignment with <strong>{row['genres'][0]}</strong> cinephiles")

            rationale = " • ".join(rationale_parts) + "."

            results.append({
                "id": movie_id,
                "title": row["title"],
                "year": row["year"],
                "runtime": row["runtime"],
                "genres": row["genres"],
                "rating": row["rating"],
                "votes": row["votes"],
                "director": row["director"],
                "director_title": row["director_title"],
                "cinematographer": row["cinematographer"],
                "cinematographer_title": row["cinematographer_title"],
                "cast": row["cast"],
                "synopsis": row["synopsis"],
                "stream_provider": row["stream_provider"],
                "quality_badge": row["quality_badge"],
                "age_rating": row["age_rating"],
                "trailer_url": row["trailer_url"],
                "similar_ids": row["similar_ids"],
                "similar_reasons": row["similar_reasons"],
                "aura_match_pct": scaled_match_pct,
                "content_sim": round(c_sim, 3),
                "mood_score": round(m_score, 3),
                "collab_score": round(b_rating, 3),
                "mood_tags": mood_tags,
                "rationale": rationale,
                "breakdown": {
                    "content_pct": int(nw_c * 100),
                    "mood_pct": int(nw_m * 100),
                    "collab_pct": int(nw_collab * 100)
                }
            })

        # Sorting
        if sort_by == "Highest Rating":
            results.sort(key=lambda x: (x["rating"], x["votes"]), reverse=True)
        elif sort_by == "Release Year":
            results.sort(key=lambda x: x["year"], reverse=True)
        else: # Default: Aura Score
            results.sort(key=lambda x: (x["aura_match_pct"], x["rating"]), reverse=True)

        return results[:top_n]

    def get_movie_by_id(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves complete movie record by ID."""
        matches = self.df[self.df["id"] == movie_id]
        if matches.empty:
            return None
        return matches.iloc[0].to_dict()
