"""
FilmAura — Cinema Dataset Loader & Artifact Manager
Loads the MovieLens movie catalogue and ensures model artifacts are initialized.
"""

import os
import json
from pathlib import Path
import pandas as pd
import numpy as np

from src.film_aura.config import ARTIFACTS_DIR
from src.film_aura.export_artifacts import run_export_pipeline

CATALOGUE_PATH = ARTIFACTS_DIR / "movies_catalogue.csv"

def ensure_artifacts_exist():
    """Generates artifacts using development dataset if not already present."""
    if not CATALOGUE_PATH.exists():
        os.makedirs(ARTIFACTS_DIR, exist_ok=True)
        print("Artifacts not found. Auto-generating baseline artifacts with dev dataset...")
        run_export_pipeline("dev")

def get_movies_dataframe() -> pd.DataFrame:
    """Returns the film catalogue as a clean Pandas DataFrame for the frontend."""
    ensure_artifacts_exist()
    df = pd.read_csv(CATALOGUE_PATH)
    
    # Ensure ID string column is present
    df["id"] = df["movieId"].astype(str)
    df["title"] = df["clean_title"] if "clean_title" in df.columns else df["title"]
    
    # Parse JSON genres and tags if needed
    if "genres_json" in df.columns:
        df["genres"] = df["genres_json"].apply(lambda x: json.loads(x) if isinstance(x, str) else [])
    elif "genres" in df.columns:
        df["genres"] = df["genres"].apply(lambda g: g.split("|") if isinstance(g, str) else [])

    if "rating_mean" in df.columns:
        df["rating"] = df["rating_mean"].round(1)
    if "rating_count" in df.columns:
        df["votes"] = df["rating_count"].astype(int)

    df["runtime"] = 115
    return df
