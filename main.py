from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from typing import List, Dict
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from email_validator import validate_email, EmailNotValidError
import sqlite3
import uvicorn

app = FastAPI()

# Enable CORS to allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    with sqlite3.connect("subscribers.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS subscribers (email TEXT PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        conn.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, package_name TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

@app.on_event("startup")
async def startup_event():
    init_db()

class Subscriber(BaseModel):
    email: EmailStr

class PlanRequest(BaseModel):
    budget: int
    days: int
    city: str
    preferences: List[str] = []

class BookingRequest(BaseModel):
    email: EmailStr
    package_name: str

def send_welcome_email(email_to: str):
    # Configuration - In production, use Environment Variables!
    smtp_server = "smtp.gmail.com" # Example for Gmail
    smtp_port = 587
    sender_email = "sharikesh462@gmail.com" 
    sender_password = "ldsmaowmarctprtd"

    subject = "Your Journey Begins with TravelGenie! 🌟"
    
    unsubscribe_url = f"http://127.0.0.1:8000/unsubscribe?email={email_to}"
    
    html_content = f"""
    <html>
        <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1f2937; line-height: 1.6; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px; border: 1px solid #e5e7eb; border-radius: 12px; background-color: #ffffff;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #4f46e5; margin: 0; font-size: 24px;">Welcome Aboard! 🌍</h1>
                </div>
                <p style="font-size: 16px;">Hello Traveler,</p>
                <p style="font-size: 16px;">Thank you for joining the <strong>TravelGenie</strong> family! We are excited to help you plan your dream vacations.</p>
                
                <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <p style="margin: 0 0 10px 0; font-weight: bold;">Here is what you can expect:</p>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li style="margin-bottom: 8px;">✨ Personalized AI itineraries</li>
                        <li style="margin-bottom: 8px;">💸 Smart budget tracking</li>
                        <li style="margin-bottom: 0;">📍 Exclusive destination guides</li>
                    </ul>
                </div>
                
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 40px 0 20px 0;">
                <p style="font-size: 12px; color: #6b7280; text-align: center;">
                    © 2024 TravelGenie AI. All rights reserved.<br>
                    You received this email because you signed up on our website.
                    <br><a href="{unsubscribe_url}" style="color: #6b7280; text-decoration: underline;">Unsubscribe</a>
                </p>
            </div>
        </body>
    </html>
    """
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email_to
    message["Subject"] = subject
    message.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        print(f"Email sent successfully to {email_to}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

@app.get("/")
def read_root():
    return {"message": "TravelGenie API is running!"}

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
            {"activity": "Akshardham Temple", "cost": 0, "hours": 3},
            {"activity": "Lodhi Gardens", "cost": 0, "hours": 1.5},
            {"activity": "Sarojini Nagar Market", "cost": 1500, "hours": 2},
            {"activity": "National Museum", "cost": 20, "hours": 2},
            {"activity": "Hauz Khas Village", "cost": 800, "hours": 2},
        ],
        "Mumbai": [
            {"activity": "Gateway of India", "cost": 0, "hours": 1},
            {"activity": "Marine Drive Walk", "cost": 0, "hours": 1.5},
            {"activity": "Elephanta Caves", "cost": 800, "hours": 4},
            {"activity": "Juhu Beach", "cost": 200, "hours": 2},
            {"activity": "Colaba Causeway Shopping", "cost": 1500, "hours": 2},
            {"activity": "Siddhivinayak Temple", "cost": 0, "hours": 1.5},
            {"activity": "Chhatrapati Shivaji Maharaj Vastu Sangrahalaya", "cost": 100, "hours": 2},
            {"activity": "Haji Ali Dargah", "cost": 0, "hours": 1},
            {"activity": "Bandra-Worli Sea Link", "cost": 0, "hours": 0.5},
            {"activity": "Sanjay Gandhi National Park", "cost": 100, "hours": 3},
            {"activity": "Crawford Market", "cost": 500, "hours": 1.5},
        ],
        "Goa": [
            {"activity": "Calangute Beach", "cost": 0, "hours": 3},
            {"activity": "Fort Aguada", "cost": 300, "hours": 2},
            {"activity": "Basilica of Bom Jesus", "cost": 0, "hours": 1},
            {"activity": "Water Sports", "cost": 2500, "hours": 2},
            {"activity": "Anjuna Flea Market", "cost": 1000, "hours": 2},
            {"activity": "Dudhsagar Falls", "cost": 500, "hours": 4},
            {"activity": "Palolem Beach", "cost": 0, "hours": 3},
            {"activity": "Chapora Fort", "cost": 0, "hours": 1.5},
            {"activity": "Reis Magos Fort", "cost": 50, "hours": 1},
            {"activity": "Naval Aviation Museum", "cost": 30, "hours": 1},
            {"activity": "Tito's Lane", "cost": 1500, "hours": 3},
        ],
        "Jaipur": [
            {"activity": "Hawa Mahal", "cost": 200, "hours": 1},
            {"activity": "Amber Fort", "cost": 500, "hours": 3},
            {"activity": "City Palace", "cost": 700, "hours": 2},
            {"activity": "Jantar Mantar", "cost": 200, "hours": 1.5},
            {"activity": "Johari Bazaar Shopping", "cost": 1500, "hours": 2},
            {"activity": "Nahargarh Fort Sunset", "cost": 200, "hours": 2},
            {"activity": "Albert Hall Museum", "cost": 300, "hours": 2},
            {"activity": "Birla Mandir", "cost": 0, "hours": 1},
            {"activity": "Jal Mahal", "cost": 0, "hours": 0.5},
            {"activity": "Patrika Gate", "cost": 0, "hours": 1},
            {"activity": "Chokhi Dhani", "cost": 800, "hours": 3},
        ],
        "Bangalore": [
            {"activity": "Lalbagh Botanical Garden", "cost": 100, "hours": 2},
            {"activity": "Bangalore Palace", "cost": 500, "hours": 2},
            {"activity": "Cubbon Park", "cost": 0, "hours": 1.5},
            {"activity": "Wonderla Amusement Park", "cost": 1500, "hours": 5},
            {"activity": "Commercial Street Shopping", "cost": 1000, "hours": 2},
            {"activity": "ISKCON Temple", "cost": 0, "hours": 1.5},
            {"activity": "Bannerghatta Biological Park", "cost": 300, "hours": 4},
            {"activity": "Tipu Sultan's Summer Palace", "cost": 20, "hours": 1},
            {"activity": "UB City Mall", "cost": 500, "hours": 2},
            {"activity": "Nandi Hills", "cost": 100, "hours": 4},
            {"activity": "Visvesvaraya Museum", "cost": 50, "hours": 2},
        ],
        "Agra": [
            {"activity": "Taj Mahal", "cost": 1100, "hours": 3},
            {"activity": "Agra Fort", "cost": 600, "hours": 2},
            {"activity": "Mehtab Bagh", "cost": 300, "hours": 1.5},
            {"activity": "Fatehpur Sikri", "cost": 600, "hours": 3},
            {"activity": "Street Food at Sadar Bazaar", "cost": 500, "hours": 1.5},
            {"activity": "Tomb of Itimad-ud-Daulah", "cost": 210, "hours": 1.5},
            {"activity": "Akbar's Tomb", "cost": 200, "hours": 2},
            {"activity": "Jama Masjid", "cost": 0, "hours": 1},
            {"activity": "Anguri Bagh", "cost": 0, "hours": 1},
            {"activity": "Kinari Bazar", "cost": 500, "hours": 2},
        ],
        "Varanasi": [
            {"activity": "Kashi Vishwanath Temple", "cost": 0, "hours": 2},
            {"activity": "Ganga Aarti at Dashashwamedh Ghat", "cost": 0, "hours": 2},
            {"activity": "Boat Ride on Ganges", "cost": 500, "hours": 1.5},
            {"activity": "Sarnath", "cost": 300, "hours": 3},
            {"activity": "Assi Ghat", "cost": 0, "hours": 1},
            {"activity": "Ramnagar Fort", "cost": 50, "hours": 2},
            {"activity": "Tulsi Manas Temple", "cost": 0, "hours": 1},
            {"activity": "Sankat Mochan Hanuman Temple", "cost": 0, "hours": 1},
            {"activity": "Manikarnika Ghat", "cost": 0, "hours": 1},
            {"activity": "Bharat Mata Mandir", "cost": 20, "hours": 1},
        ],
        "Udaipur": [
            {"activity": "City Palace", "cost": 400, "hours": 3},
            {"activity": "Lake Pichola Boat Ride", "cost": 500, "hours": 1},
            {"activity": "Jag Mandir", "cost": 0, "hours": 1},
            {"activity": "Saheliyon Ki Bari", "cost": 100, "hours": 1},
            {"activity": "Bagore Ki Haveli", "cost": 200, "hours": 1.5},
            {"activity": "Monsoon Palace (Sajjangarh)", "cost": 150, "hours": 2},
            {"activity": "Vintage Car Museum", "cost": 350, "hours": 1},
            {"activity": "Shilpgram", "cost": 50, "hours": 2},
            {"activity": "Ambrai Ghat", "cost": 0, "hours": 1},
            {"activity": "Fateh Sagar Lake", "cost": 0, "hours": 1.5},
        ],
        "Jaisalmer": [
            {"activity": "Jaisalmer Fort", "cost": 250, "hours": 3},
            {"activity": "Sam Sand Dunes Camel Safari", "cost": 1500, "hours": 4},
            {"activity": "Patwon Ki Haveli", "cost": 200, "hours": 1},
            {"activity": "Gadisar Lake", "cost": 0, "hours": 1},
            {"activity": "Kuldhara Village", "cost": 100, "hours": 2},
            {"activity": "Bada Bagh", "cost": 100, "hours": 1},
            {"activity": "Jain Temples", "cost": 50, "hours": 1},
            {"activity": "Desert National Park", "cost": 100, "hours": 3},
            {"activity": "Tanot Mata Temple", "cost": 0, "hours": 4},
            {"activity": "Jaisalmer War Museum", "cost": 50, "hours": 1.5},
        ],
        "Munnar": [
            {"activity": "Tea Gardens Tour", "cost": 500, "hours": 3},
            {"activity": "Eravikulam National Park", "cost": 200, "hours": 3},
            {"activity": "Mattupetty Dam", "cost": 0, "hours": 1},
            {"activity": "Echo Point", "cost": 0, "hours": 0.5},
            {"activity": "Tea Museum", "cost": 150, "hours": 1},
            {"activity": "Top Station", "cost": 0, "hours": 2},
            {"activity": "Pothamedu View Point", "cost": 0, "hours": 1},
            {"activity": "Attukad Waterfalls", "cost": 0, "hours": 1.5},
            {"activity": "Blossom Park", "cost": 50, "hours": 1.5},
            {"activity": "Kundala Lake", "cost": 0, "hours": 1},
        ],
        "Alleppey": [
            {"activity": "Houseboat Cruise", "cost": 3000, "hours": 5},
            {"activity": "Alappuzha Beach", "cost": 0, "hours": 2},
            {"activity": "Marari Beach", "cost": 0, "hours": 2},
            {"activity": "Ambalapuzha Temple", "cost": 0, "hours": 1},
            {"activity": "Kayaking", "cost": 800, "hours": 2},
            {"activity": "Kuttanad Backwaters", "cost": 500, "hours": 3},
            {"activity": "Krishnapuram Palace", "cost": 50, "hours": 1.5},
            {"activity": "Pathiramanal Island", "cost": 0, "hours": 2},
            {"activity": "Alleppey Lighthouse", "cost": 20, "hours": 1},
            {"activity": "Revi Karunakaran Museum", "cost": 150, "hours": 1.5},
        ],
        "Manali": [
            {"activity": "Hadimba Temple", "cost": 50, "hours": 1},
            {"activity": "Solang Valley Adventure", "cost": 2000, "hours": 4},
            {"activity": "Jogini Waterfalls Trek", "cost": 0, "hours": 3},
            {"activity": "Mall Road Shopping", "cost": 1000, "hours": 2},
            {"activity": "Old Manali Cafe Hopping", "cost": 800, "hours": 2},
            {"activity": "Vashisht Hot Water Springs", "cost": 0, "hours": 1},
            {"activity": "Manu Temple", "cost": 0, "hours": 1},
            {"activity": "Naggar Castle", "cost": 30, "hours": 2},
            {"activity": "Beas River", "cost": 0, "hours": 1},
            {"activity": "Hampta Pass (Day trek)", "cost": 0, "hours": 5},
        ],
        "Shimla": [
            {"activity": "The Ridge", "cost": 0, "hours": 1},
            {"activity": "Mall Road", "cost": 1000, "hours": 2},
            {"activity": "Jakhu Temple", "cost": 0, "hours": 2},
            {"activity": "Kufri Fun World", "cost": 1500, "hours": 4},
            {"activity": "Christ Church", "cost": 0, "hours": 0.5},
            {"activity": "Viceregal Lodge", "cost": 50, "hours": 1.5},
            {"activity": "Green Valley", "cost": 0, "hours": 1},
            {"activity": "Tara Devi Temple", "cost": 0, "hours": 2},
            {"activity": "Chadwick Falls", "cost": 0, "hours": 2},
            {"activity": "Annandale", "cost": 0, "hours": 1},
        ],
        "Leh": [
            {"activity": "Pangong Lake", "cost": 1000, "hours": 5},
            {"activity": "Shanti Stupa", "cost": 0, "hours": 1},
            {"activity": "Leh Palace", "cost": 200, "hours": 1},
            {"activity": "Magnetic Hill", "cost": 0, "hours": 1},
            {"activity": "Nubra Valley", "cost": 2000, "hours": 6},
            {"activity": "Thiksey Monastery", "cost": 50, "hours": 2},
            {"activity": "Hemis National Park", "cost": 100, "hours": 3},
            {"activity": "Hall of Fame", "cost": 50, "hours": 1.5},
            {"activity": "Spituk Gompa", "cost": 0, "hours": 1},
            {"activity": "Gurudwara Pathar Sahib", "cost": 0, "hours": 1},
        ],
        "Srinagar": [
            {"activity": "Dal Lake Shikara Ride", "cost": 600, "hours": 2},
            {"activity": "Mughal Gardens", "cost": 100, "hours": 2},
            {"activity": "Shankaracharya Temple", "cost": 0, "hours": 1.5},
            {"activity": "Local Market", "cost": 1000, "hours": 2},
            {"activity": "Hazratbal Shrine", "cost": 0, "hours": 1},
            {"activity": "Nigeen Lake", "cost": 0, "hours": 1.5},
            {"activity": "Pari Mahal", "cost": 50, "hours": 1},
            {"activity": "Indira Gandhi Memorial Tulip Garden", "cost": 60, "hours": 2},
            {"activity": "Chashme Shahi", "cost": 20, "hours": 1},
            {"activity": "Jamia Masjid", "cost": 0, "hours": 1},
        ],
        "Hyderabad": [
            {"activity": "Charminar", "cost": 200, "hours": 1},
            {"activity": "Golconda Fort", "cost": 500, "hours": 3},
            {"activity": "Ramoji Film City", "cost": 2000, "hours": 6},
            {"activity": "Hussain Sagar Lake", "cost": 0, "hours": 1},
            {"activity": "Biryani Food Walk", "cost": 800, "hours": 2},
            {"activity": "Salar Jung Museum", "cost": 50, "hours": 3},
            {"activity": "Chowmahalla Palace", "cost": 100, "hours": 2},
            {"activity": "Qutb Shahi Tombs", "cost": 20, "hours": 1.5},
            {"activity": "Birla Mandir", "cost": 0, "hours": 1},
            {"activity": "Nehru Zoological Park", "cost": 60, "hours": 3},
        ],
        "Kolkata": [
            {"activity": "Victoria Memorial", "cost": 500, "hours": 2},
            {"activity": "Howrah Bridge", "cost": 0, "hours": 0.5},
            {"activity": "Dakshineswar Kali Temple", "cost": 0, "hours": 2},
            {"activity": "Park Street Food", "cost": 1000, "hours": 2},
            {"activity": "Indian Museum", "cost": 200, "hours": 2},
            {"activity": "Science City", "cost": 60, "hours": 3},
            {"activity": "Belur Math", "cost": 0, "hours": 2},
            {"activity": "Marble Palace", "cost": 0, "hours": 1},
            {"activity": "Kalighat Kali Temple", "cost": 0, "hours": 1.5},
            {"activity": "Eco Park", "cost": 30, "hours": 2},
        ],
        "Amritsar": [
            {"activity": "Golden Temple", "cost": 0, "hours": 3},
            {"activity": "Jallianwala Bagh", "cost": 0, "hours": 1},
            {"activity": "Wagah Border Ceremony", "cost": 0, "hours": 4},
            {"activity": "Partition Museum", "cost": 200, "hours": 2},
            {"activity": "Kulcha Food Tour", "cost": 400, "hours": 1},
            {"activity": "Durgiana Temple", "cost": 0, "hours": 1},
            {"activity": "Gobindgarh Fort", "cost": 200, "hours": 2},
            {"activity": "Maharaja Ranjit Singh Museum", "cost": 40, "hours": 1.5},
            {"activity": "Ram Bagh Gardens", "cost": 0, "hours": 1},
            {"activity": "Hall Bazaar", "cost": 500, "hours": 2},
        ],
        "Mysore": [
            {"activity": "Mysore Palace", "cost": 200, "hours": 2},
            {"activity": "Chamundi Hill", "cost": 0, "hours": 2},
            {"activity": "Brindavan Gardens", "cost": 100, "hours": 2},
            {"activity": "Mysore Zoo", "cost": 150, "hours": 3},
            {"activity": "St. Philomena's Church", "cost": 0, "hours": 1},
            {"activity": "Jaganmohan Palace", "cost": 40, "hours": 1.5},
            {"activity": "Railway Museum", "cost": 50, "hours": 1},
            {"activity": "Karanji Lake", "cost": 50, "hours": 1.5},
            {"activity": "St. Philomena's Cathedral", "cost": 0, "hours": 1},
            {"activity": "Devaraja Market", "cost": 200, "hours": 1.5},
        ],
        "Rishikesh": [
            {"activity": "River Rafting", "cost": 1500, "hours": 3},
            {"activity": "Laxman Jhula", "cost": 0, "hours": 1},
            {"activity": "Ganga Aarti at Parmarth Niketan", "cost": 0, "hours": 2},
            {"activity": "Beatles Ashram", "cost": 600, "hours": 2},
            {"activity": "Neer Garh Waterfall", "cost": 100, "hours": 2},
            {"activity": "Triveni Ghat", "cost": 0, "hours": 1},
            {"activity": "Ram Jhula", "cost": 0, "hours": 1},
            {"activity": "Vashishta Gufa", "cost": 0, "hours": 1.5},
            {"activity": "Neelkanth Mahadev Temple", "cost": 0, "hours": 3},
            {"activity": "Jumpin Heights (Bungee)", "cost": 3500, "hours": 2},
            {"activity": "Paragliding", "cost": 4000, "hours": 2},
        ],
        "Pondicherry": [
            {"activity": "Promenade Beach", "cost": 0, "hours": 2},
            {"activity": "Auroville", "cost": 0, "hours": 3},
            {"activity": "Sri Aurobindo Ashram", "cost": 0, "hours": 1},
            {"activity": "French Colony Walk", "cost": 0, "hours": 2},
            {"activity": "Paradise Beach", "cost": 300, "hours": 3},
            {"activity": "Serenity Beach", "cost": 0, "hours": 2},
            {"activity": "Basilica of the Sacred Heart", "cost": 0, "hours": 1},
            {"activity": "Botanical Garden", "cost": 20, "hours": 1.5},
            {"activity": "Rock Beach", "cost": 0, "hours": 1},
            {"activity": "Ousteri Lake", "cost": 0, "hours": 2},
        ],
        "Uttarakhand": [
            {"activity": "Rishikesh River Rafting", "cost": 1500, "hours": 3},
            {"activity": "Nainital Lake Boating", "cost": 500, "hours": 2},
            {"activity": "Jim Corbett Jungle Safari", "cost": 4000, "hours": 4},
            {"activity": "Mussoorie Mall Road", "cost": 0, "hours": 2},
            {"activity": "Har Ki Pauri Aarti", "cost": 0, "hours": 1.5},
            {"activity": "Auli Ropeway", "cost": 1000, "hours": 2},
            {"activity": "Valley of Flowers Trek", "cost": 200, "hours": 6},
            {"activity": "Tehri Dam Water Sports", "cost": 1500, "hours": 3},
            {"activity": "Kempty Falls", "cost": 100, "hours": 2},
            {"activity": "Robber's Cave", "cost": 50, "hours": 2},
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

@app.post("/subscribe")
async def subscribe(subscriber: Subscriber):
    """
    Subscribes a user to the newsletter and sends a welcome email immediately.
    """
    try:
        # Validate email deliverability (checks if domain exists)
        validate_email(subscriber.email, check_deliverability=True)
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=f"Invalid email: {str(e)}")

    try:
        with sqlite3.connect("subscribers.db") as conn:
            conn.execute("INSERT INTO subscribers (email) VALUES (?)", (subscriber.email,))
            conn.commit()
    except sqlite3.IntegrityError:
        # If already subscribed, continue to send email (useful if previous attempt failed)
        pass
    
    try:
        send_welcome_email(subscriber.email)
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
    
    return {"message": "Subscription successful", "email": subscriber.email}

@app.get("/subscribers")
async def get_subscribers(password: str):
    if password != "admin123":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    with sqlite3.connect("subscribers.db") as conn:
        cursor = conn.execute("SELECT email, created_at FROM subscribers ORDER BY created_at DESC")
        subscribers = [{"email": row[0], "joined_at": row[1]} for row in cursor.fetchall()]
    
    return subscribers

@app.get("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe(email: str):
    return f"""
    <html>
        <head>
            <title>Unsubscribe Confirmation</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f3f4f6; color: #1f2937; }}
                .container {{ text-align: center; background: white; padding: 3rem; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); max-width: 400px; }}
                h1 {{ color: #4f46e5; margin-top: 0; }}
                p {{ color: #6b7280; margin-bottom: 1.5rem; }}
                .btn {{ background-color: #ef4444; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 0.5rem; font-size: 1rem; cursor: pointer; transition: background-color 0.2s; }}
                .btn:hover {{ background-color: #dc2626; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Unsubscribe?</h1>
                <p>Are you sure you want to remove <strong>{{email}}</strong> from our newsletter?</p>
                <button class="btn" onclick="confirmUnsubscribe()">Yes, Unsubscribe</button>
            </div>
            <script>
                async function confirmUnsubscribe() {{
                    const email = "{{email}}";
                    try {{
                        const response = await fetch('/unsubscribe/confirm', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ email: email }})
                        }});
                        const html = await response.text();
                        document.open();
                        document.write(html);
                        document.close();
                    }} catch (err) {{
                        alert('Error processing request');
                    }}
                }}
            </script>
        </body>
    </html>
    """

@app.post("/unsubscribe/confirm", response_class=HTMLResponse)
async def unsubscribe_confirm(subscriber: Subscriber):
    email = subscriber.email
    with sqlite3.connect("subscribers.db") as conn:
        conn.execute("DELETE FROM subscribers WHERE email = ?", (email,))
        conn.commit()
    
    return f"""
    <html>
        <head>
            <title>Unsubscribe Successful</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f3f4f6; color: #1f2937; }}
                .container {{ text-align: center; background: white; padding: 3rem; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); max-width: 400px; }}
                h1 {{ color: #4f46e5; margin-top: 0; }}
                p {{ color: #6b7280; margin-bottom: 1.5rem; }}
                .btn {{ background-color: #4f46e5; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 0.5rem; font-size: 1rem; cursor: pointer; transition: background-color 0.2s; }}
                .btn:hover {{ background-color: #4338ca; }}
                .btn:disabled {{ background-color: #9ca3af; cursor: not-allowed; }}
                #snackbar {{ visibility: hidden; min-width: 250px; margin-left: -125px; background-color: #333; color: #fff; text-align: center; border-radius: 4px; padding: 16px; position: fixed; z-index: 1; left: 50%; bottom: 30px; font-size: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                #snackbar.show {{ visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }}
                @keyframes fadein {{ from {{bottom: 0; opacity: 0;}} to {{bottom: 30px; opacity: 1;}} }}
                @keyframes fadeout {{ from {{bottom: 30px; opacity: 1;}} to {{bottom: 0; opacity: 0;}} }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Unsubscribed</h1>
                <p>You have been successfully removed from the TravelGenie newsletter.</p>
                <button class="btn" onclick="resubscribe()">Mistake? Resubscribe</button>
            </div>
            <div id="snackbar"></div>
            <script>
                async function resubscribe() {{
                    const email = "{{email}}";
                    const btn = document.querySelector('.btn');
                    
                    btn.disabled = true;
                    btn.textContent = 'Resubscribing...';
                    
                    try {{
                        const response = await fetch('/subscribe', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ email: email }})
                        }});
                        
                        if (response.ok) {{
                            showSnackbar('Successfully resubscribed! You can close this tab.', false);
                            btn.textContent = 'Resubscribed ✓';
                        }} else {{
                            const data = await response.json();
                            showSnackbar(data.detail || 'Failed to resubscribe.', true);
                            btn.disabled = false;
                            btn.textContent = 'Mistake? Resubscribe';
                        }}
                    }} catch (err) {{
                        showSnackbar('Network error.', true);
                        btn.disabled = false;
                        btn.textContent = 'Mistake? Resubscribe';
                    }}
                }}

                function showSnackbar(message, isError) {{
                    const x = document.getElementById("snackbar");
                    x.innerText = message;
                    x.style.backgroundColor = isError ? "#ef4444" : "#10b981";
                    x.className = "show";
                    setTimeout(function(){{ x.className = x.className.replace("show", ""); }}, 3000);
                }}
            </script>
        </body>
    </html>
    """

@app.post("/book-package")
async def book_package(request: BookingRequest):
    with sqlite3.connect("subscribers.db") as conn:
        conn.execute("INSERT INTO bookings (email, package_name) VALUES (?, ?)", (request.email, request.package_name))
        conn.commit()
    return {"message": "Booking request received!"}

@app.get("/tour-packages", response_class=HTMLResponse)
async def tour_packages():
    return """
    <html>
        <head>
            <title>Tour Packages</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                body { 
                    font-family: 'Poppins', sans-serif; 
                    margin: 0; 
                    background-color: #f8fafc; 
                    color: #1e293b; 
                    padding: 60px 20px; 
                }
                .header { 
                    text-align: center; 
                    margin-bottom: 60px; 
                }
                h1 { 
                    color: #0f172a; 
                    margin: 0 0 16px 0; 
                    font-size: 3rem; 
                    font-weight: 800;
                    letter-spacing: -0.025em;
                }
                p { 
                    color: #64748b; 
                    font-size: 1.25rem; 
                    max-width: 600px;
                    margin: 0 auto;
                    line-height: 1.6;
                }
                .container { 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); 
                    gap: 40px; 
                }
                .card { 
                    background: white; 
                    border-radius: 24px; 
                    overflow: hidden; 
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); 
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); 
                    display: flex; 
                    flex-direction: column; 
                    border: 1px solid #f1f5f9;
                }
                .card:hover { 
                    transform: translateY(-12px); 
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04); 
                }
                .card-header { 
                    height: 240px; 
                    position: relative;
                    overflow: hidden;
                }
                .card-header img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    transition: transform 0.6s ease;
                }
                .card:hover .card-header img {
                    transform: scale(1.1);
                }
                .card-body { 
                    padding: 32px; 
                    flex-grow: 1; 
                    display: flex; 
                    flex-direction: column; 
                }
                .card-title { 
                    font-size: 1.5rem; 
                    font-weight: 700; 
                    color: #0f172a; 
                    margin-bottom: 12px; 
                }
                .card-text { 
                    color: #64748b; 
                    line-height: 1.6; 
                    margin-bottom: 24px; 
                    flex-grow: 1; 
                    font-size: 1rem;
                }
                .price-tag { 
                    font-size: 1.75rem; 
                    font-weight: 800; 
                    color: #4f46e5; 
                    margin-bottom: 24px; 
                }
                .btn { 
                    background: linear-gradient(to right, #4f46e5, #4338ca); 
                    color: white; 
                    border: none; 
                    padding: 16px; 
                    border-radius: 12px; 
                    font-size: 1.1rem; 
                    font-weight: 600; 
                    cursor: pointer; 
                    width: 100%; 
                    transition: all 0.2s; 
                    box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
                }
                .btn:hover { 
                    background: linear-gradient(to right, #4338ca, #3730a3); 
                    transform: translateY(-2px);
                    box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
                }
                .btn:active {
                    transform: translateY(0);
                }
                .search-container {
                    max-width: 500px;
                    margin: 40px auto 0;
                }
                .search-input {
                    width: 100%;
                    padding: 16px 24px;
                    font-size: 1rem;
                    border: 2px solid #e2e8f0;
                    border-radius: 50px;
                    outline: none;
                    transition: all 0.3s ease;
                    font-family: 'Poppins', sans-serif;
                    box-sizing: border-box;
                }
                .search-input:focus {
                    border-color: #4f46e5;
                    box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Discover Your Next Adventure</h1>
                <p>Curated itineraries for unforgettable memories. Choose your destination and let the journey begin.</p>
                <div class="search-container">
                    <input type="text" id="searchInput" class="search-input" placeholder="Search destinations (e.g., Kerala, Rajasthan)...">
                </div>
            </div>
            <div class="container">
                <div class="card">
                    <div class="card-header">
                        <img src="https://images.unsplash.com/photo-1477587458883-47145ed94245?w=500&q=80" alt="Rajasthan">
                    </div>
                    <div class="card-body">
                        <div class="card-title">Royal Rajasthan</div>
                        <div class="card-text">Experience the grandeur of Jaipur, Udaipur, and Jaisalmer. Includes fort tours, desert safaris, and cultural nights.</div>
                        <div class="price-tag">₹24,999</div>
                        <button class="btn">Book Now</button>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <img src="https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=500&q=80" alt="Kerala">
                    </div>
                    <div class="card-body">
                        <div class="card-title">Kerala Backwaters</div>
                        <div class="card-text">Relax on a houseboat in Alleppey, visit Munnar tea gardens, and enjoy authentic Ayurvedic spa treatments.</div>
                        <div class="price-tag">₹19,500</div>
                        <button class="btn">Book Now</button>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <img src="https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=500&q=80" alt="Himalayas">
                    </div>
                    <div class="card-body">
                        <div class="card-title">Himalayan Adventure</div>
                        <div class="card-text">Thrilling trek in Manali, paragliding in Solang Valley, and a peaceful stay in Kasol near the Parvati river.</div>
                        <div class="price-tag">₹15,000</div>
                        <button class="btn">Book Now</button>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <img src="https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=500&q=80" alt="Uttarakhand">
                    </div>
                    <div class="card-body">
                        <div class="card-title">Divine Uttarakhand</div>
                        <div class="card-text">Experience the spiritual bliss of Rishikesh, the lakes of Nainital, and the majestic peaks of Auli.</div>
                        <div class="price-tag">₹18,500</div>
                        <button class="btn">Book Now</button>
                    </div>
                </div>
            </div>
            <script>
                document.getElementById('searchInput').addEventListener('keyup', function() {
                    const searchQuery = this.value.toLowerCase();
                    const cards = document.querySelectorAll('.card');
                    
                    cards.forEach(card => {
                        const title = card.querySelector('.card-title').innerText.toLowerCase();
                        card.style.display = title.includes(searchQuery) ? 'flex' : 'none';
                    });
                });

                async function bookPackage(packageName) {
                    const email = prompt("Please enter your email address to book " + packageName + ":");
                    if (email) {
                        try {
                            const response = await fetch("/book-package", {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json",
                                },
                                body: JSON.stringify({ email: email, package_name: packageName }),
                            });
                            if (response.ok) {
                                alert("Thanks! We have received your booking request for " + packageName + ". We will contact you at " + email + " shortly.");
                            } else {
                                alert("Failed to submit booking. Please check your email and try again.");
                            }
                        } catch (error) {
                            console.error("Error:", error);
                            alert("An error occurred. Please try again later.");
                        }
                    }
                }

                document.querySelectorAll('.btn').forEach(button => {
                    button.addEventListener('click', function() {
                        const card = this.closest('.card');
                        const title = card.querySelector('.card-title').innerText;
                        bookPackage(title);
                    });
                });
            </script>
        </body>
    </html>
    """