import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# Enable CORS security clearances
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup directories for UI components
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize client wrapper targeting the Groq API Cloud Engine
# Make sure your GROQ_API_KEY environment variable is set in your system
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class TravelRequest(BaseModel):
    destination: str
    days: int
    budget: str
    travelers: int
    travel_type: str
    interests: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        name="index.html",
        context={"request": request}
    )

@app.post("/generate")
async def generate_plan(data: TravelRequest):
    try:
        print(data)  # Server debug log

        # Engineered System Prompt forcing structural JSON mode with inner budget estimation
        prompt = f"""
        You are an expert travel planner. Generate a detailed, highly realistic travel itinerary based on these parameters:
        Destination: {data.destination}
        Days: {data.days}
        Budget Constraint: {data.budget}
        Total Travelers: {data.travelers}
        Trip Profile: {data.travel_type}
        Core Interests: {data.interests}

        You MUST respond ONLY with a raw JSON object matching this exact schema layout. 
        Ensure you budget smart allocations across the days. Every activity string MUST include an estimated cost element appended:
        {{
            "destination": "{data.destination}",
            "total_estimated_cost": "string (e.g., Rs. 35,000 total)",
            "itinerary": [
                {{
                    "day": 1,
                    "theme": "string description",
                    "activities": [
                        "Activity detail string (Estimated Cost: Rs. XXX)",
                        "Activity detail string (Estimated Cost: Rs. XXX)",
                        "Dining/Food detail string (Estimated Cost: Rs. XXX)"
                    ]
                }}
            ]
        }}
        Do not include any chat introductions, pleasantries, markdown blocks, or text outside the raw JSON payload.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        # Parse string output block safely back to dictionary object parameters
        json_content = json.loads(response.choices[0].message.content)
        return {"plan": json_content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))