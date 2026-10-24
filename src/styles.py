"""
FilmAura — Design System & Custom CSS Styling Module
Faithfully implements the 'Nocturne Cinema' design tokens from Google Stitch.
"""

def get_custom_css() -> str:
    return """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet">

<style>
/* Reset and base background */
:root {
    --bg-surface: #0e1323;
    --bg-surface-lowest: #080d1d;
    --bg-surface-low: #161b2b;
    --bg-surface-container: #1a1f30;
    --bg-surface-container-high: #25293a;
    --bg-surface-container-highest: #2f3446;
    --primary: #d0bcff;
    --primary-container: #a078ff;
    --on-primary: #3c0091;
    --secondary: #7bd0ff;
    --secondary-container: #00a6e0;
    --tertiary: #bec7d7;
    --on-surface: #dee1f9;
    --on-surface-variant: #cbc3d7;
    --outline: #958ea0;
    --outline-variant: #494454;
    --error: #ffb4ab;
}

/* Force Streamlit app background */
.stApp {
    background-color: var(--bg-surface) !important;
    color: var(--on-surface) !important;
    font-family: 'Inter', sans-serif !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Hide default streamlit menu decoration */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg-surface-lowest);
}
::-webkit-scrollbar-thumb {
    background: var(--outline-variant);
    border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--primary-container);
}

/* Typography classes */
.font-inter {
    font-family: 'Inter', sans-serif;
}

.text-on-surface {
    color: var(--on-surface);
}

.text-on-surface-variant {
    color: var(--on-surface-variant);
}

.text-primary {
    color: var(--primary);
}

.text-secondary {
    color: var(--secondary);
}

.text-tertiary {
    color: var(--tertiary);
}

/* Material Symbols Icon support */
.material-symbols-outlined {
    font-family: 'Material Symbols Outlined' !important;
    font-weight: normal;
    font-style: normal;
    font-size: 20px;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
    vertical-align: middle;
}

/* Container cards */
.aura-card {
    background-color: var(--bg-surface-container);
    border: 1px solid var(--outline-variant);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 20px -2px rgba(10, 14, 28, 0.6);
    transition: all 0.25s ease-in-out;
}

.aura-card:hover {
    border-color: var(--primary-container);
    box-shadow: 0 8px 30px -4px rgba(160, 120, 255, 0.15);
}

.aura-card-interactive {
    background-color: var(--bg-surface-container);
    border: 1px solid var(--outline-variant);
    border-radius: 14px;
    padding: 16px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.aura-card-interactive:hover {
    background-color: var(--bg-surface-container-high);
    border-color: var(--secondary);
    transform: translateY(-2px);
}

.aura-card-selected {
    background-color: rgba(160, 120, 255, 0.12) !important;
    border: 2px solid var(--primary-container) !important;
    box-shadow: 0 0 16px rgba(160, 120, 255, 0.25);
}

/* Pills and Badges */
.aura-badge-primary {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(160, 120, 255, 0.18);
    color: var(--primary);
    border: 1px solid rgba(208, 188, 255, 0.3);
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.04em;
}

.aura-badge-secondary {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0, 166, 224, 0.18);
    color: var(--secondary);
    border: 1px solid rgba(123, 208, 255, 0.3);
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.04em;
}

.aura-badge-match {
    background: linear-gradient(135deg, rgba(160, 120, 255, 0.25), rgba(123, 208, 255, 0.25));
    border: 1px solid var(--secondary);
    color: var(--secondary);
    font-weight: 700;
    font-size: 13px;
    padding: 3px 10px;
    border-radius: 9999px;
}

/* Hero Section */
.hero-glow-title {
    font-size: 2.75rem;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 30%, var(--primary) 70%, var(--secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
}

.hero-subtitle {
    font-size: 1.05rem;
    line-height: 1.6;
    color: var(--on-surface-variant);
    max-width: 680px;
    margin-bottom: 24px;
}

/* Diagnostic Progress Bar */
.diag-bar-bg {
    background: var(--bg-surface-lowest);
    border-radius: 9999px;
    height: 8px;
    width: 100%;
    overflow: hidden;
    margin: 6px 0 10px 0;
}

.diag-bar-fill-content {
    background: linear-gradient(90deg, #a078ff, #d0bcff);
    height: 100%;
    border-radius: 9999px;
}

.diag-bar-fill-mood {
    background: linear-gradient(90deg, #00a6e0, #7bd0ff);
    height: 100%;
    border-radius: 9999px;
}

.diag-bar-fill-collab {
    background: linear-gradient(90deg, #ec4899, #f472b6);
    height: 100%;
    border-radius: 9999px;
}

/* Streamlit buttons custom overrides */
div.stButton > button {
    background-color: var(--bg-surface-container);
    color: var(--on-surface);
    border: 1px solid var(--outline-variant);
    border-radius: 9999px;
    padding: 8px 20px;
    font-weight: 600;
    font-size: 14px;
    transition: all 0.2s ease-in-out;
}

div.stButton > button:hover {
    background-color: var(--bg-surface-container-high);
    border-color: var(--primary);
    color: #ffffff;
    box-shadow: 0 0 12px rgba(160, 120, 255, 0.3);
}

div.stButton > button:active {
    transform: scale(0.98);
}

/* Primary buttons in Streamlit */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--primary-container), #8b5cf6) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(160, 120, 255, 0.4) !important;
}

div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 22px rgba(160, 120, 255, 0.6) !important;
    transform: translateY(-1px);
}

/* Streamlit input fields */
div[data-baseweb="input"] {
    background-color: var(--bg-surface-lowest) !important;
    border: 1px solid var(--outline-variant) !important;
    border-radius: 12px !important;
    color: var(--on-surface) !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 10px rgba(160, 120, 255, 0.3) !important;
}

div[data-baseweb="input"] input {
    color: var(--on-surface) !important;
}

/* Streamlit Selectbox and Multiselect */
div[data-baseweb="select"] {
    background-color: var(--bg-surface-lowest) !important;
    border-radius: 12px !important;
}

/* Top Navigation Bar */
.top-nav-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 18px;
    background-color: rgba(26, 31, 48, 0.8);
    backdrop-filter: blur(12px);
    border: 1px solid var(--outline-variant);
    border-radius: 16px;
    margin-bottom: 24px;
}

.brand-container {
    display: flex;
    align-items: center;
    gap: 10px;
}

.brand-logo-text {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff, var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Cinematic film card */
.film-card {
    position: relative;
    background: var(--bg-surface-container);
    border: 1px solid var(--outline-variant);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 20px;
    transition: all 0.25s ease;
}

.film-card:hover {
    border-color: var(--primary-container);
    box-shadow: 0 8px 32px rgba(14, 19, 35, 0.8), 0 0 20px rgba(160, 120, 255, 0.2);
}

.film-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 18px;
    border-bottom: 1px solid rgba(73, 68, 84, 0.35);
}

.film-card-body {
    padding: 18px;
}

.film-rationale-box {
    background: rgba(14, 19, 35, 0.7);
    border-left: 3px solid var(--secondary);
    border-radius: 0 10px 10px 0;
    padding: 12px 14px;
    margin: 14px 0;
    font-size: 13px;
    line-height: 1.5;
    color: var(--on-surface);
}

/* Cast & Crew avatar circles */
.cast-item {
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--bg-surface-container-high);
    padding: 10px 14px;
    border-radius: 12px;
    border: 1px solid var(--outline-variant);
}

.cast-avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-container), var(--secondary));
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
    color: #ffffff;
}
</style>
"""
