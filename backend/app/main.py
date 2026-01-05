import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlmodel import Session

# Import routes
from .betting_routes import router as betting_router
from .prediction_routes import router as prediction_router

# FastAPI app
app = FastAPI(title="Football Betting Platform - Backend")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/betting_db")
engine = create_engine(DATABASE_URL, echo=False)

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Include routers
app.include_router(betting_router)
app.include_router(prediction_router)
