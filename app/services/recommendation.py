from collections import defaultdict
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

NOW = datetime.utcnow()
MAX_COMMENT_AGE_DAYS = 365 

def build_user_profile(user):
    tag_weights = defaultdict(float)
    for tag in user.tags:
        tag_weights[tag.lower()] += 1.0
    for r in user.subscribed_restaurants:
        for tag in r["tags"]:
            tag_weights[tag.lower()] += 0.8
    for r in user.reservations:
        for tag in r["restaurant"]["tags"]:
            tag_weights[tag.lower()] += 0.6
    for p in user.saved_products:
        for tag in p.get("tags", []):
            tag_weights[tag.lower()] += 0.5
    for c in user.comments:
        comment_rating = c.get("rating", 3)
        comment_likes = c.get("likes", 0)
        comment_date = c.get("datetime", NOW)
        comment_date = datetime.strptime(comment_date, "%Y-%m-%dT%H:%M:%SZ") if isinstance(comment_date, str) else comment_date

        # weight according to antiquity of the comment
        days_since = (NOW - comment_date).days
        time_weight = max(0.1, 1 - days_since / MAX_COMMENT_AGE_DAYS)

        # weight according to likes
        like_weight = min(comment_likes / 50, 1.0) * 0.3

        # weight according to rating
        if comment_rating >= 4:
            sentiment_weight = 0.6
        elif comment_rating <= 2:
            sentiment_weight = -0.6
        else:
            sentiment_weight = 0.0

        total_weight = (sentiment_weight + like_weight) * time_weight

        for tag in c["restaurant"]["tags"]:
            tag_weights[tag.lower()] += total_weight

    max_weight = max(tag_weights.values(), default=1)
    return {tag: w / max_weight for tag, w in tag_weights.items()}

def expand_user_profile(profile, affinity_map, weight_factor=0.5):
    expanded_profile = defaultdict(float, profile)
    for tag, weight in profile.items():
        for related in affinity_map.get(tag, []):
            expanded_profile[related] += weight * weight_factor
    return dict(expanded_profile)

def recommend_restaurants(expanded_profile, restaurants_df, top_n=10):
    user_text = ' '.join([f"{tag}" for tag, weight in expanded_profile.items() if weight > 0.1])
    restaurants_df['tag_text'] = restaurants_df['tags'].apply(lambda tags: ' '.join(tags).lower())
    vectorizer = TfidfVectorizer()
    rest_vectors = vectorizer.fit_transform(restaurants_df['tag_text'])
    user_vector = vectorizer.transform([user_text])
    similarities = cosine_similarity(user_vector, rest_vectors).flatten()
    restaurants_df['similarity'] = similarities
    restaurants_df['score'] = (
        restaurants_df['similarity'] *
        restaurants_df['rating'].fillna(3.5) *
        (restaurants_df['popularity'].fillna(1) + 1) ** 0.2
    )
    return restaurants_df.sort_values(by='score', ascending=False).head(top_n)
