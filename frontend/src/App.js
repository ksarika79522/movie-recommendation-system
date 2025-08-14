import React, { useState, useEffect } from 'react';
import './App.css';
import MovieSearch from './components/MovieSearch';
import MovieRecommendations from './components/MovieRecommendations';
import PopularMovies from './components/PopularMovies';
import LoadingSpinner from './components/LoadingSpinner';

const API_BASE_URL = 'http://localhost:5001/api';

function App() {
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [systemInitialized, setSystemInitialized] = useState(false);

  useEffect(() => {
    initializeSystem();
  }, []);

  const initializeSystem = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/initialize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        setSystemInitialized(true);
        setError('');
      } else {
        setError('Failed to initialize recommendation system');
      }
    } catch (err) {
      setError('Failed to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  const handleMovieSelect = async (movie) => {
    setSelectedMovie(movie);
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          movie_title: movie.title,
          num_recommendations: 12
        })
      });

      const data = await response.json();

      if (response.ok) {
        setRecommendations(data.recommendations);
      } else {
        setError(data.error || 'Failed to get recommendations');
        setRecommendations([]);
      }
    } catch (err) {
      setError('Failed to fetch recommendations');
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  const clearSelection = () => {
    setSelectedMovie(null);
    setRecommendations([]);
    setError('');
  };

  if (!systemInitialized && loading) {
    return (
      <div className="app-loading">
        <LoadingSpinner />
        <h2>Initializing Movie Recommendation System...</h2>
        <p>This may take a few moments while we set up the recommendation engine.</p>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>🎬 MovieRec Pro</h1>
        <p>Find Your Next Watch!</p>
      </header>

      <main className="main-content">
        {error && (
          <div className="error-message">
            <span>⚠️ {error}</span>
            {!systemInitialized && (
              <button onClick={initializeSystem} className="retry-btn">
                Retry Initialization
              </button>
            )}
          </div>
        )}

        {systemInitialized && (
          <>
            <section className="search-section">
              <MovieSearch onMovieSelect={handleMovieSelect} />
              {selectedMovie && (
                <div className="selected-movie">
                  <h3>Selected Movie:</h3>
                  <div className="movie-info">
                    <h4>{selectedMovie.title}</h4>
                    <p><strong>Genres:</strong> {selectedMovie.genres}</p>
                    <p><strong>Rating:</strong> ⭐ {selectedMovie.vote_average?.toFixed(1)}</p>
                    <p>{selectedMovie.overview}</p>
                    <button onClick={clearSelection} className="clear-btn">
                      Clear Selection
                    </button>
                  </div>
                </div>
              )}
            </section>

            {loading && (
              <div className="loading-section">
                <LoadingSpinner />
                <p>Getting recommendations...</p>
              </div>
            )}

            {recommendations.length > 0 && (
              <MovieRecommendations 
                recommendations={recommendations}
                basedOn={selectedMovie?.title}
              />
            )}

            {!selectedMovie && !loading && (
              <PopularMovies onMovieSelect={handleMovieSelect} />
            )}
          </>
        )}
      </main>

      <footer className="app-footer">
        <p>&#x00A9; 2025 MovieRec Pro. All Rights Reserved.</p>
      </footer>
    </div>
  );
}

export default App;
