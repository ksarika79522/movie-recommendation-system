import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:5001/api';

const PopularMovies = ({ onMovieSelect }) => {
  const [popularMovies, setPopularMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchPopularMovies();
  }, []);

  const fetchPopularMovies = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/movies/popular?limit=20`);
      const data = await response.json();

      if (response.ok) {
        setPopularMovies(data.movies || []);
        setError('');
      } else {
        setError('Failed to load popular movies');
        setPopularMovies([]);
      }
    } catch (err) {
      setError('Failed to connect to server');
      setPopularMovies([]);
    } finally {
      setLoading(false);
    }
  };

  const handleMovieClick = (movie) => {
    onMovieSelect(movie);
  };

  if (loading) {
    return (
      <div className="popular-movies-loading">
        <div className="section-header">
          <h2>🔥 Popular Movies</h2>
          <p>Loading top-rated movies...</p>
        </div>
        <div className="loading-section">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="popular-movies-error">
        <div className="section-header">
          <h2>🔥 Popular Movies</h2>
          <div className="error-message">
            <span>⚠️ {error}</span>
            <button onClick={fetchPopularMovies} className="retry-btn">
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="popular-movies">
      <div className="section-header">
        <h2>🔥 Popular Movies</h2>
        <p>Discover highly-rated movies or click on one to get personalized recommendations</p>
      </div>
      
      {popularMovies.length > 0 ? (
        <div className="movies-grid">
          {popularMovies.map((movie, index) => (
            <div 
              key={index} 
              className="movie-card"
              onClick={() => handleMovieClick(movie)}
            >
              <h4>{movie.title}</h4>
              
              <div className="movie-rating">
                ⭐ {movie.vote_average?.toFixed(1) || 'N/A'}
              </div>
              
              <div className="movie-genres">
                {movie.genres}
              </div>
              
              <div className="movie-overview">
                {movie.overview || 'No overview available.'}
              </div>
              
              <div className="click-hint">
                <small>💡 Click to get recommendations</small>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-movies">
          <p>No popular movies available at the moment.</p>
          <button onClick={fetchPopularMovies} className="retry-btn">
            Refresh
          </button>
        </div>
      )}
    </div>
  );
};

export default PopularMovies;