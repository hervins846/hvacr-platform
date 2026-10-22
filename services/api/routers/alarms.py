# services/api/routers/alarms.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/alarms",
    tags=["Alarms"]
)

class AlarmSchema(BaseModel):
    alarm_id: str
    equipment_id: str
    severity: str  # "CRITICAL", "WARNING", "INFO"
    message: str
    created_at: str
    acknowledged: bool

# Exemples d'alarmes récentes
ALARMS_DB = [
    {
        "alarm_id": "alm_101",
        "equipment_id": "eq_chambre_01",
        "severity": "CRITICAL",
        "message": "Pression de refoulement > 18.0 bar (Haute Pression)",
        "created_at": datetime.utcnow().isoformat(),
        "acknowledged": False
    }
]

@router.get("/", response_model=List[AlarmSchema])
def list_active_alarms(equipment_id: str = None):
    """Récupère les alarmes actives."""
    if equipment_id:
        return [a for a in ALARMS_DB if a["equipment_id"] == equipment_id]
    return ALARMS_DB