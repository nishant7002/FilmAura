import React, { useState, useEffect } from 'react';
import CursorFollower from './components/CursorFollower';

const MOOD_OPTIONS = [
  { id: 'Dark', label: '⚡ Dark (Brooding, Psychological, Neo-Noir)' },
  { id: 'Motivational', label: '🌟 Motivational (Triumph, Perseverance, Inspiring)' },
  { id: 'Happy', label: '😄 Happy (Uplifting, Joyous, Lighthearted)' },
  { id: 'Relaxed', label: '☕ Relaxed (Calm, Serene, Gentle Pace)' },
  { id: 'Romantic', label: '❤️ Romantic (Passionate, Heartfelt, Intimate)' },
  { id: 'Adventurous', label: '🧭 Adventurous (Daring, Quests, Exploration)' },
  { id: 'Thoughtful', label: '💭 Thoughtful (Philosophical, Mind-Bending, Cerebral)' },
  { id: 'Emotional', label: '🎭 Emotional (Moving, Tearjerking, Poignant)' },
  { id: 'Suspenseful', label: '🔍 Suspenseful (Edge-of-Your-Seat, Tense, Mystery)' },
  { id: 'Funny', label: '😂 Funny (Hilarious, Witty, Laugh-out-Loud)' }
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

  // Fetch initial metadata on mount (genres and movie catalog)
  useEffect(() => {
    fetch('/api/metadata')
      .then((res) => {
        if (!res.ok) throw new Error('Could not connect to FilmAura backend.');
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
        setError('Model artifacts not found or backend server is not running.');
        setMetadataLoading(false);
      });
  }, []);

  // ONLY execute recommendations when the user explicitly clicks the button
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
        throw new Error(errData.detail || 'Recommendation engine returned an error.');
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
      <CursorFollower />

      <div className="app-container">
        {/* Hero Header */}
        <header className="hero">
          <h1 className="hero-title">🎬 FilmAura</h1>
          <p className="hero-tagline">
            Your mood. Your taste. <span>Your next movie.</span>
          </p>
          <p className="hero-desc">
            Discover cinema tuned precisely to your emotional frequency. Select your mood, 
            filter by genre, or anchor with a cherished film — then click 
            <strong style={{ color: '#f472b6' }}> Recommend Movies</strong> to activate the hybrid recommendation pipeline.
          </p>
        </header>

        {/* Global Error Banner */}
        {error && (
          <div style={{
            background: 'rgba(239, 68, 68, 0.15)',
            border: '1px solid rgba(239, 68, 68, 0.4)',
            borderRadius: '14px',
            padding: '16px 20px',
            color: '#fca5a5',
            marginBottom: '30px'
          }}>
            <strong>⚠️ System Notice:</strong> {error}
          </div>
        )}

        {/* Control Panel Form */}
        <form className="control-panel" onSubmit={handleRecommend}>
          <div className="panel-header">
            <span>🎛️</span>
            <span>Customize Your Taste Profile</span>
          </div>

          <div className="grid-2">
            {/* Mood Selector */}
            <div className="form-group">
              <label className="form-label" htmlFor="mood-select">
                1. Select your current mood:
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
                Affective mood archetypes mapped to latent features and tags.
              </span>
            </div>

            {/* Genre Selector */}
            <div className="form-group">
              <label className="form-label" htmlFor="genre-select">
                2. Select preferred genre:
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
                    {g === 'All Genres' ? '🌌 All Genres' : `🎬 ${g}`}
                  </option>
                ))}
              </select>
              <span className="form-hint">
                Filters candidate pool to include your selected genre.
              </span>
            </div>
          </div>

          {/* Anchor Film Autocomplete / Dropdown */}
          <div className="form-group" style={{ marginBottom: '22px' }}>
            <label className="form-label" htmlFor="movie-select">
              3. (Optional) Anchor with a cherished film:
            </label>
            <select
              id="movie-select"
              className="custom-select"
              value={favoriteMovieId}
              onChange={(e) => setFavoriteMovieId(e.target.value)}
              disabled={metadataLoading}
            >
              <option value="">
                None (Recommend based purely on mood &amp; genre resonance)
              </option>
              {moviesList.map((m) => (
                <option key={m.movieId} value={m.movieId}>
                  🎞️ {m.title}
                </option>
              ))}
            </select>
            <span className="form-hint">
              When selected, TF-IDF and SVD will align visual tone, style, and narrative resonance to this movie.
            </span>
          </div>

          {/* Slider & Submit Button */}
          <div className="grid-2" style={{ alignItems: 'center', marginBottom: 0 }}>
            <div className="form-group">
              <label className="form-label" htmlFor="topk-slider">
                Results to display:
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
                <span className="slider-val">{topK}</span>
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
                    <span>Analyzing Cinema Vectors...</span>
                  </>
                ) : (
                  <>
                    <span>✨</span>
                    <span>Recommend Movies</span>
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
              <h2 className="results-title">🎯 Top Recommendations for You</h2>
              {lastQuery && (
                <div className="results-badge-info">
                  Mood: <strong style={{ color: '#c084fc' }}>{lastQuery.mood}</strong> |{' '}
                  Genre: <strong style={{ color: '#38bdf8' }}>{lastQuery.genre}</strong>
                </div>
              )}
            </div>

            {recommendations.length === 0 ? (
              <div className="placeholder-box">
                <div className="placeholder-icon">🔍</div>
                <div className="placeholder-title">No direct matches found</div>
                <p className="placeholder-text">
                  No movies matched all chosen criteria. Try selecting "All Genres" or picking a different mood archetype.
                </p>
              </div>
            ) : (
              recommendations.map((film, index) => {
                const isHighMatch = film.match_pct >= 90;
                return (
                  <div
                    key={film.movieId}
                    className="film-card"
                    style={{ animationDelay: `${index * 0.08}s` }}
                  >
                    <div className="card-top">
                      <div>
                        <span className="movie-title">
                          {index + 1}. {film.title}
                        </span>
                        <span className="movie-year">({film.year})</span>
                      </div>
                      <div>
                        <span className={`match-badge ${isHighMatch ? 'match-high' : 'match-mid'}`}>
                          ⚡ {film.match_pct}% Match
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
                        ⭐ {film.rating} / 5.0
                      </span>
                      <span className="votes-info">
                        ({film.votes.toLocaleString()} votes)
                      </span>
                    </div>

                    <div className="explanation-box">
                      💡 <strong>Why this movie?</strong> {film.explanation}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        ) : (
          /* Initial Hero Placeholder before user clicks Recommend */
          <div className="placeholder-box">
            <div className="placeholder-icon">🍿 🔮 🎬</div>
            <div className="placeholder-title">Ready to find your next favorite film?</div>
            <p className="placeholder-text">
              Customize your mood and taste preferences above, then click{' '}
              <strong style={{ color: '#f472b6' }}>"✨ Recommend Movies"</strong> to generate your tailored recommendations.
            </p>
          </div>
        )}

        {/* Footer */}
        <footer className="app-footer">
          🎬 <strong>FilmAura</strong> • Machine Learning Essentials (MLE) Course Project • Built with Python, Scikit-learn &amp; React
        </footer>
      </div>
    </>
  );
}
