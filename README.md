# FilmAura — Personalized Movie Recommendation System

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)

> **Tagline:** *Your mood. Your taste. Your next movie.*

**Course:** Machine Learning Essentials (MLE) — 3rd Year BTech CSE (AI/ML)  
**Author:** Student Capstone Project  
**Core Technologies:** Python, Scikit-learn, Pandas, NumPy, Streamlit, Jupyter Notebook

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

- **Application & Frontend:** Streamlit (Python native interactive UI).
- **Core ML Algorithms:** Scikit-learn (`TfidfVectorizer`, `cosine_similarity`, `TruncatedSVD`).
- **Data Manipulation:** Pandas & NumPy (optimized `int32`/`float32` vector operations).
- **Visualizations:** Matplotlib & Seaborn.
- **Testing:** Pytest.
- **Model Training:** Google Colab / Kaggle Notebooks (free cloud CPU/GPU environments).

---

## 4. Simplified Project Structure

```
FilmAura/
├── app.py                             # Clean, minimal Streamlit web application
├── recommender.py                     # Standalone inference engine (loads artifacts)
├── requirements.txt                   # Standard Python dependencies
├── README.md                          # Complete project documentation & viva guide
├── .gitignore                         # Git exclusion rules
├── artifacts/                         # Exported model files for frontend serving
│   ├── config.json                    # Model hyperparameters & mood dictionary
│   ├── movies_catalogue.csv           # Cleaned catalogue with ratings & moods
│   ├── svd_components.npy             # SVD latent item factor matrix
│   ├── tfidf_matrix.npz               # Sparse TF-IDF content matrix
│   ├── tfidf_vectorizer.pkl           # Fitted TF-IDF vectorizer
│   └── README.md                      # Artifact bundle documentation
├── notebooks/
│   └── FilmAura_ML_Backend.ipynb      # The complete 19-stage ML research notebook
├── data/
│   └── dev/                           # Small test fixtures for unit tests
└── tests/
    └── test_recommender.py            # Unit tests for the recommendation engine
```

---

## 5. Machine Learning Pipeline (19 Required Stages)

The central deliverable is the Jupyter notebook:  
`notebooks/FilmAura_ML_Backend.ipynb`

It is structured into all 19 mandatory course stages:
1. **Problem Definition**: Choice paralysis, affective disconnect, top-K ranking vs. rating prediction.
2. **Dataset Acquisition**: Automated download of MovieLens 32M with SSL verification handling.
3. **Dataset Understanding**: Dimensions, data types, timestamp analysis, relational schema.
4. **Data Quality Checks**: Auditing missing values, duplicates, and 0.5–5.0 half-star boundaries.
5. **Exploratory Data Analysis (EDA)**: Matplotlib/Seaborn plots (Figures 1 to 4: rating distributions, active user activity, genre representation, release year histograms).
6. **Data Preprocessing**: Title cleaning, release year extraction via regex, genre parsing into lists.
7. **Feature Engineering**: 10-mood heuristic feature engineering (Happy, Relaxed, Emotional, Romantic, Dark, Suspenseful, Adventurous, Funny, Thoughtful, Motivational).
8. **Feature Selection**: Filtering active items ($\ge 25$ ratings) for collaborative density.
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

## 6. How to Execute the Notebook in Google Colab

1. Open **[colab.research.google.com](https://colab.research.google.com)**.
2. Click **Upload** $\rightarrow$ select `notebooks/FilmAura_ML_Backend.ipynb`.
3. In the top menu, click **Runtime $\rightarrow$ Run all** (`Ctrl + F9`).
4. Cell 1 will automatically:
   - Download the official MovieLens 32M archive (`--no-check-certificate`).
   - Extract it into `data/ml-32m/`.
   - Run all 19 stages and export production artifacts to `/content/FilmAura/artifacts/`.

---

## 7. How to Execute the Notebook in Kaggle

1. Go to **[kaggle.com/code](https://kaggle.com/code)** and click **"New Notebook"**.
2. Click **File $\rightarrow$ Import Notebook** $\rightarrow$ select `FilmAura_ML_Backend.ipynb`.
3. In the right panel under **Settings**, ensure Internet is **ON**.
4. Click **Run All** (`Shift + Enter`).
5. Artifacts are automatically exported to `/kaggle/working/artifacts/`.

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

### Step 2: (Optional) Create & Activate a Virtual Environment
```powershell
& "C:\Users\Admin\AppData\Local\Programs\Python\Python311\python.exe" -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run Automated Unit Tests
```powershell
pytest tests/test_recommender.py -v
```

### Step 5: Launch the Streamlit Frontend
```powershell
streamlit run app.py
```
*FilmAura will open automatically in your browser at `http://localhost:8501`.*

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
