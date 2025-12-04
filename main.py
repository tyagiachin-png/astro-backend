from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 👇👇 यहां अपना frontend URL डालो
origins = [
    "https://astro-frontend.vercel.app",
    "https://*.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # <-- OPTIONS, GET, POST सब allow
    allow_headers=["*"],
)

class BirthData(BaseModel):
    name: str
    dob: str
    tob: str
    place: str

@app.get("/")
def home():
    return {"message": "Backend live hai!"}

@app.post("/analyze")
def analyze(data: BirthData):
    return {
        "name": data.name,
        "nakshatra": "Mrigashira 4 (sample)",
        "prediction": "Aapka buddhi bal strong hai."
    }


