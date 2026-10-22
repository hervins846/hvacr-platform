# services/analytics/tewi.py

def calculate_tewi(
    initial_charge_kg: float,
    annual_leak_rate_percent: float,
    system_lifespan_years: int,
    recovery_factor: float,
    annual_energy_kwh: float,
    emission_factor_kg_co2_per_kwh: float = 0.500  # Facteur d'émission moyen du mix électrique (kg CO2/kWh)
) -> dict:
    """
    Calcule le TEWI (Total Equivalent Warming Impact) selon la formule standard :
    TEWI = (GWP × M × n) + (GWP × n_rec × L_annual) + (E_annual × n × Beta)
    Simplifié pour une exploitation industrielle : Effet direct + Effet indirect.
    """
    # Valeurs de GWP (Global Warming Potential) indicatives selon les types de fréon
    gwp_values = {
        "R134a": 1430,
        "R404A": 3922,
        "R410A": 2088,
        "R744": 1       # CO2 (naturel)
    }
    
    # Pour l'exemple, prenons le R134a par défaut
    gwp = gwp_values.get("R134a", 1430)

    # 1. Effet Direct (Fuites cumulées sur la durée de vie + fin de vie)
    # Masse perdue par an estimée via le taux de fuite
    annual_leak_kg = initial_charge_kg * (annual_leak_rate_percent / 100.0)
    direct_impact = (annual_leak_kg * gwp * system_lifespan_years) + (initial_charge_kg * gwp * (1 - recovery_factor))

    # 2. Effet Indirect (Émissions dues à la consommation électrique sur la durée de vie)
    indirect_impact = annual_energy_kwh * system_lifespan_years * emission_factor_kg_co2_per_kwh

    total_tewi = direct_impact + indirect_impact

    return {
        "refrigerant_gwp": gwp,
        "direct_impact_kg_co2": round(direct_impact, 2),
        "indirect_impact_kg_co2": round(indirect_impact, 2),
        "total_tewi_kg_co2": round(total_tewi, 2),
        "carbon_cost_status": "Élevé" if total_tewi > 50000 else "Maîtrisé"
    }