"""
Routes API - Simplifiées
"""
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select, create_engine
import os

from . import models

router = APIRouter(prefix="/api", tags=["betting"])

# DB Engine
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/sports")
engine = create_engine(DATABASE_URL)


@router.get("/events")
def get_events():
    """Récupère tous les événements de football"""
    with Session(engine) as session:
        events = session.exec(select(models.Event)).all()
        return {"events": [{"id": e.id, "team1": e.team1, "team2": e.team2} for e in events]}


@router.post("/bets")
def place_bet(event_id: int, bet_type: str, amount: float, odds: float, user_id: int = 1):
    """Place un pari"""
    return {"status": "ok"}


@router.get("/my-bets")
def get_my_bets(user_id: int = 1):
    """Get user bets"""
    return {"bets": []}


@router.post("/seed-data")
def seed_data():
    """Create test data"""
    from datetime import datetime, timedelta
    
    with Session(engine) as session:
        existing = session.exec(select(models.Event)).first()
        if existing:
            return {"message": "Data already exists"}
        
        events = [
            models.Event(team1="PSG", team2="Lyon", date=datetime.utcnow() + timedelta(days=1), status="active"),
            models.Event(team1="Man Utd", team2="Liverpool", date=datetime.utcnow() + timedelta(days=2), status="active"),
            models.Event(team1="Real Madrid", team2="Barcelona", date=datetime.utcnow() + timedelta(days=3), status="active"),
        ]
        
        for event in events:
            session.add(event)
        session.commit()
        
        return {"message": "Data seeded successfully"}
