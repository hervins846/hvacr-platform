// apps/simulator/src/run_scenario.js

const fs = require('fs');
const ColdRoomSimulator = require('./model');

// Charger le scénario
const scenarioPath = './data/scenarios/panne_fui_condenseur.json';
const scenario = JSON.parse(fs.readFileSync(scenarioPath, 'utf8'));

console.log(`[SCÉNARIO] Lancement : ${scenario.name}`);
console.log(`[DESCRIPTION] ${scenario.description}\n`);

// Initialisation du simulateur
const sim = new ColdRoomSimulator({
    initialRoomTemp: scenario.initial_state.room_temp,
    targetTemp: scenario.initial_state.target_temp,
    ambientTemp: scenario.initial_state.ambient_temp
});

let currentDischargePressure = scenario.initial_state.discharge_pressure_bar;

// Simulation pas à pas
let timeElapsed = 0;
const interval = scenario.step_interval_minutes;

const simulationInterval = setInterval(() => {
    timeElapsed += interval;

    // Vérifier si un événement se déclenche à ce minute-clé
    const activeEvent = scenario.events.find(e => e.minute === timeElapsed);
    if (activeEvent) {
        console.log(`\n⚠️ [ÉVÉNEMENT [t=${timeElapsed} min]] : ${activeEvent.description}`);
        if (activeEvent.action === 'increase_ambient_temp') {
            sim.ambientTemp = activeEvent.value;
        }
        if (activeEvent.action === 'simulate_condenser_fouling') {
            currentDischargePressure += activeEvent.delta_discharge_bar;
        }
    }

    // Exécuter un pas du modèle physique
    const state = sim.step(interval);
    
    // Estimation simple de la pression HP en fonction de la température ambiante et de l'encrassement
    currentDischargePressure = Number((10.0 + (sim.ambientTemp - 25) * 0.4 + (sim.isCompressorOn ? 2.0 : 0)).toFixed(1));

    console.log(`[t=${timeElapsed.toString().padStart(2, '0')} min] T° Chambre: ${state.roomTemp}°C | Compresseur: ${state.isCompressorOn ? 'MARCHE' : 'ARRÊT'} | Pression HP: ${currentDischargePressure} bar`);

    // Vérification des seuils d'alarme simulés
    if (currentDischargePressure > 18.0) {
        console.log(`🚨 [ALARME DÉCLENCHÉE] Haute Pression critique (${currentDischargePressure} bar) ! Arrêt de sécurité requis.`);
    }

    // Fin du scénario
    if (timeElapsed >= scenario.duration_minutes) {
        console.log(`\n[FIN DU SCÉNARIO] Bilan énergétique total : ${state.energyKWh} kWh | Démarrages : ${state.startCount}`);
        clearInterval(simulationInterval);
    }
}, 1000); // 1 seconde réelle = 5 minutes simulées pour l'exemple