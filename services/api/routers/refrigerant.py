# services/api/routers/refrigerant.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(
    prefix="/refrigerant",
    tags=["Refrigerant Tracking & Thermodynamics (F-Gas & COP)"]
)

class RefrigerantConfig(BaseModel):
    equipment_id: str
    refrigerant_type: str  # ex: "R134a", "R404A", "R744", etc.
    initial_charge_kg: float
    recharge_history_kg: List[float] = []
    leak_test_passed: bool = True

# Base de données enrichie avec la liste complète des fluides et paramètres thermodynamiques de pointe
REFRIGERANT_DB = {
    "eq_chambre_01": {
        "equipment_id": "eq_chambre_01",
        "refrigerant_type": "R134a",
        "initial_charge_kg": 15.0,
        "recharge_history_kg": [1.2, 0.8],
        "leak_test_passed": True,
        "suction_pressure_bar": 2.0,
        "discharge_pressure_bar": 16.0,
        "superheat_k": 8.0,
        "subcooling_k": 5.0,
        "cop": 4.8,
        "cooling_capacity_kw": 35.2,
        "mass_flow_kg_s": 0.19
    }
}

SUPPORTED_REFRIGERANTS = [
    "R134a", "R404A", "R744 (CO2)", "R22 (Ancien)", "R290 (Propane)", "R410A", "R1234yf", "R407C"
]

@router.get("/supported-fluids")
def get_supported_fluids():
    return {"fluids": SUPPORTED_REFRIGERANTS}

@router.get("/{equipment_id}")
def get_refrigerant_status(equipment_id: str):
    """Calcule le taux de fuite, la conformité F-Gas et renvoie les indicateurs thermodynamiques complets (COP, puissances, débits)."""
    data = REFRIGERANT_DB.get(equipment_id)
    if not data:
        raise HTTPException(status_code=404, detail="Équipement non trouvé dans le registre.")
    
    total_added = sum(data["recharge_history_kg"])
    leak_rate_percent = (total_added / data["initial_charge_kg"]) * 100
    is_compliant = leak_rate_percent <= 5.0 and data["leak_test_passed"]

    return {
        "equipment_id": equipment_id,
        "refrigerant_type": data["refrigerant_type"],
        "initial_charge_kg": data["initial_charge_kg"],
        "total_recharged_kg": round(total_added, 2),
        "estimated_leak_rate_percent": round(leak_rate_percent, 1),
        "compliance_status": "CONFORME" if is_compliant else "ALERTE FUITE / NON-CONFORME",
        "thermodynamics": {
            "suction_pressure_bar": data["suction_pressure_bar"],
            "discharge_pressure_bar": data["discharge_pressure_bar"],
            "superheat_k": data["superheat_k"],
            "subcooling_k": data["subcooling_k"],
            "cop": data["cop"],
            "cooling_capacity_kw": data["cooling_capacity_kw"],
            "mass_flow_kg_s": data["mass_flow_kg_s"]
        },
        "tewi_kg_co2e_per_year": 12500.0  # Indicateur d'impact environnemental global (Total Equivalent Warming Impact)
    }

@router.post("/recharge")
def add_recharge_log(equipment_id: str, amount_kg: float):
    if equipment_id not in REFRIGERANT_DB:
        raise HTTPException(status_code=404, detail="Équipement non trouvé.")
    REFRIGERANT_DB[equipment_id]["recharge_history_kg"].append(amount_kg)
    return {"status": "success", "added_kg": amount_kg, "new_history": REFRIGERANT_DB[equipment_id]["recharge_history_kg"]}