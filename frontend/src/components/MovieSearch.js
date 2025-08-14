import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';

const API_BASE_URL = 'http://localhost:5001/api';

const MovieSearch = ({ onMovieSelect }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const abortControllerRef = useRef(null);
  const inputRef = useRef(null);

  const fetchMovies = async (query) => {
    if (!query) return;
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const controller = new AbortController();
    abortControllerRef.current = controller;

    setLoading(true);
    try {
      const response = await fetch(
        `${API_BASE_URL}/movies/search?q=${encodeURIComponent(query)}&limit=10`,
        { signal: controller.signal }
      );
      const data = await response.json();
      if (response.ok) {
        setSearchResults(data.movies || []);
        setShowResults(true);
      } else {
        setSearchResults([]);
        setShowResults(false);
      }
    } catch (error) {
      if (error.name !== 'AbortError') console.error('Search error:', error);
      setSearchResults([]);
      setShowResults(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const debounceTimeout = setTimeout(() => {
      if (searchQuery.trim().length > 2) fetchMovies(searchQuery);
      else {
        setSearchResults([]);
        setShowResults(false);
      }
    }, 300);

    return () => clearTimeout(debounceTimeout);
  }, [searchQuery]);

  const handleMovieSelect = (movie) => {
    onMovieSelect(movie);
    setSearchQuery(movie.title);
    setShowResults(false);
  };

  // Compute dropdown position
  const [dropdownStyle, setDropdownStyle] = useState({});
  useEffect(() => {
    if (inputRef.current) {
      const rect = inputRef.current.getBoundingClientRect();
      setDropdownStyle({
        position: 'fixed',
        top: rect.bottom + 8,
        left: rect.left,
        width: rect.width,
        maxHeight: '300px',
        overflowY: 'auto',
        zIndex: 9999,
        borderRadius: '12px',
        boxShadow: '0 6px 20px rgba(0,0,0,0.2)',
        backgroundColor: '#fff',
        animation: 'fadeIn 0.2s ease-in',
      });
    }
  }, [showResults, searchResults]);

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', position: 'relative' }}>
      <h2 style={{ marginBottom: '0.5rem' }}>🔍 Search for Movies</h2>
      <p style={{ marginBottom: '1rem', color: '#555' }}>
        Type a movie name to get personalized recommendations
      </p>

      <input
        ref={inputRef}
        type="text"
        placeholder="e.g., The Matrix, Inception..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        onFocus={() => searchResults.length > 0 && setShowResults(true)}
        style={{
          width: '100%',
          padding: '12px 20px',
          borderRadius: '30px',
          border: '1px solid #ccc',
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
          outline: 'none',
          fontSize: '16px',
          backgroundColor: '#f9f9ff',
          transition: 'box-shadow 0.2s ease',
        }}
        onBlur={() => setTimeout(() => setShowResults(false), 250)}
      />

      {showResults &&
        createPortal(
          <div style={dropdownStyle}>
            {loading ? (
              <div style={{ padding: '20px', textAlign: 'center' }}>
                <div
                  style={{
                    border: '4px solid #f3f3f3',
                    borderTop: '4px solid #6c63ff',
                    borderRadius: '50%',
                    width: '24px',
                    height: '24px',
                    animation: 'spin 1s linear infinite',
                    margin: '0 auto 8px',
                  }}
                />
                <span style={{ color: '#555' }}>Searching...</span>
              </div>
            ) : searchResults.length > 0 ? (
              searchResults.map((movie, index) => (
                <div
                  key={index}
                  onClick={() => handleMovieSelect(movie)}
                  style={{
                    padding: '12px 16px',
                    cursor: 'pointer',
                    transition: 'background 0.2s ease',
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = '#f0f0ff')}
                  onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
                >
                  <div style={{ fontWeight: '600' }}>{movie.title}</div>
                  <div style={{ fontSize: '13px', color: '#666' }}>
                    {movie.genres} • ⭐ {movie.vote_average?.toFixed(1)}
                  </div>
                </div>
              ))
            ) : (
              <div style={{ padding: '16px', textAlign: 'center', color: '#888' }}>
                No movies found for "{searchQuery}"
              </div>
            )}
          </div>,
          document.body
        )}

      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
          }
        `}
      </style>
    </div>
  );
};

export default MovieSearch;
