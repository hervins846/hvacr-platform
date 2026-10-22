# services/analytics/derives.py

from datetime import datetime

class HVACRDerivativesEngine:
    def __init__(self):
        # Seuils de référence normatifs ou constructeur
        self.BASELINE_COP = 3.2
        self.MAX_ANNUAL_LEAK_RATE_PERCENT = 5.0  # Seuil réglementaire indicatif F-Gas (%)

    def analyze_energy_drift(self, power_readings_kwh, operating_hours):
        """
        Analyse la dérive de consommation énergétique par rapport à la production frigorifique.
        """
        if operating_hours <= 0:
            return {"status": "error", "message": "Heures de fonctionnement invalides."}

        total_kwh = sum(power_readings_kwh)
        avg_power_kw = total_kwh / operating_hours

        # Simulation d'un calcul de COP instantané moyen
        estimated_cooling_power_kw = 3.5  # Puissance frigorifique nominale
        current_cop = estimated_cooling_power_kw / max(avg_power_kw, 0.1)

        # Calcul du pourcentage de dégradation du COP
        cop_degradation_percent = ((self.BASELINE_COP - current_cop) / self.BASELINE_COP) * 100

        drift_detected = cop_degradation_percent > 15.0  # Alerte si perte de performance > 15%

        return {
            "metric": "energy_and_cop",
            "average_power_kw": round(avg_power_kw, 2),
            "current_cop": round(current_cop, 2),
            "cop_degradation_percent": round(cop_degradation_percent, 1),
            "drift_alert": drift_detected,
            "message": "⚠️ Dérive énergétique importante : surconsommation détectée." if drift_detected else "Performance nominale."
        }

    def analyze_refrigerant_leak_drift(self, fluid_logs):
        """
        Analyse le registre des fluides frigorigènes (conformité F-Gas / traçabilité des charges).
        Vérifie les appoints successifs pour détecter une fuite chronique.
        """
        total_initial_charge_kg = fluid_logs.get("initial_charge_kg", 10.0)
        total_added_kg = sum(fluid_logs.get("recharge_history_kg", []))
        inspections_ok = fluid_logs.get("leak_test_compliant", True)

        leak_rate_percent = (total_added_kg / total_initial_charge_kg) * 100

        compliance_issue = leak_rate_percent > self.MAX_ANNUAL_LEAK_RATE_PERCENT or not inspections_ok

        return {
            "metric": "refrigerant_fgas",
            "total_added_kg": round(total_added_kg, 2),
            "estimated_leak_rate_percent": round(leak_rate_percent, 1),
            "compliance_status": "NON-CONFORME" if compliance_issue else "CONFORME",
            "alerts": [
                f"🚨 [F-GAS] Taux de fuite annuel estimé à {leak_rate_percent}% (Seuil max : {self.MAX_ANNUAL_LEAK_RATE_PERCENT}%)." if compliance_issue else "Registre F-Gas en ordre."
            ]
        }

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    engine = HVACRDerivativesEngine()

    # 1. Test de dérive énergétique (ex: 6 relevés horaires de puissance)
    readings = [1.2, 1.4, 1.6, 1.8, 2.1, 2.3] # kWh par heure
    energy_report = engine.analyze_energy_drift(readings, operating_hours=6)
    print("--- RAPPORT ÉNERGÉTIQUE ---")
    print(energy_report)

    # 2. Test de suivi des fluides frigorigènes (F-Gas)
    equipment_fluid_data = {
        "initial_charge_kg": 15.0,
        "recharge_history_kg": [1.5, 2.0], # Appoints réalisés lors de l'année
        "leak_test_compliant": True
    }
    fgas_report = engine.analyze_refrigerant_leak_drift(equipment_fluid_data)
    print("\n--- RAPPORT F-GAS ---")
    print(fgas_report)