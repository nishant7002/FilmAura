# FilmAura — Scalable Movie Recommendation Engine (MovieLens 32M)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-6.0+-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)

> **Tagline:** *Cinema discovery calibrated to your emotional state.*

**Project Type:** Self-Directed Machine Learning Engineering & Recommender Systems Project  
**Core Technologies:** Python 3.11, Scikit-learn, SciPy, Pandas, NumPy, Starlette / Uvicorn, React 18 (Vite), OGL (WebGL)

---

## 1. Project Overview

**FilmAura** is an end-to-end, production-grade movie recommendation platform engineered to resolve streaming **choice paralysis**. Instead of overwhelming viewers with generic carousels, FilmAura personalizes discovery through three complementary input vectors:
1. **Affective Mood Archetype** (e.g. *Dark, Thoughtful, Happy, Romantic, Suspenseful, Adventurous*)
2. **Genre Constraint** (e.g. *Sci-Fi, Film-Noir, Drama, Comedy*)
3. **Optional Anchor Reference Film** (e.g. *Inception, Blade Runner, Spirited Away*)

The recommendation engine benchmarks classical and modern recommendation models across **32 Million user-movie interactions** from the MovieLens 32M benchmark dataset.

---

## 2. Recommendation Architecture & Model Suite

FilmAura benchmarks five distinct model formulations strictly following a progressive recommendation hierarchy:

| Model Slot | Model Name | scikit-learn / Custom Class | What it Learns & How it Works | Hyperparameters Tuned |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline** | **Bayesian Popularity Baseline** | Custom / Empirical Bayes | Uses IMDB Bayesian shrinkage ($WR = \frac{v}{v+m}R + \frac{m}{v+m}C$) to penalize obscure movies with sparse ratings. | Threshold $m \in \{100, 250, 500\}$ ratings |
| **Model 1** | **Item-Item Collaborative Filtering (KNN)** | `sklearn.neighbors.NearestNeighbors` | Explicit instance-based ML model learning item co-occurrence neighborhood vectors across user rating interactions. | `n_neighbors` ($k \in [10, 20, 50]$), `metric` (`'cosine'`, `'correlation'`) |
| **Model 2** | **Latent Matrix Factorization (SVD)** | `sklearn.decomposition.TruncatedSVD` | Unsupervised linear factor model decomposing the 32M sparse matrix into $K$ orthogonal latent taste dimensions minimizing reconstruction error. | `n_components` ($K \in [5, 10, 15, 20]$), `n_iter` ($5, 10, 15$) |
| **Model 3** | **Non-Negative Matrix Factorization (NMF)** | `sklearn.decomposition.NMF` | Unsupervised factor model enforcing non-negative weights ($W \ge 0, H \ge 0$). Highly interpretable because it isolates pure additive themes (e.g., pure comedy, pure noir). | `n_components` ($K \in [10, 15, 20]$), `alpha_W` ($0.0, 0.01, 0.1$) |
| **Additional Model (Ensemble)** | **FilmAura Tri-Hybrid Late-Fusion Ensemble** | Custom Late-Fusion Ensemble | Blends normalized prediction score vectors from Content (TF-IDF), SVD/NMF latent factors, and Bayesian Prior. | Dynamic blend weights ($w_{\text{content}}, w_{\text{mood}}, w_{\text{pop}}$) |

---

## 3. Dataset Source & Scale

FilmAura benchmarks on the official **MovieLens 32M** dataset released by GroupLens Research:
- **Dataset Source:** [GroupLens MovieLens 32M](https://grouplens.org/datasets/movielens/32m/)
- **Documentation:** [Official MovieLens README](https://files.grouplens.org/datasets/movielens/ml-32m-README.html)
- **Data Volume:**
  - `ratings.csv`: **32,000,204 ratings** across **200,905 users** on **87,585 movies**.
  - `tags.csv`: **2,054,618 user-applied community tags** for rich semantic representation.
  - `movies.csv`: Titles, release years, and genre labels.
  - `links.csv`: Identifiers linking to IMDb and TMDb.

---

## 4. Repository Structure

```
FilmAura/
├── server.py                                # Production ASGI API server & static React host
├── recommender.py                           # Vectorized low-latency inference engine
├── requirements.txt                         # Python dependencies
├── README.md                                # Project documentation
├── .gitignore                               # Git exclusion rules (ignores raw data, node_modules, cache)
├── FilmAura_Presentation.pptx               # Complete 16:9 executive presentation deck
├── FilmAura_Project_Report.docx             # Comprehensive technical research report
├── frontend/                                # High-performance React 18 + Vite Web Application
│   ├── index.html                           # Single-page HTML root
│   ├── package.json                         # Frontend dependencies (React, Vite, OGL)
│   ├── vite.config.js                       # Vite proxy & build configuration
│   ├── src/
│   │   ├── main.jsx                         # Application entrypoint
│   │   ├── App.jsx                          # Film discovery UI & recommendation interaction
│   │   ├── index.css                        # Cinema-inspired design system (strict 4px grid)
│   │   └── components/
│   │       ├── Lightfall.jsx                # WebGL cosmic light streak shader background
│   │       └── CursorFollower.jsx           # Cleaned component shell
│   └── dist/                                # Pre-built production static web bundle
├── artifacts/                               # Exported model weights & metadata for web serving
│   ├── config.json                          # Hyperparameters, mood mappings & metadata
│   ├── movies_catalogue.csv                 # Cleaned catalog with community statistics
│   ├── svd_components.npy                   # SVD latent item factor matrix
│   ├── tfidf_matrix.npz                     # Sparse TF-IDF semantic narrative matrix
│   ├── tfidf_vectorizer.pkl                 # Fitted TF-IDF vocabulary vectorizer
│   └── README.md                            # Artifact bundle documentation
├── notebooks/
│   ├── FilmAura_ML_Backend_Full_32M.ipynb   # Complete 32M training pipeline notebook (Kaggle/Colab)
│   └── FilmAura_ML_Backend_lite.ipynb       # Lightweight local prototype pipeline
└── tests/
    └── test_recommender.py                  # Automated unit test suite (pytest)
```

---

## 5. Machine Learning Pipeline Architecture

The complete training and benchmarking pipeline in `notebooks/FilmAura_ML_Backend_Full_32M.ipynb` covers:
1. **Problem Formulation**: Formalizing top-$K$ ranking vs. rating prediction; addressing cold-start and choice paralysis.
2. **Dataset Acquisition**: Automated download and extraction of MovieLens 32M.
3. **Dataset Ingestion & Schema Audit**: Vectorized parsing of interactions and tags.
4. **Data Quality Verification**: Auditing duplicates, null values, and valid rating bounds ($[0.5, 5.0]$).
5. **Exploratory Data Analysis (EDA)**: Rating distributions, user activity long-tails, genre frequencies, release year trends.
6. **Data Preprocessing**: Title regex normalization, 4-digit release year extraction, genre tokenization.
7. **Affective Mood Archetype Engineering**: 10 continuous mood dimensions derived from genre Jaccard similarity and community tag distributions.
8. **Feature Selection & Interaction Matrix**: $k$-core item filtering ($\ge 15$ ratings) and high-density sparse CSR matrix construction.
9. **Leak-Free Temporal Split**: Chronological train (80%), validation (10%), and test (10%) splits.
10. **Baseline Model**: Bayesian shrinkage weighted rating formula ($m \in \{100, 250, 500\}$).
11. **Model 1: Item-Item KNN**: Neighborhood graph model on item interaction profiles with cosine and correlation metrics.
12. **Model 2: Latent Factor SVD**: Dimensionality reduction via randomized TruncatedSVD decomposing 32M interactions into orthogonal latent vectors.
13. **Model 3: Non-Negative Matrix Factorization (NMF)**: Parts-based additive decomposition with non-negativity constraints ($W \ge 0, H \ge 0$).
14. **Additional Model: Tri-Hybrid Late-Fusion Ensemble**: Dynamic convex combination of Content TF-IDF, Factorization Latent Factors, and Bayesian Popularity.
15. **Evaluation Suite**: Top-$K$ ranking metrics evaluated on held-out test interactions (Precision@K, Recall@K, HitRate@K, NDCG@K).
16. **Comparative Analysis & Benchmark Leaderboard**: Quantitative ranking accuracy, latency, and catalog coverage comparisons.
17. **Error Analysis**: Cold-start performance diagnosis and popularity bias trade-offs.
18. **Model Interpretability**: Dynamic rationale generation explaining recommendations.
19. **Artifact Serialization**: Exporting compressed production artifacts for sub-15ms web serving.

---

## 6. How to Run the Training Pipeline on Kaggle

1. Visit **[kaggle.com/code](https://kaggle.com/code)** and click **"New Notebook"**.
2. Click **File $\rightarrow$ Import Notebook** and upload `notebooks/FilmAura_ML_Backend_Full_32M.ipynb`.
3. In the right-hand **Settings** panel:
   - Toggle **Internet** to **ON** (required for downloading MovieLens 32M).
   - Set **Accelerator** to **None (CPU)** or **GPU P100 / T4** (Standard CPU with 30GB RAM executes smoothly in ~8-12 minutes).
4. Run all cells (`Shift + Enter` or click **Run All**).
5. Once completed, navigate to the **Output** section in the right sidebar (`/kaggle/working`), download `filmaura_32m_artifacts.zip`, and extract it into your local `artifacts/` folder.

---

## 7. How to Run FilmAura Locally (Windows / macOS / Linux)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Automated Tests
```bash
python -m pytest tests/test_recommender.py -v
```

### Step 3: Launch Production Web Server
```bash
python server.py
```
Open **`http://localhost:8000`** in any web browser to access the application.

---

## 8. Key Engineering Highlights

- **Scale:** Trained on all 32,000,204 ratings from MovieLens 32M without subsampling.
- **Memory Optimization:** Utilizes Scipy `csr_matrix` and randomized truncated SVD algorithms to keep RAM usage under 4.5 GB during 32M factorization.
- **Latency:** Sub-15ms vector dot-product inference per query via pre-computed normalized factor matrices.
- **Interpretability:** Generates transparent, human-readable explanations detailing why a specific film was surfaced for the user's mood.
