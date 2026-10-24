"""
FilmAura — About & ML Methodology View
Documents the mathematical foundations, system architecture, and course credits.
"""

import streamlit as st

def render_about_view():
    """Renders the comprehensive architectural and mathematical methodology documentation."""
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span class="material-symbols-outlined" style="color: #d0bcff;">insights</span>
                <span style="font-size: 12px; font-weight: 600; color: #d0bcff; letter-spacing: 0.05em;">ALGORITHMIC ARCHITECTURE</span>
            </div>
            <h2 style="font-size: 30px; font-weight: 800; color: #ffffff; margin: 0 0 8px 0;">About & Methodology</h2>
            <p style="font-size: 14px; color: #cbc3d7; margin: 0;">
                Behind FilmAura's Nocturne Cinema interface: Mathematical rigor meets human emotional resonance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1. Executive Overview Card
    st.markdown(
        """
        <div class="aura-card" style="margin-bottom: 24px;">
            <h3 style="font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 8px;">1. The Problem with Classical Recommenders</h3>
            <p style="font-size: 13px; color: #dee1f9; line-height: 1.6;">
                Most mainstream recommender systems rely predominantly on high-level genre tags or collaborative popularity matrices.
                This results in standard clichés: if a user likes <em>Blade Runner 2049</em>, they are repeatedly recommended mainstream blockbuster Sci-Fi regardless of whether their actual longing is for contemplative existential dread, single-take survival tension, or visual neo-noir melancholy.
            </p>
            <p style="font-size: 13px; color: #dee1f9; line-height: 1.6;">
                <strong>FilmAura solves this via a Tri-Partite Hybrid Engine</strong>:
                combining NLP Vector Space Modeling, 10-Dimensional Mood Tonal Embeddings, and Bayesian Shrinkage quality weighting.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Mathematical Formulations Card
    st.markdown(
        """
        <div class="aura-card" style="margin-bottom: 24px;">
            <h3 style="font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 12px;">2. Mathematical Formulations</h3>
            
            <div style="margin-bottom: 16px;">
                <h4 style="font-size: 15px; font-weight: 700; color: #d0bcff; margin-bottom: 4px;">A. Content Vector Cosine Similarity</h4>
                <p style="font-size: 13px; color: #cbc3d7; line-height: 1.5;">
                    Films are vectorized across rich n-gram feature spaces (unigrams and bigrams) spanning verified synopsis narratives, director styles, cinematographers, lead cast ensembles, and thematic keywords:
                </p>
                <div style="background: rgba(14, 19, 35, 0.9); padding: 12px 16px; border-radius: 10px; font-family: monospace; font-size: 13px; color: #7bd0ff; margin: 8px 0;">
                    Sim(u, v) = (u · v) / (||u|| ||v||) = Σ (u_i * v_i) / ( √Σ(u_i²) * √Σ(v_i²) )
                </div>
            </div>

            <div style="margin-bottom: 16px;">
                <h4 style="font-size: 15px; font-weight: 700; color: #7bd0ff; margin-bottom: 4px;">B. 10-Dimensional Mood Resonance</h4>
                <p style="font-size: 13px; color: #cbc3d7; line-height: 1.5;">
                    Each film in the catalogue possesses calibrated affinity weights across 10 fundamental human mood spectrums (Happy, Relaxed, Emotional, Romantic, Dark, Suspenseful, Adventurous, Funny, Thoughtful, Motivational).
                    When a user anchors a primary mood M_p and secondary twist M_s:
                </p>
                <div style="background: rgba(14, 19, 35, 0.9); padding: 12px 16px; border-radius: 10px; font-family: monospace; font-size: 13px; color: #d0bcff; margin: 8px 0;">
                    Score_mood(Film) = 0.65 · Affinity(Film, M_p) + 0.35 · Affinity(Film, M_s)
                </div>
            </div>

            <div>
                <h4 style="font-size: 15px; font-weight: 700; color: #f472b6; margin-bottom: 4px;">C. Bayesian Shrinkage Rating (IMDb Formula)</h4>
                <p style="font-size: 13px; color: #cbc3d7; line-height: 1.5;">
                    To prevent low-vote niche titles from overwhelming the catalogue while protecting indie classics:
                </p>
                <div style="background: rgba(14, 19, 35, 0.9); padding: 12px 16px; border-radius: 10px; font-family: monospace; font-size: 13px; color: #f472b6; margin: 8px 0;">
                    WR = ( v / (v + m) ) · R + ( m / (v + m) ) · C
                </div>
                <div style="font-size: 12px; color: #cbc3d7; margin-top: 4px;">
                    Where <em>v</em> is number of ratings, <em>m</em> is minimum threshold quantile (35th percentile), <em>R</em> is average rating, and <em>C</em> is mean across the global film set.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. Hybrid Re-ranking & Architecture
    st.markdown(
        """
        <div class="aura-card" style="margin-bottom: 24px;">
            <h3 style="font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 12px;">3. Hybrid Re-Ranking & Score Synthesis</h3>
            <p style="font-size: 13px; color: #dee1f9; line-height: 1.6;">
                The final calibrated Aura Match Score combines the three vectors with user-tunable weights:
            </p>
            <div style="background: rgba(14, 19, 35, 0.9); padding: 12px 16px; border-radius: 10px; font-family: monospace; font-size: 13px; color: #dee1f9; margin: 8px 0;">
                AuraScore = w_content · Sim_content + w_mood · Score_mood + w_collab · Normalized(WR)
            </div>
            <p style="font-size: 13px; color: #dee1f9; line-height: 1.6;">
                Every recommendation presents an <strong>Aura Diagnostic Breakdown</strong>, ensuring total transparency into why the machine learning model selected each title.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4. Mandatory Course & Tech Stack Verification
    st.markdown(
        """
        <div class="aura-card">
            <h3 style="font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 12px;">4. Tech Stack & Environment Constraints</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
                <div style="background: rgba(14, 19, 35, 0.8); padding: 12px; border-radius: 10px; border: 1px solid var(--outline-variant);">
                    <div style="font-size: 11px; color: #7bd0ff; font-weight: 700;">APPLICATION LAYER</div>
                    <div style="font-size: 14px; font-weight: 700; color: #ffffff;">Python & Streamlit</div>
                    <div style="font-size: 11px; color: #cbc3d7;">Single-tier native frontend</div>
                </div>
                <div style="background: rgba(14, 19, 35, 0.8); padding: 12px; border-radius: 10px; border: 1px solid var(--outline-variant);">
                    <div style="font-size: 11px; color: #d0bcff; font-weight: 700;">MACHINE LEARNING</div>
                    <div style="font-size: 14px; font-weight: 700; color: #ffffff;">Scikit-learn, Pandas, NumPy</div>
                    <div style="font-size: 11px; color: #cbc3d7;">TF-IDF & Cosine Similarity</div>
                </div>
                <div style="background: rgba(14, 19, 35, 0.8); padding: 12px; border-radius: 10px; border: 1px solid var(--outline-variant);">
                    <div style="font-size: 11px; color: #10b981; font-weight: 700;">DESIGN SYSTEM</div>
                    <div style="font-size: 14px; font-weight: 700; color: #ffffff;">Google Stitch (Nocturne Cinema)</div>
                    <div style="font-size: 11px; color: #cbc3d7;">Visual Source of Truth</div>
                </div>
                <div style="background: rgba(14, 19, 35, 0.8); padding: 12px; border-radius: 10px; border: 1px solid var(--outline-variant);">
                    <div style="font-size: 11px; color: #f59e0b; font-weight: 700;">COURSE CONTEXT</div>
                    <div style="font-size: 14px; font-weight: 700; color: #ffffff;">Machine Learning Essentials</div>
                    <div style="font-size: 11px; color: #cbc3d7;">Semester 5 Capstone</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
