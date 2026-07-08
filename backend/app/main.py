from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app import models 
from app.api import companies

app = FastAPI(title="Interview Tracker API")
app.include_router(companies.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}