"""
Routes de Prédictions Bayésiennes
"""

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select, create_engine
import os

from .models import Event
from .bayesian_model import BayesianFootballModel

router = APIRouter(prefix="/api", tags=["predictions"])

# Global state
bayesian_model = BayesianFootballModel()
model_fitted = False

# Engine
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/sports")
engine = create_engine(DATABASE_URL)


def ensure_model_fitted():
    """Entraîner le modèle si pas déjà fait"""
    global model_fitted
    
    if model_fitted:
        return
    
    # Charger les matchs depuis la DB
    with Session(engine) as session:
        events = session.exec(select(Event)).all()
        
        if len(events) < 2:
            # Pas assez de données, initialiser le modèle vide
            bayesian_model.fit([])
            model_fitted = True
            return
        
        # Convertir en format attendu
        matches = []
        for event in events:
            matches.append({
                'team1': event.team1,
                'team2': event.team2,
                'home_score': 0,
                'away_score': 0,
            })
        
        try:
            bayesian_model.fit(matches, draws=500, tune=500)
            model_fitted = True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")


@router.post("/predict-match")
async def predict_match(team1: str, team2: str):
    """Prédire le résultat d'un match"""
    try:
        ensure_model_fitted()
        result = bayesian_model.predict_match(team1, team2)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team-stats")
async def get_team_stats():
    """Obtenir les stats d'attaque/défense des équipes"""
    try:
        ensure_model_fitted()
        return bayesian_model.get_team_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train-model")
async def train_model():
    """Réentraîner le modèle"""
    global model_fitted
    
    try:
        model_fitted = False
        ensure_model_fitted()
        return {"status": "Model retrained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
