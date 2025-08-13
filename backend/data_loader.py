import pandas as pd
import numpy as np
import requests
import zipfile
import os
import json

def download_tmdb_instructions():
    """
    Instructions for downloading TMDB Movie Metadata from Kaggle:
    
    1. Go to https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
    2. Click "Download" (you'll need a Kaggle account)
    3. Extract the downloaded ZIP file
    4. You should get these files:
       - tmdb_5000_movies.csv
       - tmdb_5000_credits.csv (optional for this project)
    5. Place tmdb_5000_movies.csv in the 'data' folder of your project
    
    Alternative: You can also use the larger dataset:
    https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
    Which contains movies_metadata.csv with 45,000+ movies
    """
    print("=== TMDB Dataset Download Instructions ===")
    print("1. Visit: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata")
    print("2. Download the dataset (requires Kaggle account)")
    print("3. Extract tmdb_5000_movies.csv to the 'data' folder")
    print("4. Run the backend application")
    print("\nAlternative larger dataset:")
    print("https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset")
    print("Extract movies_metadata.csv to the 'data' folder")

def verify_tmdb_dataset():
    """Verify if TMDB dataset exists and check its structure"""
    data_files = []
    
    # Check for different possible TMDB file names
    possible_files = [
        'data/tmdb_5000_movies.csv',
        'data/movies_metadata.csv',
        'data/tmdb_movies.csv'
    ]
    
    for file_path in possible_files:
        if os.path.exists(file_path):
            data_files.append(file_path)
            print(f"✅ Found: {file_path}")
            
            # Load and inspect the dataset
            try:
                df = pd.read_csv(file_path, nrows=5)  # Load first 5 rows to check structure
                print(f"   Columns: {list(df.columns)}")
                print(f"   Shape (first 5 rows): {df.shape}")
                print(f"   Sample titles: {df['title'].tolist()[:3] if 'title' in df.columns else 'No title column'}")
                print()
            except Exception as e:
                print(f"   ⚠️ Error reading file: {e}")
    
    if not data_files:
        print("❌ No TMDB dataset found!")
        print("Please download the dataset following the instructions above.")
        return False
    
    return True

def load_and_analyze_tmdb_data():
    """Load TMDB dataset and provide analysis"""
    try:
        # Try different file names
        df = None
        file_loaded = None
        
        if os.path.exists('data/tmdb_5000_movies.csv'):
            df = pd.read_csv('data/tmdb_5000_movies.csv')
            file_loaded = 'tmdb_5000_movies.csv'
        elif os.path.exists('data/movies_metadata.csv'):
            df = pd.read_csv('data/movies_metadata.csv', low_memory=False)
            file_loaded = 'movies_metadata.csv'
            # Clean problematic rows for the larger dataset
            df = df[df['adult'] == 'False']  # Remove adult content
        else:
            print("No TMDB dataset found. Please download it first.")
            return None
        
        print(f"Successfully loaded {file_loaded}")
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Data analysis
        print("\n=== Dataset Analysis ===")
        print(f"Total movies: {len(df)}")
        print(f"Date range: {df['release_date'].min()} to {df['release_date'].max()}")
        print(f"Average vote: {df['vote_average'].mean():.2f}")
        print(f"Movies with overview: {df['overview'].notna().sum()}")
        
        # Genre analysis
        if 'genres' in df.columns:
            print(f"Movies with genres: {df['genres'].notna().sum()}")
            
            # Extract unique genres
            all_genres = set()
            for genres_str in df['genres'].dropna():
                try:
                    genres_list = json.loads(genres_str.replace("'", '"'))
                    for genre in genres_list:
                        if isinstance(genre, dict) and 'name' in genre:
                            all_genres.add(genre['name'])
                except:
                    pass
            
            print(f"Unique genres found: {sorted(list(all_genres))}")
        
        # Top movies by popularity/rating
        print("\n=== Top 10 Movies by Vote Average ===")
        top_movies = df.nlargest(10, 'vote_average')[['title', 'vote_average', 'vote_count']]
        for idx, row in top_movies.iterrows():
            print(f"  {row['title']} - {row['vote_average']}/10 ({row['vote_count']} votes)")
        
        return df
        
    except Exception as e:
        print(f"Error loading TMDB data: {e}")
        return None

def create_sample_tmdb_format():
    """Create a sample dataset in TMDB format for testing"""
    print("Creating sample dataset in TMDB format...")
    
    # Sample data in TMDB format
    sample_genres = [
        '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]',
        '[{"id": 35, "name": "Comedy"}, {"id": 10749, "name": "Romance"}]',
        '[{"id": 18, "name": "Drama"}, {"id": 53, "name": "Thriller"}]',
        '[{"id": 27, "name": "Horror"}, {"id": 9648, "name": "Mystery"}]',
        '[{"id": 878, "name": "Science Fiction"}, {"id": 28, "name": "Action"}]'
    ]
    
    np.random.seed(42)
    n_movies = 5000
    
    data = {
        'id': range(1, n_movies + 1),
        'title': [f'Sample Movie {i}' for i in range(1, n_movies + 1)],
        'overview': [
            f'An engaging story about adventure and mystery. Movie {i} features compelling characters and an intricate plot that will keep you on the edge of your seat.'
            for i in range(1, n_movies + 1)
        ],
        'genres': [np.random.choice(sample_genres) for _ in range(n_movies)],
        'release_date': [
            f'{np.random.randint(1970, 2024)}-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}'
            for _ in range(n_movies)
        ],
        'vote_average': np.random.uniform(3.0, 9.5, n_movies),
        'vote_count': np.random.randint(10, 5000, n_movies),
        'popularity': np.random.uniform(0.1, 100.0, n_movies),
        'adult': ['False'] * n_movies,
        'original_language': ['en'] * n_movies,
        'runtime': np.random.randint(80, 200, n_movies)
    }
    
    df = pd.DataFrame(data)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    df.to_csv('data/tmdb_5000_movies.csv', index=False)
    print(f"Created sample TMDB dataset with {len(df)} movies")
    print("Saved to: data/tmdb_5000_movies.csv")
    
    return df

def setup_tmdb_dataset():
    """Main function to setup TMDB dataset"""
    print("=== TMDB Movie Dataset Setup ===\n")
    
    # Check if dataset already exists
    if verify_tmdb_dataset():
        print("Dataset found! Loading and analyzing...")
        df = load_and_analyze_tmdb_data()
        if df is not None:
            print("\n✅ TMDB dataset is ready to use!")
            return df
    
    print("\n📥 TMDB dataset not found.")
    download_tmdb_instructions()
    
    # Ask user if they want to create sample data
    response = input("\nWould you like to create a sample dataset for testing? (y/n): ").strip().lower()
    
    if response in ['y', 'yes']:
        df = create_sample_tmdb_format()
        print("\n✅ Sample dataset created! You can replace it with real TMDB data later.")
        return df
    else:
        print("\nPlease download the TMDB dataset and run this script again.")
        return None

if __name__ == "__main__":
    dataset = setup_tmdb_dataset()
    if dataset is not None:
        print(f"\nDataset ready with {len(dataset)} movies!")
        print("You can now run the Flask application (app.py)")
    else:
        print("\nDataset setup incomplete. Please download the TMDB dataset.")

def get_dataset_info():
    """Get information about the current dataset"""
    if os.path.exists('data/tmdb_5000_movies.csv'):
        df = pd.read_csv('data/tmdb_5000_movies.csv')
        return {
            'filename': 'tmdb_5000_movies.csv',
            'shape': df.shape,
            'columns': list(df.columns),
            'sample_titles': df['title'].head(5).tolist()
        }
    elif os.path.exists('data/movies_metadata.csv'):
        df = pd.read_csv('data/movies_metadata.csv', nrows=100)
        return {
            'filename': 'movies_metadata.csv', 
            'shape': df.shape,
            'columns': list(df.columns),
            'sample_titles': df['title'].head(5).tolist()
        }
    else:
        return None