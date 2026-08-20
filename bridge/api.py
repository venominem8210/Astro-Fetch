import sys
from pathlib import Path

# Add the backend directory to Python's path
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.append(str(backend_path))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import BLS function from algorithms file
from astro.algorithms import box_least_squares_search

app = FastAPI(title="Astro-Pipeline Bridge")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "Astro-Pipeline Bridge is up and running!"}

@app.get("/api/analyze/{target_name}")
def analyze_target(target_name: str):
    try:
        result = box_least_squares_search(target_name)

        return {
            "status": "success",
            "target": target_name,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))