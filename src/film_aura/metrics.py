"""
FilmAura — Offline Evaluation & Recommender Metrics
Implements standard Information Retrieval and Ranking metrics:
- Precision@K
- Recall@K
- HitRate@K
- NDCG@K
- Catalog Coverage
- Novelty
- RMSE and MAE for rating prediction
"""

from typing import List, Set, Dict, Any, Optional
import numpy as np

def precision_at_k(recommended: List[int], relevant: Set[int], k: int = 10) -> float:
    """Calculates Precision@K: proportion of recommended items that are relevant."""
    if k <= 0:
        return 0.0
    rec_k = recommended[:k]
    if not rec_k:
        return 0.0
    hits = sum(1 for item in rec_k if item in relevant)
    return hits / k

def recall_at_k(recommended: List[int], relevant: Set[int], k: int = 10) -> float:
    """Calculates Recall@K: proportion of relevant items captured in top K."""
    if not relevant or k <= 0:
        return 0.0
    rec_k = recommended[:k]
    hits = sum(1 for item in rec_k if item in relevant)
    return hits / len(relevant)

def hit_rate_at_k(recommended: List[int], relevant: Set[int], k: int = 10) -> float:
    """Calculates HitRate@K: 1.0 if at least one relevant item is in top K, else 0.0."""
    rec_k = recommended[:k]
    return 1.0 if any(item in relevant for item in rec_k) else 0.0

def ndcg_at_k(recommended: List[int], relevant: Set[int], k: int = 10) -> float:
    """
    Calculates Normalized Discounted Cumulative Gain (NDCG@K) with binary relevance.
    """
    if not relevant or k <= 0:
        return 0.0
    rec_k = recommended[:k]
    
    dcg = 0.0
    for i, item in enumerate(rec_k):
        if item in relevant:
            # i + 1 is the 1-based rank; discount is log2(rank + 1)
            dcg += 1.0 / np.log2(i + 2)

    # Ideal DCG (all top positions filled with relevant items)
    ideal_hits = min(k, len(relevant))
    idcg = sum(1.0 / np.log2(i + 2) for i in range(ideal_hits))

    return (dcg / idcg) if idcg > 0 else 0.0

def catalog_coverage(all_recommendations: List[List[int]], total_catalog_size: int) -> float:
    """Calculates catalog coverage: percentage of all items recommended at least once."""
    if total_catalog_size <= 0:
        return 0.0
    unique_rec = set()
    for rec_list in all_recommendations:
        unique_rec.update(rec_list)
    return len(unique_rec) / total_catalog_size

def novelty(recommended: List[int], item_popularity: Dict[int, float], k: int = 10) -> float:
    """
    Calculates novelty as mean self-information of recommended items:
    Novelty = - (1 / K) * sum(log2(P(item)))
    where P(item) is relative item popularity (fraction of total ratings).
    """
    rec_k = recommended[:k]
    if not rec_k:
        return 0.0
    self_info = []
    for item in rec_k:
        prob = max(1e-6, item_popularity.get(item, 1e-4))
        self_info.append(-np.log2(prob))
    return float(np.mean(self_info))

def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculates Root Mean Squared Error."""
    if len(y_true) == 0:
        return 0.0
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculates Mean Absolute Error."""
    if len(y_true) == 0:
        return 0.0
    return float(np.mean(np.abs(y_true - y_pred)))
