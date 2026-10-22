# services/api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Platform HVACR Intelligente et Analyse 4.0",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de données et logique intégrée pour le fluide et les calculs
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

@app.get("/refrigerant/supported-fluids")
def get_supported_fluids():
    return {"fluids": SUPPORTED_REFRIGERANTS}

@app.get("/refrigerant/{equipment_id}")
def get_refrigerant_status(equipment_id: str):
    data = REFRIGERANT_DB.get(equipment_id)
    if not data:
        raise HTTPException(status_code=404, detail="Équipement non trouvé.")
    return data

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    """Sert directement l'application complète en un clic."""
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Platform HVACR Intelligente et Analyse 4.0</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            body { background-color: #0b0f19; color: #ffffff; padding: 20px; }
            header { display: flex; justify-content: space-between; align-items: center; background: #131b2e; padding: 15px 25px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px; }
            h1 { font-size: 1.4rem; color: #38bdf8; }
            .dashboard-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 20px; }
            .bottom-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
            .card { background: #131b2e; border: 1px solid #1e293b; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            .card h3 { font-size: 1rem; margin-bottom: 15px; color: #94a3b8; }
            .visual-container { display: flex; gap: 15px; align-items: center; background: #090d16; padding: 15px; border-radius: 8px; height: 220px; justify-content: center; color: #64748b; font-style: italic; border: 1px dashed #334155; text-align: center; }
            .metrics-row { display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.9rem; color: #cbd5e1; }
            select { width: 100%; padding: 10px; background: #1e293b; color: white; border: 1px solid #334155; border-radius: 6px; margin-top: 10px; cursor: pointer; }
            .highlight-value { font-size: 1.8rem; font-weight: bold; color: #38bdf8; }
            .status-running { color: #4ade80; font-weight: bold; }
        </style>
    </head>
    <body>
        <header>
            <h1>🌐 Platform HVACR Intelligente et Analyse 4.0</h1>
            <div><span>🇫🇷</span> <span>🇬🇧</span> <span>🇨🇳</span></div>
        </header>

        <div class="dashboard-grid">
            <div class="card">
                <h3>Jumeau Numérique 3D & État de Maintenance (eq_chambre_01)</h3>
                <div class="visual-container">[Modèle 3D Interactif - Compresseur Semi-Hermétique & Condenseur à air]</div>
                <div class="metrics-row">
                    <span>État : <span class="status-running">En marche (Running)</span></span>
                    <span>Taux d'Usure : <strong>88%</strong></span>
                </div>
            </div>
            <div class="card">
                <h3>Schéma P&ID Dynamique (Circulation Fréon HP / BP)</h3>
                <div class="visual-container" style="background: #05070b; border-color: #ef4444;">[Synoptique Circuit - Refoulement HP (16 bar / 75°C) & Aspiration BP (2 bar / -15°C)]</div>
                <div class="metrics-row">
                    <span>Surchauffe (ΔT_sur) : <strong>8 K</strong></span>
                    <span>Sous-refroidissement (ΔT_se) : <strong>5 K</strong></span>
                </div>
            </div>
        </div>

        <div class="bottom-grid">
            <div class="card">
                <h3>Courbe de Tendance</h3>
                <div style="height: 120px; display: flex; align-items: center; justify-content: center; background: #090d16; border-radius: 6px; color: #64748b; font-size: 0.85rem;">[Graphique Temps Réel T° & Pression]</div>
            </div>
            <div class="card">
                <h3>Maintenance Prédictive & IA</h3>
                <div style="text-align: center; padding: 10px 0;">
                    <div class="highlight-value" style="color: #f59e0b;">88%</div>
                    <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 5px;">Analyse : <span style="color: #ef4444;">Critique - Maintenance sous 48h</span></p>
                </div>
            </div>
            <div class="card">
                <h3>Calculs Thermodynamiques & COP</h3>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="font-size: 0.85rem; color: #94a3b8;">COP Froid :</p>
                        <div class="highlight-value">4.8</div>
                    </div>
                    <div style="text-align: right; font-size: 0.85rem; color: #cbd5e1;">
                        <p>Puissance : <strong>35.2 kW</strong></p>
                        <p>Débit : <strong>0.19 kg/s</strong></p>
                    </div>
                </div>
            </div>
            <div class="card">
                <h3>Sélection Fluide Frigorigène</h3>
                <label for="fluid-select" style="font-size: 0.85rem; color: #94a3b8;">Fluide Actif :</label>
                <select id="fluid-select">
                    <option value="R134a">R134a (Standard)</option>
                    <option value="R404A">R404A (Basse Température)</option>
                    <option value="R744">R744 (CO2 Écologique)</option>
                    <option value="R22">R22 (Ancien / Rétrofit)</option>
                    <option value="R290">R290 (Propane)</option>
                    <option value="R410A">R410A (Clim & PAC)</option>
                    <option value="R1234yf">R1234yf (Faible GWP)</option>
                    <option value="R407C">R407C (Remplacement R22)</option>
                </select>
            </div>
        </div>
    </body>
    </html>
    """