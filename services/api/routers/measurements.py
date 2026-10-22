# services/api/routers/measurements.py

from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/measurements",
    tags=["Measurements"]
)

class MeasurementInput(BaseModel):
    equipment_id: str
    timestamp: Optional[str] = None
    room_temp: float
    suction_pressure_bar: float
    discharge_pressure_bar: float
    compressor_status: bool
    electrical_power_kw: Optional[float] = 1.2

@router.post("/", status_code=status.HTTP_201_CREATED)
def record_measurement(data: MeasurementInput):
    """Enregistre une nouvelle mesure en provenance des capteurs ou du simulateur."""
    timestamp = data.timestamp or datetime.utcnow().isoformat()
    
    # Ici, intégration future vers TimescaleDB / Postgres
    return {
        "status": "recorded",
        "equipment_id": data.equipment_id,
        "timestamp": timestamp
    }