"""
FilmAura — Configuration & Paths Module
Defines default settings, dataset paths, mood mappings, and hybrid weights.
"""

import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Dataset Paths (Supports MovieLens 32M and Development Subset)
MOVIELENS_FULL_DIR = Path(os.environ.get("MOVIELENS_DATA_DIR", DATA_DIR / "ml-32m"))
MOVIELENS_DEV_DIR = DATA_DIR / "dev"

# Database Configuration (Optional Neon PostgreSQL)
DATABASE_URL = os.environ.get("DATABASE_URL", None)

# 10 Documented Heuristic Mood Categories
# Mapped to MovieLens Genres and community tags
MOOD_MAPPINGS = {
    "Happy": {
        "genres": ["Animation", "Children", "Comedy", "Musical"],
        "tags": ["feel-good", "uplifting", "whimsical", "cute", "fun", "lighthearted", "cheerful", "optimistic", "family", "charming"],
        "description": "Uplifting, bright, and heartwarming cinema."
    },
    "Relaxed": {
        "genres": ["Documentary", "Animation", "Comedy"],
        "tags": ["gentle", "calm", "mellow", "nature", "slice of life", "peaceful", "soothing", "nostalgic", "slow cinema", "quiet"],
        "description": "Calm, gentle, and contemplative pacing."
    },
    "Emotional": {
        "genres": ["Drama", "Romance"],
        "tags": ["poignant", "tearjerker", "bittersweet", "moving", "heartbreaking", "touching", "grief", "emotional", "melancholy", "human connection"],
        "description": "Deep, poignant human connection and catharsis."
    },
    "Romantic": {
        "genres": ["Romance", "Drama", "Comedy"],
        "tags": ["love", "relationship", "intimate", "passion", "courtship", "romantic comedy", "soulmates", "chemistry", "infatuation", "affection"],
        "description": "Intimate, poetic, and passionate relationships."
    },
    "Dark": {
        "genres": ["Film-Noir", "Crime", "Horror", "Thriller"],
        "tags": ["gritty", "cynical", "bleak", "dystopia", "nihilistic", "shadowy", "psychological", "disturbing", "noir", "violence"],
        "description": "Shadowy, bleak, and morally ambiguous tales."
    },
    "Suspenseful": {
        "genres": ["Thriller", "Mystery", "Crime", "Horror"],
        "tags": ["suspense", "twist", "taut", "mindfuck", "mystery", "paranoia", "tension", "ticking clock", "investigation", "edge of seat"],
        "description": "Taut, high-stakes mystery and cognitive tension."
    },
    "Adventurous": {
        "genres": ["Adventure", "Action", "Fantasy", "Sci-Fi"],
        "tags": ["journey", "quest", "exploration", "space", "epic", "survival", "treasure", "expedition", "heroic", "world building"],
        "description": "Thrilling exploration and heroic quests."
    },
    "Funny": {
        "genres": ["Comedy"],
        "tags": ["hilarious", "satire", "parody", "witty", "absurd", "slapstick", "dark comedy", "dry humor", "cult comedy", "witty dialogue"],
        "description": "Witty, absurd, and laugh-out-loud entertainment."
    },
    "Thoughtful": {
        "genres": ["Sci-Fi", "Mystery", "Drama"],
        "tags": ["philosophical", "existential", "complex", "non-linear", "surreal", "intellectual", "dystopian", "cyberpunk", "symbolism", "thought-provoking"],
        "description": "Mind-bending, existential, and intellectually stimulating."
    },
    "Motivational": {
        "genres": ["Drama", "Documentary"],
        "tags": ["inspiring", "overcoming odds", "triumph", "perseverance", "courage", "sports", "heroism", "hope", "ambition", "redemption"],
        "description": "Inspiring triumph and the perseverance of the human spirit."
    }
}

# Standard MovieLens All Genres
ALL_GENRES = [
    "Action", "Adventure", "Animation", "Children", "Comedy", "Crime",
    "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
    "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
]

# Default Hybrid Weights (Evaluated on Validation Set)
DEFAULT_HYBRID_WEIGHTS = {
    "content": 0.40,
    "item_knn": 0.25,
    "svd": 0.15,
    "popularity": 0.10,
    "mood": 0.10
}
