from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Input structure
class BirthData(BaseModel):
    name: str
    dob: str
    tob: str
    place: str

@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.post("/analyze")
def analyze(data: BirthData):
    # फिलहाल simple response
    return {
        "name": data.name,
        "nakshatra": "Mrigashira 4",
        "prediction": "You have high intuition and deep thinking ability."
    }
