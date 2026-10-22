# Plateforme Industrielle HVACR (Chauffage, Ventilation, Climatisation et Réfrigération)

Plateforme modulaire de supervision, de simulation de jumeau numérique et d'analyse prédictive pour les installations frigorifiques et thermiques industrielles.

---

## 🏗️ Architecture du Projet (Monorepo)

```text
hvacr-platform/
├── .vscode/                  # Configurations VS Code (tâches, extensions, debug)
├── apps/
│   ├── simulator/            # Simulateur de chambre froide (modèle physique + scénarios)
│   ├── dashboard/            # Supervision web temps réel (optionnel)
│   └── mobile/               # Application technicien (hors ligne)
├── services/
│   ├── api/                  # API REST FastAPI (équipements, mesures, alarmes)
│   │   └── routers/          # Routeurs modulaires (equipments, measurements, alarms)
│   ├── ingestion/            # Passerelle IoT (MQTT vers API REST)
│   └── analytics/            # Moteur de maintenance prédictive et suivi des dérives (COP, F-Gas)
├── packages/
│   ├── thermo/               # Propriétés thermodynamiques (R134a, COP, surchauffe)
│   └── shared/               # Constantes et types communs
├── data/
│   ├── samples/              # Relevés d'exemple (CSV)
│   └── scenarios/            # Scénarios de pannes pour le simulateur (JSON)
├── infra/
│   └── docker-compose.yml    # Broker MQTT (Mosquitto) & TimescaleDB
├── docs/                     # Documentation technique, schémas P&ID
└── README.md
```
