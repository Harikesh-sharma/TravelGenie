from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import random

app = FastAPI()

# Enable CORS to allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanRequest(BaseModel):
    budget: int
    days: int
    city: str
    preferences: List[str] = []

@app.post("/plan")
async def generate_plan(request: PlanRequest):
    # Mock logic to generate a valid response for the frontend
    itinerary: Dict[str, List[dict]] = {}
    total_cost = 0

    # Define activities for specific cities
    city_data = {
        "Delhi": [
            {"activity": "Red Fort", "cost": 500, "hours": 2},
            {"activity": "India Gate", "cost": 0, "hours": 1},
            {"activity": "Qutub Minar", "cost": 500, "hours": 2},
            {"activity": "Chandni Chowk Food Walk", "cost": 1000, "hours": 2},
            {"activity": "Lotus Temple", "cost": 0, "hours": 1.5},
            {"activity": "Humayun's Tomb", "cost": 500, "hours": 2},
        ],
        "Mumbai": [
            {"activity": "Gateway of India", "cost": 0, "hours": 1},
            {"activity": "Marine Drive Walk", "cost": 0, "hours": 1.5},
            {"activity": "Elephanta Caves", "cost": 800, "hours": 4},
            {"activity": "Juhu Beach", "cost": 200, "hours": 2},
            {"activity": "Colaba Causeway Shopping", "cost": 1500, "hours": 2},
            {"activity": "Siddhivinayak Temple", "cost": 0, "hours": 1.5},
        ],
        "Goa": [
            {"activity": "Calangute Beach", "cost": 0, "hours": 3},
            {"activity": "Fort Aguada", "cost": 300, "hours": 2},
            {"activity": "Basilica of Bom Jesus", "cost": 0, "hours": 1},
            {"activity": "Water Sports", "cost": 2500, "hours": 2},
            {"activity": "Anjuna Flea Market", "cost": 1000, "hours": 2},
            {"activity": "Dudhsagar Falls", "cost": 500, "hours": 4},
        ],
        "Jaipur": [
            {"activity": "Hawa Mahal", "cost": 200, "hours": 1},
            {"activity": "Amber Fort", "cost": 500, "hours": 3},
            {"activity": "City Palace", "cost": 700, "hours": 2},
            {"activity": "Jantar Mantar", "cost": 200, "hours": 1.5},
            {"activity": "Johari Bazaar Shopping", "cost": 1500, "hours": 2},
            {"activity": "Nahargarh Fort Sunset", "cost": 200, "hours": 2},
        ],
        "Bangalore": [
            {"activity": "Lalbagh Botanical Garden", "cost": 100, "hours": 2},
            {"activity": "Bangalore Palace", "cost": 500, "hours": 2},
            {"activity": "Cubbon Park", "cost": 0, "hours": 1.5},
            {"activity": "Wonderla Amusement Park", "cost": 1500, "hours": 5},
            {"activity": "Commercial Street Shopping", "cost": 1000, "hours": 2},
            {"activity": "ISKCON Temple", "cost": 0, "hours": 1.5},
        ]
    }

    default_activities = [
        {"activity": "Visit Local Museum", "cost": 500, "hours": 2},
        {"activity": "City Park Walk", "cost": 0, "hours": 1},
        {"activity": "Famous Temple Visit", "cost": 0, "hours": 1.5},
        {"activity": "Street Food Tour", "cost": 800, "hours": 2},
        {"activity": "Shopping at Market", "cost": 2000, "hours": 3},
        {"activity": "Historical Fort", "cost": 300, "hours": 2.5},
        {"activity": "Lake View Point", "cost": 0, "hours": 1},
    ]

    # Select activities based on city, fallback to default if city not found
    activities_pool = city_data.get(request.city, default_activities)

    for day in range(1, request.days + 1):
        day_key = f"Day {day}"
        day_activities = []
        day_cost = 0
        
        # Shuffle activities to maintain randomness
        daily_candidates = list(activities_pool)
        random.shuffle(daily_candidates)
        
        # Try to add up to 2 activities that fit in the budget
        for act in daily_candidates:
            if len(day_activities) >= 2:
                break
            if total_cost + day_cost + act["cost"] <= request.budget:
                day_activities.append(act)
                day_cost += act["cost"]
            
        itinerary[day_key] = day_activities
        total_cost += day_cost

    return {
        "city": request.city,
        "total_budget": request.budget,
        "total_cost": total_cost,
        "itinerary": itinerary
    }