import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

from aperture_jwst.fetcher import fetch_exoplanet_lightcurve

app = FastAPI(title="JWST Exoplanet Dashbord API", version="1.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hack Club AI Proxy setup
API_KEY = os.getenv("HACK_CLUB_API_KEY", "PENDING_VERIFICATION")
client = OpenAI(
    api_key=API_KEY,
    base_url="https://ai.hackclub.com/proxy/v1"
)

class AnalysisRequest(BaseModel):
    target: str
    transit_depth_pct: float
    equilibrium_temp_k: float
    user_prompt: str

@app.get("/")
def read_root():
    return{"status": "online", "message": "JWST Exoplanet Backend is running smoothly!"}

@app.get("/api/lightcurve/{target}")
def get_lightcurve(target: str):
    try:
        data = fetch_exoplanet_lightcurve(target_name=target)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/analyze")
def analyze_planet(payload: AnalysisRequest):
    if API_KEY == "PENDING VERIFICATION":
        return {
            "ai_response": ( 
                f"[MOCK AI COPILOT MODE] Target {payload.target} analyzed: "
                f"Transit depth at {payload.transit_depth_pct}% and {payload.equilibrium_temp_k}K."
                f"Once your key is wired in, this switched straight to live AI!"
            )
        }
    try:
        system_prompt = (
            f"You are an expert astronomer A! compilot in a JWST exoplanet dashboard. "
            f"Target: {payload.target}. Transit Depth: {payload.transit_depth_pct}%, Temp: {payload.equilibrium_temp_k}K."
        )
        response = client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": payload.user_prompt}
            ]
        )
        return {"ai_response": response.choices[0].message.content}
    except Exception as e:
        print(f"ACTUAL ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"AI Proxy Error: {str(e)}")
    