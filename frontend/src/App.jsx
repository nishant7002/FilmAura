import React, { useState, useEffect } from 'react';
import CursorFollower from './components/CursorFollower';
import Lightfall from './components/Lightfall';

// Semantic line icons (16x16, 1.5 stroke, matching text color)
function FilmIcon({ size = 16, className = '' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18" />
      <line x1="7" y1="2" x2="7" y2="22" />
      <line x1="17" y1="2" x2="17" y2="22" />
      <line x1="2" y1="12" x2="22" y2="12" />
      <line x1="2" y1="7" x2="7" y2="7" />
      <line x1="2" y1="17" x2="7" y2="17" />
      <line x1="17" y1="17" x2="22" y2="17" />
      <line x1="17" y1="7" x2="22" y2="7" />
    </svg>
  );
}

function SlidersIcon({ size = 16, className = '' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <line x1="4" y1="21" x2="4" y2="14" />
      <line x1="4" y1="10" x2="4" y2="3" />
      <line x1="12" y1="21" x2="12" y2="12" />
      <line x1="12" y1="8" x2="12" y2="3" />
      <line x1="20" y1="21" x2="20" y2="16" />
      <line x1="20" y1="12" x2="20" y2="3" />
      <line x1="1" y1="14" x2="7" y2="14" />
      <line x1="9" y1="8" x2="15" y2="8" />
      <line x1="17" y1="16" x2="23" y2="16" />
    </svg>
  );
}

function StarIcon({ size = 14, className = '' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" stroke="none" className={className}>
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  );
}

function AlertIcon({ size = 16, className = '' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  );
}

function SearchIcon({ size = 28, className = '' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  );
}

const MOOD_OPTIONS = [
  { id: 'Dark', label: 'Dark — Brooding, Psychological, Neo-Noir' },
  { id: 'Motivational', label: 'Motivational — Triumph, Perseverance, Inspiring' },
  { id: 'Happy', label: 'Happy — Uplifting, Joyous, Lighthearted' },
  { id: 'Relaxed', label: 'Relaxed — Calm, Contemplative, Gentle Pace' },
  { id: 'Romantic', label: 'Romantic — Passionate, Heartfelt, Intimate' },
  { id: 'Adventurous', label: 'Adventurous — Daring, Epic Journeys, Exploration' },
  { id: 'Thoughtful', label: 'Thoughtful — Philosophical, Mind-Bending, Cerebral' },
  { id: 'Emotional', label: 'Emotional — Poignant Catharsis, Human Drama' },
  { id: 'Suspenseful', label: 'Suspenseful — High-Stakes Mystery, Tense' },
  { id: 'Funny', label: 'Funny — Satirical, Witty, Humorous' }
];

export default function App() {
  const [mood, setMood] = useState('Dark');
  const [genre, setGenre] = useState('All Genres');
  const [favoriteMovieId, setFavoriteMovieId] = useState('');
  const [topK, setTopK] = useState(5);

  const [availableGenres, setAvailableGenres] = useState(['All Genres']);
  const [moviesList, setMoviesList] = useState([]);
  const [recommendations, setRecommendations] = useState(null);
  const [lastQuery, setLastQuery] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [metadataLoading, setMetadataLoading] = useState(true);

  // Fetch metadata on mount (genre vocabulary & movie candidate index)
  useEffect(() => {
    fetch('/api/metadata')
      .then((res) => {
        if (!res.ok) throw new Error('Could not connect to FilmAura backend service.');
        return res.json();
      })
      .then((data) => {
        if (data.genres) {
          setAvailableGenres(['All Genres', ...data.genres]);
        }
        if (data.movies) {
          setMoviesList(data.movies);
        }
        setMetadataLoading(false);
      })
      .catch((err) => {
        console.error('Metadata error:', err);
        setError('Model artifacts not found or backend service is offline.');
        setMetadataLoading(false);
      });
  }, []);

  // Submit recommendation query
  const handleRecommend = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const payload = {
        mood: mood,
        genre: genre !== 'All Genres' ? genre : null,
        favorite_movie_id: favoriteMovieId ? parseInt(favoriteMovieId, 10) : null,
        top_k: parseInt(topK, 10)
      };

      const res = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Recommendation engine returned an unexpected error.');
      }

      const data = await res.json();
      setRecommendations(data.recommendations || []);
      setLastQuery({ mood, genre });
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Dynamic Ambient Background Canvas */}
      <div className="lightfall-bg-wrapper" aria-hidden="true">
        <Lightfall />
      </div>

      <CursorFollower />

      <div className="app-container">
        {/* Header */}
        <header className="hero">
          <div className="hero-badge-strip">
            <span className="live-dot" />
            <span>Hybrid Engine • 32M Interactions</span>
          </div>
          <h1 className="hero-title">FilmAura</h1>
          <p className="hero-tagline">
            Cinema discovery calibrated to your emotional state. Filter by affective mood archetype, genre constraint, or anchor with a reference film.
          </p>
        </header>

        {/* Global Error Banner */}
        {error && (
          <div className="error-banner">
            <AlertIcon />
            <span>{error}</span>
          </div>
        )}

        {/* Control Panel Form */}
        <form className="control-panel" onSubmit={handleRecommend}>
          <div className="panel-header">
            <SlidersIcon />
            <span>Discovery Parameters</span>
          </div>

          <div className="grid-2">
            {/* Mood Selector */}
            <div className="form-group">
              <label className="form-label" htmlFor="mood-select">
                Target Mood
              </label>
              <select
                id="mood-select"
                className="custom-select"
                value={mood}
                onChange={(e) => setMood(e.target.value)}
              >
                {MOOD_OPTIONS.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.label}
                  </option>
                ))}
              </select>
              <span className="form-hint">
                Projects user emotional intent onto continuous tag &amp; genre distributions.
              </span>
            </div>

            {/* Genre Selector */}
            <div className="form-group">
              <label className="form-label" htmlFor="genre-select">
                Genre Filter
              </label>
              <select
                id="genre-select"
                className="custom-select"
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                disabled={metadataLoading}
              >
                {availableGenres.map((g) => (
                  <option key={g} value={g}>
                    {g}
                  </option>
                ))}
              </select>
              <span className="form-hint">
                Hard catalog constraint applied before hybrid ranking.
              </span>
            </div>
          </div>

          {/* Anchor Film Dropdown */}
          <div className="form-group" style={{ marginBottom: '20px' }}>
            <label className="form-label" htmlFor="movie-select">
              Anchor Film (Optional)
            </label>
            <select
              id="movie-select"
              className="custom-select"
              value={favoriteMovieId}
              onChange={(e) => setFavoriteMovieId(e.target.value)}
              disabled={metadataLoading}
            >
              <option value="">
                None (Pure affective mood &amp; genre ranking)
              </option>
              {moviesList.map((m) => (
                <option key={m.movieId} value={m.movieId}>
                  {m.title}
                </option>
              ))}
            </select>
            <span className="form-hint">
              When selected, activates TF-IDF semantic narrative similarity and SVD collaborative latent alignment.
            </span>
          </div>

          {/* Slider & Submit Action */}
          <div className="grid-2" style={{ alignItems: 'flex-end', marginBottom: 0 }}>
            <div className="form-group">
              <label className="form-label" htmlFor="topk-slider">
                <span>Recommendations</span>
                <span className="slider-val">{topK} films</span>
              </label>
              <div className="slider-container">
                <input
                  id="topk-slider"
                  type="range"
                  min="3"
                  max="15"
                  value={topK}
                  onChange={(e) => setTopK(e.target.value)}
                  className="custom-range"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="btn-recommend"
                disabled={loading || metadataLoading}
              >
                {loading ? (
                  <>
                    <div className="spinner" />
                    <span>Scoring candidates...</span>
                  </>
                ) : (
                  <>
                    <FilmIcon />
                    <span>Recommend Films</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </form>

        {/* Recommendations Section */}
        {recommendations !== null ? (
          <div>
            <div className="results-header">
              <h2 className="results-title">Ranked Candidates</h2>
              {lastQuery && (
                <div className="results-badge-info">
                  Mood: <strong>{lastQuery.mood}</strong> • Genre: <strong>{lastQuery.genre}</strong>
                </div>
              )}
            </div>

            {recommendations.length === 0 ? (
              <div className="placeholder-box">
                <div className="placeholder-icon">
                  <SearchIcon />
                </div>
                <div className="placeholder-title">No matching films found</div>
                <p className="placeholder-text">
                  The selected genre filter produced no films matching this mood threshold. Try selecting "All Genres" or choosing an adjacent mood archetype.
                </p>
              </div>
            ) : (
              recommendations.map((film, index) => {
                const isTop = index === 0;
                const isHighMatch = film.match_pct >= 90;
                return (
                  <div
                    key={film.movieId}
                    className={`film-card ${isTop ? 'top-rank' : ''}`}
                  >
                    <div className="card-top">
                      <div className="movie-title-group">
                        <span className="movie-rank">
                          {String(index + 1).padStart(2, '0')}.
                        </span>
                        <span className="movie-title">
                          {film.title}
                        </span>
                        <span className="movie-year">
                          {film.year}
                        </span>
                      </div>
                      <div>
                        <span className={`match-badge ${isHighMatch ? 'high-match' : ''}`}>
                          {film.match_pct}% Match
                        </span>
                      </div>
                    </div>

                    <div className="genre-container">
                      {film.genres && film.genres.map((g) => (
                        <span key={g} className="genre-pill">
                          {g}
                        </span>
                      ))}
                      <span className="rating-info">
                        <StarIcon />
                        {film.rating}
                      </span>
                      <span className="votes-info">
                        ({film.votes.toLocaleString()} ratings)
                      </span>
                    </div>

                    <div className="explanation-box">
                      <strong>Rationale:</strong> {film.explanation}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        ) : (
          /* Initial Empty State */
          <div className="placeholder-box">
            <div className="placeholder-icon">
              <FilmIcon size={32} />
            </div>
            <div className="placeholder-title">Awaiting Discovery Query</div>
            <p className="placeholder-text">
              Select your affective mood and optional anchor film above, then click Recommend Films to generate your personalized cinema candidates.
            </p>
          </div>
        )}

        {/* Footer */}
        <footer className="app-footer">
          FilmAura • Machine Learning Essentials (ECSCI24302) • Built with Scikit-Learn, LightGBM, SVD &amp; React
        </footer>
      </div>
    </>
  );
}
