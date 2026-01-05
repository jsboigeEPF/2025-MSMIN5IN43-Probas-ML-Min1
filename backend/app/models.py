from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Match(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: Optional[str] = None
    team1: Optional[str] = None
    team2: Optional[str] = None
    score1: Optional[int] = None
    score2: Optional[int] = None
    source: Optional[str] = None

class Event(SQLModel, table=True):
    """Événement de football avec cotes de paris"""
    id: Optional[int] = Field(default=None, primary_key=True)
    team1: str
    team2: str
    date: datetime
    status: str = "active"  # active, finished, cancelled
    odds_team1: float = 1.5
    odds_draw: float = 3.0
    odds_team2: float = 2.5
    result: Optional[str] = None  # team1, draw, team2

class Player(SQLModel, table=True):
    """Joueur avec critères de jeu style FIFA"""
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    team: str
    name: str
    number: int
    position: str  # GK, DF, MF, FW
    photo_url: Optional[str] = None
    
    # Critères de jeu (0-100)
    attack: int = 75
    defense: int = 75
    speed: int = 75
    strength: int = 75
    dexterity: int = 75
    stamina: int = 75

class Bet(SQLModel, table=True):
    """Pari placé par un utilisateur"""
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    user_id: Optional[int] = None
    bet_type: str  # team1, draw, team2, player_goal, player_assist, etc.
    amount: float
    odds: float
    status: str = "pending"  # pending, won, lost, cancelled
    created_at: datetime = Field(default_factory=datetime.utcnow)
    result_at: Optional[datetime] = None
