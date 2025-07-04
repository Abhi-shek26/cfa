from fastapi import FastAPI
from app.routers import stocks
from app.db import database, models

# This line creates the database tables if they don't exist.
models.Base.metadata.create_all(bind=database.engine)

# Initialize the FastAPI application
app = FastAPI(
    title="Stock Technical Analysis API",
    description="An API for calculating stock technical indicators with a tiered subscription model.",
    version="1.0.0"
)

# Include the stocks router for handling stock-related endpoints
app.include_router(stocks.router)

# Root endpoint for the API
@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Technical Analysis API"}

