from fastapi import FastAPI
from routes.applications import router as applications_router

app = FastAPI()

app.include_router(applications_router)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Job Tracker FastAPI is running"
    }