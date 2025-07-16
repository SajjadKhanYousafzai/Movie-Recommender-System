# 🎥 CineMatch: Intelligent Movie Recommender System
Your AI-powered guide to finding movies you’ll love.

## 🌟 Overview
CineMatch is a smart, content-based movie recommender system built using:

- 🧠 Natural Language Processing (NLP)
- 🎬 The Movie Database (TMDb) API
- 🌐 Streamlit frontend

Get recommendations for similar movies based on plot, genres, cast, crew, and keywords — complete with posters, ratings, and overviews.

## 🖼️ Screenshots
| Home Page | Recommendations |
|-----------|-----------------|
| *Image coming soon* | *Image coming soon* |

## 🚀 Features
- 🎯 Smart movie recommendations using TF-IDF + Cosine Similarity
- 📸 Live movie posters and info from TMDb API
- 🎨 Custom cinematic UI with CSS
- 🔍 Sort by Similarity, Rating, or Name
- 💾 Pickled model and data for reuse

## 🧰 Tech Stack
| Component         | Tools Used                              |
|-------------------|-----------------------------------------|
| **Frontend**      | Streamlit, HTML/CSS                    |
| **Backend**       | Python, Scikit-learn, NLTK             |
| **NLP/ML**        | TF-IDF, Cosine Similarity              |
| **Data**          | TMDb 5000 Dataset                      |
| **API**           | The Movie Database (TMDb)              |
| **Packaging**     | pickle for model/data storage          |

## 📂 Project Structure

```bash
CineMatch/
├── app.py
├── movie_list.pkl
├── similarity.pkl
├── tfidf_vectorizer.pkl
├── Dataset/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
├── requirements.txt
└── README.md
```



## ⚙️ How to Run Locally
### 🔧 1. Clone the Repository
```bash
git clone https://github.com/yourusername/CineMatch.git
cd CineMatch

pip install -r requirements.txt
