from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from services.recommendation_service import (
    recommend_hospitals,
)


app = FastAPI(
    title="MedRoute API",
    description=(
        "Hospital routing API using traffic-aware "
        "travel times and predicted wait times."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendationRequest(BaseModel):
    user_latitude: float = Field(
        ge=-90,
        le=90,
    )

    user_longitude: float = Field(
        ge=-180,
        le=180,
    )

    triage_category: str

    age_group: str

    arrival_method: str = "Walk-in"

    limit: int = Field(
        default=5,
        ge=1,
        le=10,
    )


@app.get("/")
def root():
    return {
        "message": "MedRoute API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/recommend")
def recommend(
    request: RecommendationRequest,
):
    recommendations = recommend_hospitals(
        user_latitude=request.user_latitude,
        user_longitude=request.user_longitude,
        triage_category=request.triage_category,
        age_group=request.age_group,
        arrival_method=request.arrival_method,
        limit=request.limit,
    )

    return {
        "count": len(recommendations),
        "recommendations": recommendations,
        "disclaimer": (
            "Wait-time estimates use simulated "
            "hospital operating conditions and are "
            "intended for prototype use only."
        ),
    }

