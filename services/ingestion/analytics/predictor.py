# services/analytics/predictor.py

import json
from datetime import datetime

class HVACRAnalyticsEngine:
    def __init__(self):
        # Seuils de référence pour l'analyse
        self.max_allowable_discharge_pressure = 16.0  # bar
        self.optimal_cop = 3.2

    def analyze_trend(self, historical_data):
        """
        Analyse une liste de mesures temporelles pour détecter des dérives
        et prédire une potentielle panne (ex: encrassement condenseur, perte de charge).
        """
        if not historical_data or len(historical_data) < 5:
            return {"status": "insufficient_data", "message": "Pas assez de données pour l'analyse."}

        discharge_pressures = [d.get("discharge_pressure_bar", 0) for d in historical_data]
        room_temps = [d.get("room_temp", 0) for d in historical_data]
        
        # Calcul de la tendance de pression de refoulement (régression linéaire simple ou delta)
        initial_hp = discharge_pressures[0]
        latest_hp = discharge_pressures[-1]
        hp_drift = latest_hp - initial_hp

        # Détection d'anomalies / Prédictions
        warnings = []
        maintenance_recommended = False

        # 1. Détection de dérive de la Haute Pression (Indice d'encrassement du condenseur)
        if hp_drift > 3.0:
            warnings.warn = True
            warnings.append(
                f"⚠️ [ANALYSE PRÉDICTIVE] Hausse anormale de la HP (+{hp_drift:.1f} bar). "
                "Risque d'encrassement du condenseur ou détérioration de l'échange thermique."
            )
            maintenance_recommended = True

        # 2. Analyse de l'inertie thermique (Rupture potentielle de régulation)
        avg_temp = sum(room_temps) / len(room_temps)
        if max(room_temps) > 6.0:
            warnings.append(
                f"⚠️ [ANALYSE] Température moyenne élevée ({avg_temp:.1f}°C). "
                "Le groupe peine à maintenir la consigne (vérifier la charge de fluide ou l'isolation)."
            )

        # 3. Estimation de la santé globale du système (Score de 0 à 100)
        health_score = 100 - min(100, max(0, (hp_drift / 5.0) * 50 + (max(0, avg_temp - 4.0) / 4.0) * 50))

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "health_score": round(health_score, 1),
            "hp_drift_bar": round(hp_drift, 2),
            "maintenance_recommended": maintenance_recommended,
            - "diagnostics": warnings
        }

# --- Exemple d'utilisation du module ---
if __name__ == "__main__":
    # Simulation d'un historique de relevés sur plusieurs heures montrant une dérive
    sample_history = [
        {"room_temp": 4.1, "discharge_pressure_bar": 11.5},
        {"room_temp": 4.2, "discharge_pressure_bar": 12.0},
        {"room_temp": 4.5, "discharge_pressure_bar": 13.2},
        {"room_temp": 4.8, "discharge_pressure_bar": 14.8},
        {"room_temp": 5.3, "discharge_pressure_bar": 16.2}
    ]

    engine = HVACRAnalyticsEngine()
    result = engine.analyze_trend(sample_history)

    print(json.dumps(result, indent=4, ensure_ascii=False))