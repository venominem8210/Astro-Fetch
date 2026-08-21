import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import lightkurve as lk

# If you were using a custom fetcher module, keep it imported here, 
# or use the direct lightkurve fallback shown below.
try:
    from aperture_jwst.fetcher import fetch_exoplanet_lightcurve
except ImportError:
    fetch_exoplanet_lightcurve = None

app = FastAPI(title="JWST Exoplanet Dashboard API", version="1.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq AI Proxy setup using OpenAI SDK client
API_KEY = os.getenv("GROQ_API_KEY", "PENDING VERIFICATION")
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

class AnalysisRequest(BaseModel):
    target: str
    transit_depth_pct: float = 1.2
    equilibrium_temp_k: float = 1200.0
    user_prompt: str

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(os.path.dirname(__file__),"index_html"))
def read_root():
    return {"status": "online", "message": "JWST Exoplanet Backend is running smoothly!"}

@app.get("/api/lightcurve/{target_id}")
async def get_lightcurve(target_id: str):
    try:
        if fetch_exoplanet_lightcurve:
            data = fetch_exoplanet_lightcurve(target_name=target_id)
            return data
            
        # Direct fallback search if module isn't present
        search_result = lk.search_lightcurve(target_id, mission="TESS")
        if len(search_result) == 0:
            search_result = lk.search_lightcurve(f"TIC {target_id}", mission="TESS")
            
        if len(search_result) == 0:
            raise HTTPException(status_code=404, detail=f"No TESS light curve found for target: {target_id}")
            
        lc = search_result[0].download().remove_nans().flatten()
        
        time_vals = lc.time.value.tolist()
        flux_vals = lc.flux.value.tolist()
        
        if len(time_vals) > 600:
            time_vals = time_vals[-600:]
            flux_vals = flux_vals[-600:]

        return {
            "target": target_id,
            "sector": getattr(search_result[0], 'sector', 'N/A'),
            "total_observations": len(lc.time),
            "time": time_vals,
            "flux": flux_vals,
            "equilibrium_temp_k": 950.0,
            "star_radius_solar": 1.0,
            "planet_radius_earth": 1.4
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze_planet(payload: AnalysisRequest):
    if API_KEY == "PENDING VERIFICATION":
        return {
            "ai_response": (
                f"[MOCK AI COPILOT MODE] Target {payload.target} analyzed: "
                f"Transit depth at {payload.transit_depth_pct}% and {payload.equilibrium_temp_k}K. "
                f"Once your key is wired in, this switches straight to live AI!"
            )
        }
    try:
        system_prompt = (
            f"""You are a world-class, super-enthusiastic astronomer talking to a literal 10-year-old kid who just clicked on an alien planet ({payload.target}) in their space dashboard.

            YOUR RESPONSE FORMAT RULES (MANDATORY):
            1. You MUST use bullet points for every single point. Do NOT write long paragraphs.
            2. Keep each bullet point to 1-2 short sentences max.
            3. Explain the numbers like a fun story (e.g., transit depth means blocking light like a tiny fruit fly).
            4. Describe what it feels like there (e.g., temperature {payload.equilibrium_temp_k}K means a blazing lava ball).
            5. ZERO math formulas, ZERO academic jargon, and ZERO markdown tables."""
        )
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # or your preferred Groq model like llama-3.3-70b-versatile
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": payload.user_prompt}
            ]
        )
        return {"ai_response": response.choices[0].message.content}
    except Exception as e:
        print(f"ACTUAL ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"AI Proxy Error: {str(e)}")