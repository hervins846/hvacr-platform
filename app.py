# app.py - HVACR Intelligent 2029 (Simulation 3D Vivante & Animée)
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
from datetime import datetime

st.set_page_config(
    page_title="HVACR Intelligent 2029 - Simulation Dynamique",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style UI 2029 : Design lumineux, professionnel et épuré
st.markdown("""
<style>
    .stApp {
        background-color: #f1f5f9;
        color: #0f172a;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    .panel-card {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        padding: 12px 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .badge-live {
        background-color: #dcfce7;
        color: #15803d;
        border: 1px solid #86efac;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }
    .val-bp { color: #0284c7; font-size: 24px; font-weight: 800; }
    .val-hp { color: #dc2626; font-size: 24px; font-weight: 800; }
    .label-title { color: #475569; font-size: 12px; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px; }
</style>
""", unsafe_allow_html=True)

if "running" not in st.session_state:
    st.session_state.running = True
if "history" not in st.session_state:
    st.session_state.history = []
if "tick" not in st.session_state:
    st.session_state.tick = 0

with st.sidebar:
    st.markdown("### ❄️ HVACR 2029")
    st.caption("Supervision & Ingénierie Avancée")
    st.markdown("---")
    
    fluid = st.selectbox("Fluide Frigorigène", ["R134a", "R404A", "R744 (CO2)", "R290 (Propane)", "R410A"])
    
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        if st.button("▶ Démarrer"): st.session_state.running = True
    with col_b2:
        if st.button("⏸ Pause"): st.session_state.running = False
    with col_b3:
        if st.button("🔄 Reset"):
            st.session_state.history = []
            st.session_state.tick = 0

    thermal_load = st.slider("Charge Thermique (%)", 10, 150, 75)
    ambient_temp = st.slider("Température Ambiante (°C)", 10, 50, 30)
    
    st.markdown("#### ⚙️ CONTRÔLE DES ANOMALIES")
    sim_leak = st.checkbox("Fuite de circuit (BP Basse)", value=False)
    sim_overload = st.checkbox("Surcharge Thermique HP", value=False)

now_str = datetime.now().strftime("%H:%M:%S | %d %b %Y")
st.markdown(f"""
<div class="header-top">
    <div>
        <span style="font-size: 20px; font-weight: 800; color: #1e293b;">🌐 PLATEFORME HVACR INTELLIGENTE 2029</span>
        <span style="color: #64748b; font-size: 13px; margin-left: 15px;">Console Industrielle à 5 Panels — Simulation Dynamique Vivante</span>
    </div>
    <div style="display: flex; align-items: center; gap: 20px;">
        <span class="badge-live">● SIMULATION ACTIVE</span>
        <span style="color: #475569; font-size: 13px; font-weight: 600;">🕒 {now_str}</span>
    </div>
</div>
""", unsafe_allow_html=True)

tick = st.session_state.tick
noise = np.sin(tick * 0.3) * 0.15

bp_bar = round(3.2 + noise - (1.2 if sim_leak else 0), 2)
hp_bar = round(11.8 + (ambient_temp - 25) * 0.2 + noise + (3.5 if sim_overload else 0), 2)
t_evap = round(5.4 + noise, 1)
t_refoul = round(68.5 + (ambient_temp - 25) * 0.5, 1)
cop_val = round(max(1.2, 4.1 - (ambient_temp - 20) * 0.04), 2)

if st.session_state.running:
    st.session_state.tick += 1
    st.session_state.history.append({
        "t": tick,
        "BP": bp_bar,
        "HP": hp_bar,
        "Signal_Oscillo": bp_bar + np.sin(tick * 0.8) * 0.2
    })
    if len(st.session_state.history) > 50:
        st.session_state.history.pop(0)

# ==========================================
# 5 PANNEAUX D'INGÉNIERIE MODERNE
# ==========================================
p1, p2 = st.columns([2.2, 1.0])

with p1:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("#### 🖼️ PANEL 1 : JUMEAU 3D & INSTALLATION FRIGORIFIQUE (ANIMÉ)")
    st.caption("Circulation fluide en direct : Basse Pression (Bleu) / Haute Pression (Rouge)")

    # Définition géométrique des circuits HP et BP
    hp_x = [0.0, 0.0, 2.5, 2.5, 1.2]
    hp_y = [0.0, 2.0, 2.0, 0.0, -0.8]
    hp_z = [0.0, 1.0, 1.0, 0.0, 0.0]

    bp_x = [1.2, 0.5, -1.0, 0.0]
    bp_y = [-0.8, -1.5, -0.5, 0.0]
    bp_z = [0.0, 0.0, 0.0, 0.0]

    fig_3d = go.Figure()

    # Lignes fixes du système
    fig_3d.add_trace(go.Scatter3d(
        x=hp_x, y=hp_y, z=hp_z,
        mode='lines',
        line=dict(color='red', width=7),
        name='Haute Pression (HP)',
        hoverinfo='none'
    ))

    fig_3d.add_trace(go.Scatter3d(
        x=bp_x, y=bp_y, z=bp_z,
        mode='lines',
        line=dict(color='blue', width=7),
        name='Basse Pression (BP)',
        hoverinfo='none'
    ))

    # --- SIMULATION VIVANTE : Particules de fluide en mouvement le long des tuyaux ---
    # Interpolation dynamique HP
    hp_steps = 10
    anim_hp_x, anim_hp_y, anim_hp_z = [], [], []
    for i in range(len(hp_x) - 1):
        for step in range(hp_steps):
            f = step / hp_steps
            anim_hp_x.append(hp_x[i] + (hp_x[i+1] - hp_x[i]) * f)
            anim_hp_y.append(hp_y[i] + (hp_y[i+1] - hp_y[i]) * f)
            anim_hp_z.append(hp_z[i] + (hp_z[i+1] - hp_z[i]) * f)
    
    # Interpolation dynamique BP
    bp_steps = 10
    anim_bp_x, anim_bp_y, anim_bp_z = [], [], []
    for i in range(len(bp_x) - 1):
        for step in range(bp_steps):
            f = step / bp_steps
            anim_bp_x.append(bp_x[i] + (bp_x[i+1] - bp_x[i]) * f)
            anim_bp_y.append(bp_y[i] + (bp_y[i+1] - bp_y[i]) * f)
            anim_bp_z.append(bp_z[i] + (bp_z[i+1] - bp_z[i]) * f)

    # Calcul des index mobiles synchronisés sur le tick
    hp_idx = (tick * 3) % len(anim_hp_x)
    bp_idx = (tick * 3) % len(anim_bp_x)

    # Ajout des marqueurs mobiles (flux actif)
    fig_3d.add_trace(go.Scatter3d(
        x=[anim_hp_x[hp_idx]], y=[anim_hp_y[hp_idx]], z=[anim_hp_z[hp_idx]],
        mode='markers',
        marker=dict(size=8, color='#ff7878', symbol='circle'),
        name='Flux HP'
    ))

    fig_3d.add_trace(go.Scatter3d(
        x=[anim_bp_x[bp_idx]], y=[anim_bp_y[bp_idx]], z=[anim_bp_z[bp_idx]],
        mode='markers',
        marker=dict(size=8, color='#7878ff', symbol='circle'),
        name='Flux BP'
    ))

    # Étiquettes des composants industriels
    component_x = [0.0, 2.5, 1.2, -0.5]
    component_y = [0.0, 1.0, -0.8, -1.0]
    component_z = [0.3, 1.3, 0.3, 0.3]
    component_names = ['Compresseur', 'Condenseur', 'Détendeur', 'Évaporateur']

    fig_3d.add_trace(go.Scatter3d(
        x=component_x, y=component_y, z=component_z,
        mode='text',
        text=component_names,
        textfont=dict(size=12, color='#0f172a', family='Arial Black'),
        name='Composants'
    ))

    fig_3d.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, visible=False),
            yaxis=dict(showbackground=False, visible=False),
            zaxis=dict(showbackground=False, visible=False),
            camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2)),
            bgcolor="#f8fafc"
        ),
        legend=dict(x=0.01, y=0.99, font=dict(size=10)),
        margin=dict(l=0, r=0, b=0, t=10),
        height=340,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        uirevision="constant"
    )

    st.plotly_chart(fig_3d, width='stretch', config={"displaylogo": False})
    st.markdown('</div>', unsafe_allow_html=True)

with p2:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 PANEL 2 : MESURES CLÉS")
    st.markdown('<hr style="margin:6px 0; border-color:#e2e8f0;">', unsafe_allow_html=True)
    
    st.markdown('<div class="label-title">Basse Pression</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="val-bp">{bp_bar} bar</div>', unsafe_allow_html=True)
    st.caption(f"Évaporation : {t_evap} °C")
    
    st.markdown('<hr style="margin:6px 0; border-color:#e2e8f0;">', unsafe_allow_html=True)
    st.markdown('<div class="label-title">Haute Pression</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="val-hp">{hp_bar} bar</div>', unsafe_allow_html=True)
    st.caption(f"Refoulement : {t_refoul} °C")

    if sim_leak: st.error("⚠️ Alerte Fuite BP")
    if sim_overload: st.warning("⚠️ Alerte Surcharge HP")
    st.markdown('</div>', unsafe_allow_html=True)

# LIGNE INFÉRIEURE : Panels 3, 4 et 5
e1, e2, e3 = st.columns(3)

with e1:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("#### ⚡ PANEL 3 : GRAPHE OSCILLOSCOPE")
    st.caption("Analyse du signal transitoire des pressions")
    if len(st.session_state.history) > 1:
        df_h = pd.DataFrame(st.session_state.history)
        fig_osc = go.Figure()
        fig_osc.add_trace(go.Scatter(y=df_h["Signal_Oscillo"], mode="lines", line=dict(color="#10b981", width=2)))
        fig_osc.update_layout(height=180, margin=dict(l=0, r=0, t=5, b=0), paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", xaxis=dict(visible=False), yaxis=dict(gridcolor="#e2e8f0"), showlegend=False)
        st.plotly_chart(fig_osc, width='stretch', config={"displaylogo": False})
    st.markdown('</div>', unsafe_allow_html=True)

with e2:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("#### 🤖 PANEL 4 : SANTÉ COMPRESSEUR")
    st.markdown("<p style='color:#15803d; font-weight:700; font-size:14px;'>✔ État : Nominal</p>", unsafe_allow_html=True)
    st.markdown("Vibrations : <b>1.8 mm/s</b>")
    st.markdown("Température carter : <b>58.2 °C</b>")
    st.markdown("Indice de santé : <b>95%</b>")
    st.markdown('</div>', unsafe_allow_html=True)

with e3:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("#### ⚙️ PANEL 5 : THERMODYNAMIQUE")
    st.markdown(f"COP Global : <span style='font-size:20px; font-weight:800; color:#0284c7;'>{cop_val}</span>", unsafe_allow_html=True)
    st.markdown("Puissance Frigorifique : <b>48.5 kW</b>")
    st.markdown("Débit Massique : <b>0.015 kg/s</b>")
    st.markdown("Fluide Actif : <b>" + fluid + "</b>")
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.running:
    time.sleep(1)
    st.rerun()