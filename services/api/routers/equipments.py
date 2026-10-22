# services/api/routers/equipments.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(
    prefix="/equipments",
    tags=["Equipments"]
)

class EquipmentSchema(BaseModel):
    id: str
    name: str
    type: str  # ex: "Chambre Froide Positive", "Groupe Frigorifique CO2"
    refrigerant: str  # ex: "R134a", "R404A", "R744"
    nominal_power_kw: float
    location: str

# Données de démonstration en mémoire
EQUIPMENTS_DB = [
    {
        "id": "eq_chambre_01",
        "name": "Chambre Froide Légumes",
        "type": "Chambre Froide Positive",
        "refrigerant": "R134a",
        "nominal_power_kw": 3.5,
        "location": "Entrepôt Pointe-Noire - Zone A"
    }
]

@router.get("/", response_model=List[EquipmentSchema])
def list_equipments():
    """Liste tous les équipements HVACR enregistrés."""
    return EQUIPMENTS_DB

@router.get("/{equipment_id}", response_model=EquipmentSchema)
def get_equipment(equipment_id: str):
    """Récupère les détails d'un équipement spécifique."""
    equipment = next((e for e in EQUIPMENTS_DB if e["id"] == equipment_id), None)
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Équipement '{equipment_id}' non trouvé."
        )
    return equipment