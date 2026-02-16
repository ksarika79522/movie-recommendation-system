# Movie Recommendation System #  
🎬 MovieRec Pro — AI Movie Recommendation System

A full-stack movie recommendation platform that suggests personalized movies using machine learning and user preference modeling.

🚀 Overview

MovieRec Pro is an end-to-end recommendation system that analyzes user ratings and behavior to generate personalized movie suggestions. The system combines collaborative filtering techniques with a modern web interface for real-time recommendations.

Designed as a portfolio project to demonstrate applied machine learning, backend engineering, and full-stack development.

✨ Features

🎯 Personalized movie recommendations

🤝 Collaborative filtering (user-based & item-based)

⭐ Rating prediction engine

🔍 Search movies by title

📊 Recommendation scoring

⚡ Fast API backend

🖥️ Modern React/Next.js frontend

🧠 Machine Learning Approach

MovieRec Pro uses collaborative filtering techniques to predict user preferences:

Algorithms Used

K-Nearest Neighbors (KNN)

Matrix Factorization (SVD via Surprise library)

User-based filtering

Item-based filtering

Workflow

Load movie dataset (MovieLens/TMDB)

Preprocess ratings

Train recommendation model

Predict unseen ratings

Generate ranked recommendations

🏗️ Tech Stack
Backend

Python

FastAPI

Scikit-learn

Surprise (recommendation library)

Pandas / NumPy

Frontend

React / Next.js

Tailwind CSS

Axios

Data

MovieLens dataset

TMDB metadata

📂 Project Structure
MovieRec-Pro/
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── recommender/
│   └── main.py
│
├── frontend/
│   ├── components/
│   ├── pages/
│   └── styles/
│
├── data/
│   └── datasets
│
└── README.md
⚙️ Installation
Clone the repository
git clone https://github.com/yourusername/MovieRec-Pro.git
cd MovieRec-Pro
Backend Setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
Frontend Setup
cd frontend
npm install
npm run dev
