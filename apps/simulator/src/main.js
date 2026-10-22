// apps/simulator/src/main.js

const ColdRoomSimulator = require("./model");
const mqtt = require("mqtt");

// Connexion au broker MQTT local (Mosquitto)
const MQTT_BROKER_URL = "mqtt://localhost:1883";
const client = mqtt.connect(MQTT_BROKER_URL);

const EQUIPMENT_ID = "eq_chambre_01";
const STEP_INTERVAL_MS = 2000; // 1 pas de simulation toutes les 2 secondes

client.on("connect", () => {
  console.log("[SIMULATEUR] Connecté avec succès au broker MQTT.");
});

client.on("error", (err) => {
  console.warn(
    "[SIMULATEUR] Avertissement MQTT : Impossible de joindre le broker. Mode console seul actif.",
  );
});

// Initialisation du modèle physique de la chambre froide
const simulator = new ColdRoomSimulator({
  initialRoomTemp: 12.0, // Température de départ (°C)
  targetTemp: 4.0, // Consigne (°C)
  ambientTemp: 32.0, // Température extérieure / local technique (°C)
});

console.log(`\n==================================================`);
console.log(`🚀 Démarrage du Jumeau Numérique - ${EQUIPMENT_ID}`);
console.log(
  `Consigne : ${simulator.targetTemp}°C | Ambiance : ${simulator.ambientTemp}°C`,
);
console.log(`==================================================\n`);

// Boucle principale de simulation
setInterval(() => {
  // Avancer la simulation d'1 minute virtuelle par pas
  const state = simulator.step(1);

  // Estimation des pressions en fonction de l'état du compresseur
  const suctionPressure = state.isCompressorOn ? 2.1 : 2.9; // bar (Basse Pression)
  const dischargePressure = state.isCompressorOn ? 14.2 : 11.0; // bar (Haute Pression)

  // Construction du paquet de télémétrie
  const telemetryPayload = {
    equipment_id: EQUIPMENT_ID,
    roomTemp: state.roomTemp,
    suctionPressure: suctionPressure,
    dischargePressure: dischargePressure,
    isCompressorOn: state.isCompressorOn,
    energyKWh: state.energyKWh,
    startCount: state.startCount,
    timestamp: new Date().toISOString(),
  };

  // Affichage formaté dans la console
  const compressorBadge = state.isCompressorOn ? "❄️ [MARCHE]" : "⏸️ [ARRÊT ]";
  console.log(
    `${compressorBadge} | T° Chambre : ${state.roomTemp.toFixed(2)}°C ` +
      `| HP : ${dischargePressure} bar | BP : ${suctionPressure} bar ` +
      `| Énergie : ${state.energyKWh} kWh`,
  );

  // Publication sur le bus MQTT si connecté
  if (client.connected) {
    client.publish(
      `hvacr/telemetry/${EQUIPMENT_ID}`,
      JSON.stringify(telemetryPayload),
    );
  }
}, STEP_INTERVAL_MS);
