"""
FilmAura — Streamlit Application
A student-built personalized movie recommendation system.
Tagline: Your mood. Your taste. Your next movie.
"""

import streamlit as st
import streamlit.components.v1 as components
from recommender import FilmAuraRecommender

# Page Configuration
st.set_page_config(
    page_title="FilmAura — Your Mood. Your Taste. Your Next Movie.",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INJECT MODERN EYE-CATCHING STYLING & ANIMATIONS ---
CUSTOM_CSS = """
<style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Custom Glowing Neon Cursor */
html, body, .stApp {
    cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='5' fill='%23a855f7'/%3E%3Ccircle cx='12' cy='12' r='8' fill='%23c084fc' fill-opacity='0.35'/%3E%3Ccircle cx='12' cy='12' r='2' fill='%23ffffff'/%3E%3C/svg%3E") 12 12, auto;
    background: radial-gradient(circle at 15% 15%, rgba(139, 92, 246, 0.16) 0%, transparent 45%),
                radial-gradient(circle at 85% 20%, rgba(236, 72, 153, 0.14) 0%, transparent 40%),
                radial-gradient(circle at 50% 85%, rgba(59, 130, 246, 0.12) 0%, transparent 50%),
                #0b0d17 !important;
    background-attachment: fixed !important;
    color: #e2e8f0;
}

/* Custom Pointer Cursor for interactive elements */
button, [role="button"], input, select, .stSelectbox, .stSlider, a {
    cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 28 28'%3E%3Ccircle cx='14' cy='14' r='8' fill='%23ec4899' fill-opacity='0.85'/%3E%3Cpolygon points='11,9 19,14 11,19' fill='%23ffffff'/%3E%3C/svg%3E") 14 14, pointer !important;
}

/* Hero Title Styling */
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 20%, #c084fc 60%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
    text-shadow: 0 0 35px rgba(168, 85, 247, 0.35);
}

.hero-tagline {
    font-size: 1.25rem;
    font-weight: 500;
    color: #cbd5e1;
    margin-bottom: 1.2rem;
}

.hero-tagline span {
    background: linear-gradient(120deg, #38bdf8, #818cf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}

/* Glassmorphism Control Panel Container */
.control-panel {
    background: linear-gradient(135deg, rgba(26, 21, 46, 0.65) 0%, rgba(15, 17, 30, 0.75) 100%);
    border: 1px solid rgba(168, 85, 247, 0.22);
    border-radius: 18px;
    padding: 24px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    margin-bottom: 2rem;
}

/* Pulsing & Shimmering Submit Button */
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #7c3aed 0%, #db2777 50%, #f59e0b 100%) !important;
    background-size: 200% 200% !important;
    animation: gradientFlow 4s ease infinite, pulseAura 2.5s infinite alternate !important;
    color: #ffffff !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 0.75rem 2rem !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 0 20px rgba(219, 39, 119, 0.45), 0 0 40px rgba(124, 58, 237, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    position: relative !important;
    overflow: hidden !important;
    margin-top: 10px !important;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 30px rgba(219, 39, 119, 0.75), 0 0 60px rgba(124, 58, 237, 0.6) !important;
    border-color: rgba(255, 255, 255, 0.7) !important;
}

div[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(1px) scale(0.98) !important;
    box-shadow: 0 2px 12px rgba(219, 39, 119, 0.4) !important;
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes pulseAura {
    0% { box-shadow: 0 0 15px rgba(219, 39, 119, 0.4), 0 0 30px rgba(124, 58, 237, 0.25); }
    100% { box-shadow: 0 0 28px rgba(219, 39, 119, 0.8), 0 0 55px rgba(124, 58, 237, 0.55); }
}

/* Recommendation Cards */
.film-card {
    background: linear-gradient(135deg, rgba(28, 23, 50, 0.8) 0%, rgba(16, 17, 30, 0.9) 100%);
    border: 1px solid rgba(168, 85, 247, 0.25);
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.45);
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    animation: cardEntrance 0.55s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.film-card:hover {
    transform: translateY(-5px) scale(1.01);
    border-color: rgba(236, 72, 153, 0.6);
    box-shadow: 0 18px 40px -10px rgba(0, 0, 0, 0.6), 0 0 25px rgba(168, 85, 247, 0.3);
}

@keyframes cardEntrance {
    from {
        opacity: 0;
        transform: translateY(22px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Match Percentage Badges */
.match-badge-high {
    background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
    color: #ffffff;
    font-weight: 800;
    font-size: 0.88rem;
    padding: 6px 14px;
    border-radius: 20px;
    box-shadow: 0 0 14px rgba(16, 185, 129, 0.45);
    display: inline-block;
    letter-spacing: 0.5px;
}

.match-badge-mid {
    background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
    color: #ffffff;
    font-weight: 800;
    font-size: 0.88rem;
    padding: 6px 14px;
    border-radius: 20px;
    box-shadow: 0 0 14px rgba(236, 72, 153, 0.45);
    display: inline-block;
    letter-spacing: 0.5px;
}

/* Genre Pills */
.genre-pill {
    display: inline-block;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.35);
    color: #c7d2fe;
    font-size: 0.82rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 8px;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* Why This Movie Callout */
.explanation-box {
    margin-top: 12px;
    padding: 10px 14px;
    background: rgba(236, 72, 153, 0.08);
    border-left: 3px solid #ec4899;
    border-radius: 0 10px 10px 0;
    color: #f1f5f9;
    font-size: 0.92rem;
    line-height: 1.45;
}

/* Intro Hero Card */
.hero-feature-box {
    background: rgba(30, 27, 50, 0.5);
    border: 1px dashed rgba(168, 85, 247, 0.3);
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    color: #94a3b8;
    margin-top: 1rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- INTERACTIVE JAVASCRIPT CURSOR GLOW FOLLOWER ---
CURSOR_JS = """
<script>
(function() {
    try {
        const doc = window.parent.document;
        if (!doc.getElementById('filmaura-cursor-aura')) {
            const aura = doc.createElement('div');
            aura.id = 'filmaura-cursor-aura';
            aura.style.cssText = `
                position: fixed;
                top: 0; left: 0;
                width: 34px; height: 34px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(236, 72, 153, 0.55) 0%, rgba(139, 92, 246, 0.25) 50%, transparent 75%);
                pointer-events: none;
                transform: translate(-50%, -50%);
                transition: width 0.2s ease, height 0.2s ease;
                z-index: 9999999;
                mix-blend-mode: screen;
                filter: drop-shadow(0 0 12px rgba(236, 72, 153, 0.7));
            `;
            doc.body.appendChild(aura);

            const core = doc.createElement('div');
            core.id = 'filmaura-cursor-core';
            core.style.cssText = `
                position: fixed;
                top: 0; left: 0;
                width: 7px; height: 7px;
                border-radius: 50%;
                background: #ffffff;
                pointer-events: none;
                transform: translate(-50%, -50%);
                z-index: 10000000;
                box-shadow: 0 0 8px #c084fc, 0 0 14px #ec4899;
            `;
            doc.body.appendChild(core);

            let mouseX = -100, mouseY = -100;
            let auraX = -100, auraY = -100;

            doc.addEventListener('mousemove', (e) => {
                mouseX = e.clientX;
                mouseY = e.clientY;
                core.style.left = mouseX + 'px';
                core.style.top = mouseY + 'px';
            });

            function animateAura() {
                auraX += (mouseX - auraX) * 0.25;
                auraY += (mouseY - auraY) * 0.25;
                aura.style.left = auraX + 'px';
                aura.style.top = auraY + 'px';
                requestAnimationFrame(animateAura);
            }
            animateAura();

            doc.addEventListener('mousedown', () => {
                aura.style.width = '48px';
                aura.style.height = '48px';
            });

            doc.addEventListener('mouseup', () => {
                aura.style.width = '34px';
                aura.style.height = '34px';
            });
        }
    } catch(e) {
        // Fallback gracefully to CSS cursors if frame access is restricted
    }
})();
</script>
"""
components.html(CURSOR_JS, height=0, width=0)

# --- APPLICATION HEADER ---
st.markdown('<div class="hero-title">🎬 FilmAura</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-tagline">Your mood. Your taste. <span>Your next movie.</span></div>',
    unsafe_allow_html=True
)
st.markdown(
    "Discover cinema tuned precisely to your emotional frequency. "
    "Select your mood, filter by genre, or anchor with a favorite film — then click "
    "**✨ Recommend Movies** to activate the hybrid recommendation pipeline."
)

# --- LOAD RECOMMENDER ENGINE ---
@st.cache_resource
def get_recommender():
    try:
        return FilmAuraRecommender(), None
    except FileNotFoundError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Unexpected error loading model artifacts: {e}"

recommender, error_msg = get_recommender()

if error_msg:
    st.error("⚠️ **Model Artifacts Not Found**")
    st.info(
        "The recommendation model has not been trained or exported yet.\n\n"
        "**To generate artifacts:**\n"
        "1. Open `notebooks/FilmAura_ML_Backend.ipynb` in Google Colab or Kaggle.\n"
        "2. Run all cells to train the hybrid recommender on MovieLens.\n"
        "3. Download the exported files from the `artifacts/` folder into your local `artifacts/` directory.\n\n"
        f"*Details: {error_msg}*"
    )
    st.stop()

# --- MOOD DISPLAY MAPPING ---
MOOD_MAP = {
    "⚡ Dark (Brooding, Psychological, Neo-Noir)": "Dark",
    "🌟 Motivational (Triumph, Perseverance, Inspiring)": "Motivational",
    "😄 Happy (Uplifting, Joyous, Lighthearted)": "Happy",
    "☕ Relaxed (Calm, Serene, Gentle Pace)": "Relaxed",
    "❤️ Romantic (Passionate, Heartfelt, Intimate)": "Romantic",
    "🧭 Adventurous (Daring, Quests, Exploration)": "Adventurous",
    "💭 Thoughtful (Philosophical, Mind-Bending, Cerebral)": "Thoughtful",
    "🎭 Emotional (Moving, Tearjerking, Poignant)": "Emotional",
    "🔍 Suspenseful (Edge-of-Your-Seat, Tense, Mystery)": "Suspenseful",
    "😂 Funny (Hilarious, Witty, Laugh-out-Loud)": "Funny"
}

# --- CONTROL PANEL FORM ---
# Using st.form ensures the application NEVER re-executes or flickers when changing options.
# It ONLY triggers when the user explicitly clicks the "✨ Recommend Movies" submit button!
with st.form("recommendation_query_form", border=True):
    st.markdown("### 🎛️ **Customize Your Taste Profile**")
    
    col1, col2 = st.columns(2)
    with col1:
        mood_labels = list(MOOD_MAP.keys())
        selected_mood_label = st.selectbox(
            "1. Select your current mood:",
            options=mood_labels,
            index=0,
            help="Affective mood archetypes mapped to latent features and tags."
        )
        selected_mood = MOOD_MAP[selected_mood_label]

    with col2:
        raw_genres = recommender.get_available_genres()
        genre_options = ["All Genres"] + raw_genres
        selected_genre = st.selectbox(
            "2. Select preferred genre:",
            options=genre_options,
            index=genre_options.index("Sci-Fi") if "Sci-Fi" in genre_options else 0,
            help="Filters candidates to include your selected genre."
        )

    st.markdown("---")
    
    # Cherished Seed Movie Picker
    movies = recommender.get_movie_titles()
    movie_options = ["None (Recommend based purely on mood & genre resonance)"] + [m["title"] for m in movies]
    
    selected_movie_title = st.selectbox(
        "3. (Optional) Anchor with a cherished film:",
        options=movie_options,
        index=0,
        help="When selected, TF-IDF and SVD will align visual tone, style, and narrative resonance to this movie."
    )

    favorite_movie_id = None
    if selected_movie_title != "None (Recommend based purely on mood & genre resonance)":
        for m in movies:
            if m["title"] == selected_movie_title:
                favorite_movie_id = m["movieId"]
                break

    st.markdown("---")
    
    col_k, col_submit = st.columns([1, 2])
    with col_k:
        top_k = st.slider("Results to display:", min_value=3, max_value=15, value=5)

    with col_submit:
        st.write("")  # Vertical alignment spacing
        submitted = st.form_submit_button("✨ Recommend Movies", use_container_width=True)

# --- EXECUTE RECOMMENDATION ONLY ON SUBMIT ---
if submitted:
    with st.spinner("🔮 FilmAura analyzing collaborative patterns, TF-IDF vectors, and affective resonance..."):
        results = recommender.recommend(
            mood=selected_mood,
            genre=selected_genre if selected_genre != "All Genres" else None,
            favorite_movie_id=favorite_movie_id,
            top_k=top_k
        )
        st.session_state["cached_results"] = results
        st.session_state["last_query"] = {
            "mood": selected_mood,
            "genre": selected_genre,
            "anchor": selected_movie_title if favorite_movie_id else "None"
        }

# --- DISPLAY RECOMMENDATION CARDS ---
if "cached_results" in st.session_state and st.session_state["cached_results"] is not None:
    recs = st.session_state["cached_results"]
    last_q = st.session_state.get("last_query", {})

    st.markdown("---")
    st.markdown(
        f"### 🎯 **Top Recommendations for You** "
        f"<span style='font-size:0.95rem; font-weight:400; color:#94a3b8;'>"
        f"(Mood: <strong style='color:#c084fc;'>{last_q.get('mood')}</strong> | "
        f"Genre: <strong style='color:#38bdf8;'>{last_q.get('genre')}</strong>)</span>",
        unsafe_allow_html=True
    )

    if not recs:
        st.warning("No movies matched all criteria. Try selecting 'All Genres' or a different mood archetype.")
    else:
        for i, film in enumerate(recs, 1):
            badge_class = "match-badge-high" if film["match_pct"] >= 90 else "match-badge-mid"
            genres_html = "".join([f'<span class="genre-pill">{g}</span>' for g in film["genres"]])

            card_html = f"""
            <div class="film-card" style="animation-delay: {i * 0.08}s;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div>
                        <span style="font-size: 1.35rem; font-weight: 700; color: #ffffff;">
                            {i}. {film['title']} 
                            <span style="font-size: 1.05rem; font-weight: 500; color: #94a3b8;">({film['year']})</span>
                        </span>
                    </div>
                    <div>
                        <span class="{badge_class}">⚡ {film['match_pct']}% Match</span>
                    </div>
                </div>
                <div style="margin-bottom: 10px;">
                    {genres_html}
                    <span style="color: #fbbf24; font-size: 0.88rem; font-weight: 600; margin-left: 8px;">
                        ⭐ {film['rating']} / 5.0
                    </span>
                    <span style="color: #64748b; font-size: 0.82rem; margin-left: 4px;">
                        ({film['votes']:,} votes)
                    </span>
                </div>
                <div class="explanation-box">
                    💡 <strong>Why this movie?</strong> {film['explanation']}
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
else:
    # Initial Hero Placeholder before user clicks Recommend
    st.markdown(
        """
        <div class="hero-feature-box">
            <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🍿 🔮 🎬</div>
            <div style="font-size: 1.05rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.3rem;">
                Ready to find your next favorite film?
            </div>
            <div style="font-size: 0.88rem; color: #94a3b8;">
                Customize your mood and taste preferences above, then click 
                <strong style="color: #f472b6;">"✨ Recommend Movies"</strong> to generate your tailored recommendations.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.84rem; padding: 10px 0;'>"
    "🎬 <strong>FilmAura</strong> • Machine Learning Essentials (MLE) Course Project • Built with Python & Streamlit"
    "</div>",
    unsafe_allow_html=True
)
