from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import lightkurve as lk

app = FastAPI(title="VOYAGER-X Backend", version="1.0")

# Enable CORS so your frontend HTML can communicate with this FastAPI server smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for hackathon testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    target: str
    transit_depth_pct: float = 1.2
    equilibrium_temp_k: float = 1200.0
    user_prompt: str

@app.get("/")
def read_root():
    return {"status": "VOYAGER-X Telemetry Bridge Online"}

@app.get("/api/lightcurve/{target_id}")
async def get_lightcurve(target_id: str):
    try:
        # Search for TESS light curve data in the MAST archive
        search_result = lk.search_lightcurve(target_id, mission="TESS")
        
        if len(search_result) == 0:
            raise HTTPException(status_code=404, detail=f"No TESS light curve found for target: {target_id}")
        
        # Download the first available matching dataset
        lc = search_result[0].download()
        
        # Clean data (remove NaN values and flatten/normalize)
        lc = lc.remove_nans().flatten()
        
        # Limit data points returned to ensure smooth browser rendering (e.g., last 600 points)
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
            "equilibrium_temp_k": 950.0, # Placeholder or extracted metadata if available
            "star_radius_solar": 1.0,
            "planet_radius_earth": 1.4
        }
        
    except Exception as e:
        # Fallback response or error indicator if MAST query fails for a weird ID
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze_target(payload: AnalyzeRequest):
    # Basic AI Copilot response stub tailored to the request
    prompt_lower = payload.user_prompt.lower()
    
    response_text = f"Analyzing target TIC {payload.target}. Based on the photometric flux variations, the light curve exhibits distinct periodic transit characteristics. The estimated equilibrium temperature of ~{payload.equilibrium_temp_k}K suggests a hot-zone candidate requiring radial velocity follow-up."
    
    if "habitable" in prompt_lower:
        response_text = f"For TIC {payload.target}, the orbital semi-major axis and stellar flux place it relative to the inner/outer bounds of the circumstellar habitable zone. Atmospheric spectroscopy via JWST would be required to confirm volatile presence."

    return {
        "target": payload.target,
        "ai_response": response_text
    }