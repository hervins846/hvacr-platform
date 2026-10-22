// apps/simulator/src/model.js

class ColdRoomSimulator {
    constructor(options = {}) {
        this.roomTemp = options.initialRoomTemp || 15.0; // °C
        this.targetTemp = options.targetTemp || 4.0;     // °C
        this.ambientTemp = options.ambientTemp || 32.0;  // °C
        this.isCompressorOn = false;
        this.totalEnergyKWh = 0;
        this.startCount = 0;
    }

    /**
     * Met à jour l'état du système pour un pas de temps donné (en minutes).
     * @param {number} dtMinutes - Pas de temps
     */
    step(dtMinutes = 1) {
        const dtHours = dtMinutes / 60;

        // Régulation Tout ou Rien (Thermostat avec hystérésis de 1°C)
        if (!this.isCompressorOn && this.roomTemp >= this.targetTemp + 1.0) {
            this.isCompressorOn = true;
            this.startCount++;
        } else if (this.isCompressorOn && this.roomTemp <= this.targetTemp - 1.0) {
            this.isCompressorOn = false;
        }

        // Dynamique thermique (apport de chaleur externe vs puissance frigorifique)
        const heatGainRate = 0.5 * (this.ambientTemp - this.roomTemp); // kW équivalent
        const coolingPower = this.isCompressorOn ? 3.5 : 0;            // kW frigorifique

        // Variation nette de température dans la chambre (inertie thermique simple)
        const netPowerKW = heatGainRate - coolingPower;
        this.roomTemp += (netPowerKW * dtHours) * 1.5; // Facteur d'inertie

        // Consommation électrique
        if (this.isCompressorOn) {
            const electricalPowerKW = 1.2; // kW électriques
            this.totalEnergyKWh += electricalPowerKW * dtHours;
        }

        return {
            roomTemp: Number(this.roomTemp.toFixed(2)),
            isCompressorOn: this.isCompressorOn,
            energyKWh: Number(this.totalEnergyKWh.toFixed(3)),
            startCount: this.startCount
        };
    }
}

module.exports = ColdRoomSimulator;