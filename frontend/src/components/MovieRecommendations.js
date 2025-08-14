import React, { useState, useEffect } from 'react';

const MovieRecommendations = ({ basedOn }) => {
  const BATCH_SIZE = 10;
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [offset, setOffset] = useState(0);
  const [selectedMovie, setSelectedMovie] = useState(null);

  // Fetch recommendations from backend
  const fetchRecommendations = async (append = false) => {
    if (!basedOn) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5001/api/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          movie_title: basedOn,
          num_recommendations: BATCH_SIZE,
          offset: append ? offset : 0,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        const newRecs = data.recommendations || [];
        if (append) {
          setRecommendations((prev) => [...prev, ...newRecs]);
          setOffset((prev) => prev + newRecs.length);
        } else {
          setRecommendations(newRecs);
          setOffset(newRecs.length);
        }
      } else {
        console.error(data.error || 'Failed to fetch recommendations');
        if (!append) setRecommendations([]);
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      if (!append) setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  // Load first batch whenever the selected movie changes
  useEffect(() => {
    setOffset(0);
    setRecommendations([]);
    fetchRecommendations(false);
  }, [basedOn]);

  const handleCardClick = (movie) => setSelectedMovie(movie);
  const closeModal = () => setSelectedMovie(null);

  return (
    <div className="movie-recommendations">
      <div className="section-header" style={{ marginBottom: '1rem' }}>
        <h2>🎯 Recommended for You</h2>
        <p>
          Based on your selection: <strong>{basedOn}</strong>
        </p>
      </div>

      <div
        className="movies-grid"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill,minmax(220px,1fr))',
          gap: '20px',
        }}
      >
        {recommendations.length === 0 && !loading && <p>No recommendations found.</p>}

        {recommendations.map((movie, index) => (
          <div
            key={index}
            className="movie-card"
            onClick={() => handleCardClick(movie)}
            style={{
              cursor: 'pointer',
              border: '1px solid #ddd',
              borderRadius: '10px',
              padding: '15px',
              transition: 'transform 0.2s ease, box-shadow 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'scale(1.02)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'scale(1)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <h4>{movie.title}</h4>
            <div className="movie-rating">⭐ {movie.vote_average?.toFixed(1) || 'N/A'}</div>
            <div className="movie-genres">{movie.genres}</div>
            <div className="movie-overview">
              {movie.overview?.length > 100
                ? movie.overview.substring(0, 100) + '...'
                : movie.overview || 'No overview available.'}
            </div>
          </div>
        ))}
      </div>

      {/* Load More Button */}
      {recommendations.length > 0 && (
        <button
          onClick={() => fetchRecommendations(true)}
          disabled={loading}
          style={{
            marginTop: '20px',
            padding: '10px 20px',
            backgroundColor: '#6c63ff',
            color: 'white',
            border: 'none',
            borderRadius: '25px',
            cursor: loading ? 'not-allowed' : 'pointer',
            boxShadow: '0 6px 12px rgba(108, 99, 255, 0.6)',
            fontWeight: 'bold',
          }}
        >
          {loading ? 'Loading...' : 'Load More'}
        </button>
      )}

      {/* Modal for full description */}
      {selectedMovie && (
        <div style={overlayStyles} onClick={closeModal}>
          <div style={modalStyles} onClick={(e) => e.stopPropagation()}>
            <button style={closeButtonStyles} onClick={closeModal} aria-label="Close">
              ×
            </button>
            <h3>{selectedMovie.title}</h3>
            <p>{selectedMovie.overview}</p>
          </div>
        </div>
      )}
    </div>
  );
};

const overlayStyles = {
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100%',
  height: '100%',
  backgroundColor: 'rgba(0,0,0,0.6)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  zIndex: 1000,
};

const modalStyles = {
  position: 'relative',
  background: '#fff',
  padding: '20px',
  borderRadius: '10px',
  maxWidth: '500px',
  width: '80%',
  boxShadow: '0 4px 10px rgba(0,0,0,0.3)',
  textAlign: 'center',
};

const closeButtonStyles = {
  position: 'absolute',
  top: '10px',
  right: '10px',
  width: '35px',
  height: '35px',
  borderRadius: '50%',
  border: 'none',
  backgroundColor: '#6c63ff',
  color: 'white',
  fontSize: '20px',
  cursor: 'pointer',
  boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
  transition: 'transform 0.2s ease, background-color 0.2s ease',
};

export default MovieRecommendations;

