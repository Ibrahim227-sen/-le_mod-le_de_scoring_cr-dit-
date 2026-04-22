# 🏦 Scoring Crédit — ISM Dakar
### MBA1 Finance Digitale | Modélisation Prédictive et IA en Finance

> Application Streamlit de scoring crédit permettant à un conseiller bancaire de prédire
> instantanément le risque de défaut d'un client, avec un score sur 1000 points.

---

## 🎯 Présentation

Ce projet déploie un modèle de **Régression Logistique** (AUC ≈ 0.9999) sous forme
d'application web interactive. L'outil est destiné aux conseillers bancaires souhaitant
évaluer rapidement le profil de risque d'un client demandeur de crédit.

**Résultat affiché pour chaque client :**
- ✅ / ❌ Décision : Crédit **Accordé** ou **Refusé**
- 📊 Probabilité de défaut (en %)
- 🏅 Score de risque sur **1000 points**
- 📈 Jauge visuelle de risque

---

## 📁 Structure du Projet

```
projet_scoring/
├── app.py                      # Application Streamlit (frontend)
├── train_model.py              # Script d'entraînement du modèle (backend)
├── credit_scoring_model.pkl    # Modèle sauvegardé (généré par train_model.py)
├── requirements.txt            # Dépendances Python
└── README.md                   # Documentation
```

---

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.9+
- pip

### 1. Cloner le dépôt
```bash
git clone https://github.com/VOTRE_USERNAME/scoring-credit-ism.git
cd scoring-credit-ism
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Entraîner le modèle
Placer `dataset_scoring_credit_900k.csv` dans le dossier, puis :
```bash
python train_model.py
```
→ Génère `credit_scoring_model.pkl`

### 4. Lancer l'application
```bash
streamlit run app.py
```
→ Ouvre automatiquement `http://localhost:8501`

---

## ☁️ Déploiement sur Streamlit Cloud

1. Pousser le dépôt sur GitHub (avec `credit_scoring_model.pkl` inclus)
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Cliquer **New app** → sélectionner le dépôt → fichier principal : `app.py`
4. Cliquer **Deploy** — l'application est en ligne en quelques minutes !

> **Note :** Le fichier `credit_scoring_model.pkl` doit être poussé sur GitHub
> (il est généré localement par `train_model.py`).

---

## 🧠 Modèle et Données

| Paramètre | Valeur |
|---|---|
| Algorithme | Régression Logistique |
| `class_weight` | `balanced` (gestion déséquilibre) |
| Prétraitement | `StandardScaler` + `OneHotEncoder` |
| AUC-ROC | ≈ 0.9999 |
| Dataset | 900 000 clients, 47 variables |

### Variables utilisées (Top 10)

| Variable | Type | Description |
|---|---|---|
| `REVENU_MENSUEL_FCFA` | Numérique | Revenu mensuel brut |
| `RATIO_ENDETTEMENT` | Numérique | Taux d'endettement (0-1) |
| `SCORE_INTERNE_BANQUE` | Numérique | Score de risque interne (0-1000) |
| `NB_INCIDENTS_PAIEMENT` | Numérique | Nb d'incidents de paiement |
| `JOURS_RETARD_MAX` | Numérique | Retard maximum en jours |
| `NB_REJETS_PRELEVEMENT` | Numérique | Nb de prélèvements rejetés |
| `NB_DECOUVERT_12MOIS` | Numérique | Nb de découverts sur 12 mois |
| `ANCIENNETE_CLIENT_MOIS` | Numérique | Durée relation bancaire (mois) |
| `TYPE_EMPLOI` | Catégorielle | CDI, CDD, Indépendant, etc. |
| `GARANTIE` | Catégorielle | Hypothèque, Assurance, etc. |

---

## 🎨 Design

Thème couleurs **ISM Dakar** : Marron (`#5C2E00`) & Or (`#C8922A`)

- 🟢 Score ≥ 700 → Risque FAIBLE → Crédit Accordé
- 🟡 Score 400-699 → Risque MODÉRÉ
- 🔴 Score < 400 → Risque ÉLEVÉ → Crédit Refusé

---

## 👥 Équipe

Projet réalisé dans le cadre du cours de **Modélisation Prédictive et IA en Finance**  
Professeur : **M. Komla Martin CHOKKI** — Lead Data Strategist  
Année Académique 2025-2026 | **ISM Dakar**
