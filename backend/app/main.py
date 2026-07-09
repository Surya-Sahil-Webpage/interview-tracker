from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app import models
from app.api import companies, rounds

app = FastAPI(title="Interview Tracker API")
app.include_router(companies.router)
app.include_router(rounds.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}