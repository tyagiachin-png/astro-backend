# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from utils.astro import simple_chart_report

app = FastAPI(title="Astro Backend (FastAPI)")

# --- CORS: development friendly (change '*' to your Vercel URL in production) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # dev में * रखो; बाद में "https://your-frontend.vercel.app"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class BirthData(BaseModel):
    name: str
    dob: str        # expected "YYYY-MM-DD"
    tob: str        # expected "HH:MM"
    place: Optional[str] = None   # optional for future geocoding

# --- Health ---
@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend live hai!"}

# --- Analyze route ---
@app.post("/analyze")
def analyze(data: BirthData):
    """
    Accepts JSON:
    {
      "name": "Ram",
      "dob": "1988-11-25",
      "tob": "17:45",
      "place": "Saharanpur"
    }
    Returns: nakshatra, ascendant, planets etc.
    """
    # 1) Validate & build datetime string
    try:
        # combine date + time to ISO-like string
        iso_string = f"{data.dob} {data.tob}"
        # parse to check validity
        dt = datetime.fromisoformat(iso_string)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid dob/tob format. Use YYYY-MM-DD and HH:MM. Error: {e}")

    # 2) Call astro engine (defaults to Asia/Kolkata; lat/lon default used)
    try:
        report = simple_chart_report(dt, tz_name='Asia/Kolkata')
    except Exception as e:
        # defensive: return readable error for debugging
        raise HTTPException(status_code=500, detail=f"Astro calculation failed: {e}")

    # 3) Build friendly output
    out = {
        "name": data.name,
        "dob": data.dob,
        "tob": data.tob,
        "place": data.place,
        "nakshatra": {
            "number": report.get("nakshatra"),
            "pada": report.get("pada"),
            "moon_longitude": report.get("moon_long")
        },
        "ascendant": report.get("ascendant"),
        "planets": report.get("planets")
    }

    return out
