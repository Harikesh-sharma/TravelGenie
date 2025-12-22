from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import random

app = FastAPI()

class PlanRequest(BaseModel):
    budget: int
    days: int
    city: str
    preferences: List[str]

@app.post("/plan")
async def generate_plan(request: PlanRequest):
    # Simple mock logic to generate a valid response for the frontend
    daily_budget = request.budget / request.days
    
    itinerary: Dict[str, List[dict]] = {}
    total_cost = 0

    activities_pool = [
        {"activity": "Visit Local Museum", "cost": 500, "hours": 2},
        {"activity": "City Park Walk", "cost": 0, "hours": 1},
        {"activity": "Famous Temple Visit", "cost": 0, "hours": 1.5},
        {"activity": "Street Food Tour", "cost": 800, "hours": 2},
        {"activity": "Shopping at Market", "cost": 2000, "hours": 3},
        {"activity": "Historical Fort", "cost": 300, "hours": 2.5},
    ]

    for day in range(1, request.days + 1):
        day_key = f"Day {day}"
        day_activities = []
        day_cost = 0
        
        # Add 2 random activities per day
        daily_acts = random.sample(activities_pool, 2)
        
        for act in daily_acts:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
