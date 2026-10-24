"""
FilmAura — Taste Calibration View (Screen 3)
Faithfully implements the Stitch Taste Calibration design.
"""

from typing import List
import streamlit as st
from src.data_loader import get_movies_dataframe

def render_taste_calibration_view():
    """Renders Step 2: Taste Calibration & Seed Film Selection."""
    df = get_movies_dataframe()

    # Step progress header
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span class="aura-badge-primary" style="font-size: 11px;">
                    <span class="material-symbols-outlined" style="font-size: 14px;">tune</span>
                    STEP 2 OF 2: TASTE CALIBRATION
                </span>
                <span style="font-size: 12px; font-weight: 700; color: #d0bcff;">100% Calibrated</span>
            </div>
            <div class="diag-bar-bg" style="height: 6px;">
                <div style="background: linear-gradient(90deg, #a078ff, #d0bcff); height: 100%; width: 100%; border-radius: 9999px;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Title & Subtitle
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span class="material-symbols-outlined" style="color: #7bd0ff;">flare</span>
                <span style="font-size: 12px; font-weight: 600; color: #7bd0ff; letter-spacing: 0.05em;">FINAL POLISH</span>
            </div>
            <h2 style="font-size: 28px; font-weight: 700; color: #ffffff; margin: 0 0 8px 0;">Anything you already love?</h2>
            <p style="font-size: 14px; color: #cbc3d7; margin: 0;">
                Anchor your recommendations with a film or director you cherish. Completely optional, always flexible.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    anchored_ids = st.session_state.get("anchor_movie_ids", ["blade-runner-2049-2017"])

    # Search bar to anchor any film
    col_search, col_search_btn = st.columns([4, 1])
    with col_search:
        movie_titles = {f"{row['title']} ({row['year']})": row["id"] for _, row in df.iterrows()}
        selected_search = st.selectbox(
            "Search and anchor a favorite film:",
            options=["Select a film to anchor..."] + list(movie_titles.keys()),
            index=0,
            key="film_search_select"
        )
    with col_search_btn:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Anchor", key="btn_add_search_anchor", use_container_width=True):
            if selected_search and selected_search != "Select a film to anchor...":
                m_id = movie_titles[selected_search]
                if m_id not in anchored_ids:
                    anchored_ids.append(m_id)
                    st.session_state.anchor_movie_ids = anchored_ids
                    st.rerun()

    # Active Anchored Films Container
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if anchored_ids:
        st.markdown(
            f"""
            <div style="margin-bottom: 8px; font-size: 12px; font-weight: 600; color: #7bd0ff; letter-spacing: 0.04em;">
                YOUR ANCHORED FILMS ({len(anchored_ids)} active)
            </div>
            """,
            unsafe_allow_html=True
        )
        anchor_cols = st.columns(max(len(anchored_ids), 1))
        for i, aid in enumerate(anchored_ids):
            match = df[df["id"] == aid]
            if not match.empty:
                title = match.iloc[0]["title"]
                year = match.iloc[0]["year"]
                with anchor_cols[i]:
                    st.markdown(
                        f"""
                        <div class="aura-card" style="padding: 10px 14px; background: rgba(160, 120, 255, 0.15); border: 1px solid var(--primary-container); display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-size: 13px; font-weight: 700; color: #ffffff;">🎬 {title} ({year})</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if st.button("Remove", key=f"btn_remove_anchor_{aid}", use_container_width=True):
                        anchored_ids.remove(aid)
                        st.session_state.anchor_movie_ids = anchored_ids
                        st.rerun()

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Hybrid Blend Slider Controller from Stitch Screen 3
    st.markdown(
        """
        <div class="aura-card" style="padding: 16px 20px; margin-bottom: 24px; background: rgba(26, 31, 48, 0.7);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="material-symbols-outlined" style="color: #a078ff;">bolt</span>
                    <span style="font-size: 15px; font-weight: 700; color: #dee1f9;">Aura Engine Hybrid Blend</span>
                </div>
                <span class="aura-badge-primary">Calibrated</span>
            </div>
            <div style="font-size: 12px; color: #cbc3d7; margin-bottom: 14px;">
                Fine-tune the balance between seed film narrative similarity and emotional mood resonance.
            </div>
        """,
        unsafe_allow_html=True
    )
    blend_slider = st.slider(
        "Content Similarity vs. Mood Resonance Ratio:",
        min_value=10,
        max_value=90,
        value=70,
        step=5,
        format="%d%% Content"
    )
    st.session_state.hybrid_blend = blend_slider
    st.markdown(
        f"""
            <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; color: #dee1f9; margin-top: 6px;">
                <span style="color: #d0bcff;">{blend_slider}% Content Similarity</span>
                <span style="color: #7bd0ff;">{100 - blend_slider}% Mood Resonance</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Recently Loved by Cinephiles (Quick Anchor Suggestions)
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
            <span class="material-symbols-outlined" style="color: #d0bcff;">flare</span>
            <span style="font-size: 16px; font-weight: 700; color: #ffffff;">Recently Loved by Cinephiles</span>
            <span style="font-size: 12px; color: #cbc3d7;">(Tap to anchor)</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    suggested = [
        ("arrival-2016", "Arrival", "2016 • Denis Villeneuve", "94% Aura Match"),
        ("ex-machina-2014", "Ex Machina", "2014 • Alex Garland", "91% Aura Match"),
        ("drive-2011", "Drive", "2011 • Nicolas Winding Refn", "88% Aura Match"),
        ("children-of-men-2006", "Children of Men", "2006 • Alfonso Cuarón", "86% Aura Match")
    ]

    s_cols = st.columns(4)
    for i, (m_id, m_title, m_meta, m_match) in enumerate(suggested):
        with s_cols[i]:
            is_anchored = m_id in anchored_ids
            border_c = "#a078ff" if is_anchored else "var(--outline-variant)"
            bg_c = "rgba(160, 120, 255, 0.15)" if is_anchored else "var(--bg-surface-container)"
            st.markdown(
                f"""
                <div class="aura-card" style="padding: 14px; border: 1px solid {border_c}; background: {bg_c}; margin-bottom: 8px;">
                    <div style="font-size: 14px; font-weight: 700; color: #dee1f9;">{m_title}</div>
                    <div style="font-size: 11px; color: #cbc3d7; margin-bottom: 6px;">{m_meta}</div>
                    <span class="aura-badge-secondary" style="font-size: 10px; padding: 2px 6px;">{m_match}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            btn_txt = "✓ Anchored" if is_anchored else "+ Add Anchor"
            if st.button(btn_txt, key=f"btn_sugg_{m_id}", use_container_width=True):
                if is_anchored:
                    anchored_ids.remove(m_id)
                else:
                    anchored_ids.append(m_id)
                st.session_state.anchor_movie_ids = anchored_ids
                st.rerun()

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Live Aura Synced Card
    moods_str = " • ".join(st.session_state.get("selected_moods", ["Dark", "Suspenseful"]))
    st.markdown(
        f"""
        <div class="aura-card" style="padding: 14px 18px; background: rgba(14, 19, 35, 0.9); border: 1px solid var(--secondary); margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="material-symbols-outlined" style="color: #7bd0ff;">auto_awesome</span>
                <div>
                    <span style="font-size: 12px; font-weight: 700; color: #7bd0ff;">LIVE AURA SYNCED</span>
                    <div style="font-size: 13px; color: #dee1f9;">Active Filters: {moods_str} {f'• {len(anchored_ids)} Anchor Films' if anchored_ids else ''}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Action Buttons
    c_back, c_skip, c_find = st.columns([1, 1, 2])
    with c_back:
        if st.button("← Back to Mood", key="btn_taste_back", use_container_width=True):
            st.session_state.page = "onboarding_mood"
            st.rerun()
    with c_skip:
        if st.button("Skip this step", key="btn_taste_skip", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()
    with c_find:
        if st.button("✨ Find My Movies", key="btn_find_movies_main", type="primary", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()
