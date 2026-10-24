"""
FilmAura — Movie Detail View (Screen 5)
Faithfully implements the Stitch Movie Detail View design.
"""

from typing import Dict, Any, Optional
import streamlit as st
from src.components import render_aura_diagnostic
from src.recommender import FilmAuraRecommender

def render_movie_detail_view(recommender: FilmAuraRecommender, movie_id: str):
    """Renders the comprehensive cinematic detail view for a specific film."""
    film = recommender.get_movie_by_id(movie_id)
    if not film:
        st.error(f"Movie with ID '{movie_id}' not found.")
        if st.button("← Back to Results"):
            st.session_state.page = "results"
            st.rerun()
        return

    watchlist = set(st.session_state.get("watchlist", []))
    watched_list = set(st.session_state.get("watched_list", []))
    is_saved = movie_id in watchlist
    is_watched = movie_id in watched_list

    # Back Navigation
    if st.button("← Back to Picks", key="btn_detail_back"):
        st.session_state.page = "results"
        st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Hero Banner
    genres_str = " / ".join(film["genres"])
    runtime_str = f"{film['runtime'] // 60}h {film['runtime'] % 60}m"
    
    st.markdown(
        f"""
        <div class="aura-card" style="background: linear-gradient(180deg, rgba(37, 41, 58, 0.9), rgba(14, 19, 35, 0.95)); border: 1px solid rgba(160, 120, 255, 0.35); padding: 28px; position: relative;">
            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
                <span class="aura-badge-primary">
                    <span class="material-symbols-outlined" style="font-size: 14px;">auto_awesome</span>
                    FilmAura Match: 98%
                </span>
                <span class="aura-badge-secondary">{film.get('quality_badge', '4K Remastered')}</span>
                <span class="aura-badge-secondary" style="color: #dee1f9; border-color: rgba(222, 225, 249, 0.3);">{film.get('age_rating', 'R')}</span>
                <span style="font-size: 13px; color: #cbc3d7; align-self: center; margin-left: 4px;">{runtime_str} • {film['year']}</span>
            </div>
            
            <h1 style="font-size: 36px; font-weight: 800; color: #ffffff; margin: 0 0 8px 0; letter-spacing: -0.02em;">{film['title']}</h1>
            <div style="font-size: 15px; color: #7bd0ff; font-weight: 600; margin-bottom: 14px;">{genres_str}</div>

            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 20px;">
                <div>
                    <span style="font-size: 18px; font-weight: 800; color: #f59e0b;">★ {film['rating']}</span>
                    <span style="font-size: 13px; color: #cbc3d7;">/ 10</span>
                    <span style="font-size: 12px; color: #958ea0; margin-left: 4px;">({film['votes']:,} ratings)</span>
                </div>
                <span class="aura-badge-primary" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border-color: rgba(16, 185, 129, 0.3);">
                    <span class="material-symbols-outlined" style="font-size: 14px;">verified</span>
                    Cinephile Essential
                </span>
                <span style="font-size: 13px; color: #dee1f9;">Stream on <strong>{film['stream_provider']}</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Action Toolbar
    col_act1, col_act2, col_act3, col_act4 = st.columns(4)
    with col_act1:
        wl_txt = "★ In Watchlist" if is_saved else "➕ Add to Watchlist"
        if st.button(wl_txt, key="btn_detail_wl", use_container_width=True):
            if is_saved:
                watchlist.remove(movie_id)
            else:
                watchlist.add(movie_id)
            st.session_state.watchlist = list(watchlist)
            st.rerun()

    with col_act2:
        show_trailer = st.session_state.get("show_trailer", False)
        trailer_btn_label = "🎬 Hide Trailer" if show_trailer else "▶️ Watch Trailer"
        if st.button(trailer_btn_label, key="btn_toggle_trailer", use_container_width=True):
            st.session_state.show_trailer = not show_trailer
            st.rerun()

    with col_act3:
        seen_txt = "✓ Marked as Seen" if is_watched else "👁️ Mark as Seen"
        if st.button(seen_txt, key="btn_detail_seen", use_container_width=True):
            if is_watched:
                watched_list.remove(movie_id)
            else:
                watched_list.add(movie_id)
            st.session_state.watched_list = list(watched_list)
            st.rerun()

    with col_act4:
        if st.button("🔗 Share Film", key="btn_detail_share", use_container_width=True):
            st.toast(f"Link copied for {film['title']}!")

    # Embedded Trailer Player (if activated)
    if st.session_state.get("show_trailer", False):
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.video(film["trailer_url"])

    # Aura Diagnostic Breakdown Widget
    render_aura_diagnostic(
        breakdown={"content_pct": 45, "mood_pct": 35, "collab_pct": 20},
        mood_tags=[("#Dark", 0.92), ("#Suspenseful", 0.88), ("#Visceral", 0.95)],
        seed_name="Blade Runner 2049"
    )

    # Synopsis & Editorial Review
    st.markdown(
        f"""
        <div class="aura-card" style="margin-bottom: 24px;">
            <div style="font-size: 11px; font-weight: 700; color: #7bd0ff; letter-spacing: 0.04em; margin-bottom: 4px;">
                EDITORIAL SYNOPSIS
            </div>
            <h3 style="font-size: 20px; font-weight: 700; color: #ffffff; margin-bottom: 12px;">Synopsis</h3>
            <div style="font-size: 14px; line-height: 1.7; color: #dee1f9; white-space: pre-line;">
                {film['synopsis']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Verified Cast & Crew
    st.markdown(
        """
        <div class="aura-card" style="margin-bottom: 24px;">
            <div style="font-size: 11px; font-weight: 700; color: #d0bcff; letter-spacing: 0.04em; margin-bottom: 4px;">
                VERIFIED CREDITS
            </div>
            <h3 style="font-size: 20px; font-weight: 700; color: #ffffff; margin-bottom: 16px;">Cast & Crew</h3>
        """,
        unsafe_allow_html=True
    )

    c_dir, c_dp = st.columns(2)
    with c_dir:
        st.markdown(
            f"""
            <div class="cast-item">
                <div class="cast-avatar">🎬</div>
                <div>
                    <div style="font-size: 14px; font-weight: 700; color: #ffffff;">{film['director']}</div>
                    <div style="font-size: 12px; color: #7bd0ff;">{film['director_title']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c_dp:
        st.markdown(
            f"""
            <div class="cast-item">
                <div class="cast-avatar">🎥</div>
                <div>
                    <div style="font-size: 14px; font-weight: 700; color: #ffffff;">{film['cinematographer']}</div>
                    <div style="font-size: 12px; color: #d0bcff;">{film['cinematographer_title']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    cast_cols = st.columns(len(film["cast"]))
    for i, actor in enumerate(film["cast"]):
        with cast_cols[i]:
            initials = "".join([part[0] for part in actor["name"].split()[:2]])
            st.markdown(
                f"""
                <div class="cast-item">
                    <div class="cast-avatar">{initials}</div>
                    <div>
                        <div style="font-size: 13px; font-weight: 700; color: #ffffff;">{actor['name']}</div>
                        <div style="font-size: 11px; color: #cbc3d7;">{actor['role']}</div>
                        <div style="font-size: 10px; color: #958ea0;">{actor['category']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # Similar Films in this Vibe (Stitch Screen 5 bottom section)
    st.markdown(
        """
        <div style="margin: 28px 0 16px 0;">
            <div style="font-size: 11px; font-weight: 700; color: #7bd0ff; letter-spacing: 0.04em;">VIBE KINSHIP</div>
            <h3 style="font-size: 20px; font-weight: 700; color: #ffffff; margin: 4px 0;">Similar Films in this Vibe</h3>
            <p style="font-size: 13px; color: #cbc3d7; margin: 0;">Dystopian realism, relentless tension & kinetic cameras</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    sim_cols = st.columns(len(film.get("similar_ids", [])))
    for i, sim_id in enumerate(film.get("similar_ids", [])):
        sim_film = recommender.get_movie_by_id(sim_id)
        if sim_film:
            sim_reason = film.get("similar_reasons", {}).get(sim_id, "Kinship in tone and theme.")
            with sim_cols[i]:
                st.markdown(
                    f"""
                    <div class="aura-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <span style="font-size: 13px; font-weight: 700; color: #f59e0b;">★ {sim_film['rating']}</span>
                                <span class="aura-badge-match" style="font-size: 10px;">90%+</span>
                            </div>
                            <h4 style="font-size: 16px; font-weight: 700; color: #ffffff; margin: 0 0 4px 0;">{sim_film['title']}</h4>
                            <div style="font-size: 11px; color: #7bd0ff; margin-bottom: 8px;">{' / '.join(sim_film['genres'][:2])}</div>
                            <p style="font-size: 12px; color: #cbc3d7; line-height: 1.4;">{sim_reason}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button(f"View {sim_film['title']}", key=f"btn_sim_view_{sim_id}", use_container_width=True):
                    st.session_state.active_movie_id = sim_id
                    st.rerun()
