"""
FilmAura — Recommender Engine Interface
Bridges the Streamlit frontend with the ML Backend models and exported artifacts.
"""

from typing import List, Dict, Any, Optional
from src.film_aura.recommender import ProductionFilmAuraRecommender, ArtifactsMissingError
from src.data_loader import ensure_artifacts_exist

class FilmAuraRecommender(ProductionFilmAuraRecommender):
    """
    Subclass of ProductionFilmAuraRecommender ensuring artifacts exist before instantiation.
    """
    def __init__(self):
        ensure_artifacts_exist()
        super().__init__()
