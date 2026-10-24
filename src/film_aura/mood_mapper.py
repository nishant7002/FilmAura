"""
FilmAura — Mood-to-Movie Heuristic Feature Engineering Engine
Maps MovieLens genres and aggregated community tags into 10 cinephile mood archetypes.
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from src.film_aura.config import MOOD_MAPPINGS

class MoodEngine:
    """
    Heuristic feature engineering system that bridges MovieLens categorical genres
    and unstructured community tags to human psychological and affective mood states.
    
    10 Documented Mood Archetypes:
    - Happy: Uplifting, whimsical, bright, heartwarming (Comedy, Animation, Musical, Children)
    - Relaxed: Calm, gentle, contemplative, peaceful (Documentary, gentle Comedy/Animation)
    - Emotional: Poignant, deep human connection, catharsis (Drama, Romance)
    - Romantic: Intimate, passionate, courtship, love (Romance, Drama)
    - Dark: Gritty, bleak, shadowy, nihilistic (Film-Noir, Crime, Horror, Thriller)
    - Suspenseful: Taut, cognitive tension, high-stakes mystery (Thriller, Mystery, Crime)
    - Adventurous: Epic exploration, quests, survival (Adventure, Action, Sci-Fi, Fantasy)
    - Funny: Satirical, absurd, witty, slapstick (Comedy)
    - Thoughtful: Existential, philosophical, mind-bending (Sci-Fi, Mystery, Drama)
    - Motivational: Inspiring triumph, perseverance, ambition (Drama, Documentary)
    """

    def __init__(self, mood_mappings: Optional[Dict[str, Dict[str, Any]]] = None):
        self.mappings = mood_mappings or MOOD_MAPPINGS
        self.all_moods = list(self.mappings.keys())

    def score_movie(self, genres_list: List[str], tags_list: List[str]) -> Dict[str, float]:
        """
        Computes affinity scores for all 10 moods for a given movie based on:
        - Genre relevance (weight: 0.55)
        - Tag resonance (weight: 0.45)
        """
        genres_lower = {g.strip().lower() for g in genres_list}
        tags_lower = {t.strip().lower() for t in tags_list}

        scores = {}
        for mood, info in self.mappings.items():
            mood_genres = {g.lower() for g in info["genres"]}
            mood_tags = {t.lower() for t in info["tags"]}

            # 1. Genre score (Jaccard-like with mood genres)
            genre_overlap = len(genres_lower.intersection(mood_genres))
            genre_score = genre_overlap / max(1, len(mood_genres))
            genre_score = min(1.0, genre_score * 1.5)  # boost if primary genre present

            # 2. Tag score
            tag_overlap = 0.0
            for t in tags_lower:
                for mt in mood_tags:
                    if mt in t or t in mt:
                        tag_overlap += 1.0
                        break
            tag_score = min(1.0, tag_overlap / 3.0)  # saturated at 3 matching tags

            # Weighted combination with minimum baseline to avoid zero-probability traps
            raw_score = (0.55 * genre_score) + (0.45 * tag_score)
            # Add small baseline prior (0.05) so every film has a valid probability mass
            affinity = float(np.clip(raw_score + 0.05, 0.05, 0.99))
            scores[mood.lower()] = round(affinity, 3)

        return scores

    def compute_alignment(
        self,
        movie_mood_dict: Dict[str, float],
        primary_mood: Optional[str] = "Dark",
        secondary_mood: Optional[str] = "Suspenseful"
    ) -> Tuple[float, List[Tuple[str, float]]]:
        """
        Calculates affective resonance between user-selected moods and movie mood vector.
        Returns:
            composite_score: float in [0.0, 1.0]
            rationale_tags: list of (tag_name, score) tuples for UI pills
        """
        tags = []
        if not primary_mood and not secondary_mood:
            return 0.70, [("General Balance", 0.70)]

        score = 0.0
        weight_sum = 0.0

        if primary_mood:
            p_key = primary_mood.lower().strip()
            p_val = movie_mood_dict.get(p_key, 0.35)
            score += 0.65 * p_val
            weight_sum += 0.65
            tags.append((f"#{primary_mood.capitalize()}", round(p_val, 2)))

        if secondary_mood:
            s_key = secondary_mood.lower().strip()
            s_val = movie_mood_dict.get(s_key, 0.30)
            score += 0.35 * s_val
            weight_sum += 0.35
            tags.append((f"#{secondary_mood.capitalize()}", round(s_val, 2)))

        composite = score / max(weight_sum, 0.001)
        return float(np.clip(composite, 0.0, 1.0)), tags

    def augment_catalog(self, df_catalog: pd.DataFrame) -> pd.DataFrame:
        """Appends computed mood score dictionaries and dominant moods to the catalogue."""
        df = df_catalog.copy()
        mood_dicts = []
        dominant_moods = []

        for _, row in df.iterrows():
            g_list = row.get("genres_list", [])
            t_list = row.get("tags_list", [])
            m_scores = self.score_movie(g_list, t_list)
            mood_dicts.append(m_scores)

            # Sort moods by score descending
            sorted_m = sorted(m_scores.items(), key=lambda x: x[1], reverse=True)
            top_2 = [m[0].capitalize() for m in sorted_m[:2]]
            dominant_moods.append(top_2)

        df["moods"] = mood_dicts
        df["dominant_moods"] = dominant_moods
        return df
