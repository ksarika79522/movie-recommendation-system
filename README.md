# 🎬 MovieRec Pro — AI Movie Recommendation System

A full-stack movie recommendation platform that generates personalized movie suggestions using machine learning and user preference modeling.

---

## 🚀 Overview

MovieRec Pro is an end-to-end recommendation system that analyzes user ratings and behavior to produce personalized movie suggestions. The system combines collaborative filtering techniques with a modern web interface for real-time recommendations.

This project demonstrates applied machine learning, backend engineering, and full-stack development.

---

## ✨ Features

- 🎯 Personalized movie recommendations  
- 🤝 Collaborative filtering (user-based & item-based)  
- ⭐ Rating prediction engine  
- 🔍 Movie search by title  
- 📊 Ranked recommendation scoring  
- ⚡ Fast API backend  
- 🖥️ Modern React/Next.js frontend  

---

## 🧠 Machine Learning Approach

MovieRec Pro uses collaborative filtering to predict user preferences and recommend unseen movies.

### Algorithms Used

- K-Nearest Neighbors (KNN)
- Matrix Factorization (SVD via Surprise library)
- User-based filtering
- Item-based filtering

### Workflow

1. Load movie dataset (MovieLens / TMDB)
2. Preprocess ratings data
3. Train recommendation model
4. Predict ratings for unseen movies
5. Generate Top-N recommendations

---

## 🏗️ Tech Stack

### Backend
- Python  
- FastAPI  
- Scikit-learn  
- Surprise (recommendation library)  
- Pandas / NumPy  

### Frontend
- React / Next.js  
- Tailwind CSS  
- Axios  

### Data
- MovieLens dataset  
- TMDB metadata  

---

## 📂 Project Structure


---

## ⚙️ Installation

### 1. Clone the Repository


### 2. Backend Setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Backend will run at:
http://127.0.0.1:8000


---

### 3. Frontend Setup

cd frontend
npm install
npm run dev


Frontend will run at:
http://localhost:3000


---

## 📈 Example Recommendation Flow

1. User selects favorite movies  
2. System analyzes similar users/items  
3. Model predicts ratings for unseen movies  
4. Top recommendations returned  

---

## 🎯 Future Improvements

- Hybrid recommender (content + collaborative)
- AI chat movie assistant
- User authentication
- Watchlist system
- Cloud deployment

---

## 🧑‍💻 Author

**Karthik Sarika**  
Computer Science Student @ NC State  
Aspiring Software Engineer & AI Developer  

---

## ⭐ Why This Project Matters

This project demonstrates:

- Applied machine learning  
- Data pipeline design  
- Full-stack engineering  
- Scalable API development  
- Real-world recommendation systems  

---

## 📜 License

This project is licensed under the MIT License.
