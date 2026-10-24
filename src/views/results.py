"""
FilmAura — Recommendation Results View (Screen 4)
Faithfully implements the Stitch Recommendation Results design.
"""

from typing import List, Dict, Any
import streamlit as st
from src.recommender import FilmAuraRecommender

def render_results_view(recommender: FilmAuraRecommender):
    """Renders the recommendation results with ranking, rationale, quick filters, and sorting."""
    
    # Session state variables
    selected_moods = st.session_state.get("selected_moods", ["Dark", "Suspenseful"])
    primary_mood = selected_moods[0] if len(selected_moods) > 0 else "Dark"
    secondary_mood = selected_moods[1] if len(selected_moods) > 1 else "Suspenseful"
    anchored_ids = st.session_state.get("anchor_movie_ids", ["blade-runner-2049-2017"])
    watchlist = set(st.session_state.get("watchlist", []))
    watched_list = set(st.session_state.get("watched_list", []))

    # Top Bar & Breadcrumb
    col_back, col_chips, col_adj = st.columns([1, 4, 1.5])
    with col_back:
        if st.button("← Back", key="btn_results_back", use_container_width=True):
            st.session_state.page = "onboarding_taste"
            st.rerun()

    with col_chips:
        mood_label = f"{primary_mood} + {secondary_mood}" if secondary_mood else primary_mood
        ref_title = "Blade Runner 2049"
        if anchored_ids:
            match = recommender.get_movie_by_id(anchored_ids[0])
            if match:
                ref_title = match["title"]
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                <span class="aura-badge-secondary" style="font-size: 11px;">{mood_label}</span>
                <span class="aura-badge-primary" style="font-size: 11px;">Ref: {ref_title}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_adj:
        if st.button("⚙️ Adjust Calibration", key="btn_adjust_calib", use_container_width=True):
            st.session_state.page = "onboarding_mood"
            st.rerun()

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Title & Subtitle
    st.markdown(
        """
        <h2 style="font-size: 30px; font-weight: 800; color: #ffffff; margin-bottom: 6px;">Your FilmAura picks.</h2>
        <p style="font-size: 14px; color: #cbc3d7; margin-bottom: 20px;">
            Matched based on high cognitive tension, dystopian atmosphere, and collaborative resonance with 14,200 cinephiles.
        </p>
        """,
        unsafe_allow_html=True
    )

    # Controls & Filter Bar
    c_sort, c_togg1, c_togg2, c_togg3 = st.columns([1.5, 1, 1, 1])
    with c_sort:
        sort_by = st.selectbox(
            "Sort recommendations:",
            options=["Aura Score", "Highest Rating", "Release Year"],
            index=0,
            key="sort_by_select"
        )
    with c_togg1:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        stream_only = st.checkbox("Streaming Only", value=False, key="check_stream_only")
    with c_togg2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        under_2h = st.checkbox("Under 2 Hours", value=False, key="check_under_2h")
    with c_togg3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        exclude_seen = st.checkbox("Exclude Seen", value=False, key="check_exclude_seen")

    # Calculate recommendations
    recs = recommender.recommend(
        primary_mood=primary_mood,
        secondary_mood=secondary_mood,
        selected_genres=st.session_state.get("selected_genres", []),
        anchor_movie_ids=anchored_ids,
        filter_under_2h=under_2h,
        filter_stream_only=stream_only,
        exclude_seen_ids=list(watched_list) if exclude_seen else [],
        sort_by=sort_by,
        top_n=8
    )

    st.markdown(
        f"""
        <div style="font-size: 13px; font-weight: 700; color: #7bd0ff; letter-spacing: 0.04em; margin: 18px 0 12px 0;">
            {len(recs)} TOP MATCHES DISCOVERED
        </div>
        """,
        unsafe_allow_html=True
    )

    if not recs:
        st.info("No films matched all active strict filters. Try loosening 'Under 2 Hours' or genre constraints.")
        return

    # Render Ranked Film Cards
    for i, film in enumerate(recs):
        rank = i + 1
        m_id = film["id"]
        is_saved = m_id in watchlist
        genre_chips = " ".join([f"<span class='aura-badge-secondary' style='font-size: 10px; padding: 2px 6px;'>{g}</span>" for g in film["genres"]])

        st.markdown(
            f"""
            <div class="film-card">
                <div class="film-card-header">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 16px; font-weight: 800; color: #a078ff;">#{rank}</span>
                        <span class="aura-badge-match">
                            <span class="material-symbols-outlined" style="font-size: 14px; vertical-align: middle;">bolt</span>
                            {film['aura_match_pct']}% Match
                        </span>
                        <span style="font-size: 12px; color: #cbc3d7;">• {film['runtime']}m • {film['year']}</span>
                    </div>
                    <span style="font-size: 12px; color: #10b981; font-weight: 600;">
                        <span class="material-symbols-outlined" style="font-size: 14px; vertical-align: middle;">check_circle</span>
                        {film['stream_provider']}
                    </span>
                </div>
                <div class="film-card-body">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <div>
                            <h3 style="font-size: 20px; font-weight: 800; color: #ffffff; margin: 0 0 4px 0;">{film['title']}</h3>
                            <div style="display: flex; gap: 6px; align-items: center;">{genre_chips}</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 15px; font-weight: 800; color: #f59e0b;">★ {film['rating']}</span>
                            <span style="font-size: 12px; color: #cbc3d7;">/ 10</span>
                            <div style="font-size: 11px; color: #958ea0;">{film['votes']:,} votes</div>
                        </div>
                    </div>
                    
                    <div class="film-rationale-box">
                        <div style="font-weight: 700; color: #7bd0ff; margin-bottom: 2px;">
                            <span class="material-symbols-outlined" style="font-size: 14px; vertical-align: middle;">psychology</span>
                            FilmAura Rationale
                        </div>
                        {film['rationale']}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_wl, col_det = st.columns([1, 1])
        with col_wl:
            wl_btn_label = "★ Saved to Watchlist" if is_saved else "➕ Add to Watchlist"
            if st.button(wl_btn_label, key=f"btn_wl_res_{m_id}_{i}", use_container_width=True):
                if is_saved:
                    watchlist.remove(m_id)
                else:
                    watchlist.add(m_id)
                st.session_state.watchlist = list(watchlist)
                st.rerun()

        with col_det:
            if st.button(f"Details for {film['title']} →", key=f"btn_det_{m_id}_{i}", type="primary", use_container_width=True):
                st.session_state.active_movie_id = m_id
                st.session_state.page = "detail"
                st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Looking for different vibes? Drawer
    with st.expander("🔍 Looking for different vibes? Adjust strictness or explore prompt shortcuts"):
        st.markdown(
            """
            <div style="font-size: 13px; color: #dee1f9; margin-bottom: 12px;">
                Your current algorithm is dialed to <strong>Maximum Suspense & Dystopian</strong>.
                Tap any prompt below to immediately re-sample FilmAura's neural index:
            </div>
            """,
            unsafe_allow_html=True
        )
        c_p1, c_p2, c_p3 = st.columns(3)
        with c_p1:
            if st.button("➕ Neo-Noir Cyberpunk", key="btn_shortcut_cyber"):
                st.session_state.selected_moods = ["Dark", "Thoughtful"]
                st.rerun()
        with c_p2:
            if st.button("➕ Slow-burn Mystery", key="btn_shortcut_mystery"):
                st.session_state.selected_moods = ["Suspenseful", "Thoughtful"]
                st.rerun()
        with c_p3:
            if st.button("⚡ Reset All Filters", key="btn_shortcut_reset"):
                st.session_state.selected_moods = ["Dark", "Suspenseful"]
                st.session_state.anchor_movie_ids = ["blade-runner-2049-2017"]
                st.rerun()
        
        st.markdown(
            """
            <div style="font-size: 11px; color: #958ea0; margin-top: 12px;">
                Engine: Collaborative & Semantic V3.4 • Calibrated for cinephiles.
            </div>
            """,
            unsafe_allow_html=True
        )
