"""
app.py — Application de Scoring Crédit
MBA1 Finance Digitale — ISM Dakar 2025-2026

Interface Streamlit permettant à un conseiller bancaire de saisir
les informations d'un client et d'obtenir instantanément :
  - La probabilité de défaut (en %)
  - La décision crédit (Accordé / Refusé)
  - Un score de risque sur 1000 points

Usage :
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ─────────────────────────────────────────────
# CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Scoring Crédit — ISM Dakar",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS PERSONNALISÉ — COULEURS ISM (Marron & Or)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Variables de couleurs ISM */
    :root {
        --ism-marron: #5C2E00;
        --ism-or:     #C8922A;
        --ism-or-clair: #F0D090;
        --vert:       #1A7F3C;
        --rouge:      #C0392B;
    }

    /* En-tête principal */
    .main-header {
        background: linear-gradient(135deg, var(--ism-marron) 0%, #8B4513 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
        border-left: 6px solid var(--ism-or);
    }
    .main-header h1 { color: var(--ism-or); margin: 0; font-size: 1.8rem; }
    .main-header p  { color: #F5E6C8; margin: 0.3rem 0 0 0; font-size: 0.95rem; }

    /* Carte de résultat — Accordé */
    .result-accord {
        background: linear-gradient(135deg, #0D4F2A, #1A7F3C);
        border: 2px solid #27AE60;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: white;
    }
    /* Carte de résultat — Refusé */
    .result-refuse {
        background: linear-gradient(135deg, #6B1A1A, #C0392B);
        border: 2px solid #E74C3C;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: white;
    }
    .result-title  { font-size: 2rem; font-weight: 700; margin: 0; }
    .result-sub    { font-size: 1rem; opacity: 0.85; margin-top: 0.3rem; }

    /* Score badge */
    .score-badge {
        background: var(--ism-marron);
        border: 3px solid var(--ism-or);
        border-radius: 50%;
        width: 130px; height: 130px;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        margin: 0 auto 1rem auto;
    }
    .score-number { color: var(--ism-or); font-size: 2.2rem; font-weight: 800; line-height: 1; }
    .score-label  { color: #F5E6C8; font-size: 0.7rem; letter-spacing: 1px; }

    /* Section formulaire */
    .section-title {
        color: var(--ism-marron);
        font-size: 1rem;
        font-weight: 700;
        border-bottom: 2px solid var(--ism-or);
        padding-bottom: 4px;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Bouton principal */
    .stButton > button {
        background: linear-gradient(135deg, var(--ism-marron), #8B4513) !important;
        color: var(--ism-or) !important;
        border: 2px solid var(--ism-or) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 0.6rem 2rem !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: var(--ism-or) !important;
        color: var(--ism-marron) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F5E6C8 0%, #FAF3E0 100%);
    }
    [data-testid="stSidebar"] .sidebar-title {
        color: var(--ism-marron);
        font-weight: 700;
        font-size: 1rem;
        border-bottom: 2px solid var(--ism-or);
        padding-bottom: 4px;
        margin-bottom: 0.5rem;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #FFF8EC;
        border: 1px solid #E8C97A;
        border-radius: 8px;
        padding: 0.5rem;
    }

    /* Historique */
    .history-item {
        background: #FFF8EC;
        border-left: 4px solid var(--ism-or);
        border-radius: 0 8px 8px 0;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.4rem;
        font-size: 0.85rem;
    }
    .history-accord { border-left-color: #27AE60; }
    .history-refuse { border-left-color: #E74C3C; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHARGEMENT DU MODÈLE
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    """Charge le modèle depuis le fichier .pkl (mis en cache)."""
    model_path = "credit_scoring_model.pkl"
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

model_data = load_model()

# ─────────────────────────────────────────────
# INITIALISATION SESSION STATE
# ─────────────────────────────────────────────
if "historique" not in st.session_state:
    st.session_state.historique = []

# ─────────────────────────────────────────────
# EN-TÊTE
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏦 Système de Scoring Crédit</h1>
    <p>MBA1 Finance Digitale — ISM Dakar | Modèle de Régression Logistique (AUC ≈ 0.9999)</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ALERTE SI MODÈLE MANQUANT
# ─────────────────────────────────────────────
if model_data is None:
    st.error("""
    ⚠️ **Modèle introuvable** — Le fichier `credit_scoring_model.pkl` est absent.

    **Solution :** Exécutez d'abord le script d'entraînement :
    ```bash
    python train_model.py
    ```
    """)
    st.stop()

pipeline            = model_data["pipeline"]
numerical_features  = model_data["numerical_features"]
categorical_features = model_data["categorical_features"]
all_features        = model_data["all_features"]
metrics             = model_data["metrics"]

# ─────────────────────────────────────────────
# SIDEBAR — À PROPOS DU MODÈLE
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">📊 Performance du Modèle</div>', unsafe_allow_html=True)
    st.metric("AUC-ROC",       f"{metrics['auc']:.4f}")
    st.metric("Rappel (Défaut)", f"{metrics['recall']:.4f}")
    st.metric("Précision",     f"{metrics['precision']:.4f}")
    st.metric("F1-Score",      f"{metrics['f1']:.4f}")

    st.markdown("---")
    st.markdown('<div class="sidebar-title">📖 À Propos</div>', unsafe_allow_html=True)
    st.markdown(f"""
    **Modèle :** Régression Logistique  
    **Algorithme :** `class_weight='balanced'`  
    **Features :** {len(all_features)} variables  
    **Dataset :** {model_data.get('dataset_rows', '900 000'):,} clients  
    **Prétraitement :** StandardScaler + OneHotEncoder  

    ---
    **Interprétation du Score :**
    - 🟢 **700 – 1000** : Risque faible
    - 🟡 **400 – 699** : Risque modéré
    - 🔴 **0 – 399** : Risque élevé

    ---
    **Seuil de décision :** 50%  
    Au-delà de 50% de probabilité de défaut → Crédit **Refusé**
    """)

    st.markdown("---")
    # Historique des prédictions
    st.markdown('<div class="sidebar-title">🗂 Historique de Session</div>', unsafe_allow_html=True)
    if not st.session_state.historique:
        st.caption("Aucune prédiction encore effectuée.")
    else:
        for h in reversed(st.session_state.historique[-10:]):
            css_class = "history-accord" if h["decision"] == "Accordé" else "history-refuse"
            icon = "✅" if h["decision"] == "Accordé" else "❌"
            st.markdown(
                f'<div class="history-item {css_class}">'
                f'{icon} <b>{h["nom"]}</b> — Score : <b>{h["score"]}/1000</b><br>'
                f'<small>Proba défaut : {h["proba"]:.1f}%</small>'
                f'</div>',
                unsafe_allow_html=True,
            )
        if st.button("🗑 Effacer l'historique"):
            st.session_state.historique = []
            st.rerun()

# ─────────────────────────────────────────────
# FORMULAIRE DE SAISIE — 3 COLONNES
# ─────────────────────────────────────────────
st.markdown("### 📝 Informations du Client")

with st.form("prediction_form"):
    # — Ligne 1 : Identification —
    st.markdown('<div class="section-title">🪪 Identification</div>', unsafe_allow_html=True)
    col_id1, col_id2 = st.columns([1, 3])
    with col_id1:
        nom_client = st.text_input("Nom du client (référence)", value="Client_001",
                                   help="Identifiant interne pour l'historique")
    st.markdown("---")

    # — Ligne 2 : Profil financier —
    st.markdown('<div class="section-title">💰 Profil Financier</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        revenu = st.number_input(
            "Revenu mensuel (FCFA)",
            min_value=0, max_value=10_000_000,
            value=350_000, step=10_000,
            help="Revenu mensuel brut déclaré du client"
        )
        ratio_endettement = st.number_input(
            "Ratio d'endettement",
            min_value=0.0, max_value=1.0,
            value=0.35, step=0.01, format="%.2f",
            help="Part du revenu mensuel consacrée aux remboursements (0 à 1)"
        )
        score_interne = st.number_input(
            "Score interne banque",
            min_value=0, max_value=1000,
            value=500, step=10,
            help="Score de risque calculé en interne par la banque (0-1000)"
        )

    with col2:
        nb_incidents = st.number_input(
            "Nombre d'incidents de paiement",
            min_value=0, max_value=50,
            value=0, step=1,
            help="Total des incidents de paiement dans l'historique crédit"
        )
        jours_retard = st.number_input(
            "Retard maximum (jours)",
            min_value=0, max_value=365,
            value=0, step=1,
            help="Nombre maximum de jours de retard observé"
        )
        nb_rejets = st.number_input(
            "Rejets de prélèvement",
            min_value=0, max_value=50,
            value=0, step=1,
            help="Nombre de prélèvements automatiques rejetés"
        )

    with col3:
        nb_decouvert = st.number_input(
            "Découverts (12 derniers mois)",
            min_value=0, max_value=30,
            value=0, step=1,
            help="Nombre de fois en découvert au cours des 12 derniers mois"
        )
        anciennete = st.number_input(
            "Ancienneté client (mois)",
            min_value=0, max_value=360,
            value=24, step=1,
            help="Durée de la relation bancaire en mois"
        )

    st.markdown("---")

    # — Ligne 3 : Informations qualitatives —
    st.markdown('<div class="section-title">🗂 Profil Professionnel & Garanties</div>',
                unsafe_allow_html=True)
    col4, col5 = st.columns(2)

    with col4:
        type_emploi = st.selectbox(
            "Type d'emploi",
            options=["CDI", "Fonctionnaire", "CDD", "Indépendant", "Entrepreneur", "Retraité", "Sans emploi"],
            index=0,
            help="Nature du contrat de travail ou statut professionnel"
        )

    with col5:
        garantie = st.selectbox(
            "Type de garantie",
            options=["Hypothèque", "Assurance", "Caution", "Nantissement", "Aucune"],
            index=0,
            help="Garantie apportée par le client pour le crédit"
        )

    st.markdown("---")

    # Bouton de prédiction
    submitted = st.form_submit_button("🔍 Prédire le Risque de Défaut", use_container_width=True)

# ─────────────────────────────────────────────
# CALCUL ET AFFICHAGE DE LA PRÉDICTION
# ─────────────────────────────────────────────
def calculer_score(proba_defaut: float) -> int:
    """
    Convertit la probabilité de défaut en score sur 1000.
    Score élevé = client fiable (faible risque de défaut).
    """
    return int(round((1 - proba_defaut) * 1000))


def get_score_color(score: int) -> str:
    if score >= 700:
        return "#27AE60"   # Vert
    elif score >= 400:
        return "#F39C12"   # Orange
    else:
        return "#C0392B"   # Rouge


def get_score_label(score: int) -> str:
    if score >= 700:
        return "✅ Risque FAIBLE"
    elif score >= 400:
        return "⚠️ Risque MODÉRÉ"
    else:
        return "❌ Risque ÉLEVÉ"


if submitted:
    # Construction du vecteur d'entrée
    input_data = pd.DataFrame([{
        "REVENU_MENSUEL_FCFA":   revenu,
        "RATIO_ENDETTEMENT":     ratio_endettement,
        "SCORE_INTERNE_BANQUE":  score_interne,
        "NB_INCIDENTS_PAIEMENT": nb_incidents,
        "JOURS_RETARD_MAX":      jours_retard,
        "NB_REJETS_PRELEVEMENT": nb_rejets,
        "NB_DECOUVERT_12MOIS":   nb_decouvert,
        "ANCIENNETE_CLIENT_MOIS": anciennete,
        "TYPE_EMPLOI":           type_emploi,
        "GARANTIE":              garantie,
    }])

    # Prédiction
    proba_defaut = pipeline.predict_proba(input_data)[0][1]
    decision     = "Refusé" if proba_defaut >= 0.50 else "Accordé"
    score        = calculer_score(proba_defaut)

    # Sauvegarde dans l'historique de session
    st.session_state.historique.append({
        "nom":      nom_client,
        "score":    score,
        "proba":    proba_defaut * 100,
        "decision": decision,
    })

    # ── Affichage des résultats ──
    st.markdown("---")
    st.markdown("### 📊 Résultats de l'Analyse")

    # Colonnes résultat
    res_col1, res_col2, res_col3 = st.columns([1.2, 1, 1])

    # — Décision principale —
    with res_col1:
        css_class = "result-accord" if decision == "Accordé" else "result-refuse"
        icon       = "✅" if decision == "Accordé" else "❌"
        msg        = ("Dossier favorable — le risque de défaut est acceptable."
                      if decision == "Accordé"
                      else "Dossier défavorable — le risque de défaut est trop élevé.")
        st.markdown(f"""
        <div class="{css_class}">
            <div class="result-title">{icon} Crédit {decision.upper()}</div>
            <div class="result-sub">{msg}</div>
        </div>
        """, unsafe_allow_html=True)

    # — Score sur 1000 —
    with res_col2:
        color = get_score_color(score)
        label = get_score_label(score)
        st.markdown(f"""
        <div style="text-align:center; padding: 1rem; background:#FFF8EC;
                    border:2px solid #C8922A; border-radius:12px;">
            <div style="font-size:0.85rem; color:#5C2E00; font-weight:600;
                        text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">
                Score de Risque
            </div>
            <div style="font-size:3rem; font-weight:800; color:{color}; line-height:1;">
                {score}
            </div>
            <div style="font-size:0.8rem; color:#888; margin-top:2px;">/ 1000</div>
            <div style="margin-top:0.5rem; font-size:0.9rem; font-weight:600; color:{color};">
                {label}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # — Probabilité de défaut —
    with res_col3:
        proba_pct = proba_defaut * 100
        bar_color = "#C0392B" if proba_defaut >= 0.5 else "#27AE60"
        st.markdown(f"""
        <div style="text-align:center; padding: 1rem; background:#FFF8EC;
                    border:2px solid #C8922A; border-radius:12px;">
            <div style="font-size:0.85rem; color:#5C2E00; font-weight:600;
                        text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">
                Probabilité de Défaut
            </div>
            <div style="font-size:3rem; font-weight:800; color:{bar_color}; line-height:1;">
                {proba_pct:.1f}%
            </div>
            <div style="font-size:0.8rem; color:#888; margin-top:2px;">seuil : 50%</div>
        </div>
        """, unsafe_allow_html=True)

    # — Jauge visuelle (barre de progression) —
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Jauge de Risque — Score sur 1000**")
    bar_pct = score / 10  # pourcentage pour la barre

    # Couleur progressive selon le score
    if score >= 700:
        jauge_color = "#27AE60"
        zone = "🟢 Zone verte — Profil fiable"
    elif score >= 400:
        jauge_color = "#F39C12"
        zone = "🟡 Zone orange — Profil à surveiller"
    else:
        jauge_color = "#C0392B"
        zone = "🔴 Zone rouge — Profil risqué"

    st.markdown(f"""
    <div style="background:#E8E8E8; border-radius:20px; height:28px; overflow:hidden;
                border:1px solid #CCC;">
        <div style="width:{bar_pct}%; background:linear-gradient(90deg, {jauge_color}, {jauge_color}CC);
                    height:100%; border-radius:20px; display:flex; align-items:center;
                    justify-content:center; transition:width 0.5s ease;">
            <span style="color:white; font-weight:700; font-size:0.9rem;">{score} / 1000</span>
        </div>
    </div>
    <div style="margin-top:0.4rem; font-size:0.9rem; color:#555;">{zone}</div>
    """, unsafe_allow_html=True)

    # — Repères de la jauge —
    st.markdown("""
    <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#888;
                margin-top:2px; padding:0 2px;">
        <span>0 — Très risqué</span>
        <span>400 — Seuil modéré</span>
        <span>700 — Seuil fiable</span>
        <span>1000 — Excellent</span>
    </div>
    """, unsafe_allow_html=True)

    # — Récapitulatif des données saisies —
    with st.expander("🔎 Récapitulatif des données saisies", expanded=False):
        recap_df = pd.DataFrame({
            "Variable": [
                "Revenu mensuel",
                "Ratio d'endettement",
                "Score interne banque",
                "Incidents de paiement",
                "Retard maximum (jours)",
                "Rejets de prélèvement",
                "Découverts (12 mois)",
                "Ancienneté client (mois)",
                "Type d'emploi",
                "Garantie",
            ],
            "Valeur saisie": [
                f"{revenu:,} FCFA",
                f"{ratio_endettement:.2f} ({ratio_endettement*100:.0f}%)",
                str(score_interne),
                str(nb_incidents),
                f"{jours_retard} jours",
                str(nb_rejets),
                str(nb_decouvert),
                f"{anciennete} mois",
                type_emploi,
                garantie,
            ],
        })
        st.dataframe(recap_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# PIED DE PAGE
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#999; font-size:0.8rem; padding:0.5rem;">
    🏫 <b>ISM Dakar</b> — MBA1 Finance Digitale 2025-2026
    &nbsp;|&nbsp; Projet de Modélisation Prédictive
    &nbsp;|&nbsp; Prof. M. Komla Martin CHOKKI
    <br><i>⚠️ Outil d'aide à la décision — Ne remplace pas le jugement du conseiller bancaire.</i>
</div>
""", unsafe_allow_html=True)
