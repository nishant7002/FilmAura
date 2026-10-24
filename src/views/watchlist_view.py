"""
FilmAura — Watchlist & Cinephile Library View
Manages user saved films, runtime statistics, and viewed status.
"""

from typing import Set
import streamlit as st
from src.recommender import FilmAuraRecommender

def render_watchlist_view(recommender: FilmAuraRecommender):
    """Renders the user's saved films, runtime summary, and library management."""
    watchlist_ids = st.session_state.get("watchlist", [])
    watched_ids = set(st.session_state.get("watched_list", []))

    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span class="material-symbols-outlined" style="color: #7bd0ff;">bookmark</span>
                <span style="font-size: 12px; font-weight: 600; color: #7bd0ff; letter-spacing: 0.05em;">PERSONAL LIBRARY</span>
            </div>
            <h2 style="font-size: 30px; font-weight: 800; color: #ffffff; margin: 0 0 8px 0;">My Watchlist</h2>
            <p style="font-size: 14px; color: #cbc3d7; margin: 0;">
                Curated cinema queue calibrated to your emotional frequencies.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not watchlist_ids:
        st.markdown(
            """
            <div class="aura-card" style="text-align: center; padding: 48px 24px; margin-top: 20px;">
                <div style="font-size: 48px; margin-bottom: 12px;">🍿</div>
                <h3 style="font-size: 20px; font-weight: 700; color: #ffffff; margin-bottom: 6px;">Your Watchlist is Empty</h3>
                <p style="font-size: 14px; color: #cbc3d7; max-width: 480px; margin: 0 auto 20px auto;">
                    You haven't added any films to your queue yet. Use the Taste Calibration to discover movies tuned to your aura.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("✨ Discover Films for My Watchlist", type="primary", use_container_width=True):
                st.session_state.page = "onboarding_mood"
                st.rerun()
        return

    # Aggregate stats
    saved_films = [recommender.get_movie_by_id(mid) for mid in watchlist_ids if recommender.get_movie_by_id(mid)]
    total_runtime_mins = sum(f["runtime"] for f in saved_films)
    total_hours = total_runtime_mins // 60
    rem_mins = total_runtime_mins % 60
    avg_rating = sum(f["rating"] for f in saved_films) / len(saved_films) if saved_films else 0.0

    st.markdown(
        f"""
        <div class="aura-card" style="padding: 18px 24px; background: rgba(26, 31, 48, 0.7); margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div>
                    <div style="font-size: 24px; font-weight: 800; color: #d0bcff;">{len(saved_films)}</div>
                    <div style="font-size: 11px; color: #cbc3d7;">Total Saved</div>
                </div>
                <div style="border-left: 1px solid var(--outline-variant); height: 36px;"></div>
                <div>
                    <div style="font-size: 24px; font-weight: 800; color: #7bd0ff;">{total_hours}h {rem_mins}m</div>
                    <div style="font-size: 11px; color: #cbc3d7;">Total Runtime</div>
                </div>
                <div style="border-left: 1px solid var(--outline-variant); height: 36px;"></div>
                <div>
                    <div style="font-size: 24px; font-weight: 800; color: #f59e0b;">★ {avg_rating:.1f}</div>
                    <div style="font-size: 11px; color: #cbc3d7;">Average Quality</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Saved Films List
    for film in saved_films:
        m_id = film["id"]
        is_watched = m_id in watched_ids
        genres_badge = " ".join([f"<span class='aura-badge-secondary' style='font-size: 10px; padding: 2px 6px;'>{g}</span>" for g in film["genres"]])
        
        st.markdown(
            f"""
            <div class="film-card" style="margin-bottom: 14px;">
                <div class="film-card-body" style="padding: 16px 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                                <h3 style="font-size: 18px; font-weight: 800; color: #ffffff; margin: 0;">{film['title']}</h3>
                                <span style="font-size: 12px; color: #cbc3d7;">({film['year']})</span>
                                {f"<span class='aura-badge-primary' style='font-size: 10px; background: rgba(16, 185, 129, 0.2); color: #10b981; border-color: rgba(16, 185, 129, 0.4);'>Watched</span>" if is_watched else ""}
                            </div>
                            <div style="font-size: 12px; color: #cbc3d7; margin-bottom: 6px;">
                                {film['runtime']}m • Stream on <strong style="color: #dee1f9;">{film['stream_provider']}</strong> • Directed by {film['director']}
                            </div>
                            <div style="display: flex; gap: 6px;">{genres_badge}</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 15px; font-weight: 800; color: #f59e0b;">★ {film['rating']}</span>
                            <span style="font-size: 11px; color: #cbc3d7;">/ 10</span>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_w1, col_w2, col_w3 = st.columns([2, 1, 1])
        with col_w1:
            if st.button(f"View Full Details: {film['title']}", key=f"wl_det_{m_id}", use_container_width=True):
                st.session_state.active_movie_id = m_id
                st.session_state.page = "detail"
                st.rerun()
        with col_w2:
            seen_lbl = "Undo Seen" if is_watched else "Mark Watched"
            if st.button(seen_lbl, key=f"wl_seen_{m_id}", use_container_width=True):
                if is_watched:
                    watched_ids.remove(m_id)
                else:
                    watched_ids.add(m_id)
                st.session_state.watched_list = list(watched_ids)
                st.rerun()
        with col_w3:
            if st.button("🗑️ Remove", key=f"wl_rem_{m_id}", use_container_width=True):
                watchlist_ids.remove(m_id)
                st.session_state.watchlist = watchlist_ids
                st.rerun()

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
