"""
FilmAura — Model Artifact Export Pipeline
Trains models on MovieLens dataset (dev or full mode) and exports serialized artifacts
to the artifacts/ directory for high-speed production inference.
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import pickle
import numpy as np
import pandas as pd
from scipy.sparse import save_npz
from sklearn.model_selection import train_test_split

from src.film_aura.config import ARTIFACTS_DIR, DEFAULT_HYBRID_WEIGHTS, MOOD_MAPPINGS
from src.film_aura.data_loader import MovieLensDataLoader
from src.film_aura.models import HybridRecommender
from src.film_aura.metrics import (
    precision_at_k, recall_at_k, hit_rate_at_k, ndcg_at_k,
    catalog_coverage, novelty
)

def run_export_pipeline(mode: str = "dev") -> dict:
    print(f"=== Starting FilmAura Artifact Export Pipeline (Mode: {mode}) ===")
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    # 1. Load Data
    loader = MovieLensDataLoader(mode=mode)
    df_movies, df_ratings, df_tags, df_links = loader.load_raw_data()
    summary = loader.get_dataset_summary()
    print(f"Loaded {summary['num_movies']} movies, {summary['num_ratings']} ratings, {summary['num_users']} users.")

    # 2. Prepare Catalogue
    df_catalog = loader.prepare_catalog()
    rating_matrix, u2r, r2u, m2c, c2m = loader.build_rating_matrix()

    # 3. Fit Hybrid Recommender
    recommender = HybridRecommender(weights=DEFAULT_HYBRID_WEIGHTS)
    recommender.fit(
        df_catalog=df_catalog,
        rating_matrix=rating_matrix,
        user_to_row=u2r,
        row_to_user=r2u,
        movie_to_col=m2c,
        col_to_movie=c2m
    )
    print("Models fitted successfully.")

    # 4. Offline Evaluation
    print("Running offline validation...")
    # Group interactions by user for testing
    user_interactions = df_ratings.groupby("userId")["movieId"].apply(list).to_dict()
    
    # Calculate item popularity distribution for novelty
    pop_series = df_ratings["movieId"].value_counts(normalize=True).to_dict()

    p5_list, r5_list, hr5_list, ndcg5_list = [], [], [], []
    p10_list, r10_list, hr10_list, ndcg10_list = [], [], [], []
    all_recs = []

    # Sample users with at least 5 ratings for evaluation
    eval_users = [u for u, items in user_interactions.items() if len(items) >= 5]
    eval_sample = eval_users[:min(50, len(eval_users))]

    for u in eval_sample:
        items = user_interactions[u]
        # Leave last 20% out as test ground truth
        train_items, test_items = train_test_split(items, test_size=0.2, random_state=42)
        test_set = set(test_items)

        # Seed with first train item
        seed_id = train_items[0] if train_items else None
        anchor_ids = [seed_id] if seed_id else []

        recs = recommender.recommend(
            primary_mood="Thoughtful",
            secondary_mood="Suspenseful",
            anchor_movie_ids=anchor_ids,
            exclude_seen_ids=train_items,
            top_n=10
        )
        rec_ids = [r["movieId"] for r in recs]
        all_recs.append(rec_ids)

        p5_list.append(precision_at_k(rec_ids, test_set, k=5))
        r5_list.append(recall_at_k(rec_ids, test_set, k=5))
        hr5_list.append(hit_rate_at_k(rec_ids, test_set, k=5))
        ndcg5_list.append(ndcg_at_k(rec_ids, test_set, k=5))

        p10_list.append(precision_at_k(rec_ids, test_set, k=10))
        r10_list.append(recall_at_k(rec_ids, test_set, k=10))
        hr10_list.append(hit_rate_at_k(rec_ids, test_set, k=10))
        ndcg10_list.append(ndcg_at_k(rec_ids, test_set, k=10))

    eval_metrics = {
        "dataset_mode": mode,
        "evaluated_users": len(eval_sample),
        "Precision@5": round(float(np.mean(p5_list)), 4),
        "Recall@5": round(float(np.mean(r5_list)), 4),
        "HitRate@5": round(float(np.mean(hr5_list)), 4),
        "NDCG@5": round(float(np.mean(ndcg5_list)), 4),
        "Precision@10": round(float(np.mean(p10_list)), 4),
        "Recall@10": round(float(np.mean(r10_list)), 4),
        "HitRate@10": round(float(np.mean(hr10_list)), 4),
        "NDCG@10": round(float(np.mean(ndcg10_list)), 4),
        "Catalog_Coverage": round(float(catalog_coverage(all_recs, len(df_catalog))), 4),
        "Novelty@10": round(float(np.mean([novelty(r, pop_series, k=10) for r in all_recs])), 4)
    }
    print(f"Evaluation Metrics: {json.dumps(eval_metrics, indent=2)}")

    # 5. Export Artifacts
    # A. Catalogue CSV & Parquet
    cat_export = recommender.df_catalog.copy()
    # Serialize complex columns to json strings for robust csv saving
    cat_export_flat = cat_export.copy()
    cat_export_flat["genres_json"] = cat_export_flat["genres_list"].apply(json.dumps)
    cat_export_flat["tags_json"] = cat_export_flat["tags_list"].apply(json.dumps)
    cat_export_flat["moods_json"] = cat_export_flat["moods"].apply(json.dumps)
    cat_export_flat["dominant_moods_json"] = cat_export_flat["dominant_moods"].apply(json.dumps)

    csv_path = ARTIFACTS_DIR / "movies_catalogue.csv"
    cat_export_flat.to_csv(csv_path, index=False)
    print(f"Exported catalogue to {csv_path}")

    # B. TF-IDF Vectorizer
    tfidf_vec_path = ARTIFACTS_DIR / "tfidf_vectorizer.pkl"
    with open(tfidf_vec_path, "wb") as f:
        pickle.dump(recommender.content.vectorizer, f)
    print(f"Exported TF-IDF Vectorizer to {tfidf_vec_path}")

    # C. TF-IDF Matrix (Sparse NPZ)
    tfidf_mat_path = ARTIFACTS_DIR / "tfidf_matrix.npz"
    save_npz(tfidf_mat_path, recommender.content.tfidf_matrix)
    print(f"Exported TF-IDF Matrix to {tfidf_mat_path}")

    # D. Item-Item Similarity Matrix (Numpy)
    if recommender.item_knn.item_sim_matrix is not None:
        item_sim_path = ARTIFACTS_DIR / "item_similarity.npy"
        np.save(item_sim_path, recommender.item_knn.item_sim_matrix)
        print(f"Exported Item Similarity to {item_sim_path}")

    # E. SVD Components (Numpy)
    if recommender.svd.item_embeddings is not None:
        svd_path = ARTIFACTS_DIR / "svd_components.npy"
        np.save(svd_path, recommender.svd.item_embeddings)
        print(f"Exported SVD Components to {svd_path}")

    # F. Model Metadata & Config JSON
    config_dict = {
        "mode": mode,
        "num_movies": summary["num_movies"],
        "num_ratings": summary["num_ratings"],
        "num_users": summary["num_users"],
        "hybrid_weights": recommender.weights,
        "mood_mappings": MOOD_MAPPINGS,
        "movie_id_map": {str(k): int(v) for k, v in recommender.content.movie_id_to_idx.items()}
    }
    config_path = ARTIFACTS_DIR / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)
    print(f"Exported Config to {config_path}")

    # G. Evaluation Metrics JSON
    metrics_path = ARTIFACTS_DIR / "evaluation_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(eval_metrics, f, indent=2)
    print(f"Exported Metrics to {metrics_path}")

    print("=== Artifact Export Pipeline Completed Successfully! ===")
    return eval_metrics

if __name__ == "__main__":
    run_export_pipeline("dev")
