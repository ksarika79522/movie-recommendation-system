import pandas as pd
import numpy as np
import json
import re
from datetime import datetime

def extract_tmdb_genres(genres_str):
    """
    Extract genre names from TMDB JSON format
    Input: '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]'
    Output: 'Action|Adventure'
    """
    try:
        if pd.isna(genres_str) or genres_str == '' or genres_str == '[]':
            return 'Unknown'
        
        # Handle string formatting issues
        genres_str = str(genres_str).replace("'", '"')
        genres_list = json.loads(genres_str)
        
        genre_names = []
        for genre in genres_list:
            if isinstance(genre, dict) and 'name' in genre:
                genre_names.append(genre['name'])
        
        return '|'.join(genre_names) if genre_names else 'Unknown'
    except (json.JSONDecodeError, TypeError, ValueError):
        return 'Unknown'

def clean_tmdb_text(text):
    """Clean text data for better processing"""
    if pd.isna(text) or text == '':
        return ''
    
    # Convert to string and clean
    text = str(text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', ' ', text)
    
    return text.strip()

def extract_year_from_date(date_str):
    """Extract year from release date string"""
    try:
        if pd.isna(date_str) or date_str == '':
            return 'Unknown'
        
        # Try to parse the date and extract year
        date_str = str(date_str)
        
        # Handle different date formats
        if len(date_str) >= 4 and date_str[:4].isdigit():
            year = int(date_str[:4])
            if 1900 <= year <= datetime.now().year + 5:  # Reasonable year range
                return str(year)
        
        return 'Unknown'
    except:
        return 'Unknown'

def calculate_weighted_rating(vote_average, vote_count, min_votes=50):
    """
    Calculate weighted rating using IMDB's formula
    WR = (v/(v+m)) * R + (m/(v+m)) * C
    where:
    WR = weighted rating
    v = number of votes for the movie
    m = minimum votes required (default 50)
    R = average rating of the movie
    C = mean vote across all movies
    """
    try:
        vote_average = float(vote_average) if not pd.isna(vote_average) else 0
        vote_count = float(vote_count) if not pd.isna(vote_count) else 0
        
        # Global average (approximate TMDB average)
        global_avg = 6.0
        
        # Calculate weighted rating
        weighted_rating = (vote_count / (vote_count + min_votes)) * vote_average + \
                         (min_votes / (vote_count + min_votes)) * global_avg
        
        return round(weighted_rating, 2)
    except:
        return 0.0

def filter_quality_movies(df, min_vote_count=10, min_overview_length=10):
    """Filter movies based on quality criteria"""
    original_count = len(df)
    
    # Remove movies with insufficient data
    df = df.dropna(subset=['title', 'overview'])
    
    # Filter by vote count
    df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce').fillna(0)
    df = df[df['vote_count'] >= min_vote_count]
    
    # Filter by overview length
    df = df[df['overview'].str.len() >= min_overview_length]
    
    # Remove adult content if column exists
    if 'adult' in df.columns:
        df = df[df['adult'] == 'False']
    
    print(f"Filtered movies: {original_count} → {len(df)} ({len(df)/original_count*100:.1f}% retained)")
    
    return df

def prepare_content_features(df):
    """Prepare combined features for content-based filtering"""
    features = []
    
    for idx, row in df.iterrows():
        # Clean and combine text features
        title = clean_tmdb_text(row.get('title', ''))
        overview = clean_tmdb_text(row.get('overview', ''))
        genres = row.get('genres', 'Unknown').replace('|', ' ')
        
        # Create combined feature string
        combined = f"{overview} {genres} {title}"
        features.append(combined.lower())
    
    return features

def get_movie_details(df, movie_id=None, title=None):
    """Get detailed information about a specific movie"""
    if movie_id is not None:
        movie = df[df['id'] == movie_id]
    elif title is not None:
        movie = df[df['title'].str.lower().str.contains(title.lower(), na=False)]
    else:
        return None
    
    if movie.empty:
        return None
    
    movie_data = movie.iloc[0]
    
    return {
        'id': movie_data.get('id'),
        'title': movie_data.get('title'),
        'overview': movie_data.get('overview'),
        'genres': movie_data.get('genres'),
        'release_date': movie_data.get('release_date'),
        'year': extract_year_from_date(movie_data.get('release_date')),
        'vote_average': round(float(movie_data.get('vote_average', 0)), 1),
        'vote_count': int(movie_data.get('vote_count', 0)),
        'popularity': round(float(movie_data.get('popularity', 0)), 1),
        'runtime': movie_data.get('runtime'),
        'original_language': movie_data.get('original_language', 'en')
    }

def validate_tmdb_dataset(df):
    """Validate TMDB dataset structure and content"""
    required_columns = ['title', 'overview', 'genres', 'vote_average', 'vote_count']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"⚠️  Missing required columns: {missing_columns}")
        return False
    
    # Check data quality
    print("=== Dataset Validation ===")
    print(f"Total movies: {len(df)}")
    print(f"Movies with title: {df['title'].notna().sum()}")
    print(f"Movies with overview: {df['overview'].notna().sum()}")
    print(f"Movies with genres: {df['genres'].notna().sum()}")
    print(f"Movies with ratings: {df['vote_average'].notna().sum()}")
    
    # Check for duplicates
    duplicates = df.duplicated(subset=['title']).sum()
    print(f"Duplicate titles: {duplicates}")
    
    return True

def get_genre_statistics(df):
    """Get statistics about genres in the dataset"""
    all_genres = {}
    
    for genres_str in df['genres'].dropna():
        genres = genres_str.split('|')
        for genre in genres:
            genre = genre.strip()
            if genre and genre != 'Unknown':
                all_genres[genre] = all_genres.get(genre, 0) + 1
    
    # Sort by frequency
    sorted_genres = sorted(all_genres.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_genres