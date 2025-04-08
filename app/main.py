from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from app.services import restaurant as restaurant_service
from app.services import user as user_service
from app.services import recommendation as recommendation_service

# affinity map
with open("app/assets/tag_affinity.json", "r") as f:
    tag_affinity = json.load(f)

app = FastAPI()

class RecommendationRequest(BaseModel):
    user_id: str
    top_n: int = 10

@app.post("/recommend")
def recommend(req: RecommendationRequest):
    user = user_service.get_user()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    restaurants_df = restaurant_service.get_restaurants()
    user_profile = recommendation_service.build_user_profile(user)
    expanded_profile = recommendation_service.expand_user_profile(user_profile, tag_affinity)
    recommendations = recommendation_service.recommend_restaurants(expanded_profile, restaurants_df, top_n=req.top_n)
    
    return recommendations.to_dict(orient="records")
