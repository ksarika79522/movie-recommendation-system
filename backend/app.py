from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

class MovieRecommendationSystem:
    def __init__(self):
        self.movies_df = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.vectorizer = None

    def load_data(self):
        """Load and preprocess the TMDB movie dataset"""
        try:
            if os.path.exists('data/tmdb_5000_movies.csv'):
                self.movies_df = pd.read_csv('data/tmdb_5000_movies.csv')
            elif os.path.exists('data/movies_metadata.csv'):
                self.movies_df = pd.read_csv('data/movies_metadata.csv', low_memory=False)
                self.movies_df = self.movies_df[self.movies_df['adult'] == 'False']
                self.movies_df['vote_average'] = pd.to_numeric(self.movies_df['vote_average'], errors='coerce')
                self.movies_df = self.movies_df.dropna(subset=['overview', 'title'])
                self.movies_df = self.movies_df[self.movies_df['vote_count'].astype(float) > 10]
            else:
                return self.create_sample_dataset()

            self.movies_df = self.clean_tmdb_data()
            return True
        except Exception as e:
            print(f"Error loading TMDB data: {e}")
            return self.create_sample_dataset()

    def create_sample_dataset(self):
        """Create fallback sample dataset"""
        try:
            sample_data = {
                'id': range(1, 5001),
                'title': [f'Sample Movie {i}' for i in range(1, 5001)],
                'genres': [self.generate_sample_genres() for _ in range(5000)],
                'overview': [f'This is a sample movie {i} with an exciting plot.' for i in range(1, 5001)],
                'vote_average': np.random.uniform(4.0, 9.0, 5000),
                'vote_count': np.random.randint(50, 5000, 5000),
                'release_date': [f'{np.random.randint(1980, 2024)}-{np.random.randint(1,13):02d}-01' for _ in range(5000)],
                'runtime': np.random.randint(80, 200, 5000),
                'popularity': np.random.uniform(1.0, 100.0, 5000)
            }
            self.movies_df = pd.DataFrame(sample_data)
            return True
        except Exception as e:
            print(f"Error creating sample dataset: {e}")
            return False

    def generate_sample_genres(self):
        genres = ['Action', 'Adventure', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller']
        selected = np.random.choice(genres, size=np.random.randint(1,4), replace=False)
        return '[{"name": "' + '"}, {"name": "'.join(selected) + '"}]'

    def clean_tmdb_data(self):
        df = self.movies_df.copy()
        df['overview'] = df['overview'].fillna('No overview available')
        df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce').fillna(0)
        df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce').fillna(0)
        df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce').fillna(0)
        df['genres'] = df['genres'].apply(self.extract_genres)
        df['title'] = df['title'].astype(str)
        df['overview'] = df['overview'].astype(str)
        df = df[df['vote_count'] >= 10]
        df = df[df['overview'].str.len() > 10]
        df = df.sort_values('popularity', ascending=False).reset_index(drop=True)
        return df

    def extract_genres(self, genres_str):
        try:
            if pd.isna(genres_str) or genres_str == '':
                return 'Unknown'
            genres_list = json.loads(genres_str.replace("'", '"'))
            genre_names = [g['name'] for g in genres_list if 'name' in g]
            return '|'.join(genre_names) if genre_names else 'Unknown'
        except:
            return 'Unknown'

    def preprocess_data(self):
        self.movies_df['clean_title'] = self.movies_df['title'].str.lower()
        self.movies_df['clean_overview'] = self.movies_df['overview'].fillna('').str.lower()
        self.movies_df['combined_features'] = (
            self.movies_df['clean_overview'] + ' ' + 
            self.movies_df['genres'].str.replace('|', ' ') + ' ' +
            self.movies_df['clean_title']
        )

    def build_recommendation_models(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1,2))
        self.tfidf_matrix = self.vectorizer.fit_transform(self.movies_df['combined_features'])
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_content_recommendations(self, movie_title, num_recommendations=10, offset=0):
        """Get recommendations with offset to avoid repeats"""
        try:
            movie_matches = self.movies_df[
                self.movies_df['title'].str.lower().str.contains(movie_title.lower(), na=False)
            ]
            if movie_matches.empty:
                return []

            idx = movie_matches.index[0]
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Skip the movie itself + previous offset
            movie_indices = [i[0] for i in sim_scores[1 + offset : 1 + offset + num_recommendations]]
            recommendations = self.movies_df.iloc[movie_indices][
                ['title', 'genres', 'vote_average', 'overview', 'release_date', 'popularity']
            ].to_dict('records')

            for movie in recommendations:
                movie['vote_average'] = round(movie['vote_average'], 1)
                movie['popularity'] = round(movie['popularity'], 1)
                movie['year'] = str(movie['release_date'])[:4] if movie['release_date'] else 'Unknown'

            return recommendations
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []

    def get_popular_movies(self, num_movies=20):
        self.movies_df['weighted_score'] = self.movies_df['popularity'] * 0.3 + self.movies_df['vote_average'] * 0.7
        popular = self.movies_df.nlargest(num_movies, 'weighted_score')[
            ['title', 'genres', 'vote_average', 'overview', 'release_date', 'popularity']
        ].to_dict('records')
        for movie in popular:
            movie['vote_average'] = round(movie['vote_average'], 1)
            movie['popularity'] = round(movie['popularity'], 1)
        return popular

    def search_movies(self, query, limit=10):
        try:
            title_mask = self.movies_df['title'].str.lower().str.contains(query.lower(), na=False)
            exact_matches = self.movies_df[self.movies_df['title'].str.lower() == query.lower()].head(limit//2)
            partial_matches = self.movies_df[title_mask & (self.movies_df['title'].str.lower() != query.lower())].head(limit - len(exact_matches))
            results_df = pd.concat([exact_matches, partial_matches]).head(limit)
            results = results_df[
                ['title', 'genres', 'vote_average', 'overview', 'release_date', 'popularity']
            ].to_dict('records')
            for movie in results:
                movie['vote_average'] = round(movie['vote_average'], 1)
                movie['popularity'] = round(movie['popularity'], 1)
                movie['year'] = str(movie['release_date'])[:4] if movie['release_date'] else 'Unknown'
            return results
        except Exception as e:
            print(f"Error searching movies: {e}")
            return []

# Initialize system
recommender = MovieRecommendationSystem()

@app.route('/api/initialize', methods=['POST'])
def initialize_system():
    try:
        success = recommender.load_data()
        if success:
            recommender.preprocess_data()
            recommender.build_recommendation_models()
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/movies/popular', methods=['GET'])
def get_popular_movies():
    try:
        limit = request.args.get('limit', 20, type=int)
        movies = recommender.get_popular_movies(limit)
        return jsonify({"movies": movies})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/movies/search', methods=['GET'])
def search_movies():
    try:
        query = request.args.get('q', '')
        limit = request.args.get('limit', 10, type=int)
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
        movies = recommender.search_movies(query, limit)
        return jsonify({"movies": movies})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.json
        movie_title = data.get('movie_title', '')
        num_recommendations = data.get('num_recommendations', 10)
        offset = data.get('offset', 0)  # <-- new

        if not movie_title:
            return jsonify({"error": "Movie title is required"}), 400

        recommendations = recommender.get_content_recommendations(
            movie_title, num_recommendations, offset
        )
        if not recommendations:
            return jsonify({"error": "No recommendations available"}), 404

        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("Starting Movie Recommendation System...")
    recommender.load_data()
    recommender.preprocess_data()
    recommender.build_recommendation_models()
    print("System ready!")
    app.run(debug=True, host='0.0.0.0', port=5001)
