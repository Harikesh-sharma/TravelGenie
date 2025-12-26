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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    with sqlite3.connect("subscribers.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS subscribers (email TEXT PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

@app.on_event("startup")
async def startup_event():
    init_db()

class Subscriber(BaseModel):
    email: EmailStr

class PlanRequest(BaseModel):
    budget: int
    days: int
    city: str
    preferences: List[str]

def send_welcome_email(email_to: str):
    # Configuration - In production, use Environment Variables!
    smtp_server = "smtp.gmail.com" # Example for Gmail
    smtp_port = 587
    
    # Try to get credentials from environment variables, fallback to placeholders
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
        return {"message": "You are already subscribed!", "email": subscriber.email}

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
                <p>Are you sure you want to remove <strong>{email}</strong> from our newsletter?</p>
                <button class="btn" onclick="confirmUnsubscribe()">Yes, Unsubscribe</button>
            </div>
            <script>
                async function confirmUnsubscribe() {{
                    const email = "{email}";
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
                .message {{ margin-top: 1rem; font-size: 0.9rem; min-height: 1.5em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Unsubscribed</h1>
                <p>You have been successfully removed from the TravelGenie newsletter.</p>
                <button class="btn" onclick="resubscribe()">Mistake? Resubscribe</button>
                <div id="msg" class="message"></div>
            </div>
            <script>
                async function resubscribe() {{
                    const email = "{email}";
                    const btn = document.querySelector('.btn');
                    const msg = document.getElementById('msg');
                    
                    btn.disabled = true;
                    btn.textContent = 'Resubscribing...';
                    
                    try {{
                        const response = await fetch('/subscribe', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ email: email }})
                        }});
                        
                        if (response.ok) {{
                            msg.style.color = '#10b981';
                            msg.textContent = 'Successfully resubscribed! You can close this tab.';
                            btn.textContent = 'Resubscribed ✓';
                        }} else {{
                            const data = await response.json();
                            msg.style.color = '#ef4444';
                            msg.textContent = data.detail || 'Failed to resubscribe.';
                            btn.disabled = false;
                            btn.textContent = 'Mistake? Resubscribe';
                        }}
                    }} catch (err) {{
                        msg.style.color = '#ef4444';
                        msg.textContent = 'Network error.';
                        btn.disabled = false;
                        btn.textContent = 'Mistake? Resubscribe';
                    }}
                }}
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
