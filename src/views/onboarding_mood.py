"""
FilmAura — Mood & Genre Onboarding View (Screen 2)
Faithfully implements the Stitch Mood & Genre Onboarding design.
"""

from typing import List, Optional
import streamlit as st
from src.data_loader import get_movies_dataframe

MOOD_DEFINITIONS = [
    {"name": "Happy", "emoji": "☀️", "desc": "uplifting & bright", "key": "happy"},
    {"name": "Relaxed", "emoji": "🌿", "desc": "calm & gentle", "key": "relaxed"},
    {"name": "Emotional", "emoji": "💧", "desc": "deep & poignant", "key": "emotional"},
    {"name": "Romantic", "emoji": "💫", "desc": "intimate & poetic", "key": "romantic"},
    {"name": "Dark", "emoji": "🌑", "desc": "shadowy & bleak", "key": "dark"},
    {"name": "Suspenseful", "emoji": "⚡", "desc": "taut & high-stakes", "key": "suspenseful"},
    {"name": "Adventurous", "emoji": "🧭", "desc": "thrilling exploration", "key": "adventurous"},
    {"name": "Funny", "emoji": "🎭", "desc": "witty & absurd", "key": "funny"},
    {"name": "Thoughtful", "emoji": "🧠", "desc": "mind-bending cinema", "key": "thoughtful"},
    {"name": "Motivational", "emoji": "🔥", "desc": "inspiring triumph", "key": "motivational"},
]

ALL_GENRES = [
    "Sci-Fi", "Thriller", "Drama", "Mystery", "Action", "Crime",
    "Neo-Noir", "Psychological Horror", "Comedy", "Adventure", "Survival"
]

def render_mood_onboarding_view():
    """Renders Step 1: Mood & Genre Calibration."""
    df = get_movies_dataframe()

    # Step progress header
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span class="aura-badge-primary" style="font-size: 11px;">
                    <span class="material-symbols-outlined" style="font-size: 14px;">tune</span>
                    STEP 1 OF 2: MOOD & VIBE
                </span>
                <span style="font-size: 12px; font-weight: 700; color: #7bd0ff;">50% Calibrated</span>
            </div>
            <div class="diag-bar-bg" style="height: 6px;">
                <div style="background: linear-gradient(90deg, #a078ff, #7bd0ff); height: 100%; width: 50%; border-radius: 9999px;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Question & subtext
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span class="material-symbols-outlined" style="color: #d0bcff;">psychology_alt</span>
                <span style="font-size: 12px; font-weight: 600; color: #d0bcff; letter-spacing: 0.05em;">ALGORITHMIC RESONANCE</span>
            </div>
            <h2 style="font-size: 28px; font-weight: 700; color: #ffffff; margin: 0 0 8px 0;">What are you in the mood for?</h2>
            <p style="font-size: 14px; color: #cbc3d7; margin: 0;">
                Pick the feeling. We'll fine-tune the cinematic frequencies. Select a primary anchor and an optional tonal twist.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Active selection summary bar
    selected_moods = st.session_state.get("selected_moods", ["Dark", "Suspenseful"])
    primary_mood = selected_moods[0] if len(selected_moods) > 0 else None
    secondary_mood = selected_moods[1] if len(selected_moods) > 1 else None

    col_summary, col_reset = st.columns([4, 1])
    with col_summary:
        if primary_mood or secondary_mood:
            parts = []
            if primary_mood:
                parts.append(f"<strong style='color: #d0bcff;'>{primary_mood}</strong> (Primary)")
            if secondary_mood:
                parts.append(f"<strong style='color: #7bd0ff;'>{secondary_mood}</strong> (Secondary)")
            summary_str = " • ".join(parts)
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 10px; padding: 8px 14px; background: rgba(26, 31, 48, 0.8); border: 1px solid var(--outline-variant); border-radius: 12px;">
                    <span class="material-symbols-outlined" style="color: #a078ff; font-size: 18px;">auto_awesome</span>
                    <span style="font-size: 13px; color: #dee1f9;">{len(selected_moods)} Moods Selected: {summary_str}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="font-size: 13px; color: #cbc3d7; padding: 8px 0;">
                    Select up to 2 mood frequencies below (first is Primary, second is Secondary).
                </div>
                """,
                unsafe_allow_html=True
            )
    with col_reset:
        if st.button("Reset Moods", key="btn_reset_moods", use_container_width=True):
            st.session_state.selected_moods = []
            st.rerun()

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 10 Mood Cards (2 rows of 5 or 5 columns)
    cols1 = st.columns(5)
    for i in range(5):
        m = MOOD_DEFINITIONS[i]
        with cols1[i]:
            is_primary = (primary_mood == m["name"])
            is_secondary = (secondary_mood == m["name"])
            
            border_color = "#a078ff" if is_primary else ("#7bd0ff" if is_secondary else "rgba(73, 68, 84, 0.5)")
            bg_card = "rgba(160, 120, 255, 0.12)" if is_primary else ("rgba(0, 166, 224, 0.12)" if is_secondary else "rgba(26, 31, 48, 0.7)")
            badge_text = "Primary" if is_primary else ("Secondary" if is_secondary else "")

            st.markdown(
                f"""
                <div style="background: {bg_card}; border: 1px solid {border_color}; border-radius: 14px; padding: 14px; text-align: center; margin-bottom: 8px;">
                    <div style="font-size: 26px; margin-bottom: 4px;">{m['emoji']}</div>
                    <div style="font-size: 14px; font-weight: 700; color: #dee1f9;">{m['name']}</div>
                    <div style="font-size: 11px; color: #cbc3d7; margin-bottom: 6px;">{m['desc']}</div>
                    {f"<span class='aura-badge-primary' style='font-size: 10px; padding: 2px 6px;'>{badge_text}</span>" if badge_text else "<span style='font-size: 10px; color: #958ea0;'>Tap to add</span>"}
                </div>
                """,
                unsafe_allow_html=True
            )
            # Toggle button
            btn_label = "Remove" if (is_primary or is_secondary) else "Select"
            if st.button(f"{btn_label} {m['name']}", key=f"btn_mood_{m['key']}", use_container_width=True):
                current = list(st.session_state.get("selected_moods", []))
                if m["name"] in current:
                    current.remove(m["name"])
                else:
                    if len(current) >= 2:
                        current.pop(0)  # shift out oldest
                    current.append(m["name"])
                st.session_state.selected_moods = current
                st.rerun()

    cols2 = st.columns(5)
    for i in range(5, 10):
        m = MOOD_DEFINITIONS[i]
        with cols2[i - 5]:
            is_primary = (primary_mood == m["name"])
            is_secondary = (secondary_mood == m["name"])
            
            border_color = "#a078ff" if is_primary else ("#7bd0ff" if is_secondary else "rgba(73, 68, 84, 0.5)")
            bg_card = "rgba(160, 120, 255, 0.12)" if is_primary else ("rgba(0, 166, 224, 0.12)" if is_secondary else "rgba(26, 31, 48, 0.7)")
            badge_text = "Primary" if is_primary else ("Secondary" if is_secondary else "")

            st.markdown(
                f"""
                <div style="background: {bg_card}; border: 1px solid {border_color}; border-radius: 14px; padding: 14px; text-align: center; margin-bottom: 8px;">
                    <div style="font-size: 26px; margin-bottom: 4px;">{m['emoji']}</div>
                    <div style="font-size: 14px; font-weight: 700; color: #dee1f9;">{m['name']}</div>
                    <div style="font-size: 11px; color: #cbc3d7; margin-bottom: 6px;">{m['desc']}</div>
                    {f"<span class='aura-badge-primary' style='font-size: 10px; padding: 2px 6px;'>{badge_text}</span>" if badge_text else "<span style='font-size: 10px; color: #958ea0;'>Tap to add</span>"}
                </div>
                """,
                unsafe_allow_html=True
            )
            btn_label = "Remove" if (is_primary or is_secondary) else "Select"
            if st.button(f"{btn_label} {m['name']}", key=f"btn_mood_{m['key']}", use_container_width=True):
                current = list(st.session_state.get("selected_moods", []))
                if m["name"] in current:
                    current.remove(m["name"])
                else:
                    if len(current) >= 2:
                        current.pop(0)
                    current.append(m["name"])
                st.session_state.selected_moods = current
                st.rerun()

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    # Genre filters section
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <div>
                <span class="aura-badge-secondary" style="font-size: 11px;">OPTIONAL</span>
                <h3 style="font-size: 18px; font-weight: 700; color: #ffffff; margin: 4px 0;">Genre Spectrum</h3>
                <p style="font-size: 12px; color: #cbc3d7; margin: 0;">Fine-tune genre spectrum for your twin moods.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    current_genres = st.session_state.get("selected_genres", ["Sci-Fi", "Thriller"])
    selected_genres = st.multiselect(
        "Choose genres to filter:",
        options=ALL_GENRES,
        default=current_genres,
        key="genre_multiselect"
    )
    st.session_state.selected_genres = selected_genres

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Predicted Match Pool Widget from Stitch Screen 2
    match_count = len(df)
    if selected_genres:
        match_count = sum(1 for _, row in df.iterrows() if any(g in row["genres"] for g in selected_genres))
    
    st.markdown(
        f"""
        <div class="aura-card" style="padding: 16px 20px; background: rgba(14, 19, 35, 0.8); border: 1px solid var(--secondary); margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="background: rgba(0, 166, 224, 0.2); width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <span class="material-symbols-outlined" style="color: #7bd0ff;">movie_filter</span>
                    </div>
                    <div>
                        <div style="font-size: 11px; font-weight: 700; color: #7bd0ff; letter-spacing: 0.04em;">PREDICTED MATCH POOL</div>
                        <div style="font-size: 16px; font-weight: 700; color: #dee1f9;">{match_count} Films Aligned</div>
                    </div>
                </div>
                <div style="font-size: 12px; color: #cbc3d7;">
                    e.g., <em>Blade Runner 2049, Children of Men, Dark City</em>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Navigation Footer
    c_back, c_skip, c_next = st.columns([1, 1, 2])
    with c_back:
        if st.button("← Back", key="btn_mood_back", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
    with c_skip:
        if st.button("Skip to Results", key="btn_mood_skip", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()
    with c_next:
        if st.button("Continue to Taste Calibration →", key="btn_mood_next", type="primary", use_container_width=True):
            st.session_state.page = "onboarding_taste"
            st.rerun()
