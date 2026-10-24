# FilmAura — ML-Powered Cinema Discovery Platform

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![SciPy](https://img.shields.io/badge/SciPy-1.10+-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)

> **"Your mood. Your taste. Your next movie."**

FilmAura is an intelligent cinema discovery platform calibrated for cinephiles. It bridges emotional sentiment with mathematical recommender rigor, translating user moods, tonal preferences, and seed films into bespoke cinema recommendations with explainable rationales in under 60 seconds.

Built as the capstone project for **Machine Learning Essentials (Semester 5)**, FilmAura combines:
1. **Google Stitch UI Design**: Faithful implementation of the approved **Nocturne Cinema** aesthetic directly in Streamlit.
2. **Machine Learning Backend**: Official **MovieLens 32M** dataset integration (`ratings.csv`, `movies.csv`, `tags.csv`, `links.csv`), an executable 14-section Jupyter research notebook, and a 5-tier hybrid recommendation system.

---

## 🎨 Visual Source of Truth: Google Stitch Design System

The visual design is derived directly from the approved Google Stitch project `projects/6513193978623036163`:
- **Theme**: *Nocturne Cinema* (Dark mode)
- **Primary Canvas**: `#0e1323` (Midnight blue/slate)
- **Container Surfaces**: `#1a1f30` (Cards), `#25293a` (High surface), `#2f3446` (Highest surface)
- **Accents**:
  - `#d0bcff` & `#a078ff` (Soft glowing lavender/violet for primary CTAs and headings)
  - `#7bd0ff` (Electric cyan for match scores, badges, and diagnostic metrics)
- **Typography**: `Inter` across all text hierarchies (display, headline, body, label).
- **Aura Diagnostic Graph**: Transparent breakdown showing Content Similarity (40%), Collaborative Filtering (40%), Bayesian Popularity (10%), and Mood Alignment (10%).

---

## 🧠 Machine Learning Backend Architecture

```
                       ┌─────────────────────────┐
                       │   User Interaction UI   │
                       │  (Mood, Genre, Anchor)  │
                       └────────────┬────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   FilmAura Hybrid Recommender Engine                   │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ 1. Content-Based   │ 2. Item-Item CF    │ 3. SVD Matrix Factorization  │
│    TF-IDF (1-2 gram│    Cosine on Item  │    Latent Factor Projections │
│    Title+Genre+Tags│    Rating Vectors  │    (TruncatedSVD K=12)       │
├────────────────────┼────────────────────┴──────────────────────────────┤
│ 4. Bayesian Rating │ 5. Heuristic Mood Resonance Engine                │
│    Shrinkage (WR)  │    10 Affective Spectrums (Genre + Tag Overlap)   │
└────────────────────┴───────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               Explainability & Dynamic Score Attribution               │
│    • Natural Language Rationale ("Resonates with your Dark mood...")    │
│    • Component Breakdown Percentages (Content / Collab / Pop / Mood)   │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. Dual-Mode Dataset Architecture
- **Development Mode (`dev`)**: A verified MovieLens-formatted subset located in `data/dev/` (`movies.csv`, `ratings.csv`, `tags.csv`, `links.csv`) with 60 iconic cinephile titles and ~4,000 ratings. Enables instant local execution, rapid CI testing, and development without downloading multi-gigabyte files.
- **Full-Data Mode (`full`)**: Connects directly to the complete GroupLens **MovieLens 32M** benchmark dataset (`data/ml-32m/`).
  - *Strict Error Handling*: If full mode is selected and files are missing, the loader raises an explicit, descriptive `FileNotFoundError` with download instructions. **It never silently substitutes a smaller dataset.**

### 2. 10 Documented Heuristic Mood Archetypes
FilmAura maps MovieLens genres and aggregated community tags into 10 cinephile moods:
1. **Happy**: Uplifting, bright, feel-good (*Animation, Children, Comedy, Musical*)
2. **Relaxed**: Gentle, calm, contemplative (*Documentary, gentle Comedy*)
3. **Emotional**: Poignant, deep human connection (*Drama, Romance*)
4. **Romantic**: Intimate, passionate, courtship (*Romance, Drama*)
5. **Dark**: Gritty, shadowy, morally ambiguous (*Film-Noir, Crime, Horror, Thriller*)
6. **Suspenseful**: Taut cognitive tension, high-stakes mystery (*Thriller, Mystery, Crime*)
7. **Adventurous**: Epic exploration, heroic journeys (*Adventure, Action, Sci-Fi, Fantasy*)
8. **Funny**: Satirical, absurd, witty (*Comedy*)
9. **Thoughtful**: Existential, philosophical, mind-bending (*Sci-Fi, Mystery, Drama*)
10. **Motivational**: Inspiring perseverance and human triumph (*Drama, Documentary*)

### 3. Five-Tier Hybrid Model Formulation
Candidate movie $i$ is scored for user $u$ as:
$$S_{\text{hybrid}}(u, i) = w_c \cdot S_{\text{content}}(i) + w_k \cdot S_{\text{item\_knn}}(i) + w_{svd} \cdot S_{\text{svd}}(i) + w_p \cdot S_{\text{pop}}(i) + w_m \cdot S_{\text{mood}}(i)$$

- **Cold-Start Fallback**: If a new user arrives with zero ratings and selects no anchor film, weights automatically shift to $w_p = 0.40$ (Bayesian Popularity) and $w_m = 0.35$ (Mood Resonance), filtered strictly by declared genres.

### 4. Offline Benchmark Validation Results
Evaluated on holdout test users:
| Model / Paradigm | Precision@5 | Recall@5 | HitRate@5 | NDCG@5 | Catalog Coverage |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Popularity Baseline (Bayesian WR)** | 0.120 | 0.080 | 0.450 | 0.135 | 25.0% |
| **Content-Based (TF-IDF + Cosine)** | 0.220 | 0.150 | 0.680 | 0.230 | 75.0% |
| **Item-Item Collaborative Filtering** | 0.245 | 0.170 | 0.760 | 0.265 | 65.0% |
| **Matrix Factorization (TruncatedSVD)** | 0.230 | 0.160 | 0.720 | 0.245 | 70.0% |
| **FilmAura Hybrid (Production)** | **0.288** | **0.201** | **0.840** | **0.299** | **90.0%** |

*(HitRate@10 reaches **98.0%** with NDCG@10 of **0.3375** and Novelty of **5.896**).*

---

## 📓 14-Section Executable Notebook

The complete research and training notebook is located at:
`notebooks/FilmAura_ML_Backend.ipynb`

### Notebook Table of Contents:
- **Section 1**: Problem definition & theoretical foundations (ranking vs rating prediction, cold-start formulation).
- **Section 2**: Dataset acquisition, schema inspection, and environment setup (Colab/Kaggle).
- **Section 3**: Data quality auditing (missing values, duplicates, rating boundary validation).
- **Section 4**: Exploratory Data Analysis (EDA) with Matplotlib/Seaborn visualizations (Figures 1 to 5).
- **Section 5**: Preprocessing & heuristic feature engineering (tag aggregation, 10-mood scoring).
- **Section 6**: Content-based recommender (TF-IDF vector space, cosine similarity, queries).
- **Section 7**: Collaborative filtering (Item-Item nearest neighbors over sparse CSR matrix).
- **Section 8**: Matrix factorization (TruncatedSVD latent dimensions, variance curve).
- **Section 9**: FilmAura hybrid recommendation engine (blending weights & cold-start testing).
- **Section 10**: Explainability mechanism & diagnostic attribution breakdown.
- **Section 11**: Quantitative offline evaluation & benchmark comparison table.
- **Section 12**: Discussion of results & viva defense talking points.
- **Section 13**: System limitations and failure modes (sparsity, popularity bias).
- **Section 14**: Export to production (saving `.pkl`, `.npz`, `.npy`, `.csv`, `.json` to `artifacts/`).

### Running in Google Colab / Kaggle:
1. Open Google Colab or Kaggle Notebooks.
2. Upload `notebooks/FilmAura_ML_Backend.ipynb` and the `src/` directory.
3. Download MovieLens 32M:
   ```bash
   !wget https://files.grouplens.org/datasets/movielens/ml-32m.zip
   !unzip -q ml-32m.zip -d data/
   ```
4. Set environment variable:
   ```python
   import os
   os.environ['MOVIELENS_DATA_DIR'] = 'data/ml-32m'
   os.environ['FILMAURA_MODE'] = 'full'
   ```
5. Run all cells.

---

## 🚀 Exact Windows PowerShell Commands to Run Locally

### 1. Navigate to Project Directory
```powershell
cd "C:\Users\Admin\OneDrive\Desktop\Nishant AU\Sem 5\MLE\Project\FilmAura"
```

### 2. Verify Python 3.11 Environment
```powershell
& "C:\Users\Admin\AppData\Local\Programs\Python\Python311\python.exe" --version
```

### 3. Install Required Dependencies
```powershell
& "C:\Users\Admin\AppData\Local\Programs\Python\Python311\python.exe" -m pip install -r requirements.txt
```

### 4. (Optional) Re-generate Model Artifacts
```powershell
& "C:\Users\Admin\AppData\Local\Programs\Python\Python311\python.exe" src/film_aura/export_artifacts.py
```

### 5. Run All Automated Unit Tests (25 Tests)
```powershell
& "C:\Users\Admin\AppData\Local\Programs\Python\Python311\python.exe" -m pytest tests/ -v
```

### 6. Launch the FilmAura Streamlit Application
```powershell
& "C:\Users\Admin\AppData\Local\Programs\Python\Python311\python.exe" -m streamlit run app.py
```
*The application will launch in your default browser at `http://localhost:8501`.*

---

## ☁️ Deployment Instructions (Streamlit Community Cloud)

FilmAura is architected for zero-configuration, 1-click deployment on **Streamlit Community Cloud**:

1. **Commit and Push to GitHub**:
   ```powershell
   git add .
   git commit -m "FilmAura Phase 2: Full ML backend, MovieLens integration, and 14-section notebook"
   git push origin master
   ```
2. **Deploy on Streamlit Community Cloud**:
   - Navigate to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
   - Click **"New app"**.
   - Select your repository (`FilmAura`), branch (`master`), and main file path (`app.py`).
   - Click **"Deploy!"**.
   - Streamlit Cloud installs `requirements.txt`, auto-loads precomputed artifacts from `artifacts/`, and deploys the production URL.

---

## 📂 Project Structure

```
FilmAura/
├── DESIGN.md                          # Full design system & token specification from Stitch
├── README.md                          # Comprehensive setup, ML architecture, & viva guide
├── requirements.txt                   # Production Python dependencies
├── app.py                             # Main Streamlit application entrypoint
├── artifacts/                         # Exported production model artifacts
│   ├── movies_catalogue.csv           # Clean catalogue with parsed metadata & moods
│   ├── tfidf_vectorizer.pkl           # Fitted Scikit-Learn TF-IDF vectorizer
│   ├── tfidf_matrix.npz               # Sparse TF-IDF matrix
│   ├── item_similarity.npy            # Item-Item collaborative similarity matrix
│   ├── svd_components.npy             # SVD item latent factor components
│   ├── config.json                    # Model hyperparameters and mood mappings
│   └── evaluation_metrics.json        # Benchmark offline evaluation metrics
├── data/
│   ├── dev/                           # Verified MovieLens development dataset (committed)
│   │   ├── movies.csv
│   │   ├── ratings.csv
│   │   ├── tags.csv
│   │   └── links.csv
│   └── ml-32m/                        # Full MovieLens 32M directory (git-ignored)
├── notebooks/
│   ├── FilmAura_ML_Backend.ipynb      # Complete 14-section executable ML backend notebook
│   └── FilmAura_ML_Recommender.ipynb  # Exploratory prototyping notebook
├── src/
│   ├── __init__.py
│   ├── styles.py                      # Nocturne Cinema custom CSS stylesheet
│   ├── data_loader.py                 # Frontend data loader & artifact manager
│   ├── recommender.py                 # Frontend recommender engine interface
│   ├── components.py                  # Reusable UI components & Aura Diagnostic widget
│   ├── views/                         # Application screen views (Stitch screens 1-7)
│   └── film_aura/                     # Machine Learning Backend Package
│       ├── __init__.py
│       ├── config.py                  # Paths, mood mappings, default hybrid weights
│       ├── data_loader.py             # Dual-mode MovieLens loader & CSR matrix builder
│       ├── mood_mapper.py             # 10-mood heuristic feature engineering engine
│       ├── models.py                  # Popularity, TF-IDF, Item-Item, SVD, & Hybrid models
│       ├── metrics.py                 # Precision@K, Recall@K, NDCG@K, HitRate@K, Coverage
│       ├── recommender.py             # High-speed production inference engine
│       ├── export_artifacts.py        # Offline training and artifact export script
│       ├── make_dev_dataset.py        # Development dataset generator
│       └── generate_notebook.py       # 14-section Jupyter notebook builder
└── tests/
    ├── test_recommender.py            # Recommender inference unit tests
    └── test_backend.py                # Comprehensive ML backend & metric unit tests (25 tests)
```

---

## 📜 Course Credits & Academic Context

- **Course**: Machine Learning Essentials (Sem 5)
- **Dataset**: GroupLens Research, MovieLens 32M
- **Visual Source of Truth**: Google Stitch (`FilmAura`, project `6513193978623036163`)
- **Theme**: Nocturne Cinema
