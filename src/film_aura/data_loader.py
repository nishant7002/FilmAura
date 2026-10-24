"""
FilmAura — MovieLens Data Loader & Catalog Manager
Supports both Development Mode (manageable verified subset) and
Full-Data Mode (complete MovieLens 32M dataset).
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from src.film_aura.config import MOVIELENS_DEV_DIR, MOVIELENS_FULL_DIR

class MovieLensDataLoader:
    """
    Robust loader for the GroupLens MovieLens dataset.
    Strictly differentiates between 'dev' mode and 'full' mode.
    Never silently falls back to dev when full mode is selected.
    """

    def __init__(self, mode: str = "dev", data_dir: Optional[Path] = None):
        self.mode = mode.lower()
        if self.mode not in ("dev", "full"):
            raise ValueError(f"Invalid mode '{mode}'. Expected 'dev' or 'full'.")

        if data_dir is not None:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = MOVIELENS_FULL_DIR if self.mode == "full" else MOVIELENS_DEV_DIR

        self.movies_path = self.data_dir / "movies.csv"
        self.ratings_path = self.data_dir / "ratings.csv"
        self.tags_path = self.data_dir / "tags.csv"
        self.links_path = self.data_dir / "links.csv"

        self._validate_paths()

        # DataFrames
        self.df_movies: Optional[pd.DataFrame] = None
        self.df_ratings: Optional[pd.DataFrame] = None
        self.df_tags: Optional[pd.DataFrame] = None
        self.df_links: Optional[pd.DataFrame] = None
        self.catalog: Optional[pd.DataFrame] = None

    def _validate_paths(self):
        """Ensures all 4 required MovieLens CSV files exist."""
        required = [
            ("movies.csv", self.movies_path),
            ("ratings.csv", self.ratings_path),
            ("tags.csv", self.tags_path),
            ("links.csv", self.links_path)
        ]
        missing = [name for name, p in required if not p.exists()]
        if missing:
            if self.mode == "full":
                raise FileNotFoundError(
                    f"Full-data mode selected, but the following MovieLens 32M files were not found in {self.data_dir}:\n"
                    f"  {', '.join(missing)}\n\n"
                    f"Please download the official MovieLens 32M dataset from:\n"
                    f"  https://grouplens.org/datasets/movielens/32m/\n"
                    f"Extract the files into '{self.data_dir}' or set the MOVIELENS_DATA_DIR environment variable."
                )
            else:
                raise FileNotFoundError(
                    f"Development dataset files missing in {self.data_dir}: {', '.join(missing)}.\n"
                    f"Please run 'python src/film_aura/make_dev_dataset.py' to generate development data."
                )

    def load_raw_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Loads the raw CSV files into DataFrames with memory-optimized dtypes."""
        dtype_ratings = {"userId": "int32", "movieId": "int32", "rating": "float32", "timestamp": "int32"}
        dtype_movies = {"movieId": "int32", "title": "string", "genres": "string"}
        dtype_tags = {"userId": "int32", "movieId": "int32", "tag": "string", "timestamp": "int32"}
        dtype_links = {"movieId": "int32"}

        self.df_movies = pd.read_csv(self.movies_path, dtype=dtype_movies)
        self.df_ratings = pd.read_csv(self.ratings_path, dtype=dtype_ratings)
        self.df_tags = pd.read_csv(self.tags_path, dtype=dtype_tags)
        self.df_links = pd.read_csv(self.links_path, dtype=dtype_links)
        return self.df_movies, self.df_ratings, self.df_tags, self.df_links

    def get_dataset_summary(self) -> Dict[str, Any]:
        """Returns statistics describing the loaded dataset."""
        if self.df_movies is None:
            self.load_raw_data()

        num_movies = len(self.df_movies)
        num_ratings = len(self.df_ratings)
        num_users = self.df_ratings["userId"].nunique()
        num_tags = len(self.df_tags)
        rating_range = (float(self.df_ratings["rating"].min()), float(self.df_ratings["rating"].max()))
        mean_rating = float(self.df_ratings["rating"].mean())

        # Sparsity calculation
        sparsity = 1.0 - (num_ratings / (num_users * num_movies))

        return {
            "mode": self.mode,
            "data_dir": str(self.data_dir),
            "num_movies": num_movies,
            "num_ratings": num_ratings,
            "num_users": num_users,
            "num_tags": num_tags,
            "rating_range": rating_range,
            "mean_rating": round(mean_rating, 3),
            "sparsity_pct": round(sparsity * 100, 2)
        }

    @staticmethod
    def extract_year(title: str) -> Tuple[str, Optional[int]]:
        """Extracts 4-digit release year from movie title if present."""
        match = re.search(r"\((\d{4})\)\s*$", title)
        if match:
            clean_title = re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()
            return clean_title, int(match.group(1))
        return title.strip(), None

    def prepare_catalog(self, max_tags_per_movie: int = 25) -> pd.DataFrame:
        """
        Prepares unified movie catalogue by merging:
        - Movies (title, cleaned genres, release year)
        - Aggregate rating statistics (vote count, mean rating)
        - Community tags aggregated and ranked by frequency
        - Content corpus representation for NLP vectorization
        """
        if self.df_movies is None:
            self.load_raw_data()

        # 1. Rating statistics per movie
        rating_stats = self.df_ratings.groupby("movieId").agg(
            rating_mean=("rating", "mean"),
            rating_count=("rating", "count")
        ).reset_index()

        # 2. Tag aggregation per movie
        clean_tags = self.df_tags.dropna(subset=["tag"]).copy()
        clean_tags["clean_tag"] = clean_tags["tag"].astype(str).str.strip().str.lower()
        tag_counts = clean_tags.groupby(["movieId", "clean_tag"]).size().reset_index(name="count")
        tag_counts = tag_counts.sort_values(["movieId", "count"], ascending=[True, False])

        # Keep top tags per movie
        top_tags = tag_counts.groupby("movieId").head(max_tags_per_movie)
        tag_agg = top_tags.groupby("movieId")["clean_tag"].apply(lambda tags: list(tags)).reset_index()
        tag_agg = tag_agg.rename(columns={"clean_tag": "tags_list"})

        # 3. Merge catalogue
        cat = self.df_movies.merge(rating_stats, on="movieId", how="left")
        cat = cat.merge(tag_agg, on="movieId", how="left")
        cat = cat.merge(self.df_links, on="movieId", how="left")

        # Fill missing rating stats for cold-start movies
        global_mean = float(self.df_ratings["rating"].mean())
        cat["rating_mean"] = cat["rating_mean"].fillna(global_mean).round(2)
        cat["rating_count"] = cat["rating_count"].fillna(0).astype(int)
        cat["tags_list"] = cat["tags_list"].apply(lambda x: x if isinstance(x, list) else [])

        # Parse year and clean title
        years = []
        clean_titles = []
        for t in cat["title"]:
            ct, yr = self.extract_year(t)
            clean_titles.append(ct)
            years.append(yr if yr is not None else 2000)

        cat["clean_title"] = clean_titles
        cat["year"] = years

        # Parse genres into Python lists
        cat["genres_list"] = cat["genres"].apply(
            lambda g: [x.strip() for x in g.split("|") if x.strip() and x != "(no genres listed)"]
            if isinstance(g, str) else []
        )

        # Build content text corpus for TF-IDF
        content_texts = []
        for _, row in cat.iterrows():
            genres_str = " ".join(row["genres_list"])
            tags_str = " ".join(row["tags_list"])
            # Weight genres and tags heavily
            text = f"{row['clean_title']} {genres_str} {genres_str} {tags_str}"
            content_texts.append(text)

        cat["content_text"] = content_texts
        self.catalog = cat
        return self.catalog

    def build_rating_matrix(
        self,
        min_user_ratings: int = 1,
        min_movie_ratings: int = 1
    ) -> Tuple[csr_matrix, Dict[int, int], Dict[int, int], Dict[int, int], Dict[int, int]]:
        """
        Constructs a sparse CSR user-item rating matrix.
        Returns:
            sparse_matrix: csr_matrix (users x movies)
            user_to_idx: map userId -> row index
            idx_to_user: map row index -> userId
            movie_to_idx: map movieId -> col index
            idx_to_movie: map col index -> movieId
        """
        if self.df_ratings is None:
            self.load_raw_data()

        df_filtered = self.df_ratings.copy()
        if min_user_ratings > 1:
            u_counts = df_filtered["userId"].value_counts()
            valid_users = u_counts[u_counts >= min_user_ratings].index
            df_filtered = df_filtered[df_filtered["userId"].isin(valid_users)]

        if min_movie_ratings > 1:
            m_counts = df_filtered["movieId"].value_counts()
            valid_movies = m_counts[m_counts >= min_movie_ratings].index
            df_filtered = df_filtered[df_filtered["movieId"].isin(valid_movies)]

        unique_users = sorted(df_filtered["userId"].unique())
        unique_movies = sorted(df_filtered["movieId"].unique())

        user_to_idx = {u: i for i, u in enumerate(unique_users)}
        idx_to_user = {i: u for i, u in enumerate(unique_users)}
        movie_to_idx = {m: i for i, m in enumerate(unique_movies)}
        idx_to_movie = {i: m for i, m in enumerate(unique_movies)}

        row_indices = df_filtered["userId"].map(user_to_idx).to_numpy(dtype=np.int32)
        col_indices = df_filtered["movieId"].map(movie_to_idx).to_numpy(dtype=np.int32)
        ratings = df_filtered["rating"].to_numpy(dtype=np.float32)

        matrix = csr_matrix(
            (ratings, (row_indices, col_indices)),
            shape=(len(unique_users), len(unique_movies)),
            dtype=np.float32
        )

        return matrix, user_to_idx, idx_to_user, movie_to_idx, idx_to_movie
