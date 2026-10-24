"""
FilmAura — Reusable UI Components
Faithfully recreates components from the Google Stitch visual source of truth.
"""

from typing import List, Dict, Any, Optional
import streamlit as st

def render_top_nav(active_page: str = "landing", watchlist_count: int = 0):
    """Renders the top navigation bar with branding, status pill, and section links."""
    col_brand, col_nav = st.columns([1.5, 2.5])
    with col_brand:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div style="background: linear-gradient(135deg, #a078ff, #7bd0ff); width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 12px rgba(160, 120, 255, 0.4);">
                    <span class="material-symbols-outlined" style="color: #0e1323; font-size: 22px;">movie</span>
                </div>
                <div>
                    <span style="font-size: 22px; font-weight: 800; letter-spacing: -0.02em; color: #ffffff;">Film<span style="color: #d0bcff;">Aura</span></span>
                    <span style="background: rgba(160, 120, 255, 0.15); color: #d0bcff; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 9999px; margin-left: 8px; border: 1px solid rgba(208, 188, 255, 0.25);">Discover</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_nav:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🎬 Discover", key="nav_discover", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()
        with c2:
            if st.button("✨ My Aura", key="nav_aura", use_container_width=True):
                st.session_state.page = "onboarding_mood"
                st.rerun()
        with c3:
            wl_label = f"🔖 Watchlist ({watchlist_count})" if watchlist_count > 0 else "🔖 Watchlist"
            if st.button(wl_label, key="nav_watchlist", use_container_width=True):
                st.session_state.page = "watchlist"
                st.rerun()
        with c4:
            if st.button("📊 Engine", key="nav_methodology", use_container_width=True):
                st.session_state.page = "methodology"
                st.rerun()

def render_hero_badges():
    """Renders the floating preview cards in the hero section."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="aura-card" style="padding: 14px; background: rgba(26, 31, 48, 0.6);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 11px; font-weight: 600; color: #7bd0ff; letter-spacing: 0.04em;">SCI-FI NOIR</span>
                    <span style="font-size: 12px; color: #f59e0b; font-weight: 700;">★ 8.6</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span class="material-symbols-outlined" style="color: #7bd0ff; font-size: 16px;">bolt</span>
                    <span style="font-size: 13px; font-weight: 700; color: #dee1f9;">98% Aura Match</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="aura-card" style="padding: 14px; background: rgba(26, 31, 48, 0.6);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 11px; font-weight: 600; color: #d0bcff; letter-spacing: 0.04em;">AMBIENT DRAMA</span>
                    <span style="font-size: 12px; color: #f59e0b; font-weight: 700;">★ 9.1</span>
                </div>
                <div style="font-size: 13px; font-weight: 700; color: #dee1f9; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    Solaris Reverie
                </div>
                <div style="font-size: 11px; color: #cbc3d7;">Matched for: Melancholic & Deep</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="aura-card" style="padding: 14px; background: rgba(26, 31, 48, 0.6);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 11px; font-weight: 600; color: #bec7d7; letter-spacing: 0.04em;">EXISTENTIAL DRIFT</span>
                    <span style="font-size: 12px; color: #f59e0b; font-weight: 700;">★ 8.8</span>
                </div>
                <div style="font-size: 13px; font-weight: 700; color: #dee1f9;">
                    Algorithmic Resonance
                </div>
                <div style="font-size: 11px; color: #7bd0ff;">Tuned for Cinephiles</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_mood_frequency_teasers():
    """Renders the 5 teaser mood frequency cards on the Landing page."""
    teasers = [
        ("🌧️", "Melancholic Noir", "Rain-slicked existential introspection"),
        ("⚡", "Adrenaline Pulse", "Relentless, high-stakes kinetic momentum"),
        ("🌌", "Cosmic Awe", "Vast sublime mysteries beyond time"),
        ("🕯️", "Quiet Intimacy", "Gentle, tender, human vulnerability"),
        ("🪞", "Surreal Dream", "Hallucinatory, mind-bending perception")
    ]
    cols = st.columns(5)
    for i, (emoji, title, desc) in enumerate(teasers):
        with cols[i]:
            st.markdown(
                f"""
                <div class="aura-card" style="padding: 16px 12px; text-align: center; height: 100%;">
                    <div style="font-size: 26px; margin-bottom: 8px;">{emoji}</div>
                    <div style="font-size: 13px; font-weight: 700; color: #dee1f9; margin-bottom: 4px;">{title}</div>
                    <div style="font-size: 11px; color: #cbc3d7; line-height: 1.3;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def render_aura_diagnostic(breakdown: Dict[str, int], mood_tags: List[Any], seed_name: Optional[str] = None):
    """Renders the 'Why FilmAura Recommended This' diagnostic breakdown from Stitch Screen 5."""
    c_pct = breakdown.get("content_pct", 45)
    m_pct = breakdown.get("mood_pct", 35)
    collab_pct = breakdown.get("collab_pct", 20)

    mood_badges_html = " ".join([
        f'<span class="aura-badge-primary" style="font-size: 11px; padding: 2px 8px; margin-right: 4px;">{tag} ({val})</span>'
        for tag, val in mood_tags
    ])

    st.markdown(
        f"""
        <div class="aura-card" style="background: rgba(26, 31, 48, 0.7); margin: 20px 0;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="material-symbols-outlined" style="color: #7bd0ff;">psychology</span>
                    <span style="font-size: 16px; font-weight: 700; color: #ffffff;">Why FilmAura Recommended This</span>
                </div>
                <span class="aura-badge-secondary">Aura Diagnostic</span>
            </div>
            
            <div style="margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600;">
                    <span style="color: #d0bcff;">Content Vector Similarity</span>
                    <span style="color: #dee1f9;">{c_pct}%</span>
                </div>
                <div class="diag-bar-bg"><div class="diag-bar-fill-content" style="width: {c_pct}%;"></div></div>
                <div style="font-size: 12px; color: #cbc3d7;">Atmospheric noir tone, futuristic dystopia, and single-shot hyper-kinetic survival thriller mechanics.</div>
            </div>

            <div style="margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600;">
                    <span style="color: #7bd0ff;">Mood Alignment</span>
                    <span style="color: #dee1f9;">{m_pct}%</span>
                </div>
                <div class="diag-bar-bg"><div class="diag-bar-fill-mood" style="width: {m_pct}%;"></div></div>
                <div style="margin-top: 4px;">{mood_badges_html}</div>
            </div>

            <div>
                <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600;">
                    <span style="color: #f472b6;">Collaborative Filtering Overlap</span>
                    <span style="color: #dee1f9;">{collab_pct}%</span>
                </div>
                <div class="diag-bar-bg"><div class="diag-bar-fill-collab" style="width: {collab_pct}%;"></div></div>
                <div style="font-size: 12px; color: #cbc3d7;">High affinity cross-match with cinephiles who highly rated Denis Villeneuve and Alfonso Cuarón works.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
