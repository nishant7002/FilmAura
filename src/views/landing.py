"""
FilmAura — Landing Page View (Screen 1)
Faithfully implements the Stitch Landing Page design.
"""

import streamlit as st
from src.components import render_hero_badges, render_mood_frequency_teasers

def render_landing_view():
    """Renders the landing page with hero, teaser frequencies, ML precision pillars, and session launcher."""
    
    # Hero Pill Badge
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px; margin-bottom: 16px;">
            <span class="aura-badge-primary">
                <span class="material-symbols-outlined" style="font-size: 16px;">auto_awesome</span>
                ML-POWERED CINEMA DISCOVERY
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Hero Title and Subtitle
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 24px;">
            <h1 class="hero-glow-title">Find the movie that feels right.</h1>
            <p class="hero-subtitle" style="margin: 0 auto;">
                FilmAura translates your current emotional vibe, taste preferences, and collaborative similarity signals
                into bespoke cinema recommendations in under 60 seconds.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Hero Action Buttons
    c_left, col_cta1, col_cta2, c_right = st.columns([1, 2, 2, 1])
    with col_cta1:
        if st.button("✨ Find My Movie", key="hero_find_movie", type="primary", use_container_width=True):
            st.session_state.page = "onboarding_mood"
            st.rerun()
    with col_cta2:
        if st.button("🍿 Explore Popular Movies", key="hero_explore_pop", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Floating preview cards
    render_hero_badges()

    st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)

    # Mood Frequency Section
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 14px;">
            <div>
                <span class="aura-badge-secondary" style="font-size: 11px; margin-bottom: 6px;">10 FREQUENCIES</span>
                <h3 style="font-size: 20px; font-weight: 700; color: #ffffff; margin: 0;">Explore by Mood Frequency</h3>
            </div>
            <span style="font-size: 12px; color: #cbc3d7;">Select to sample vibe</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    render_mood_frequency_teasers()

    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # Cinephile Precision Pillars
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 24px;">
            <h2 style="font-size: 26px; font-weight: 700; color: #ffffff; margin-bottom: 6px;">Cinephile Precision</h2>
            <p style="font-size: 14px; color: #cbc3d7;">Built on algorithmic rigor, tuned for emotional resonance.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown(
            """
            <div class="aura-card" style="height: 100%;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="background: rgba(0, 166, 224, 0.2); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                        <span class="material-symbols-outlined" style="color: #7bd0ff;">psychology</span>
                    </div>
                    <span class="aura-badge-secondary" style="font-size: 10px;">10 VIBES</span>
                </div>
                <h4 style="font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 6px;">Mood Matching</h4>
                <p style="font-size: 13px; color: #cbc3d7; line-height: 1.5;">
                    Pinpoint your emotional frequency across ten curated tonal spectrums from contemplative quiet to high-voltage thrills.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with p2:
        st.markdown(
            """
            <div class="aura-card" style="height: 100%;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="background: rgba(160, 120, 255, 0.2); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                        <span class="material-symbols-outlined" style="color: #d0bcff;">hub</span>
                    </div>
                    <span class="aura-badge-primary" style="font-size: 10px;">MATRIX FACT.</span>
                </div>
                <h4 style="font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 6px;">Hybrid ML Engine</h4>
                <p style="font-size: 13px; color: #cbc3d7; line-height: 1.5;">
                    Content similarity matrices seamlessly blended with collaborative factorization vectors for zero-cliché suggestions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with p3:
        st.markdown(
            """
            <div class="aura-card" style="height: 100%;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="background: rgba(244, 114, 182, 0.2); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                        <span class="material-symbols-outlined" style="color: #f472b6;">live_tv</span>
                    </div>
                    <span class="aura-badge-secondary" style="font-size: 10px; color: #f472b6; border-color: rgba(244, 114, 182, 0.3);">REAL-TIME</span>
                </div>
                <h4 style="font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 6px;">Live Catalogue</h4>
                <p style="font-size: 13px; color: #cbc3d7; line-height: 1.5;">
                    Continuously refreshed worldwide streaming availability, festival circuits, and archival restorations updated hourly.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)

    # Tonight's Session Banner
    st.markdown(
        """
        <div class="aura-card" style="background: linear-gradient(135deg, rgba(26, 31, 48, 0.95), rgba(47, 52, 70, 0.6)); border: 1px solid rgba(160, 120, 255, 0.3); padding: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div>
                    <span class="aura-badge-primary" style="margin-bottom: 8px;">
                        <span class="material-symbols-outlined" style="font-size: 14px;">schedule</span>
                        TONIGHT'S SESSION
                    </span>
                    <h3 style="font-size: 22px; font-weight: 700; color: #ffffff; margin: 4px 0;">Ready to discover tonight's film?</h3>
                    <p style="font-size: 13px; color: #cbc3d7; margin: 0;">Takes under 60 seconds with our two-step calibrator.</p>
                </div>
                <div style="display: flex; gap: 24px; align-items: center;">
                    <div style="text-align: center;">
                        <div style="font-size: 22px; font-weight: 800; color: #dee1f9;">42,000+</div>
                        <div style="font-size: 11px; color: #cbc3d7;">Films Indexed</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 22px; font-weight: 800; color: #7bd0ff;">94.8%</div>
                        <div style="font-size: 11px; color: #cbc3d7;">Match Precision</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 22px; font-weight: 800; color: #d0bcff;">&lt; 60s</div>
                        <div style="font-size: 11px; color: #cbc3d7;">Recommendation</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    c_btn1, c_btn2, c_btn3 = st.columns([1, 2, 1])
    with c_btn2:
        if st.button("🚀 Start Taste Calibration Now", key="btn_start_calib_banner", type="primary", use_container_width=True):
            st.session_state.page = "onboarding_mood"
            st.rerun()

    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # Footer
    st.markdown(
        """
        <div style="text-align: center; border-top: 1px solid rgba(73, 68, 84, 0.4); padding-top: 24px; margin-top: 32px;">
            <div style="font-size: 13px; color: #cbc3d7; margin-bottom: 8px;">
                <span style="cursor: pointer;">About</span> • 
                <span style="cursor: pointer;">Methodology</span> • 
                <span style="cursor: pointer;">Data Sources</span> • 
                <span style="cursor: pointer;">Privacy</span>
            </div>
            <div style="font-size: 11px; color: #958ea0;">
                © 2026 FilmAura Engine. Calibrated for cinephiles everywhere.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
