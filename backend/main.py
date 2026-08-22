import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from pathlib import Path

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
API_KEY = os.getenv("GROQ_API_KEY", "PENDING VERIFICATION")
class AnalysisRequest(BaseModel):
    target: str
    transit_depth_pct: float = 1.2
    equilibrium_temp_k: float = 1200.0
    user_prompt: str

    
import math

def calculate_planetary_physics(transit_depth_pct: float, equilibrium_temp_k: float, star_radius_solar: float = 1.0):
    """
    Translates raw observational metrics into physical planetary parameters.
    """
    # 1. Calculate Planet Size (R_earth = R_star * sqrt(Depth_fraction) * 109.2)
    depth_fraction = transit_depth_pct / 100.0
    r_planet_earth = star_radius_solar * math.sqrt(depth_fraction) * 109.2
    
    # 2. Estimate Physical Mass & Volume Classifications
    if r_planet_earth < 1.25:
        planet_type = "Rocky Earth-sized World"
    elif r_planet_earth < 2.0:
        planet_type = "Super-Earth"
    elif r_planet_earth < 6.0:
        planet_type = "Sub-Neptune Gas Dwarf"
    else:
        planet_type = "Massive Gas Giant"

    # 3. Thermal Classification based on Kelvin
    if equilibrium_temp_k > 1000:
        climate = "Scorching Lava Ball"
    elif equilibrium_temp_k > 373:
        climate = "Boiling Super-Heated Desert"
    elif equilibrium_temp_k > 200:
        climate = "Temperate / Goldilocks Zone Candidate"
    else:
        climate = "Deep-Freeze Ice World"

    return {
        "calculated_radius_earth": round(r_planet_earth, 2),
        "planet_type": planet_type,
        "climate_zone": climate
    }

@app.get("/") 
async def read_index():
    index_path = Path(__file__).parent / "index.html"
    return FileResponse(str(index_path))

def read_root():
    return {"status": "online", "message": "JWST Exoplanet Backend is running smoothly!"}

@app.get("/api/lightcurve/{target_id}")
async def get_lightcurve(target_id: str):
    import lightkurve as lk
    try:
        if fetch_exoplanet_lightcurve:
            data = fetch_exoplanet_lightcurve(target_name=target_id)
            return data
            
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
    # Check API key
    if API_KEY == "PENDING VERIFICATION":
        return {
            "ai_response": "[MOCK AI COPILOT MODE] Target {payload.target} analyzed: Transit depth at {payload.transit_depth_pct}% and {payload.equilibrium_temp_k}K. Once your key is wired in, this switches straight to live AI!"
        }
    
    try:
        
        client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.groq.com/openai/v1"
)
        # Input validation
        if not payload or not payload.target:
            raise ValueError("Missing required field: target")
        
        if payload.transit_depth_pct is None or payload.equilibrium_temp_k is None:
            raise ValueError("Missing required fields: transit_depth_pct or equilibrium_temp_k")
        
        # Validate numeric ranges
        if not (0 <= payload.transit_depth_pct <= 100):
            raise ValueError("transit_depth_pct must be between 0 and 100")
        
        if payload.equilibrium_temp_k < 0:
            raise ValueError("equilibrium_temp_k cannot be negative")
        
        # Run the math engine using parameters sent from your dashboard
        physics = calculate_planetary_physics(
            payload.transit_depth_pct, 
            payload.equilibrium_temp_k
        )
        
        size_description = f"{physics['planet_type']} ({physics['calculated_radius_earth']} times the size of Earth)"
        climate_description = f"{physics['climate_zone']}"
        
        system_prompt = f"""You are a world-class, super-enthusiastic astronomer talking to a literal 10-year-old kid who just clicked on an alien planet ({payload.target}) in their space dashboard.

YOUR CURRENT SENSOR READINGS FOR THIS HUNTED PLANET:
- Planet Size Profile: {size_description}
- Climate Profile: {climate_description} (Temperature: {payload.equilibrium_temp_k}K)

YOUR RESPONSE FORMAT RULES (MANDATORY):
1. You MUST use bullet points for every single point. Do NOT write long paragraphs.
2. Keep each bullet point to 1-2 short sentences max.
3. Use the fun physics data above to explain the numbers like a storytelling cosmic tracker. Explain that the transit depth ({payload.transit_depth_pct}%) is how much light the planet blocks as it passes in front of its star, like a tiny fly floating in front of a giant flashlight.
4. Make the kid feel like an incredible explorer for hunting and tracking down this specific candidate.
5. ZERO math formulas, ZERO academic jargon, and ZERO markdown tables."""
        
        response = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": payload.user_prompt}
            ]
        )
        
        return {"ai_response": response.choices[0].message.content}
    
    except ValueError as ve:
        print(f"VALIDATION ERROR: {ve}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    
    except Exception as e:
        print(f"ACTUAL ERROR: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"AI Proxy Error: {str(e)}"
        )
