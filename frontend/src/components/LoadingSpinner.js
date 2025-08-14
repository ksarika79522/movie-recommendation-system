import React from 'react';

const LoadingSpinner = ({ size = 50, color = '#667eea' }) => {
  const spinnerStyle = {
    width: `${size}px`,
    height: `${size}px`,
    border: `4px solid #f3f3f3`,
    borderTop: `4px solid ${color}`,
    borderRadius: '50%',
    animation: 'spin 1s linear infinite'
  };

  return (
    <div className="loading-spinner">
      <div style={spinnerStyle}></div>
    </div>
  );
};

export default LoadingSpinner;