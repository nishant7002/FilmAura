# FilmAura — Design System & Implementation Specification
*Extracted from Google Stitch Project: FilmAura (`projects/6513193978623036163`)*

---

## 1. Executive Summary & Design Vision

**FilmAura** is a premium, ML-powered cinema discovery platform tailored for cinephiles. It bridges emotional sentiment with mathematical recommender rigor, translating user moods, tonal preferences, and seed films into highly calibrated film recommendations in under 60 seconds.

The visual theme, codenamed **Nocturne Cinema**, employs deep midnight blues, moody violet/lavender accents, vibrant cyan secondary highlights, subtle glowing outlines, and clean sans-serif typography (`Inter`). The interface evokes the atmosphere of an intimate indie screening room paired with a precision audio/algorithmic laboratory.

---

## 2. Colour Palette & Design Tokens

Derived from the Google Stitch design tokens and Tailwind configuration:

| Token Name | Hex Code | Purpose / Usage |
| :--- | :--- | :--- |
| `background` / `surface` | `#0e1323` | Main canvas background, primary page container |
| `surface-container-lowest` | `#080d1d` | Deep inset backgrounds, input backgrounds |
| `surface-container-low` | `#161b2b` | Section backdrops, sub-panels |
| `surface-container` | `#1a1f30` | Default card background, modals, list containers |
| `surface-container-high` | `#25293a` | Elevated cards, hovered chips, dropdown menus |
| `surface-container-highest` | `#2f3446` | Highlights, active filters, selected states |
| `primary` | `#d0bcff` | Soft lavender/violet, primary headings, hero text |
| `primary-container` | `#a078ff` | Primary CTA buttons, glowing badges, active state fills |
| `on-primary` | `#3c0091` | High-contrast text on primary buttons |
| `secondary` | `#7bd0ff` | Electric cyan, match percentages, metrics, aura highlights |
| `secondary-container` | `#00a6e0` | Secondary badges, progress bars, active toggles |
| `tertiary` | `#bec7d7` | Muted cool gray, secondary icons, metadata badges |
| `on-surface` | `#dee1f9` | High-emphasis body text, titles, prominent labels |
| `on-surface-variant` | `#cbc3d7` | Medium-emphasis text, secondary descriptions, ratings |
| `outline` | `#958ea0` | Borders for cards, dividers, unfocused input fields |
| `outline-variant` | `#494454` | Subtle borders, quiet dividers |
| `error` | `#ffb4ab` | Error messages, destructive alerts, reset badges |

### Ambient Lighting & Effects
- **Card Glow**: `box-shadow: 0 4px 20px -2px rgba(160, 120, 255, 0.12);`
- **Neon Accent Glow**: `box-shadow: 0 0 16px rgba(123, 208, 255, 0.25);`
- **Border Radii**:
  - Small elements / tags: `0.25rem` (4px)
  - Cards & containers: `0.75rem` - `1.0rem` (12px - 16px)
  - Interactive buttons & pills: `9999px` (Full pill shape)

---

## 3. Typography Hierarchy

The type system is built on **Inter** (Google Font):

| Level | Font Size | Line Height | Weight | Letter Spacing | Target Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `display` | `48px` (3rem) | `56px` | `700` (Bold) | `-0.02em` | Hero landing headline |
| `display-mobile`| `32px` (2rem) | `40px` | `700` (Bold) | `-0.01em` | Mobile landing title |
| `headline-lg` | `32px` (2rem) | `40px` | `600` (SemiBold) | `-0.02em` | Section titles, feature banners |
| `headline-md` | `24px` (1.5rem) | `32px` | `600` (SemiBold) | `-0.01em` | Step questions, film title (detail) |
| `headline-sm` | `18px` (1.125rem) | `26px` | `600` (SemiBold) | `-0.005em` | Card titles, feature titles |
| `title-md` | `16px` (1rem) | `24px` | `600` (SemiBold) | `0` | Subsection headings, filter labels |
| `body-lg` | `16px` (1rem) | `26px` | `400` (Regular) | `0` | Lead paragraphs, synopsis |
| `body-md` | `14px` (0.875rem)| `22px` | `400` (Regular) | `0` | Default body text, descriptions |
| `body-sm` | `12px` (0.75rem) | `18px` | `400` (Regular) | `0` | Metadata notes, timestamps |
| `label-md` | `12px` (0.75rem) | `16px` | `600` (SemiBold) | `+0.04em` | Badge text, category chips, stats |
| `label-sm` | `11px` (0.6875rem)| `14px` | `500` (Medium) | `+0.02em` | Secondary tags, pill subtext |

---

## 4. Screen Inventory & Flow Specifications

### Screen 1: Landing Page (`FilmAura - Landing Page`)
- **Header**: FilmAura branding, `Discover` badge, `auto_awesome` icon.
- **Hero Section**:
  - Pill badge: `auto_awesome ML-Powered Cinema Discovery`
  - Headline: `Find the movie that feels right.`
  - Lead description: Emotional vibe + taste preferences + collaborative similarity.
  - CTAs: Primary `Find My Movie ->` button and secondary `Explore Popular Movies`.
- **Hero Floating Highlight Cards**:
  - `Sci-Fi Noir` (★ 8.6, 98% Aura Match)
  - `Ambient Drama` (★ 9.1, Matched for Melancholic & Deep)
  - `Existential Drift` (★ 8.8)
- **Mood Frequency Teaser Grid**:
  - 5 key frequencies: 🌧️ Melancholic Noir, ⚡ Adrenaline Pulse, 🌌 Cosmic Awe, 🕯️ Quiet Intimacy, 🪞 Surreal Dream.
- **Cinephile Precision Pillars**:
  1. *Mood Matching* (10 Curated Vibes)
  2. *Hybrid ML Engine* (Matrix Factorization + Content Vectors)
  3. *Live Catalogue* (Real-time curation & streaming availability)
- **Quick Launch Bar**: Tonight's session launcher with key stats (42k+ Indexed, 94.8% Precision, < 60s).

### Screen 2: Mood & Genre Onboarding (`FilmAura - Mood & Genre Onboarding`)
- **Step Header**: `Step 1 of 3: Mood & Vibe` (or Step 1 of 2), `33% Calibrated` with glowing progress bar.
- **Mood Selection Grid (10 Spectrum Anchors)**:
  1. ☀️ **Happy** (uplifting & bright)
  2. 🌿 **Relaxed** (calm & gentle)
  3. 💧 **Emotional** (deep & poignant)
  4. 💫 **Romantic** (intimate & poetic)
  5. 🌑 **Dark** (shadowy & bleak)
  6. ⚡ **Suspenseful** (taut & high-stakes)
  7. 🧭 **Adventurous** (thrilling exploration)
  8. 🎭 **Funny** (witty & absurd)
  9. 🧠 **Thoughtful** (mind-bending cinema)
  10. 🔥 **Motivational** (inspiring triumph)
  - Selection logic: Supports Primary Anchor and Secondary Tonal Twist.
- **Genre Filters (Collapsible / Multi-Select)**:
  - Thriller, Sci-Fi, Mystery, Drama, Crime, Fantasy, Animation, Horror, Comedy, Romance, Adventure, Action.
- **Dynamic Match Pool Counter**: Real-time reactive feedback showing number of films matching current criteria.

### Screen 3: Taste Calibration (`FilmAura - Taste Calibration`)
- **Step Header**: `Step 2: Taste Calibration` (100% complete) with `Final Polish` badge.
- **Question**: `Anything you already love?` (Anchor recommendations with a favorite film or director).
- **Search & Auto-Suggest**: Search bar with real-time matching against the film dataset.
- **Active Anchors**: Visual chips of selected seed movies with dismiss button.
- **Engine Weight Slider / Hybrid Blend Control**:
  - Content Similarity vs. Mood Resonance ratio control (default 70% / 30%).
- **Quick Anchor Suggestions**:
  - Curated classics: *Arrival*, *Ex Machina*, *Drive*, *Children of Men*, *Interstellar*, *Parasite*.
- **CTA**: `Find My Movies (X Filters Active)` with live sync indicator.

### Screen 4: Recommendation Results (`FilmAura - Recommendation Results`)
- **Filter Breadcrumb Bar**: Shows active moods, reference films, and an `Adjust` button.
- **Header**: `Your FilmAura picks.` with personalized subtitle.
- **Controls & Sorting**:
  - Sort by: `Aura Score (Top Match)`, `Highest Rating`, `Release Year`.
  - Filters: `Available to Stream`, `Under 2h`, `Exclude Seen`.
- **Film Result Cards**:
  - Match badge: `#1`, `bolt 98% Match`.
  - Metadata: Runtime (e.g. `109m`), Year, Genre pills, Star rating + vote count.
  - Streaming Provider Badge: e.g. `Stream on Prime Video`, `Stream on Max`.
  - **FilmAura Rationale**: Natural language ML explanation of why this was recommended.
  - Actions: `+ Watchlist` toggle and `Details ->` button.
- **Algorithm Tuner**:
  - Drawer to loosen/tighten mood constraints, explore alternate vibe prompts.

### Screen 5: Movie Detail View (`FilmAura - Movie Detail View`)
- **Back Navigation**: `<- Back to Picks`.
- **Cinematic Hero**:
  - High-res poster/backdrop with gradient vignettes.
  - Badges: `FilmAura Match: 98%`, `4K Remastered`, Age Rating (`R`), Runtime, Year.
  - Title, tagline, and genres.
  - Verified Cinephile Essential badge.
- **Action Toolbar**:
  - `In Watchlist` toggle, `Watch Trailer`, `Mark as Seen`, `Share Film`.
- **Aura Diagnostic Breakdown**:
  - **Content Vector Similarity** (Progress bar + explanation)
  - **Mood Alignment** (Tag breakdown with affinity weights)
  - **Collaborative Filtering** (Affinity cross-match with similar cinephiles)
- **Synopsis & Editorial Review**: Deep story context and cinematic craft notes.
- **Verified Cast & Crew**: Director, Cinematographer, Lead actors.
- **Similar Films in this Vibe**: Carousel or cards of connected films with similarity scores.
- **Embedded Trailer Player**: Integrated video preview.

### Screen 6: Watchlist & Library
- Stored in persistent session state (or optional database).
- Organized with quick filters: All, To Watch, Watched.
- Total watch-time calculator and mood breakdown of saved library.
- Direct links back into movie details.

### Screen 7: About & Machine Learning Methodology
- In-depth technical explanation of the recommender:
  - Vector Space Model (TF-IDF & Cosine Similarity).
  - Sentiment & Emotional Lexicon mapping for mood extraction.
  - Bayesian Weighted Rating equation: $WR = \frac{v}{v+m} R + \frac{m}{v+m} C$.
  - Hybrid re-ranking equation: $\text{AuraScore} = w_c \cdot S_{\text{content}} + w_m \cdot S_{\text{mood}} + w_r \cdot S_{\text{rating}}$.
- Academic & course credits for Machine Learning Essentials.

---

## 5. Streamlit Architecture & Styling Strategy

Streamlit cannot run arbitrary React components natively, but it supports full HTML/CSS injection via `st.markdown(..., unsafe_allow_html=True)` and custom CSS theming.

### CSS Injection Architecture
We inject a comprehensive custom CSS stylesheet that mirrors the Stitch Tailwind design tokens:
- Deep `#0e1323` background across the entire viewport.
- Custom styled cards with `#1a1f30` background, 1px `#25293a` borders, and subtle glowing hovers.
- High-fidelity typography styling with Google Font `Inter`.
- Glowing badges, gradient action buttons (`#a078ff` to `#7bd0ff`).
- Seamless bottom/top navigation and tabs.

### State Management
Session state (`st.session_state`) manages:
- `page`: Navigation router (`landing`, `onboarding_mood`, `onboarding_taste`, `results`, `detail`, `watchlist`, `methodology`).
- `selected_moods`: Array containing Primary and Secondary mood selections.
- `selected_genres`: Array of chosen genres.
- `seed_movie_ids`: List of anchored movie IDs.
- `filter_stream_only`: Boolean.
- `filter_under_2h`: Boolean.
- `filter_exclude_seen`: Boolean.
- `sort_by`: Selected sort criteria.
- `active_movie_id`: Current film in Detail View.
- `watchlist`: Set of saved movie IDs.
- `watched_list`: Set of films marked as seen.
- `hybrid_weights`: Dict with content and mood weighting.

---

## 6. Machine Learning Recommender Specification

The recommender engine is decoupled into `src/recommender.py`:

1. **Curated Cinema Dataset**: A high-quality dataset containing diverse international and classic films (covering all Stitch reference films including *Blade Runner 2049*, *Children of Men*, *Ex Machina*, *Dark City*, *Annihilation*, *1917*, *Snowpiercer*, *The Road*, *Arrival*, *Drive*, *Interstellar*, *Inception*, *Parasite*, *Dune*, *Solaris*, etc.) with rich attributes:
   - Metadata: `id`, `title`, `year`, `runtime`, `genres`, `rating`, `votes`, `director`, `cinematographer`, `cast`, `synopsis`, `poster_url`, `backdrop_url`, `trailer_url`, `stream_provider`.
   - Mood vector tags: Scores for all 10 core moods.
   - Text corpus: Combined tags (overview + genres + keywords + director + cast).

2. **Feature Engineering**:
   - `TfidfVectorizer` (with unigrams and bigrams, English stop words removed).
   - Pre-computed or on-demand Cosine Similarity matrix.
   - Mood semantic alignment scoring using calibrated feature weights.

3. **Hybrid Re-ranking Algorithm**:
   $$\text{Score}(M) = \alpha \cdot \text{Sim}_{\text{seed}}(M) + \beta \cdot \text{Score}_{\text{mood}}(M) + \gamma \cdot \text{BayesianRating}(M)$$
   - Generates transparent breakdown percentages for the UI (Content %, Mood %, Collaborative %).
   - Generates dynamic natural-language rationale: `"Matches your [Primary] & [Secondary] mood • Similar visual tone to [Seed]."`

4. **Fault Tolerance**:
   - If pre-computed artifacts are absent, the module automatically generates or falls back gracefully with a clear setup guide and self-healing initialization.
