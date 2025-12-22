from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from TravelPlannerAgent import generate_itinerary, ACTIVITIES

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    city: str
    days: int
    budget: int
    preferences: list[str]

@app.post("/plan")
def plan_trip(request: TripRequest):
    if request.city not in ACTIVITIES:
        raise HTTPException(status_code=404, detail="City not found")
    
    plan = generate_itinerary(request.city, request.days, request.budget, request.preferences)
    return plan

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)