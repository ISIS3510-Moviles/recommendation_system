
# 🍽️ Restaurant Recommendation System

This project implements a **personalized restaurant recommendation system** using FastAPI and a combination of content-based filtering techniques. The engine analyzes user preferences and behaviors, expands them semantically using external data, and returns a ranked list of restaurants most aligned with the user’s profile.

---

## 🚀 Features

- FastAPI backend with a single `/recommend` endpoint
- Builds a rich user profile based on:
  - Explicit dietary tags
  - Subscribed restaurants
  - Reservations
  - Saved products
  - Comments (weighted by rating, likes, and recency)
- Uses a precomputed tag affinity map based on Yelp data
- Content-based recommendation using:
  - TF-IDF vectorization of tags
  - Cosine similarity between user preferences and restaurants
- Final ranking integrates similarity, average rating, and popularity
- Dockerized for easy deployment

---

## 🧠 How It Works

### 1. User Profile Construction

User preferences are encoded into a weighted dictionary based on all forms of interaction. For example, tags from recent, liked 5-star comments will be weighted more than old 3-star reviews. Tags from subscriptions and saved products are also included.

### 2. Profile Expansion

A tag affinity map, generated from the Yelp dataset using TF-IDF and cosine similarity, is used to semantically expand the user profile. For instance, a user interested in "vegan" might also receive recommendations for "organic", "salad", or "juice bars".

### 3. Restaurant Ranking

Each restaurant is vectorized using its tags (via TF-IDF), and compared with the user profile vector using cosine similarity. The final score is calculated as:

```
score = similarity * rating * (popularity + 1) ^ 0.2
```

This ensures that popular, well-rated, and semantically aligned restaurants are recommended.

---

## 🧪 API

### POST `/recommend`

Request:
```json
{
  "user_id": "user_001",
  "top_n": 10
}
```

Response:
Returns a list of top N restaurants with metadata and scores.

---

## 🐳 Deployment (Docker)

Build and run the app locally using Docker:

```bash
docker build -t recommender .
docker run -p 8000:8000 recommender
```

Or with Docker Compose:

```bash
docker-compose up
```

The service will be available at `http://localhost:8000/recommend`.

---

## 🧾 Files Overview

- `main.py`: FastAPI app and entrypoint.
- `recommendation.py`: Core recommendation logic (profile building, expansion, scoring).
- `user.py`: Loads mock user data from URL.
- `restaurant.py`: Loads and processes restaurant data from URL.
- `tag_affinity.json`: Semantic similarity map between tags.
- `Dockerfile`: Container setup.
- `docker-compose.yml`: Orchestration config.

---

## 📚 Tag Affinity Map

The `tag_affinity.json` file was generated using the Yelp dataset by:

1. Extracting and cleaning `categories` from Yelp business data.
2. Applying TF-IDF vectorization to restaurant tag data.
3. Computing cosine similarity between tag vectors.
4. For each tag, selecting the top-5 most similar tags.

This map enhances recommendations by allowing semantic generalization beyond exact matches.

More details in [`tag_affinity.ipynb`](app/assets/tag_affinity.ipynb).

---

