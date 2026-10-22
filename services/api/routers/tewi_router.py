# services/api/routers/tewi_router.py

from fastapi import APIRouter
from services.analytics.tewi import calculate_tewi

router = APIRouter(
    prefix="/tewi",
    tags=["Carbon Footprint & TEWI"]
)

@router.get("/{equipment_id}")
def get_equipment_tewi(equipment_id: str):
    """Retourne l'impact environnemental TEWI pour un équipement donné."""
    
    # Simulation de données récupérées de la base pour l'équipement
    initial_charge = 15.0       # kg
    leak_rate = 3.5             # % par an
    annual_energy = 12500.0     # kWh/an
    
    result = calculate_tewi(
        initial_charge_kg=initial_charge,
        annual_leak_rate_percent=leak_rate,
        system_lifespan_years=10,
        recovery_factor=0.85,
        annual_energy_kwh=annual_energy
    )
    
    return {
        "equipment_id": equipment_id,
        **result,
        "message": "Indicateur TEWI calculé avec succès pour la conformité environnementale."
    }