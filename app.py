"""
app.py — Application de Scoring Crédit
MBA1 Finance Digitale — ISM Dakar 2025-2026
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="CreditScore Pro — ISM Dakar",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════
#  DESIGN SYSTEM — Dark Pro Theme + ISM Brand Colors
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0D0F12 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ── Masquer éléments Streamlit par défaut ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
.block-container { padding: 1.5rem 2rem 2rem !important; max-width: 1400px; }

/* ══════════════════════════════════
   SIDEBAR
══════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #111318 !important;
    border-right: 1px solid #1E2028 !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }



.sidebar-brand {
    background: linear-gradient(135deg, #1a0a00 0%, #2d1200 100%);
    border-bottom: 1px solid #C8922A33;
    padding: 1.4rem 1.2rem 1.2rem;
    margin-bottom: 0;
}
.sidebar-brand-logo {
    display: flex; align-items: center; gap: 10px; margin-bottom: 6px;
}
.sidebar-brand-logo svg { flex-shrink: 0; }
.sidebar-brand-title {
    font-size: 1rem; font-weight: 800; color: #C8922A;
    letter-spacing: -0.3px; line-height: 1.2;
}
.sidebar-brand-sub {
    font-size: 0.7rem; color: #8A7060; letter-spacing: 0.5px; text-transform: uppercase;
    margin-left: 34px;
}

/* Sections sidebar */
.sb-section {
    padding: 1rem 1.2rem 0.5rem;
    border-bottom: 1px solid #1E2028;
}
.sb-section-label {
    font-size: 0.65rem; font-weight: 700; color: #C8922A;
    letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: 0.8rem; display: flex; align-items: center; gap: 6px;
}
.sb-section-label::after {
    content: ''; flex: 1; height: 1px; background: #C8922A33;
}

/* Metric cards dans la sidebar */
.sb-metric {
    display: flex; align-items: center; justify-content: space-between;
    background: #161920; border: 1px solid #1E2028;
    border-radius: 8px; padding: 0.6rem 0.8rem;
    margin-bottom: 0.5rem;
}
.sb-metric-label {
    font-size: 0.75rem; color: #8B909A; font-weight: 500;
    display: flex; align-items: center; gap: 6px;
}
.sb-metric-label svg { opacity: 0.7; }
.sb-metric-value {
    font-size: 0.9rem; font-weight: 700; color: #E8E9EC;
    font-variant-numeric: tabular-nums;
}
.sb-metric-value.good { color: #22C55E; }
.sb-metric-badge {
    font-size: 0.6rem; color: #22C55E; background: #22C55E18;
    border: 1px solid #22C55E33; border-radius: 4px;
    padding: 1px 5px; font-weight: 600;
}

/* Score legend dans sidebar */
.sb-legend-item {
    display: flex; align-items: center; gap: 8px;
    padding: 0.45rem 0; font-size: 0.78rem; color: #B0B5BE;
}
.sb-legend-dot {
    width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
}
.sb-legend-range { margin-left: auto; font-weight: 600; color: #E8E9EC; font-size: 0.75rem; }

/* Historique sidebar */
.sb-hist-item {
    display: flex; align-items: center; gap: 8px;
    background: #161920; border: 1px solid #1E2028;
    border-radius: 7px; padding: 0.5rem 0.7rem;
    margin-bottom: 0.4rem; cursor: default;
    transition: border-color 0.2s;
}
.sb-hist-item:hover { border-color: #C8922A44; }
.sb-hist-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.sb-hist-name { font-size: 0.78rem; color: #C8CDD6; font-weight: 500; flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.sb-hist-score { font-size: 0.75rem; font-weight: 700; }
.sb-hist-proba { font-size: 0.68rem; color: #686D78; }

/* ══════════════════════════════════
   TOPBAR / HEADER
══════════════════════════════════ */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 1.5rem;
    background: #111318;
    border: 1px solid #1E2028;
    border-radius: 12px;
    margin-bottom: 1.25rem;
}
.topbar-left { display: flex; align-items: center; gap: 14px; }
.topbar-icon {
    width: 44px; height: 44px; border-radius: 10px;
    background: linear-gradient(135deg, #2d1200, #5C2E00);
    border: 1px solid #C8922A44;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.topbar-title { font-size: 1.15rem; font-weight: 800; color: #E8E9EC; line-height: 1.2; }
.topbar-sub { font-size: 0.72rem; color: #686D78; margin-top: 2px; }
.topbar-right { display: flex; gap: 8px; align-items: center; }
.topbar-badge {
    font-size: 0.68rem; font-weight: 600; color: #C8922A;
    background: #C8922A12; border: 1px solid #C8922A33;
    border-radius: 6px; padding: 4px 10px; white-space: nowrap;
}
.topbar-badge.green {
    color: #22C55E; background: #22C55E10; border-color: #22C55E30;
}

/* ══════════════════════════════════
   SECTION HEADERS
══════════════════════════════════ */
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 1rem; margin-top: 0.25rem;
}
.section-icon {
    width: 32px; height: 32px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.section-icon.blue  { background: #1E3A5F; border: 1px solid #2D5A8E33; }
.section-icon.gold  { background: #2D1E00; border: 1px solid #C8922A33; }
.section-icon.slate { background: #1A1E2A; border: 1px solid #2D3344; }
.section-title-text { font-size: 0.82rem; font-weight: 700; color: #B0B5BE; text-transform: uppercase; letter-spacing: 1px; }

/* ══════════════════════════════════
   FORM CARD
══════════════════════════════════ */
.form-card {
    background: #111318;
    border: 1px solid #1E2028;
    border-radius: 12px;
    padding: 1.25rem 1.5rem 1rem;
    margin-bottom: 1rem;
}
.form-divider {
    height: 1px; background: #1E2028; margin: 1rem 0;
}

/* Inputs Streamlit — style dark */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: #161920 !important;
    border: 1px solid #252830 !important;
    border-radius: 8px !important;
    color: #E8E9EC !important;
    font-size: 0.88rem !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #C8922A66 !important;
    box-shadow: 0 0 0 3px #C8922A18 !important;
    outline: none !important;
}
[data-testid="stNumberInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label {
    font-size: 0.78rem !important; font-weight: 600 !important;
    color: #8B909A !important; letter-spacing: 0.3px;
    text-transform: uppercase !important;
}
/* +/- buttons */
[data-testid="stNumberInput"] button {
    background: #1E2028 !important; border: 1px solid #252830 !important;
    color: #8B909A !important; border-radius: 6px !important;
}
[data-testid="stNumberInput"] button:hover {
    background: #C8922A22 !important; color: #C8922A !important;
    border-color: #C8922A66 !important;
}
/* ══════════════════════════════════
   SELECTBOX — Solution définitive
   Streamlit injecte les styles inline
   via BaseWeb, donc on cible tout
══════════════════════════════════ */

/* Wrapper global: force couleur sur tous descendants */
[data-testid="stSelectbox"] * {
    color: #E8E9EC !important;
}

/* Le bouton trigger (rectangle visible) */
[data-testid="stSelectbox"] > div > div,
[data-testid="stSelectbox"] > div > div > div,
[data-baseweb="select"] > div {
    background-color: #161920 !important;
    border-color: #2A2D38 !important;
    border-radius: 8px !important;
    color: #E8E9EC !important;
}

/* Fond transparent pour les enfants directs du trigger */
[data-baseweb="select"] > div > div {
    background-color: transparent !important;
    color: #E8E9EC !important;
}

/* Hover */
[data-baseweb="select"] > div:hover {
    border-color: #C8922A66 !important;
}

/* Icône chevron */
[data-testid="stSelectbox"] svg {
    fill: #8B909A !important;
    color: #8B909A !important;
}

/* ── Dropdown list ── */
[data-baseweb="popover"],
[data-baseweb="popover"] > div {
    background-color: #1C1F27 !important;
    border: 1px solid #2A2D38 !important;
    border-radius: 10px !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.8) !important;
}

/* Liste */
[data-baseweb="menu"],
[data-baseweb="menu"] > ul,
[data-baseweb="menu"] > div {
    background-color: #1C1F27 !important;
    color: #C8CDD6 !important;
}

/* Chaque item */
[data-baseweb="menu"] li {
    background-color: #1C1F27 !important;
    color: #C8CDD6 !important;
    border-radius: 6px !important;
    margin: 2px 4px !important;
}
[data-baseweb="menu"] li * {
    color: #C8CDD6 !important;
    background-color: transparent !important;
}
[data-baseweb="menu"] li:hover {
    background-color: #C8922A22 !important;
    color: #E8E9EC !important;
}
[data-baseweb="menu"] li:hover * {
    color: #E8E9EC !important;
}

/* Item sélectionné */
[data-baseweb="menu"] li[aria-selected="true"],
[aria-selected="true"] {
    background-color: #C8922A25 !important;
    color: #C8922A !important;
    font-weight: 600 !important;
}
[aria-selected="true"] * {
    color: #C8922A !important;
}

[data-testid="stTooltipIcon"] { color: #686D78 !important; }

/* ══════════════════════════════════
   RADIO BUTTONS — Style pill horizontal
══════════════════════════════════ */

/* Conteneur flex horizontal */
[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 6px !important;
    flex-direction: row !important;
}

/* Chaque label = pill */
[data-testid="stRadio"] label {
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    padding: 6px 14px !important;
    border-radius: 20px !important;
    border: 1px solid #252830 !important;
    background: #161920 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #C8CDD6 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    white-space: nowrap !important;
    margin: 0 !important;
    width: auto !important;
}
[data-testid="stRadio"] label:hover {
    border-color: #C8922A88 !important;
    background: #1E2028 !important;
    color: #E8E9EC !important;
}

/* Cacher le radio natif, garder le comportement */
[data-testid="stRadio"] input[type="radio"] {
    display: none !important;
}

/* Pill sélectionnée */
[data-testid="stRadio"] label:has(input:checked) {
    border-color: #C8922A !important;
    background: linear-gradient(135deg, #2D1500, #3D1E00) !important;
    color: #C8922A !important;
    font-weight: 700 !important;
    box-shadow: 0 0 0 1px #C8922A44 !important;
}

/* Texte dans le label */
[data-testid="stRadio"] p {
    color: inherit !important;
    font-size: 0.82rem !important;
    margin: 0 !important;
    line-height: 1 !important;
}

/* ══════════════════════════════════
   BOUTON PRÉDIRE
══════════════════════════════════ */
[data-testid="stFormSubmitButton"] > button,
.stButton > button {
    background: linear-gradient(135deg, #5C2E00 0%, #8B4513 100%) !important;
    color: #C8922A !important;
    border: 1px solid #C8922A55 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    font-family: 'Inter', sans-serif !important;
    text-transform: uppercase !important;
}
[data-testid="stFormSubmitButton"] > button:hover,
.stButton > button:hover {
    background: linear-gradient(135deg, #C8922A 0%, #D4A843 100%) !important;
    color: #1a0a00 !important;
    border-color: transparent !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px #C8922A33 !important;
}

/* ══════════════════════════════════
   RÉSULTATS
══════════════════════════════════ */
.result-banner {
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    position: relative; overflow: hidden;
}
.result-banner.accord {
    background: linear-gradient(135deg, #0A2417 0%, #0F3620 100%);
    border: 1px solid #22C55E44;
}
.result-banner.refuse {
    background: linear-gradient(135deg, #240A0A 0%, #361010 100%);
    border: 1px solid #EF444444;
}
.result-icon { font-size: 2.2rem; margin-bottom: 0.4rem; line-height: 1; }
.result-label {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 0.3rem;
}
.result-label.accord { color: #4ADE80; }
.result-label.refuse { color: #F87171; }
.result-decision {
    font-size: 1.6rem; font-weight: 800; line-height: 1.1;
}
.result-decision.accord { color: #22C55E; }
.result-decision.refuse { color: #EF4444; }
.result-msg {
    font-size: 0.76rem; margin-top: 0.5rem; opacity: 0.7; line-height: 1.4;
}
.result-msg.accord { color: #BBF7D0; }
.result-msg.refuse { color: #FECACA; }

/* Carte score / proba */
.kpi-card {
    background: #111318; border: 1px solid #1E2028;
    border-radius: 12px; padding: 1.25rem 1rem;
    text-align: center; height: 100%;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.kpi-label {
    font-size: 0.65rem; font-weight: 700; color: #686D78;
    text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.6rem;
}
.kpi-value { font-size: 2.8rem; font-weight: 800; line-height: 1; }
.kpi-sub { font-size: 0.72rem; color: #686D78; margin-top: 4px; }
.kpi-badge {
    margin-top: 0.5rem; font-size: 0.7rem; font-weight: 600;
    padding: 3px 10px; border-radius: 20px;
}
.kpi-badge.faible { color: #22C55E; background: #22C55E15; border: 1px solid #22C55E30; }
.kpi-badge.modere { color: #F59E0B; background: #F59E0B15; border: 1px solid #F59E0B30; }
.kpi-badge.eleve  { color: #EF4444; background: #EF444415; border: 1px solid #EF444430; }

/* Jauge */
.gauge-wrap { margin-top: 1.25rem; }
.gauge-title {
    font-size: 0.68rem; font-weight: 700; color: #686D78;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.6rem;
    display: flex; align-items: center; justify-content: space-between;
}
.gauge-track {
    height: 10px; background: #1E2028; border-radius: 20px; overflow: hidden; position: relative;
}
.gauge-fill {
    height: 100%; border-radius: 20px;
    transition: width 0.6s cubic-bezier(.4,0,.2,1);
    position: relative;
}
.gauge-fill::after {
    content: ''; position: absolute; right: 0; top: 0;
    width: 4px; height: 100%;
    background: rgba(255,255,255,0.4); border-radius: 0 20px 20px 0;
}
.gauge-ticks {
    display: flex; justify-content: space-between;
    margin-top: 5px; padding: 0 2px;
}
.gauge-tick { font-size: 0.62rem; color: #3A3F4A; }
.gauge-tick.active { color: #686D78; }

/* Récapitulatif */
.recap-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.5rem 0; border-bottom: 1px solid #1E2028;
}
.recap-row:last-child { border-bottom: none; }
.recap-key { font-size: 0.78rem; color: #686D78; font-weight: 500; }
.recap-val { font-size: 0.78rem; color: #C8CDD6; font-weight: 600; }

/* Footer */
.app-footer {
    display: flex; align-items: center; justify-content: center; gap: 16px;
    padding: 1rem 0 0.5rem;
    border-top: 1px solid #1E2028;
    margin-top: 1.5rem;
}
.footer-text { font-size: 0.72rem; color: #3A3F4A; }
.footer-sep { color: #1E2028; }

/* Expander dark */
[data-testid="stExpander"] {
    background: #111318 !important; border: 1px solid #1E2028 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary { color: #8B909A !important; font-size: 0.82rem !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0D0F12; }
::-webkit-scrollbar-thumb { background: #252830; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #C8922A55; }

/* Cacher le label vide de la colonne d'identification */
.id-row [data-testid="stTextInput"] { margin-bottom: 0; }

/* sidebar toggle géré par JS */
</style>
""", unsafe_allow_html=True)

# Sidebar toggle supprimé — géré nativement par Streamlit

# ═══════════════════════════════════════════════════════════
#  SVG ICONS
# ═══════════════════════════════════════════════════════════
def icon_bank():
    # Icône banque / institution financière premium
    return """<svg width="22" height="22" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="2" y="28" width="28" height="2.5" rx="1.25" fill="#C8922A"/>
  <rect x="4" y="14" width="3" height="13" rx="1" fill="#C8922A" opacity="0.85"/>
  <rect x="9.5" y="14" width="3" height="13" rx="1" fill="#C8922A" opacity="0.85"/>
  <rect x="15" y="14" width="3" height="13" rx="1" fill="#C8922A" opacity="0.85"/>
  <rect x="20.5" y="14" width="3" height="13" rx="1" fill="#C8922A" opacity="0.85"/>
  <rect x="25" y="14" width="3" height="13" rx="1" fill="#C8922A" opacity="0.85"/>
  <rect x="2" y="11" width="28" height="3" rx="1.5" fill="#C8922A"/>
  <path d="M16 2L30 10H2L16 2Z" fill="#C8922A"/>
  <circle cx="16" cy="7" r="1.5" fill="#13151C"/>
</svg>"""

def icon_chart():
    # Icône graphique analytique avec courbe ROC stylisée
    return """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M3 20h18M3 20V4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M7 16l3-4 3 2 4-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="7" cy="16" r="1.5" fill="currentColor"/>
  <circle cx="10" cy="12" r="1.5" fill="currentColor"/>
  <circle cx="13" cy="14" r="1.5" fill="currentColor"/>
  <circle cx="17" cy="8" r="1.5" fill="currentColor"/>
</svg>"""

def icon_target():
    # Icône cible / précision
    return """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="12" cy="12" r="6" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="12" cy="12" r="2.5" fill="currentColor"/>
  <line x1="12" y1="2" x2="12" y2="5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="12" y1="19" x2="12" y2="22" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="2" y1="12" x2="5" y2="12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="19" y1="12" x2="22" y2="12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
</svg>"""

def icon_zap():
    # Icône éclair / performance
    return """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="currentColor" fill-opacity="0.15"/>
</svg>"""

def icon_award():
    # Icône médaille / récompense premium
    return """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="9" r="6" stroke="currentColor" stroke-width="1.8"/>
  <path d="M9 15.5l-2 6 5-2.5 5 2.5-2-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M10 9l1.5 1.5L14 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

def icon_user():
    # Icône utilisateur avec badge professionnel
    return """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="7" r="4" stroke="#C8922A" stroke-width="1.8"/>
  <path d="M4 21v-1a8 8 0 0 1 16 0v1" stroke="#C8922A" stroke-width="1.8" stroke-linecap="round"/>
  <circle cx="19" cy="8" r="3" fill="#22C55E"/>
  <path d="M17.5 8l1 1 2-2" stroke="white" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

def icon_money():
    # Icône monnaie africaine / FCFA
    return """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="1" y="5" width="22" height="14" rx="3" stroke="#C8922A" stroke-width="1.8"/>
  <circle cx="12" cy="12" r="3.5" stroke="#C8922A" stroke-width="1.8"/>
  <line x1="1" y1="9.5" x2="23" y2="9.5" stroke="#C8922A" stroke-width="1.5"/>
  <line x1="1" y1="14.5" x2="23" y2="14.5" stroke="#C8922A" stroke-width="1.5"/>
</svg>"""

def icon_briefcase():
    # Icône portefeuille professionnel
    return """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="2" y="8" width="20" height="13" rx="2.5" stroke="#C8922A" stroke-width="1.8"/>
  <path d="M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke="#C8922A" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="2" y1="14" x2="22" y2="14" stroke="#C8922A" stroke-width="1.5" stroke-dasharray="2 1"/>
  <circle cx="12" cy="14" r="1.5" fill="#C8922A"/>
</svg>"""

def icon_history():
    # Icône historique avec horloge moderne
    return """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/>
  <polyline points="12 7 12 12 16 14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M3.5 6.5A9.5 9.5 0 0 1 6.5 3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  <polyline points="1 4 3.5 6.5 6 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

def icon_info():
    # Icône information premium avec fond
    return """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="12" cy="8" r="1.2" fill="currentColor"/>
  <line x1="12" y1="11.5" x2="12" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>"""

# ═══════════════════════════════════════════════════════════
#  CHARGEMENT MODÈLE
# ═══════════════════════════════════════════════════════════
@st.cache_resource(ttl=0)   # ttl=0 = pas de cache persistant entre déploiements
def load_model():
    path = "credit_scoring_model.pkl"
    if not os.path.exists(path):
        return None
    data = joblib.load(path)
    # Garantir que le threshold est présent
    if "threshold" not in data:
        data["threshold"] = 0.50
    return data

# Force rechargement si version du modèle a changé
if "model_version" not in st.session_state:
    load_model.clear()
    st.session_state["model_version"] = "v3_threshold050"

model_data = load_model()

if "historique" not in st.session_state:
    st.session_state.historique = []


# ═══════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    # — Brand —
    st.markdown(f"""
    <div class="sidebar-brand">
        <div class="sidebar-brand-logo">
            {icon_bank()}
            <div class="sidebar-brand-title">CreditScore Pro</div>
        </div>
        <div class="sidebar-brand-sub">ISM Dakar · MBA1 Finance Digitale</div>
    </div>
    """, unsafe_allow_html=True)

    if model_data:
        m = model_data["metrics"]

        # — Performance —
        st.markdown(f"""
        <div class="sb-section">
            <div class="sb-section-label">{icon_chart()} Performance</div>
            <div class="sb-metric">
                <div class="sb-metric-label">{icon_target()} AUC-ROC</div>
                <div>
                    <span class="sb-metric-value good">{m['auc']:.4f}</span>
                    <span class="sb-metric-badge">TOP</span>
                </div>
            </div>
            <div class="sb-metric">
                <div class="sb-metric-label">{icon_zap()} Rappel Défaut</div>
                <span class="sb-metric-value">{m['recall']:.4f}</span>
            </div>
            <div class="sb-metric">
                <div class="sb-metric-label">{icon_award()} Précision</div>
                <span class="sb-metric-value">{m['precision']:.4f}</span>
            </div>
            <div class="sb-metric">
                <div class="sb-metric-label">{icon_chart()} F1-Score</div>
                <span class="sb-metric-value">{m['f1']:.4f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # — Légende scores —
        st.markdown(f"""
        <div class="sb-section">
            <div class="sb-section-label">{icon_info()} Grille des Scores</div>
            <div class="sb-legend-item">
                <div class="sb-legend-dot" style="background:#22C55E;"></div>
                <span>Risque Faible</span>
                <span class="sb-legend-range">700 – 1000</span>
            </div>
            <div class="sb-legend-item">
                <div class="sb-legend-dot" style="background:#F59E0B;"></div>
                <span>Risque Modéré</span>
                <span class="sb-legend-range">400 – 699</span>
            </div>
            <div class="sb-legend-item">
                <div class="sb-legend-dot" style="background:#EF4444;"></div>
                <span>Risque Élevé</span>
                <span class="sb-legend-range">0 – 399</span>
            </div>
            <div style="margin-top:0.7rem; padding-top:0.7rem; border-top:1px solid #1E2028;">
                <div style="font-size:0.72rem; color:#686D78; line-height:1.5;">
                    <span style="color:#C8922A; font-weight:600;">Seuil décision :</span> 50% de probabilité de défaut.<br>
                    Au-delà → Crédit <span style="color:#EF4444; font-weight:600;">Refusé</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # — Historique —
    st.markdown(f"""
    <div class="sb-section">
        <div class="sb-section-label">{icon_history()} Historique Session</div>
    """, unsafe_allow_html=True)

    if not st.session_state.historique:
        st.markdown('<div style="font-size:0.75rem; color:#3A3F4A; padding:0.3rem 0 0.8rem;">Aucune analyse effectuée.</div>', unsafe_allow_html=True)
    else:
        for h in reversed(st.session_state.historique[-8:]):
            dot_color = "#22C55E" if h["decision"] == "Accordé" else "#EF4444"
            score_color = "#22C55E" if h["score"] >= 700 else ("#F59E0B" if h["score"] >= 400 else "#EF4444")
            st.markdown(f"""
            <div class="sb-hist-item">
                <div class="sb-hist-dot" style="background:{dot_color};"></div>
                <div style="flex:1; min-width:0;">
                    <div class="sb-hist-name">{h['nom']}</div>
                    <div class="sb-hist-proba">{h['proba']:.1f}% défaut</div>
                </div>
                <div class="sb-hist-score" style="color:{score_color};">{h['score']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Effacer l'historique", key="clear_hist"):
            st.session_state.historique = []
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  VÉRIFICATION MODÈLE
# ═══════════════════════════════════════════════════════════
if model_data is None:
    st.error("**Modèle introuvable** — Lancez d'abord `python train_model.py`")
    st.stop()

pipeline             = model_data["pipeline"]
numerical_features   = model_data["numerical_features"]
categorical_features = model_data["categorical_features"]
all_features         = model_data["all_features"]
THRESHOLD            = model_data.get("threshold", 0.50)  # Seuil 0.5 (consigne prof)

# ═══════════════════════════════════════════════════════════
#  TOPBAR + MODALE PERFORMANCES  (st.dialog — Streamlit ≥ 1.32)
# ═══════════════════════════════════════════════════════════

@st.dialog("Performances du Modèle", width="large")
def show_perf_dialog():
    m = model_data["metrics"]
    st.markdown(f"""
<style>
/* Styles internes à la dialog Streamlit */
[data-testid="stDialog"] {{
    background: transparent !important;
}}
[data-testid="stDialog"] > div {{
    background: linear-gradient(145deg,#13151C,#0e1018) !important;
    border: 1px solid rgba(200,146,42,0.3) !important;
    border-radius: 18px !important;
    box-shadow: 0 25px 70px rgba(0,0,0,0.8) !important;
}}
</style>

<div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;
            padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.06);">
  <div style="width:40px;height:40px;border-radius:10px;
              background:linear-gradient(135deg,#1a2e1a,#0d1f0d);
              border:1px solid rgba(34,197,94,0.3);
              display:flex;align-items:center;justify-content:center;flex-shrink:0;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
    </svg>
  </div>
  <div>
    <div style="font-size:0.72rem;color:#4B5261;margin-top:2px;">
      Régression Logistique · Pipeline Scikit-Learn · Évaluation sur jeu de test
    </div>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;">

  <div style="background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.18);border-radius:12px;padding:16px;">
    <div style="display:flex;align-items:center;gap:7px;margin-bottom:8px;">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2.5">
        <circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/>
      </svg>
      <span style="font-size:0.62rem;color:#4B5261;text-transform:uppercase;letter-spacing:1px;font-weight:700;">AUC-ROC</span>
    </div>
    <div style="font-size:1.8rem;font-weight:800;color:#22C55E;letter-spacing:-1px;line-height:1;">{m['auc']:.4f}</div>
    <div style="font-size:0.64rem;color:#22C55E;opacity:0.7;margin-top:5px;">Excellent pouvoir discriminant</div>
  </div>

  <div style="background:rgba(200,146,42,0.06);border:1px solid rgba(200,146,42,0.18);border-radius:12px;padding:16px;">
    <div style="display:flex;align-items:center;gap:7px;margin-bottom:8px;">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#C8922A" stroke-width="2.5">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
      </svg>
      <span style="font-size:0.62rem;color:#4B5261;text-transform:uppercase;letter-spacing:1px;font-weight:700;">F1-Score</span>
    </div>
    <div style="font-size:1.8rem;font-weight:800;color:#C8922A;letter-spacing:-1px;line-height:1;">{m['f1']:.4f}</div>
    <div style="font-size:0.64rem;color:#C8922A;opacity:0.7;margin-top:5px;">Équilibre précision / rappel</div>
  </div>

  <div style="background:rgba(59,130,246,0.06);border:1px solid rgba(59,130,246,0.18);border-radius:12px;padding:16px;">
    <div style="display:flex;align-items:center;gap:7px;margin-bottom:8px;">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2.5">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
        <polyline points="22 4 12 14.01 9 11.01"/>
      </svg>
      <span style="font-size:0.62rem;color:#4B5261;text-transform:uppercase;letter-spacing:1px;font-weight:700;">Précision</span>
    </div>
    <div style="font-size:1.8rem;font-weight:800;color:#3B82F6;letter-spacing:-1px;line-height:1;">{m['precision']:.4f}</div>
    <div style="font-size:0.64rem;color:#3B82F6;opacity:0.7;margin-top:5px;">Vrais positifs / prédits positifs</div>
  </div>

  <div style="background:rgba(168,85,247,0.06);border:1px solid rgba(168,85,247,0.18);border-radius:12px;padding:16px;">
    <div style="display:flex;align-items:center;gap:7px;margin-bottom:8px;">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#A855F7" stroke-width="2.5">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <span style="font-size:0.62rem;color:#4B5261;text-transform:uppercase;letter-spacing:1px;font-weight:700;">Rappel Défaut</span>
    </div>
    <div style="font-size:1.8rem;font-weight:800;color:#A855F7;letter-spacing:-1px;line-height:1;">{m['recall']:.4f}</div>
    <div style="font-size:0.64rem;color:#A855F7;opacity:0.7;margin-top:5px;">Détection des mauvais payeurs</div>
  </div>
</div>

<div style="background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.2);
            border-radius:12px;padding:13px 16px;
            display:flex;align-items:center;justify-content:space-between;">
  <div style="display:flex;align-items:center;gap:8px;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2">
      <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
      <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
    <span style="font-size:0.77rem;color:#9CA3AF;">Seuil de décision optimisé</span>
  </div>
  <div style="font-size:0.92rem;font-weight:800;color:#EF4444;">{THRESHOLD*100:.0f}% <span style="font-size:0.68rem;font-weight:500;color:#6B7280;">probabilité de défaut</span></div>
</div>

<div style="margin-top:12px;font-size:0.63rem;color:#2D3244;text-align:center;">
  ISM Dakar · MBA1 Finance Digitale
</div>
    """, unsafe_allow_html=True)

# ─── Topbar ───────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebarCollapsedControl"] { display:none !important; }
</style>
""", unsafe_allow_html=True)

_col_left, _col_right = st.columns([5, 1])

with _col_left:
    st.markdown(f"""
    <div class="topbar">
        <div class="topbar-left">
            <div class="topbar-icon">{icon_bank()}</div>
            <div>
                <div class="topbar-title">Système d'Analyse de Risque Crédit</div>
                <div class="topbar-sub">Régression Logistique · Pipeline Scikit-Learn · {len(all_features)} features</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with _col_right:
    st.markdown("""<style>
    section.main > div > div:nth-child(1) > div > div:nth-child(2) button {
        font-size:0.7rem !important; font-weight:700 !important;
        padding:5px 12px !important; border-radius:20px !important;
        color:#22C55E !important; background:#0d2918 !important;
        border:1px solid #22C55E55 !important;
        box-shadow:0 0 10px rgba(34,197,94,0.12) !important;
    }
    </style>""", unsafe_allow_html=True)
    if st.button(f"● Modèle Actif  ·  AUC {model_data['metrics']['auc']:.4f}", key="btn_perf_open"):
        show_perf_dialog()

# ═══════════════════════════════════════════════════════════
#  NAVIGATION — ONGLETS
# ═══════════════════════════════════════════════════════════
tab_scoring, tab_batch, tab_importance, tab_about = st.tabs([
    "◈  Analyse Client",
    "⊞  Prédiction en Lot (CSV)",
    "⟁  Importance des Variables",
    "◉  À Propos du Modèle",
])

# ══════════════════════════════════════════════════════════
#  ONGLET 2 — BATCH CSV
# ══════════════════════════════════════════════════════════
with tab_batch:
    st.markdown("""
    <div style="background:#13151C;border:1px solid #1E2028;border-radius:12px;padding:20px 24px;margin-bottom:16px;">
      <div style="display:flex;align-items:center;gap:9px;margin-bottom:6px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C8922A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
          <polyline points="13 2 13 9 20 9"/>
          <line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/>
        </svg>
        <div style="font-size:0.95rem;font-weight:700;color:#E8E9EC;">Prédiction en lot — Chargement CSV</div>
      </div>
      <div style="font-size:0.78rem;color:#686D78;">Chargez un fichier CSV contenant plusieurs clients. Téléchargez d'abord le template, remplissez-le, puis importez-le pour obtenir les scores en masse.</div>
    </div>
    """, unsafe_allow_html=True)

    col_dl, _ = st.columns([1, 2])
    with col_dl:
        # Template CSV téléchargeable
        template_data = {
            "REVENU_MENSUEL_FCFA":    [350000, 180000, 650000],
            "RATIO_ENDETTEMENT":      [0.35, 0.60, 0.20],
            "SCORE_INTERNE_BANQUE":   [500, 300, 750],
            "NB_INCIDENTS_PAIEMENT":  [0, 3, 0],
            "JOURS_RETARD_MAX":       [0, 45, 0],
            "NB_REJETS_PRELEVEMENT":  [0, 2, 0],
            "NB_DECOUVERT_12MOIS":    [0, 5, 0],
            "ANCIENNETE_CLIENT_MOIS": [24, 6, 60],
            "TYPE_EMPLOI":            ["CDI", "Sans emploi", "Fonctionnaire"],
            "GARANTIE":               ["Hypothèque", "Aucune", "Assurance"],
        }
        import io
        template_df = pd.DataFrame(template_data)
        csv_bytes = template_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️  Télécharger le template CSV",
            data=csv_bytes,
            file_name="template_scoring_clients.csv",
            mime="text/csv",
        )

    uploaded_csv = st.file_uploader(
        "Chargez votre fichier CSV de clients",
        type=["csv"],
        help="Le fichier doit contenir exactement les 10 colonnes du template."
    )

    if uploaded_csv is not None:
        try:
            batch_df = pd.read_csv(uploaded_csv)
            st.success(f"✅ {len(batch_df)} clients chargés")

            num_cols_all = model_data.get("numerical_cols", model_data["numerical_features"])
            cat_cols_all = model_data.get("categorical_cols", model_data["categorical_features"])
            required_cols = num_cols_all + cat_cols_all
            # Construire le DataFrame avec toutes les colonnes attendues
            batch_full = pd.DataFrame()
            for c in num_cols_all:
                batch_full[c] = batch_df[c] if c in batch_df.columns else 0
            for c in cat_cols_all:
                batch_full[c] = batch_df[c] if c in batch_df.columns else "Inconnu"
            missing = [c for c in ["REVENU_MENSUEL_FCFA","RATIO_ENDETTEMENT","SCORE_INTERNE_BANQUE",
                                   "NB_INCIDENTS_PAIEMENT","JOURS_RETARD_MAX","NB_REJETS_PRELEVEMENT",
                                   "NB_DECOUVERT_12MOIS","ANCIENNETE_CLIENT_MOIS"] if c not in batch_df.columns]
            if missing:
                st.error(f"Colonnes obligatoires manquantes : {missing}")
            else:
                probas = pipeline.predict_proba(batch_full)[:, 1]
                batch_df["PROBABILITE_DEFAUT_%"] = (probas * 100).round(2)
                batch_df["DECISION"] = ["Refusé" if p >= THRESHOLD else "Accordé" for p in probas]
                batch_df["SCORE_1000"] = [(1 - p) * 1000 for p in probas]
                batch_df["SCORE_1000"] = batch_df["SCORE_1000"].round(0).astype(int)

                # Stats résumé
                n_accorde = (batch_df["DECISION"] == "Accordé").sum()
                n_refuse  = (batch_df["DECISION"] == "Refusé").sum()

                c1, c2, c3 = st.columns(3)
                c1.metric("Total clients", len(batch_df))
                c2.metric("✅ Accordés", n_accorde, f"{n_accorde/len(batch_df):.0%}")
                c3.metric("❌ Refusés",  n_refuse,  f"{n_refuse/len(batch_df):.0%}")

                # Affichage tableau avec couleurs
                def color_decision(val):
                    color = "#22C55E" if val == "Accordé" else "#EF4444"
                    return f"color: {color}; font-weight: 700"

                styled = batch_df[["PROBABILITE_DEFAUT_%","DECISION","SCORE_1000"] +
                                   [c for c in batch_df.columns if c not in ["PROBABILITE_DEFAUT_%","DECISION","SCORE_1000"]]
                                 ].style.applymap(color_decision, subset=["DECISION"])
                st.dataframe(styled, use_container_width=True, height=350)

                # Téléchargement résultats
                result_csv = batch_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️  Télécharger les résultats",
                    data=result_csv,
                    file_name="resultats_scoring_lot.csv",
                    mime="text/csv",
                )
        except Exception as e:
            st.error(f"Erreur lors du traitement : {e}")

# ══════════════════════════════════════════════════════════
#  ONGLET 3 — FEATURE IMPORTANCE
# ══════════════════════════════════════════════════════════
with tab_importance:
    st.markdown("""
    <div style="background:#13151C;border:1px solid #1E2028;border-radius:12px;padding:20px 24px;margin-bottom:16px;">
      <div style="display:flex;align-items:center;gap:9px;margin-bottom:6px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C8922A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>
          <line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/>
        </svg>
        <div style="font-size:0.95rem;font-weight:700;color:#E8E9EC;">Importance des Variables — Top 10</div>
      </div>
      <div style="font-size:0.78rem;color:#686D78;">Valeur absolue des coefficients de la Régression Logistique après standardisation. Plus le coefficient est élevé, plus la variable influence la prédiction.</div>
    </div>
    """, unsafe_allow_html=True)

    if "feature_importance" in model_data:
        fi = model_data["feature_importance"]
        fi_df = pd.DataFrame(list(fi.items()), columns=["Variable", "Importance"])
        fi_df = fi_df.sort_values("Importance", ascending=False).head(10).reset_index(drop=True)
        fi_df["Rang"] = fi_df.index + 1
        max_imp = fi_df["Importance"].max()

        labels_fr = {
            "REVENU_MENSUEL_FCFA":    "Revenu mensuel (FCFA)",
            "RATIO_ENDETTEMENT":      "Ratio d'endettement",
            "SCORE_INTERNE_BANQUE":   "Score interne banque",
            "NB_INCIDENTS_PAIEMENT":  "Incidents de paiement",
            "JOURS_RETARD_MAX":       "Retard maximum (jours)",
            "NB_REJETS_PRELEVEMENT":  "Rejets de prélèvement",
            "NB_DECOUVERT_12MOIS":    "Découverts (12 mois)",
            "ANCIENNETE_CLIENT_MOIS": "Ancienneté client",
        }

        colors = ["#C8922A","#E8A93A","#D4A044","#B8863C","#C89A50",
                  "#22C55E","#3B82F6","#A855F7","#EF4444","#F59E0B"]

        html_bars = ""
        for i, row in fi_df.iterrows():
            label = labels_fr.get(row["Variable"], row["Variable"])
            pct   = row["Importance"] / max_imp * 100
            color = colors[i % len(colors)]
            html_bars += f"""
            <div style="margin-bottom:14px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                <span style="font-size:0.8rem;color:#B0B5BE;font-weight:600;">
                  <span style="color:{color};margin-right:8px;">#{row['Rang']}</span>{label}
                </span>
                <span style="font-size:0.78rem;color:{color};font-weight:700;">{row['Importance']:.4f}</span>
              </div>
              <div style="background:#1C1F27;border-radius:6px;height:10px;overflow:hidden;">
                <div style="height:100%;width:{pct:.1f}%;background:linear-gradient(90deg,{color}cc,{color});
                            border-radius:6px;transition:width 0.4s ease;"></div>
              </div>
            </div>"""

        st.markdown(f"""
        <div style="background:#13151C;border:1px solid #1E2028;border-radius:12px;padding:24px 28px;">
          {html_bars}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Réentraînez le modèle avec le nouveau train_model.py pour afficher les importances.")

# ══════════════════════════════════════════════════════════
#  ONGLET 4 — À PROPOS
# ══════════════════════════════════════════════════════════
with tab_about:
    m = model_data["metrics"] if model_data else {}
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px;">
      <div style="background:#13151C;border:1px solid #C8922A33;border-radius:12px;padding:22px 24px;">
        <div style="display:flex;align-items:center;gap:7px;margin-bottom:10px;">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8922A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
          </svg>
          <div style="font-size:0.7rem;color:#686D78;text-transform:uppercase;letter-spacing:1px;">Contexte académique</div>
        </div>
        <div style="font-size:0.85rem;color:#B0B5BE;line-height:1.7;">
          <strong style="color:#E8E9EC;">Institution :</strong> ISM Dakar<br>
          <strong style="color:#E8E9EC;">Filière :</strong> MBA1 Finance Digitale<br>
          <strong style="color:#E8E9EC;">Module :</strong> Modélisation Prédictive & IA en Finance<br>
          <strong style="color:#E8E9EC;">Professeur :</strong> M. Komla Martin CHOKKI<br>
          <strong style="color:#E8E9EC;">Année :</strong> 2025-2026
        </div>
      </div>
      <div style="background:#13151C;border:1px solid #22C55E33;border-radius:12px;padding:22px 24px;">
        <div style="display:flex;align-items:center;gap:7px;margin-bottom:10px;">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>
            <path d="M15.54 8.46a5 5 0 0 1 0 7.07M8.46 8.46a5 5 0 0 0 0 7.07"/>
          </svg>
          <div style="font-size:0.7rem;color:#686D78;text-transform:uppercase;letter-spacing:1px;">Modèle utilisé</div>
        </div>
        <div style="font-size:0.85rem;color:#B0B5BE;line-height:1.7;">
          <strong style="color:#E8E9EC;">Algorithme :</strong> Régression Logistique<br>
          <strong style="color:#E8E9EC;">Librairie :</strong> Scikit-Learn<br>
          <strong style="color:#E8E9EC;">Prétraitement :</strong> StandardScaler + OneHotEncoder<br>
          <strong style="color:#E8E9EC;">Déséquilibre :</strong> class_weight='balanced'<br>
          <strong style="color:#E8E9EC;">Dataset :</strong> 900 000 observations, 47 variables
        </div>
      </div>
    </div>

    <div style="background:#13151C;border:1px solid #3B82F633;border-radius:12px;padding:22px 24px;margin-bottom:14px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#C8922A" stroke-width="2">
          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
        </svg>
        <div style="font-size:0.7rem;color:#686D78;text-transform:uppercase;letter-spacing:1px;">Performances du modèle sur le jeu de test (20%)</div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;">
        <div style="text-align:center;padding:16px 10px;background:linear-gradient(145deg,#0d2918,#0a1f12);border-radius:12px;border:1px solid #22C55E33;position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#22C55E,transparent);"></div>
          <div style="font-size:1.6rem;font-weight:900;color:#22C55E;letter-spacing:-1px;">{m.get('auc',0):.4f}</div>
          <div style="font-size:0.6rem;color:#22C55E;opacity:0.7;margin-top:4px;text-transform:uppercase;letter-spacing:1px;">AUC-ROC</div>
          <div style="font-size:0.55rem;color:#3A3F4A;margin-top:3px;">Excellent</div>
        </div>
        <div style="text-align:center;padding:16px 10px;background:linear-gradient(145deg,#1a1000,#130c00);border-radius:12px;border:1px solid #C8922A33;position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#C8922A,transparent);"></div>
          <div style="font-size:1.6rem;font-weight:900;color:#C8922A;letter-spacing:-1px;">{m.get('f1',0):.4f}</div>
          <div style="font-size:0.6rem;color:#C8922A;opacity:0.7;margin-top:4px;text-transform:uppercase;letter-spacing:1px;">F1-Score</div>
          <div style="font-size:0.55rem;color:#3A3F4A;margin-top:3px;">Équilibré</div>
        </div>
        <div style="text-align:center;padding:16px 10px;background:linear-gradient(145deg,#0a1628,#081020);border-radius:12px;border:1px solid #3B82F633;position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#3B82F6,transparent);"></div>
          <div style="font-size:1.6rem;font-weight:900;color:#3B82F6;letter-spacing:-1px;">{m.get('precision',0):.4f}</div>
          <div style="font-size:0.6rem;color:#3B82F6;opacity:0.7;margin-top:4px;text-transform:uppercase;letter-spacing:1px;">Précision</div>
          <div style="font-size:0.55rem;color:#3A3F4A;margin-top:3px;">Fiable</div>
        </div>
        <div style="text-align:center;padding:16px 10px;background:linear-gradient(145deg,#160a28,#100720);border-radius:12px;border:1px solid #A855F733;position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#A855F7,transparent);"></div>
          <div style="font-size:1.6rem;font-weight:900;color:#A855F7;letter-spacing:-1px;">{m.get('recall',0):.4f}</div>
          <div style="font-size:0.6rem;color:#A855F7;opacity:0.7;margin-top:4px;text-transform:uppercase;letter-spacing:1px;">Rappel</div>
          <div style="font-size:0.55rem;color:#3A3F4A;margin-top:3px;">Sensible</div>
        </div>
      </div>
    </div>

    <div style="background:#13151C;border:1px solid #1E2028;border-radius:12px;padding:22px 24px;">
      <div style="display:flex;align-items:center;gap:7px;margin-bottom:12px;">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        <line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/>
      </svg>
      <div style="font-size:0.7rem;color:#686D78;text-transform:uppercase;letter-spacing:1px;">Pourquoi la Régression Logistique ?</div>
    </div>
      <div style="font-size:0.82rem;color:#B0B5BE;line-height:1.8;">
        La Régression Logistique est l'algorithme de référence en scoring crédit bancaire pour plusieurs raisons :
        <br><br>
        <span style="color:#C8922A;font-weight:600;">① Interprétabilité :</span> Chaque coefficient est directement lisible et justifiable auprès d'un régulateur (Bâle III).<br>
        <span style="color:#22C55E;font-weight:600;">② Performance :</span> Avec un AUC de {m.get('auc',0):.4f}, elle capture l'essentiel de la relation risque-défaut.<br>
        <span style="color:#3B82F6;font-weight:600;">③ Rapidité :</span> Entraînement et inférence quasi-instantanés sur 900 000 observations.<br>
        <span style="color:#A855F7;font-weight:600;">④ Standard industrie :</span> Utilisée par la quasi-totalité des banques africaines pour le scoring réglementaire.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  ONGLET 1 — FORMULAIRE SCORING (contenu existant)
# ══════════════════════════════════════════════════════════
with tab_scoring:

    with st.form("scoring_form"):
    
        # ── Section 1 : Identification ──
        st.markdown(f"""
        <div class="section-header">
            <div class="section-icon blue">{icon_user()}</div>
            <div class="section-title-text">Identification du Client</div>
        </div>
        """, unsafe_allow_html=True)
    
        nom_client = st.text_input(
            "Référence Client",
            value="CLI-2025-001",
            placeholder="ex. CLI-2025-001",
            help="Identifiant interne pour l'historique de session"
        )
    
        st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)
    
        # ── Section 2 : Profil Financier ──
        st.markdown(f"""
        <div class="section-header">
            <div class="section-icon gold">{icon_money()}</div>
            <div class="section-title-text">Profil Financier & Comportement Bancaire</div>
        </div>
        """, unsafe_allow_html=True)
    
        # ── Ligne 1 : 4 variables numériques ──
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            revenu = st.number_input(
                "Revenu Mensuel (FCFA)",
                min_value=0, max_value=10_000_000, value=350_000, step=10_000,
                help="Revenu mensuel brut déclaré du client")
        with c2:
            ratio_endettement = st.number_input(
                "Ratio d'Endettement",
                min_value=0.0, max_value=1.0, value=0.35, step=0.01, format="%.2f",
                help="Part du revenu mensuel consacrée aux remboursements (0 à 1)")
        with c3:
            score_interne = st.number_input(
                "Score Interne Banque",
                min_value=0, max_value=1000, value=500, step=10,
                help="Score de risque calculé en interne (0 = très risqué, 1000 = excellent)")
        with c4:
            nb_incidents = st.number_input(
                "Incidents de Paiement",
                min_value=0, max_value=50, value=0, step=1,
                help="Nombre total d'incidents de paiement dans l'historique")
    
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    
        # ── Ligne 2 : 4 variables numériques ──
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            jours_retard = st.number_input(
                "Retard Maximum (jours)",
                min_value=0, max_value=365, value=0, step=1,
                help="Nombre maximal de jours de retard observé sur un crédit")
        with c6:
            nb_rejets = st.number_input(
                "Rejets de Prélèvement",
                min_value=0, max_value=50, value=0, step=1,
                help="Nombre de prélèvements automatiques rejetés faute de provision")
        with c7:
            nb_decouvert = st.number_input(
                "Découverts (12 mois)",
                min_value=0, max_value=30, value=0, step=1,
                help="Nombre de fois en situation de découvert sur les 12 derniers mois")
        with c8:
            anciennete = st.number_input(
                "Ancienneté Client (mois)",
                min_value=0, max_value=360, value=24, step=1,
                help="Durée de la relation bancaire en mois")
    
        st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)
    
        # ── Section 3 : Profil Pro & Garanties ──
        st.markdown(f"""
        <div class="section-header">
            <div class="section-icon slate">{icon_briefcase()}</div>
            <div class="section-title-text">Profil Professionnel & Garanties — Variables 9 &amp; 10</div>
        </div>
        """, unsafe_allow_html=True)
    
        c9, c10 = st.columns(2)
        with c9:
            st.markdown("<p style='font-size:0.72rem;font-weight:700;color:#8B909A;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;'>Type d'Emploi</p>", unsafe_allow_html=True)
            type_emploi = st.radio(
                "Type d'Emploi",
                options=["CDI", "Fonctionnaire", "CDD", "Indépendant", "Entrepreneur", "Retraité", "Sans emploi"],
                horizontal=True,
                label_visibility="collapsed",
                key="type_emploi_radio"
            )
        with c10:
            st.markdown("<p style='font-size:0.72rem;font-weight:700;color:#8B909A;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;'>Garantie Apportée</p>", unsafe_allow_html=True)
            garantie = st.radio(
                "Garantie Apportée",
                options=["Hypothèque", "Assurance", "Caution", "Nantissement", "Aucune"],
                horizontal=True,
                label_visibility="collapsed",
                key="garantie_radio"
            )
    
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "  ANALYSER LE RISQUE DE CRÉDIT",
            use_container_width=True
        )
    
    # ═══════════════════════════════════════════════════════════
    #  RÉSULTATS
    # ═══════════════════════════════════════════════════════════
    def score_from_proba(p): return int(round((1 - p) * 1000))
    
    def badge_score(s):
        if s >= 700: return "faible", "Risque Faible"
        elif s >= 400: return "modere", "Risque Modéré"
        else: return "eleve", "Risque Élevé"
    
    def gauge_color(s):
        if s >= 700: return "linear-gradient(90deg, #15803D, #22C55E)"
        elif s >= 400: return "linear-gradient(90deg, #B45309, #F59E0B)"
        else: return "linear-gradient(90deg, #991B1B, #EF4444)"
    
    if submitted:
        # Données saisies dans l'interface (10 variables clés)
        input_saisie = {
            "REVENU_MENSUEL_FCFA":    revenu,
            "RATIO_ENDETTEMENT":      ratio_endettement,
            "SCORE_INTERNE_BANQUE":   score_interne,
            "NB_INCIDENTS_PAIEMENT":  nb_incidents,
            "JOURS_RETARD_MAX":       jours_retard,
            "NB_REJETS_PRELEVEMENT":  nb_rejets,
            "NB_DECOUVERT_12MOIS":    nb_decouvert,
            "ANCIENNETE_CLIENT_MOIS": anciennete,
            "TYPE_EMPLOI":            type_emploi,
            "GARANTIE":               garantie,
        }
        # Construction du DataFrame complet pour le pipeline
        # (le modèle a été entraîné sur toutes les colonnes du dataset)
        num_cols_all = model_data.get("numerical_cols", model_data["numerical_features"])
        cat_cols_all = model_data.get("categorical_cols", model_data["categorical_features"])
        row = {}
        for c in num_cols_all:
            row[c] = input_saisie.get(c, 0)   # 0 pour les colonnes non saisies
        for c in cat_cols_all:
            row[c] = input_saisie.get(c, "Inconnu")
        input_df = pd.DataFrame([row])

        proba    = pipeline.predict_proba(input_df)[0][1]
        decision = "Refusé" if proba >= THRESHOLD else "Accordé"
        score    = score_from_proba(proba)
        proba_p  = proba * 100
        badge_cls, badge_lbl = badge_score(score)
        g_color  = gauge_color(score)
        p_color  = "#EF4444" if proba >= THRESHOLD else "#22C55E"
    
        st.session_state.historique.append({
            "nom": nom_client, "score": score,
            "proba": proba_p, "decision": decision,
        })
    
        # ── Ligne de résultats ──
        st.markdown("<br>", unsafe_allow_html=True)
    
        r1, r2, r3 = st.columns([1.1, 0.95, 0.95])
    
        with r1:
            is_ok = decision == "Accordé"
            banner_cls = "accord" if is_ok else "refuse"
            d_icon = "✓" if is_ok else "✕"
            d_label = "DÉCISION CRÉDIT"
            d_msg = ("Dossier validé — le profil de risque est acceptable." if is_ok
                     else "Dossier refusé — risque de défaut trop élevé.")
            st.markdown(f"""
            <div class="result-banner {banner_cls}">
                <div class="result-icon">{d_icon}</div>
                <div class="result-label {banner_cls}">{d_label}</div>
                <div class="result-decision {banner_cls}">Crédit {decision.upper()}</div>
                <div class="result-msg {banner_cls}">{d_msg}</div>
            </div>
            """, unsafe_allow_html=True)
    
        with r2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Score de Risque</div>
                <div class="kpi-value" style="color:{p_color if score < 400 else ('#F59E0B' if score < 700 else '#22C55E')};">{score}</div>
                <div class="kpi-sub">sur 1 000 points</div>
                <div class="kpi-badge {badge_cls}">{badge_lbl}</div>
            </div>
            """, unsafe_allow_html=True)
    
        with r3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Probabilité de Défaut</div>
                <div class="kpi-value" style="color:{p_color};">{proba_p:.1f}<span style="font-size:1.4rem;">%</span></div>
                <div class="kpi-sub">seuil de décision : {int(THRESHOLD*100)}%</div>
                <div class="kpi-badge {'eleve' if proba >= THRESHOLD else 'faible'}">{'Au-dessus' if proba >= THRESHOLD else 'En-dessous'} du seuil</div>
            </div>
            """, unsafe_allow_html=True)
    
        # ── Jauge ──
        bar_w = score / 10
        st.markdown(f"""
        <div class="gauge-wrap">
            <div class="gauge-title">
                <span>Jauge de Risque — Score sur 1000</span>
                <span style="color:#C8CDD6; font-weight:700;">{score} / 1000</span>
            </div>
            <div class="gauge-track">
                <div class="gauge-fill" style="width:{bar_w}%; background:{g_color};"></div>
            </div>
            <div class="gauge-ticks">
                <span class="gauge-tick">0</span>
                <span class="gauge-tick {'active' if score >= 400 else ''}">▲ 400</span>
                <span class="gauge-tick {'active' if score >= 700 else ''}">▲ 700</span>
                <span class="gauge-tick active">1000</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
        # ── Récapitulatif ──
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("Récapitulatif des données saisies", expanded=False):
            rows = [
                ("Référence client",      nom_client),
                ("Revenu mensuel",        f"{revenu:,} FCFA"),
                ("Ratio d'endettement",   f"{ratio_endettement:.2f}  ({ratio_endettement*100:.0f}%)"),
                ("Score interne banque",  str(score_interne)),
                ("Incidents de paiement", str(nb_incidents)),
                ("Retard maximum",        f"{jours_retard} jours"),
                ("Rejets prélèvement",    str(nb_rejets)),
                ("Découverts (12 mois)",  str(nb_decouvert)),
                ("Ancienneté client",     f"{anciennete} mois"),
                ("Type d'emploi",         type_emploi),
                ("Garantie",              garantie),
            ]
            html = ""
            for k, v in rows:
                html += f'<div class="recap-row"><span class="recap-key">{k}</span><span class="recap-val">{v}</span></div>'
            st.markdown(f'<div style="background:#111318;border:1px solid #1E2028;border-radius:10px;padding:0.75rem 1rem;">{html}</div>', unsafe_allow_html=True)
    

# ── Footer ──
st.markdown("""
<div class="app-footer">
    <span class="footer-text">ISM Dakar · MBA1 Finance Digitale 2025-2026</span>
    <span class="footer-sep">|</span>
    <span class="footer-text">Prof. M. Komla Martin CHOKKI</span>
    <span class="footer-sep">|</span>
    <span class="footer-text">Outil d'aide à la décision — usage professionnel uniquement</span>
</div>
""", unsafe_allow_html=True)
