JavaScript
// packages/thermo/thermo.js

/**
 * Calcule la pression de saturation approximative du R134a en fonction de la température (°C).
 * @param {number} tempCelsius - Température en °C
 * @returns {number} - Pression en bar (absolue)
 */
function getSaturationPressureR134a(tempCelsius) {
    // Approximation polynomiale ou Antoine simplifiée pour le R134a
    const t = tempCelsius;
    // Formule empirique simplifiée pour l'exemple
    return Number((0.0001 * Math.pow(t, 3) + 0.032 * Math.pow(t, 2) + 0.95 * t + 4.5).toFixed(2));
}

/**
 * Calcule le COP (Coefficient de Performance) d'un système frigorifique.
 * @param {number} coolingPowerKW - Puissance frigorifique utile (kW)
 * @param {number} electricalPowerKW - Puissance électrique absorbée par le compresseur (kW)
 * @returns {number} - COP
 */
function calculateCOP(coolingPowerKW, electricalPowerKW) {
    if (electricalPowerKW <= 0) return 0;
    return Number((coolingPowerKW / electricalPowerKW).toFixed(2));
}

/**
 * Calcule la surchauffe à l'évaporateur.
 * @param {number} tempAspirationCelsius - Température réelle des gaz à l'aspiration (°C)
 * @param {number} pressionEvapBar - Pression d'évaporation lue au manomètre (bar)
 * @returns {number} - Surchauffe en Kelvin (K)
 */
function calculateSuperheat(tempAspirationCelsius, pressionEvapBar) {
    // Estimation inverse simplifiée de la température de saturation
    const tempSaturation = (pressionEvapBar - 4.5) / 0.95; 
    const superheat = tempAspirationCelsius - tempSaturation;
    return Number(Math.max(0, superheat).toFixed(1));
}

module.exports = {
    getSaturationPressureR134a,
    calculateCOP,
    calculateSuperheat
};