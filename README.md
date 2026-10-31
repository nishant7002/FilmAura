# FilmAura — Personalized Movie Recommendation System

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-6.0+-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)

> **Tagline:** *Your mood. Your taste. Your next movie.*

**Course:** Machine Learning Essentials (MLE) — 3rd Year BTech CSE (AI/ML)  
**Author:** Student Capstone Project  
**Core Technologies:** Python, Scikit-learn, React (Vite), Starlette / Uvicorn, Pandas, NumPy, Jupyter Notebook

---

## 1. Project Overview

**FilmAura** is a personalized movie recommendation system designed to solve streaming **choice paralysis**. Instead of forcing users to scroll through endless carousels, FilmAura asks three simple questions:
1. **Current Mood** (e.g. *Dark, Thoughtful, Happy, Romantic*)
2. **Preferred Genre** (e.g. *Sci-Fi, Comedy, Drama*)
3. **(Optional) Cherished Anchor Film** (e.g. *Inception, Blade Runner*)

Using a 4-tier hybrid machine learning engine, FilmAura ranks suitable films and generates an intuitive, human-readable rationale explaining *why* each film was recommended.

---

## 2. Dataset Source & Attribution

FilmAura uses the official **MovieLens 32M** benchmark dataset provided by GroupLens Research:
- **Dataset Source:** [GroupLens MovieLens 32M](https://grouplens.org/datasets/movielens/32m/)
- **Documentation:** [Official MovieLens README](https://files.grouplens.org/datasets/movielens/ml-32m-README.html)
- **Files Used:**
  - `ratings.csv`: ~32,000,000 ratings across 200,900 users.
  - `movies.csv`: ~87,000 movie titles and pipe-separated genres.
  - `tags.csv`: User-applied community tags for thematic content representation.
  - `links.csv`: Identifiers linking to IMDb and TMDb.

---

## 3. Technology Stack

- **Frontend Application:** React 18 with Vite (Modern component architecture, glassmorphism UI, interactive cursor animations).
- **Backend API & Server:** Python Starlette / Uvicorn (High-performance async ASGI server with CORS & static React serving).
- **Core ML Algorithms:** Scikit-learn (`TfidfVectorizer`, `cosine_similarity`, `TruncatedSVD`).
- **Data Manipulation:** Pandas & NumPy (Vectorized array calculations & Bayesian shrinkage).
- **Sparse Computation:** SciPy (`scipy.sparse.csr_matrix` for memory-efficient candidate ranking).
- **Visualizations:** Matplotlib & Seaborn.
- **Testing:** Pytest.
- **Model Training:** Google Colab / Kaggle Notebooks (free cloud CPU/GPU environments).

---

## 4. Simplified Project Structure

```
FilmAura/
├── server.py                          # Unified Python API server (serves React frontend & ML endpoints)
├── recommender.py                     # Standalone vectorized inference engine (loads artifacts)
├── requirements.txt                   # Standard Python dependencies
├── README.md                          # Complete project documentation & viva guide
├── .gitignore                         # Git exclusion rules
├── frontend/                          # Modern React Frontend (Vite)
│   ├── index.html                     # HTML root with fonts & meta
│   ├── package.json                   # Node dependencies (React 18, Vite)
│   ├── vite.config.js                 # Vite proxy & build configuration
│   ├── src/
│   │   ├── main.jsx                   # React root mount
│   │   ├── App.jsx                    # Core recommendation UI component
│   │   ├── index.css                  # Custom cinematic theme, glowing cursor & animations
│   │   └── components/
│   │       └── CursorFollower.jsx     # Interactive inertia-tracked cursor glow trail
│   └── dist/                          # Production-ready pre-built React static assets
├── artifacts/                         # Exported model files for frontend serving
│   ├── config.json                    # Model hyperparameters & mood dictionary
│   ├── movies_catalogue.csv           # Cleaned catalogue with ratings & moods
│   ├── svd_components.npy             # SVD latent item factor matrix
│   ├── tfidf_matrix.npz               # Sparse TF-IDF content matrix
│   ├── tfidf_vectorizer.pkl           # Fitted TF-IDF vectorizer
│   └── README.md                      # Artifact bundle documentation
├── notebooks/
│   ├── FilmAura_ML_Backend_Full_32M.ipynb  # Complete 100% MovieLens 32M training pipeline (Kaggle/Colab)
│   └── FilmAura_ML_Backend_lite.ipynb      # Fast development prototype pipeline
├── app.py                             # Legacy Streamlit alternative
└── tests/
    └── test_recommender.py            # Unit tests for the recommendation engine
```

---

## 5. Machine Learning Pipeline (19 Required Stages)

The central research and training deliverable is available in two dedicated notebooks:
- **`notebooks/FilmAura_ML_Backend_Full_32M.ipynb`**: Trains on the **complete, unsampled MovieLens 32M dataset (~32,000,000 ratings, 87,500+ movies, 200,900+ users, 2,050,000+ tags)** using memory-optimized sparse CSR representations.
- **`notebooks/FilmAura_ML_Backend_lite.ipynb`**: Lightweight prototype notebook for fast local verification.

Both notebooks are organized across all 19 mandatory course stages:
1. **Problem Definition**: Choice paralysis, affective disconnect, top-K ranking vs. rating prediction.
2. **Dataset Acquisition**: Automated download of MovieLens 32M with SSL verification handling.
3. **Dataset Understanding**: Dimensions, data types, timestamp analysis, relational schema.
4. **Data Quality Checks**: Auditing missing values, duplicates, and 0.5–5.0 half-star boundaries.
5. **Exploratory Data Analysis (EDA)**: Matplotlib/Seaborn plots (Figures 1 to 4: rating distributions, active user activity, genre representation, release year histograms).
6. **Data Preprocessing**: Title cleaning, release year extraction via regex, genre parsing into lists.
7. **Feature Engineering**: 10-mood heuristic feature engineering (Happy, Relaxed, Emotional, Romantic, Dark, Suspenseful, Adventurous, Funny, Thoughtful, Motivational).
8. **Feature Selection**: Filtering active items ($\ge 15$ ratings) for collaborative density.
9. **Train, Validation, and Test Split**: Chronological temporal split (80% Train, 10% Validation, 10% Test) to prevent data leakage.
10. **Baseline Model**: Bayesian shrinkage weighted rating formula:
    $$WR = \frac{v}{v+m} R + \frac{m}{v+m} C$$
11. **Model Selection**: Comparing Popularity, Content-Based, Item-Item CF, and SVD.
12. **Model Training**: TF-IDF n-grams, sparse CSR rating matrix, and TruncatedSVD.
13. **Hyperparameter Tuning**: SVD components ($K=15$) and hybrid blend weights on validation split.
14. **Evaluation**: Computing Precision@K, Recall@K, HitRate@K, and NDCG@K on test split.
15. **Model Comparison**: Benchmark evaluation table and comparison bar charts (Figures 6 & 7).
16. **Error Analysis**: Cold-start diagnosis, popularity bias mitigation, and long-tail tag sparsity.
17. **Model Interpretation**: Dynamic natural language explanation generation.
18. **Final Recommendation Demonstration**: Demonstration of seeded and pure cold-start queries.
19. **Conclusion & Model Export**: Summary for viva defense and serializing artifacts to `artifacts/`.

---

## 6. How to Execute the Full 32M Notebook on Kaggle

1. Go to **[kaggle.com/code](https://kaggle.com/code)** and click **"New Notebook"**.
2. Click **File $\rightarrow$ Import Notebook** and upload:
   `notebooks/FilmAura_ML_Backend_Full_32M.ipynb`
3. In the right sidebar under **Settings**:
   - Ensure **Internet** is toggled **ON** (required to download GroupLens dataset).
   - Set **Environment** to Standard CPU or GPU (Standard CPU with 30 GB RAM is more than enough).
4. Click **Run All** (`Shift + Enter` or the double play icon).
5. **What happens during execution (~8-12 minutes total):**
   - Stage 2 downloads the official MovieLens 32M archive (`ml-32m.zip`) in under 60 seconds.
   - Stage 3 loads all ~32,000,000 ratings and all 2,050,000+ community tags.
   - Stage 12 builds a sparse CSR matrix across all ~200,900 users and fits TruncatedSVD in ~90 seconds.
   - Stage 19 exports all artifacts to `/kaggle/working/artifacts/` and automatically creates `filmaura_32m_artifacts.zip`.
6. **Download Artifacts**:
   - In the right-hand panel under **Output** (`/kaggle/working`), click the three dots next to `filmaura_32m_artifacts.zip` and select **Download**.
   - Unzip and copy the files into your local `artifacts/` folder to upgrade your local React application with the full 32M models!

---

## 8. How to Transfer Model Artifacts to Your Local Project

After running in Colab or Kaggle:
1. Run this in a notebook cell to zip and download:
   ```python
   from google.colab import files
   !zip -j -r filmaura_artifacts.zip /content/FilmAura/artifacts/*
   files.download('filmaura_artifacts.zip')
   ```
2. Unzip the downloaded file and place the contents directly into your local `artifacts/` folder:
   ```
   FilmAura/artifacts/
     ├── config.json
     ├── movies_catalogue.csv
     ├── svd_components.npy
     ├── tfidf_matrix.npz
     └── tfidf_vectorizer.pkl
   ```

---

## 9. How to Install and Run FilmAura on Windows

### Step 1: Open PowerShell in the Project Directory
```powershell
cd "C:\Users\Admin\OneDrive\Desktop\Nishant AU\Sem 5\MLE\Project\FilmAura"
```

### Step 2: Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run Automated Unit Tests
```powershell
python -m pytest tests/test_recommender.py -v
```

### Step 4: Launch the FilmAura React Application

#### Option A: One-Command Production Launch (Recommended)
`server.py` hosts the backend API and serves the pre-built React frontend directly on a single port:
```powershell
python server.py
```
*Open your browser at **`http://localhost:8000`** to experience the full React interface.*

#### Option B: React Live Development Mode (Vite Hot Reload)
If you want to edit the React frontend with instant live reloading:

**Terminal 1 (Python Backend API):**
```powershell
python server.py
```

**Terminal 2 (React Vite Dev Server):**
```powershell
cd frontend
npm run dev
```
*Vite will open at `http://localhost:5173` with automatic API proxying to port 8000.*

*(Note: The legacy Streamlit application also remains available via `python -m streamlit run app.py` at `http://localhost:8501` if needed).*

---

## 10. Troubleshooting Common Issues

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **`FileNotFoundError: Required model artifacts are missing`** | App started before training notebook finished or artifacts not downloaded. | Make sure `movies_catalogue.csv`, `tfidf_vectorizer.pkl`, etc. are placed in `artifacts/`. |
| **`wget certificate error` in Colab** | University CA certificate not recognized. | Handled automatically in Cell 1 using `--no-check-certificate`. |
| **Colab Session Out of Memory (OOM)** | Creating dense arrays from 32M interactions. | Handled in notebook: we use sparse CSR matrices and vector mapping instead of dense arrays. |

---

## 11. Project Limitations

1. **Tag Sparsity**: Obscure movies with few reviews rely primarily on genres rather than user tags.
2. **Heuristic Mood Boundaries**: Mood mappings are based on rule-based feature engineering, which provides interpretability but may not capture all subtle emotional nuances.
3. **Streaming Rights**: MovieLens does not include real-time regional streaming provider licenses.
