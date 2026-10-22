// --- Configuration & État Global ---
const API_BASE_URL = "http://localhost:8000";
let jwtToken = localStorage.getItem("hvacr_token") || null;

// Données d'exemple/fallback si l'API est hors-ligne
let currentEquipment = {
    id: "eq_chambre_01",
    refrigerant: "R134a",
    charge_kg: 25.0,
    annual_leak_rate_pct: 1.2,
    kwh_annual: 45000,
    grid_emission_factor: 0.45
};

// --- Initialisation au Chargement de la Page ---
document.addEventListener("DOMContentLoaded", () => {
    checkAuthentication();
    setupEventListeners();
    refreshDashboardData();

    // Actualisation automatique des données toutes les 5 secondes
    setInterval(refreshDashboardData, 5000);
});

// --- 1. Gestion de l'Authentification (JWT) ---
function checkAuthentication() {
    if (!jwtToken) {
        console.warn("Utilisateur non authentifié. Mode démonstration ou connexion requise.");
        updateUIForUser({ username: "invité", role: "auditor" });
        return;
    }

    // Récupération des infos de l'utilisateur connecté depuis l'API
    fetch(`${API_BASE_URL}/users/me`, {
        headers: { "Authorization": `Bearer ${jwtToken}` }
    })
    .then(res => {
        if (!res.ok) throw new Error("Token expiré ou invalide");
        return res.json();
    })
    .then(user => updateUIForUser(user))
    .catch(() => {
        logout();
    });
}

function updateUIForUser(user) {
    const roleElem = document.getElementById("userRole");
    const nameElem = document.getElementById("userName");

    if (nameElem) nameElem.textContent = `Opérateur: ${user.username}`;
    if (roleElem) {
        roleElem.textContent = `Rôle: ${user.role.toUpperCase()}`;
        roleElem.className = `badge ${user.role === "admin" ? "badge-admin" : "badge-warning"}`;
    }
}

function logout() {
    localStorage.removeItem("hvacr_token");
    jwtToken = null;
    alert("Vous avez été déconnecté.");
    window.location.reload();
}

// --- 2. Écouteurs d'Événements (Inputs & Selects) ---
function setupEventListeners() {
    const equipSelect = document.getElementById("equipSelect");
    if (equipSelect) {
        equipSelect.addEventListener("change", (e) => {
            currentEquipment.id = e.target.value;
            refreshDashboardData();
        });
    }
}

function updateRefrigerant() {
    const refSelect = document.getElementById("refrigerantSelect");
    if (refSelect) {
        currentEquipment.refrigerant = refSelect.value;
        refreshDashboardData();
    }
}

// --- 3. Intégration Backend API : Calcul TEWI & Télémétrie ---
async function refreshDashboardData() {
    try {
        // Envoi des données de l'équipement au calculateur TEWI de FastAPI
        const response = await fetch(`${API_BASE_URL}/analytics/tewi`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...(jwtToken && { "Authorization": `Bearer ${jwtToken}` })
            },
            body: JSON.stringify({
                refrigerant_type: currentEquipment.refrigerant,
                refrigerant_charge_kg: currentEquipment.charge_kg,
                annual_leak_rate_pct: currentEquipment.annual_leak_rate_pct,
                annual_energy_kwh: currentEquipment.kwh_annual,
                grid_emission_factor: currentEquipment.grid_emission_factor,
                system_lifespan_years: 10
            })
        });

        if (!response.ok) throw new Error("Erreur serveur lors du calcul TEWI");

        const data = await response.json();
        updateDashboardUI(data);
    } catch (err) {
        console.warn("API indisponible, mise à jour en mode simulé local :", err.message);
        updateSimulatedUI();
    }
}

// --- 4. Mise à Jour de l'Interface Utilisateur (KPIs) ---
function updateDashboardUI(tewiData) {
    // Mise à jour de la carte TEWI globale
    const tewiElem = document.getElementById("tewiValue");
    if (tewiElem) {
        tewiElem.innerHTML = `${tewiData.total_tewi_kg_co2e.toLocaleString()} <span class="unit">kg CO₂e/an</span>`;
    }

    const leakElem = document.getElementById("leakValue");
    if (leakElem) {
        leakElem.innerHTML = `${currentEquipment.annual_leak_rate_pct} <span class="unit">% / an</span>`;
    }

    // Mise à jour visuelle du statut d'impact
    const statusElem = document.getElementById("tewiStatus");
    if (statusElem) {
        if (tewiData.direct_emissions_kg_co2e > tewiData.indirect_emissions_kg_co2e) {
            statusElem.textContent = "Alerte: Fuites Directes Prédominantes";
            statusElem.className = "kpi-status status-warning";
        } else {
            statusElem.textContent = "Effet Indirect (Énergie) Prédominant";
            statusElem.className = "kpi-status status-ok";
        }
    }
}

function updateSimulatedUI() {
    // Variation légère pour la simulation en direct
    const randomHP = (14.0 + (Math.random() * 0.6 - 0.3)).toFixed(1);
    const randomBP = (2.8 + (Math.random() * 0.2 - 0.1)).toFixed(1);

    const hpElem = document.getElementById("hpValue");
    const bpElem = document.getElementById("bpValue");

    if (hpElem) hpElem.innerHTML = `${randomHP} <span class="unit">bar</span>`;
    if (bpElem) bpElem.innerHTML = `${randomBP} <span class="unit">bar</span>`;
}

// --- 5. Actions d'Astreinte (Commandes Manuel & Alarmes) ---
async function simulateLeak() {
    currentEquipment.annual_leak_rate_pct = parseFloat((currentEquipment.annual_leak_rate_pct + 1.5).toFixed(1));
    
    // Ajout d'une ligne dans le tableau des alarmes
    const alarmsTable = document.getElementById("alarmsBody");
    if (alarmsTable) {
        const now = new Date().toLocaleString();
        const row = `
            <tr>
                <td>${now}</td>
                <td><span class="badge badge-warning">Alerte Fuite</span></td>
                <td>${currentEquipment.id}</td>
                <td>Augmentation anormale du taux de fuite (${currentEquipment.annual_leak_rate_pct}%)</td>
                <td>Actif</td>
            </tr>
        `;
        alarmsTable.insertAdjacentHTML("afterbegin", row);
    }

    refreshDashboardData();
}

async function clearAlarms() {
    currentEquipment.annual_leak_rate_pct = 1.2;
    const alarmsTable = document.getElementById("alarmsBody");
    if (alarmsTable) {
        alarmsTable.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; color: var(--text-muted);">Aucune alarme active.</td>
            </tr>
        `;
    }
    refreshDashboardData();
}