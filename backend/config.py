import os

class Config:
    """Configuration settings for the Movie Recommendation System"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'movie-rec-secret-key-2024'
    DEBUG = True
    
    # API settings
    API_HOST = '0.0.0.0'
    API_PORT = 5000
    
    # Data settings
    DATA_FOLDER = 'data'
    
    # TMDB Dataset file paths (in order of preference)
    TMDB_FILES = [
        'data/tmdb_5000_movies.csv',
        'data/movies_metadata.csv',
        'data/tmdb_movies.csv'
    ]
    
    # Recommendation settings
    MAX_FEATURES_TFIDF = 5000
    NGRAM_RANGE = (1, 2)
    MIN_VOTE_COUNT = 10
    MIN_OVERVIEW_LENGTH = 10
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    @staticmethod
    def get_available_dataset():
        """Get the first available dataset file"""
        for file_path in Config.TMDB_FILES:
            if os.path.exists(file_path):
                return file_path
        return None
    
    @staticmethod
    def ensure_data_directory():
        """Ensure data directory exists"""
        os.makedirs(Config.DATA_FOLDER, exist_ok=True)