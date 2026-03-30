from pydantic import BaseModel
from typing import List, Optional

class Observation(BaseModel):
    email_text: str
    sender: str
    gravity: float  # Urgency score (0.0 - 1.0)
    email_id: Optional[int] = None
    history: List[str] = []

class Action(BaseModel):
    category: str  # spam, urgent, normal
    priority: str  # low, medium, high
    response: str
    antigravity: float = 0.5  # Strategic delay/override (0.0 - 1.0)

class Reward(BaseModel):
    score: float
    contribution: str
