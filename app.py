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

# ═══════════════════════════════════════════════════════════
#  SIDEBAR TOGGLE — FIX JAVASCRIPT
# ═══════════════════════════════════════════════════════════
# Sidebar toggle via components.html (seule méthode qui exécute vraiment le JS)
components.html("""
<script>
(function() {
    function fixSidebarToggle() {
        var toggleBtn = document.querySelector('[data-testid="stSidebarCollapsedControl"]');

        if (toggleBtn) {
            toggleBtn.style.cssText = [
                "display:flex!important",
                "visibility:visible!important",
                "opacity:1!important",
                "z-index:99999!important",
                "position:fixed!important",
                "left:0",
                "top:50%",
                "transform:translateY(-50%)",
                "background:#1C1F27",
                "border:1px solid #C8922A88",
                "border-left:none",
                "border-radius:0 8px 8px 0",
                "padding:8px 6px",
                "cursor:pointer",
                "box-shadow:3px 0 12px rgba(0,0,0,0.5)"
            ].join(";");
            toggleBtn.querySelectorAll("svg").forEach(function(s){
                s.style.color="#C8922A"; s.style.fill="#C8922A"; s.style.stroke="#C8922A";
            });
        } else {
            // Créer bouton custom si natif absent
            if (window.top.document.getElementById("__csb__")) return;
            var btn = window.top.document.createElement("button");
            btn.id = "__csb__";
            btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C8922A" stroke-width="2.5" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>';
            btn.style.cssText = [
                "position:fixed","left:0","top:50%","transform:translateY(-50%)",
                "z-index:99999","background:#1C1F27",
                "border:1px solid #C8922A88","border-left:none",
                "border-radius:0 8px 8px 0","padding:10px 8px","cursor:pointer",
                "box-shadow:3px 0 12px rgba(0,0,0,0.5)",
                "display:flex","align-items:center","justify-content:center"
            ].join(";");
            btn.onclick = function() {
                var nb = window.top.document.querySelector('[data-testid="stSidebarCollapsedControl"] button');
                if (nb) { nb.click(); return; }
                window.top.document.querySelectorAll("button").forEach(function(b){
                    var a = b.getAttribute("aria-label")||"";
                    if(a.toLowerCase().includes("sidebar")||a.toLowerCase().includes("navigation")) b.click();
                });
            };
            btn.onmouseenter = function(){ btn.style.background="#C8922A22"; btn.style.borderColor="#C8922A"; };
            btn.onmouseleave = function(){ btn.style.background="#1C1F27";   btn.style.borderColor="#C8922A88"; };
            window.top.document.body.appendChild(btn);
        }
    }

    // Observer DOM parent (Streamlit tourne dans un iframe)
    var target = window.top ? window.top.document.body : document.body;
    new MutationObserver(fixSidebarToggle).observe(target, {childList:true, subtree:true});
    setInterval(fixSidebarToggle, 600);
    fixSidebarToggle();
})();
</script>
""", height=0, scrolling=False)

# ═══════════════════════════════════════════════════════════
#  SVG ICONS
# ═══════════════════════════════════════════════════════════
def icon_bank():
    return """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#C8922A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/>
  <line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/>
  <line x1="18" y1="18" x2="18" y2="11"/>
  <polygon points="12 2 20 7 4 7"/></svg>"""

def icon_chart():
    return """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>
  <line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/></svg>"""

def icon_target():
    return """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>"""

def icon_zap():
    return """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>"""

def icon_award():
    return """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/></svg>"""

def icon_user():
    return """<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#C8922A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
  <circle cx="12" cy="7" r="4"/></svg>"""

def icon_money():
    return """<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#C8922A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="5" width="20" height="14" rx="2"/>
  <line x1="2" y1="10" x2="22" y2="10"/></svg>"""

def icon_briefcase():
    return """<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#C8922A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="7" width="20" height="14" rx="2"/>
  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
  <line x1="2" y1="12" x2="22" y2="12"/></svg>"""

def icon_history():
    return """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="1 4 1 10 7 10"/>
  <path d="M3.51 15a9 9 0 1 0 .49-4.54"/></svg>"""

def icon_info():
    return """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="12" y1="16" x2="12" y2="12"/>
  <line x1="12" y1="8" x2="12.01" y2="8"/></svg>"""

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
        data["threshold"] = 0.76
    return data

# Force rechargement si version du modèle a changé
if "model_version" not in st.session_state:
    load_model.clear()
    st.session_state["model_version"] = "v2_threshold076"

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
                    <span style="color:#C8922A; font-weight:600;">Seuil décision :</span> 76% de probabilité de défaut.<br>
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
THRESHOLD            = model_data.get("threshold", 0.76)  # Seuil optimisé

# ═══════════════════════════════════════════════════════════
#  TOPBAR
# ═══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="topbar">
    <div class="topbar-left">
        <div class="topbar-icon">{icon_bank()}</div>
        <div>
            <div class="topbar-title">Système d'Analyse de Risque Crédit</div>
            <div class="topbar-sub">Régression Logistique · Pipeline Scikit-Learn · {len(all_features)} features</div>
        </div>
    </div>
    <div class="topbar-right">
        <div class="topbar-badge green" id="badge-modele-actif" style="cursor:pointer;" title="Voir les performances du modèle">● Modèle Actif</div>
        <div class="topbar-badge" id="badge-auc" style="cursor:pointer;" title="Voir les performances du modèle">AUC {model_data['metrics']['auc']:.4f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  MODALE PERFORMANCES — via components.html (JS réellement exécuté)
# ═══════════════════════════════════════════════════════════
_auc       = f"{model_data['metrics']['auc']:.4f}"
_f1        = f"{model_data['metrics']['f1']:.4f}"
_precision = f"{model_data['metrics']['precision']:.4f}"
_recall    = f"{model_data['metrics']['recall']:.4f}"
_threshold = f"{THRESHOLD*100:.0f}"

components.html(f"""
<script>
(function() {{
  // ── Créer la modale dans le document PARENT (Streamlit) ──
  var doc = window.parent.document;

  // Supprimer ancienne modale si elle existe déjà (rechargement Streamlit)
  var existing = doc.getElementById("__perf_modal__");
  if (existing) existing.remove();

  // ── HTML de la modale ──
  var modal = doc.createElement("div");
  modal.id = "__perf_modal__";
  modal.style.cssText = [
    "display:none","position:fixed","inset:0","z-index:999999",
    "background:rgba(0,0,0,0.78)","align-items:center","justify-content:center"
  ].join(";");

  modal.innerHTML = `
    <div style="background:#13151C;border:1px solid rgba(200,146,42,0.27);border-radius:14px;
                padding:28px 32px;max-width:520px;width:92%;
                box-shadow:0 20px 60px rgba(0,0,0,0.7);position:relative;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
        <div>
          <div style="font-size:1rem;font-weight:800;color:#E8E9EC;">Performances du Modèle</div>
          <div style="font-size:0.72rem;color:#686D78;margin-top:3px;">Régression Logistique · Pipeline Scikit-Learn</div>
        </div>
        <button id="__perf_close__"
          style="background:none;border:none;color:#686D78;font-size:1.4rem;
                 cursor:pointer;line-height:1;padding:4px 8px;border-radius:6px;">✕</button>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px;">
        <div style="background:#1C1F27;border:1px solid rgba(34,197,94,0.2);border-radius:10px;padding:14px 16px;">
          <div style="font-size:0.68rem;color:#686D78;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px;">AUC-ROC</div>
          <div style="font-size:1.55rem;font-weight:800;color:#22C55E;">{_auc}</div>
          <div style="font-size:0.65rem;color:#22C55E;margin-top:3px;">Excellent discriminant</div>
        </div>
        <div style="background:#1C1F27;border:1px solid rgba(200,146,42,0.2);border-radius:10px;padding:14px 16px;">
          <div style="font-size:0.68rem;color:#686D78;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px;">F1-Score</div>
          <div style="font-size:1.55rem;font-weight:800;color:#C8922A;">{_f1}</div>
          <div style="font-size:0.65rem;color:#C8922A;margin-top:3px;">Équilibre précision/rappel</div>
        </div>
        <div style="background:#1C1F27;border:1px solid rgba(59,130,246,0.2);border-radius:10px;padding:14px 16px;">
          <div style="font-size:0.68rem;color:#686D78;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px;">Précision</div>
          <div style="font-size:1.55rem;font-weight:800;color:#3B82F6;">{_precision}</div>
          <div style="font-size:0.65rem;color:#3B82F6;margin-top:3px;">Vrais positifs / prédits positifs</div>
        </div>
        <div style="background:#1C1F27;border:1px solid rgba(168,85,247,0.2);border-radius:10px;padding:14px 16px;">
          <div style="font-size:0.68rem;color:#686D78;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px;">Rappel Défaut</div>
          <div style="font-size:1.55rem;font-weight:800;color:#A855F7;">{_recall}</div>
          <div style="font-size:0.65rem;color:#A855F7;margin-top:3px;">Détection des mauvais payeurs</div>
        </div>
      </div>
      <div style="background:#1C1F27;border:1px solid #1E2028;border-radius:10px;
                  padding:12px 16px;display:flex;align-items:center;justify-content:space-between;">
        <div style="font-size:0.78rem;color:#B0B5BE;">Seuil de décision optimisé</div>
        <div style="font-size:0.92rem;font-weight:700;color:#EF4444;">{_threshold}% probabilité de défaut</div>
      </div>
      <div style="margin-top:14px;font-size:0.68rem;color:#3A3F4A;text-align:center;">
        ISM Dakar · MBA1 Finance Digitale · Cliquez en dehors pour fermer
      </div>
    </div>`;

  doc.body.appendChild(modal);

  // ── Fonctions open / close ──
  function openModal()  {{ modal.style.display = "flex"; }}
  function closeModal() {{ modal.style.display = "none"; }}

  // Fermer en cliquant sur le fond
  modal.addEventListener("click", function(e) {{ if (e.target === modal) closeModal(); }});

  // Bouton ✕
  doc.getElementById("__perf_close__").addEventListener("click", closeModal);

  // ── Brancher les badges dans le DOM parent ──
  function attachBadges() {{
    var b1 = doc.getElementById("badge-modele-actif");
    var b2 = doc.getElementById("badge-auc");
    if (b1) {{ b1.addEventListener("click", openModal); b1.style.cursor = "pointer"; }}
    if (b2) {{ b2.addEventListener("click", openModal); b2.style.cursor = "pointer"; }}
    if (!b1 || !b2) setTimeout(attachBadges, 200);
  }}
  attachBadges();
}})();
</script>
""", height=0, scrolling=False)

# ═══════════════════════════════════════════════════════════
#  FORMULAIRE
# ═══════════════════════════════════════════════════════════
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
    input_df = pd.DataFrame([{
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
    }])

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
            <div class="kpi-sub">seuil de décision : 76%</div>
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
