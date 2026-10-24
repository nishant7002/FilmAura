# FilmAura — ML-Powered Cinema Discovery Platform

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)

FilmAura is an intelligent cinema discovery platform calibrated for cinephiles. It bridges emotional sentiment with mathematical recommender rigor, translating user moods, tonal preferences, and seed films into bespoke cinema recommendations in under 60 seconds.

Built as the capstone project for **Machine Learning Essentials (Semester 5)**, FilmAura implements the approved **Google Stitch** design system (**Nocturne Cinema**) directly into an interactive, high-fidelity Streamlit application.

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
- **Aura Diagnostic Graph**: Transparent breakdown showing Content Similarity (45%), Mood Alignment (35%), and Collaborative Filtering Overlap (20%).

---

## 🚀 Exact Windows PowerShell Commands to Run Locally

### 1. Navigate to Project Directory
```powershell
cd "C:\Users\Admin\OneDrive\Desktop\Nishant AU\Sem 5\MLE\Project\FilmAura"
```

### 2. (Optional) Create and Activate Virtual Environment
```powershell
& "C:\Users\Admin\AppData\Local\Programs\Python\Python311\python.exe" -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```powershell
streamlit run app.py
```
*The application will launch automatically in your browser at `http://localhost:8501`.*

### 5. Run Automated Unit Tests
```powershell
pytest tests\test_recommender.py -v
```

---

## ☁️ Deployment Instructions (Streamlit Community Cloud)

FilmAura is architected for zero-configuration, 1-click deployment on **Streamlit Community Cloud**:

1. **Push to GitHub**:
   ```powershell
   git init
   git add .
   git commit -m "FilmAura initial release: Stitch design implementation with hybrid ML engine"
   git branch -M main
   git remote add origin https://github.com/<your-username>/FilmAura.git
   git push -u origin main
   ```
2. **Deploy on Streamlit Community Cloud**:
   - Navigate to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
   - Click **"New app"**.
   - Select your repository (`<your-username>/FilmAura`), branch (`main`), and main file path (`app.py`).
   - Click **"Deploy!"**.
   - Streamlit Cloud automatically detects `requirements.txt`, installs dependencies, and deploys the production live URL.

---

## 🧠 Machine Learning Engine & Methodology

FilmAura avoids standard collaborative clichés by employing a **Tri-Partite Hybrid Recommender**:

1. **Content-Based Vector Space Model (TF-IDF & Cosine Similarity)**:
   - Synopsis texts, verified cast ensembles, cinematographers, directors, and thematic tags are vectorized into an unigram/bigram feature space.
   - Cosine distance matrix:
     $$\text{Sim}(u, v) = \frac{u \cdot v}{\|u\| \|v\|}$$
2. **10-Dimensional Mood Resonance Embeddings**:
   - 10 fundamental mood spectrums: *Happy, Relaxed, Emotional, Romantic, Dark, Suspenseful, Adventurous, Funny, Thoughtful, Motivational*.
   - Computes weighted dot product against user's primary anchor ($65\%$) and secondary tonal twist ($35\%$).
3. **Bayesian Shrinkage Rating (IMDb Formula)**:
   - Mitigates low-vote bias using empirical Bayesian shrinkage:
     $$WR = \frac{v}{v+m} R + \frac{m}{v+m} C$$
     *(where $m$ is the 35th percentile vote threshold and $C$ is the mean rating across the catalogue).*
4. **Hybrid Score Synthesis**:
   $$\text{AuraScore} = w_{\text{content}} \cdot \text{Sim}_{\text{content}} + w_{\text{mood}} \cdot \text{Score}_{\text{mood}} + w_{\text{collab}} \cdot \text{Normalized}(WR)$$

---

## 🔍 Known Differences: Stitch Prototype vs. Streamlit Implementation

| Feature / Element | Google Stitch Prototype | Streamlit Implementation | Note / Solution |
| :--- | :--- | :--- | :--- |
| **Component Architecture** | Web / React mockup HTML | Python / Streamlit native | Injected customized CSS stylesheet matching Stitch tokens; full responsive layouts without external React dependencies. |
| **Tab Bar Navigation** | Fixed mobile bottom tab bar | Dynamic top navigation bar + sticky control pills | Streamlit's desktop/browser viewport layout is optimized via top navigation and responsive column grids for cinephiles on both desktop and mobile. |
| **Interactive Modals** | Native DOM popup overlays | Streamlit expanders & dynamic session-state views | Trailer video preview and algorithm adjustment drawer are smoothly embedded in-view, preventing disruptive browser popups. |
| **Dynamic Sliders** | Static vector illustration | Live reactive Streamlit slider | Allows users to interactively drag the Content Similarity vs. Mood Resonance blend ratio (default 70% / 30%) with instant live recalculation. |

---

## 📂 Project Structure

```
FilmAura/
├── DESIGN.md                   # Full design system & token specification from Stitch
├── README.md                   # Setup, deployment guide, and architecture docs
├── requirements.txt            # Python dependencies
├── app.py                      # Main Streamlit application entrypoint
├── artifacts/                  # Exported catalogue and similarity caches
├── notebooks/
│   └── FilmAura_ML_Recommender.ipynb  # ML development and experimentation notebook
├── src/
│   ├── __init__.py
│   ├── styles.py               # Nocturne Cinema custom CSS stylesheet
│   ├── data_loader.py          # Curated film dataset and artifact exporter
│   ├── recommender.py          # Hybrid ML recommender engine
│   ├── components.py           # Reusable UI components & Aura Diagnostic widget
│   └── views/
│       ├── landing.py          # Screen 1: Landing Page
│       ├── onboarding_mood.py  # Screen 2: Mood & Genre Onboarding
│       ├── onboarding_taste.py # Screen 3: Taste Calibration
│       ├── results.py          # Screen 4: Recommendation Results
│       ├── movie_detail.py     # Screen 5: Movie Detail View
│       ├── watchlist_view.py   # Screen 6: Personal Watchlist
│       └── about_view.py       # Screen 7: Methodology & Architecture
└── tests/
    └── test_recommender.py     # Unit test suite
```

---

## 📜 Course Credits

- **Course**: Machine Learning Essentials (Sem 5)
- **Design Source**: Google Stitch (`FilmAura`)
- **Visual Palette**: Nocturne Cinema
