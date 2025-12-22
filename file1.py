from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import json
import os
from TravelPlannerAgent import ACTIVITIES

class TravelPlannerAgent:
    def __init__(self, budget, days, city, preferences):
        self.budget = budget
        self.days = days
        self.city = city
        self.preferences = preferences
        self.daily_hours_limit = 8
        self.itinerary = {}
        self.total_cost = 0
        self.visited_activities = set()
        self.remaining_budget = budget
        self.daily_hours_used = {}

    @staticmethod
    def validate_input(data):
        if data["budget"] <= 0:
            raise ValueError("Invalid budget")
        if data["days"] < 1:
            raise ValueError("Invalid days")
        
        # Case-insensitive city matching
        city_input = data["city"].strip().lower()
        found_city = None
        for city_key in ACTIVITIES.keys():
            if city_key.lower() == city_input:
                found_city = city_key
                break
        
        if not found_city:
            raise ValueError(f"City '{data['city']}' not found")
        
        # Update data with the correct casing
        data["city"] = found_city

        if not data["preferences"]:
            raise ValueError("Preferences cannot be empty")

    def plan_day(self, day_budget):
        day_plan = []
        used_hours = 0
        spent = 0

        for pref in self.preferences:
            for activity in ACTIVITIES[self.city].get(pref, []):
                # Check constraints: Not visited, Cost <= daily budget, Time <= daily limit
                if activity["name"] in self.visited_activities:
                    continue
                if spent + activity["cost"] > day_budget:
                    continue
                # Check Time limit per day
                if used_hours + activity["hours"] > self.daily_hours_limit:
                    continue

                day_plan.append(activity)
                spent += activity["cost"]
                used_hours += activity["hours"]
                self.visited_activities.add(activity["name"])

        return day_plan, spent, used_hours

    def generate_plan(self):
        if self.city not in ACTIVITIES:
            print(f"⚠ Error: City '{self.city}' not found.")
            return

        self.remaining_budget = self.budget

        # Splits the trip into days
        for day in range(1, self.days + 1):
            remaining_days = self.days - day + 1
            
            # Allocates a dynamic budget per day
            day_budget = self.remaining_budget / remaining_days
            
            # Starts selecting activities
            day_plan, spent, used_hours = self.plan_day(day_budget)

            self.itinerary[f"Day {day}"] = day_plan
            self.daily_hours_used[f"Day {day}"] = used_hours
            self.total_cost += spent
            self.remaining_budget -= spent

        self.validate_plan()

    def validate_plan(self):
        # Constraint Checking (Self-Evaluation)
        # Check Total cost vs budget
        if self.total_cost > self.budget:
            print("⚠ Budget exceeded. Re-planning...")
            self.replan_with_llm()

    def get_activity_category(self, activity_name):
        if self.city in ACTIVITIES:
            for category, acts in ACTIVITIES[self.city].items():
                for act in acts:
                    if act["name"] == activity_name:
                        return category
        return None

    def recalculate_state(self):
        """Recalculates costs and usage based on the current itinerary."""
        self.total_cost = 0
        self.visited_activities = set()
        self.daily_hours_used = {}
        
        for day, acts in self.itinerary.items():
            day_hours = 0
            for act in acts:
                self.total_cost += act["cost"]
                day_hours += act["hours"]
                self.visited_activities.add(act["name"])
            self.daily_hours_used[day] = day_hours
            
        self.remaining_budget = self.budget - self.total_cost

    def replan_with_llm(self):
        """Uses an LLM to intelligently adjust the itinerary if budget is exceeded."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠ OPENAI_API_KEY not found. Using heuristic replanning.")
            self.replan()
            return

        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            available_activities = ACTIVITIES.get(self.city, {})
            prompt = f"""
            You are an expert travel planner. The current itinerary exceeds the budget.
            Budget: {self.budget}
            Current Cost: {self.total_cost}
            City: {self.city}
            
            Current Itinerary: {json.dumps(self.itinerary)}
            Available Activities: {json.dumps(available_activities)}
            
            Task: Modify the itinerary to fit strictly within the budget. You can replace expensive activities with cheaper ones or remove them. Maintain a logical flow.
            Output: Return ONLY valid JSON matching the structure of the Current Itinerary (keys like 'Day 1', 'Day 2').
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                          {"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("LLM returned empty response")
            new_plan = json.loads(content)
            # Handle potential nesting if LLM wraps it
            self.itinerary = new_plan.get("itinerary", new_plan)
            self.recalculate_state()
            print("✅ LLM Re-planning successful.")
            
        except Exception as e:
            print(f"⚠ LLM Re-planning failed: {e}. Using heuristic replanning.")
            self.replan()

    def replan(self):
        while self.total_cost > self.budget:
            # Find the single most expensive activity across the entire itinerary
            most_expensive = None
            target_day = None

            for day, activities in self.itinerary.items():
                if activities:
                    day_max = max(activities, key=lambda x: x["cost"])
                    if most_expensive is None or day_max["cost"] > most_expensive["cost"]:
                        most_expensive = day_max
                        target_day = day

            if most_expensive and target_day:
                # Try to replace with a cheaper activity from the same category
                category = self.get_activity_category(most_expensive["name"])
                replaced = False

                if category:
                    current_day_hours = self.daily_hours_used[target_day]
                    freed_hours = most_expensive["hours"]

                    # Find candidates: same category, cheaper, not visited, fits in time
                    candidates = []
                    if self.city in ACTIVITIES and category in ACTIVITIES[self.city]:
                        for act in ACTIVITIES[self.city][category]:
                            if (act["name"] not in self.visited_activities and 
                                act["cost"] < most_expensive["cost"]):
                                if (current_day_hours - freed_hours + act["hours"]) <= self.daily_hours_limit:
                                    candidates.append(act)

                    if candidates:
                        # Pick the most expensive candidate (highest quality) that is still cheaper
                        best_candidate = max(candidates, key=lambda x: x["cost"])

                        # Replace in itinerary
                        idx = self.itinerary[target_day].index(most_expensive)
                        self.itinerary[target_day][idx] = best_candidate

                        # Update stats
                        self.total_cost = self.total_cost - most_expensive["cost"] + best_candidate["cost"]
                        self.remaining_budget = self.remaining_budget + most_expensive["cost"] - best_candidate["cost"]
                        self.daily_hours_used[target_day] = self.daily_hours_used[target_day] - most_expensive["hours"] + best_candidate["hours"]

                        # Update visited
                        if most_expensive["name"] in self.visited_activities:
                            self.visited_activities.remove(most_expensive["name"])
                        self.visited_activities.add(best_candidate["name"])
                        replaced = True
                        print(f"Replaced '{most_expensive['name']}' with '{best_candidate['name']}'")

                if not replaced:
                    self.itinerary[target_day].remove(most_expensive)
                    self.total_cost -= most_expensive["cost"]
                    self.remaining_budget += most_expensive["cost"]
                    self.daily_hours_used[target_day] -= most_expensive["hours"]
                    if most_expensive["name"] in self.visited_activities:
                        self.visited_activities.remove(most_expensive["name"])
                    print(f"Removed '{most_expensive['name']}'")
            else:
                break

    def final_output(self):
        formatted_itinerary = {}
        for day, acts in self.itinerary.items():
            formatted_itinerary[day] = [
                {"activity": act["name"], "cost": act["cost"], "hours": act["hours"]}
                for act in acts
            ]

        return {
            "city": self.city,
            "total_budget": self.budget,
            "total_cost": self.total_cost,
            "itinerary": formatted_itinerary
        }

    def print_formatted_itinerary(self):
        data = self.final_output()
        remaining_budget = data["total_budget"] - data["total_cost"]
        cost_breakdown = {day: sum(act["cost"] for act in acts) for day, acts in data["itinerary"].items()}
        
        print("\n" + "="*50)
        print(f"{'TRIP SUMMARY':^50}")
        print("="*50)
        print(f"{'City':<20}: {data['city']}")
        print(f"{'Total Budget':<20}: ₹{data['total_budget']}")
        print(f"{'Total Cost':<20}: ₹{data['total_cost']}")
        print(f"{'Remaining Budget':<20}: ₹{remaining_budget}")
        print("-" * 50)

        print("\n" + "="*65)
        print(f"{'DETAILED ITINERARY':^65}")
        print("="*65)
        print(f"{'Day':<8} | {'Activity':<30} | {'Cost':<8} | {'Hours':<5}")
        print("-" * 65)
        
        for day, activities in data['itinerary'].items():
            for act in activities:
                print(f"{day:<8} | {act['activity']:<30} | ₹{act['cost']:<7} | {act['hours']:<5}")
        print("-" * 65)

        print("\n" + "="*30)
        print(f"{'COST BREAKDOWN':^30}")
        print("="*30)
        print(f"{'Day':<15} | {'Total':<10}")
        print("-" * 30)
        for day, cost in cost_breakdown.items():
            print(f"{day:<15} | ₹{cost:<10}")
        print("="*30 + "\n")

if __name__ == "__main__":
    pass

app = FastAPI()

# Add CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Default Vite port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripInput(BaseModel):
    budget: int
    days: int
    city: str
    preferences: List[str]

@app.get("/")
def home():
    return FileResponse('index.html')

@app.post("/plan")
def plan_trip(input_data: TripInput):
    data = input_data.dict()
    try:
        TravelPlannerAgent.validate_input(data)
        agent = TravelPlannerAgent(
            budget=data["budget"],
            days=data["days"],
            city=data["city"],
            preferences=data["preferences"]
        )
        agent.generate_plan()
        return agent.final_output()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("file1:app", host="127.0.0.1", port=8000, reload=True)
