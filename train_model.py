"""
train_model.py — Script d'entraînement du modèle de scoring crédit
MBA1 Finance Digitale — ISM Dakar 2025-2026

Ce script charge le dataset, entraîne un pipeline complet
(prétraitement + Régression Logistique) et sauvegarde le modèle.

Usage :
    python train_model.py
"""

import pandas as pd
import numpy as np
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, roc_auc_score,
    recall_score, precision_score, f1_score
)

# ─────────────────────────────────────────────
# 1. CHARGEMENT DU DATASET
# ─────────────────────────────────────────────
print("=" * 60)
print("  SCORING CRÉDIT — Entraînement du modèle")
print("  ISM Dakar | MBA1 Finance Digitale 2025-2026")
print("=" * 60)

DATASET_PATH = "dataset_scoring_credit_900k.csv"

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(
        f"Dataset introuvable : '{DATASET_PATH}'\n"
        "Veuillez placer le fichier CSV dans le même répertoire."
    )

print(f"\n[1/5] Chargement du dataset : {DATASET_PATH} ...")
df = pd.read_csv(DATASET_PATH)
print(f"      ✓ {df.shape[0]:,} lignes × {df.shape[1]} colonnes chargées.")
print(f"      ✓ Taux de défaut global : {df['DEFAUT'].mean():.2%}")

# ─────────────────────────────────────────────
# 2. SÉLECTION DES FEATURES (Top 10 variables)
# ─────────────────────────────────────────────
# Ces 10 variables ont été identifiées comme les plus importantes
# lors de l'analyse exploratoire en cours.
NUMERICAL_FEATURES = [
    "REVENU_MENSUEL_FCFA",        # Revenu mensuel du client
    "RATIO_ENDETTEMENT",          # Part du revenu consacrée au remboursement
    "SCORE_INTERNE_BANQUE",       # Score de risque interne
    "NB_INCIDENTS_PAIEMENT",      # Historique d'incidents de paiement
    "JOURS_RETARD_MAX",           # Retard maximum observé (jours)
    "NB_REJETS_PRELEVEMENT",      # Nombre de prélèvements rejetés
    "NB_DECOUVERT_12MOIS",        # Nombre de découverts sur 12 mois
    "ANCIENNETE_CLIENT_MOIS",     # Ancienneté dans la banque
]

CATEGORICAL_FEATURES = [
    "TYPE_EMPLOI",                # CDI, CDD, Indépendant, etc.
    "GARANTIE",                   # Type de garantie du crédit
]

ALL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
TARGET = "DEFAUT"

print(f"\n[2/5] Features sélectionnées :")
print(f"      • {len(NUMERICAL_FEATURES)} variables numériques")
print(f"      • {len(CATEGORICAL_FEATURES)} variables catégorielles")

X = df[ALL_FEATURES].copy()
y = df[TARGET].copy()

# ─────────────────────────────────────────────
# 3. SÉPARATION TRAIN / TEST
# ─────────────────────────────────────────────
print("\n[3/5] Séparation train/test (80/20, stratifiée) ...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"      ✓ Entraînement : {X_train.shape[0]:,} observations")
print(f"      ✓ Test         : {X_test.shape[0]:,} observations")

# ─────────────────────────────────────────────
# 4. CONSTRUCTION DU PIPELINE COMPLET
# ─────────────────────────────────────────────
print("\n[4/5] Construction et entraînement du pipeline ...")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), NUMERICAL_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
    ],
    remainder="drop",
)

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        random_state=42,
        class_weight="balanced",   # Gère le déséquilibre des classes
        max_iter=1000,
        solver="lbfgs",
        C=1.0,
    )),
])

pipeline.fit(X_train, y_train)
print("      ✓ Pipeline entraîné avec succès.")

# ─────────────────────────────────────────────
# 5. ÉVALUATION ET SAUVEGARDE
# ─────────────────────────────────────────────
print("\n[5/5] Évaluation du modèle sur le jeu de test ...")

y_pred  = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

auc       = roc_auc_score(y_test, y_proba)
recall    = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
f1        = f1_score(y_test, y_pred)

print(f"\n  ┌─────────────────────────────────────┐")
print(f"  │  RÉSULTATS — Régression Logistique  │")
print(f"  ├─────────────────────────────────────┤")
print(f"  │  AUC-ROC      : {auc:.4f}              │")
print(f"  │  Rappel défaut: {recall:.4f}              │")
print(f"  │  Précision    : {precision:.4f}              │")
print(f"  │  F1-Score     : {f1:.4f}              │")
print(f"  └─────────────────────────────────────┘")

print("\n" + classification_report(y_test, y_pred, target_names=["Non-défaut", "Défaut"]))

# Sauvegarde du modèle et des métadonnées
MODEL_PATH = "credit_scoring_model.pkl"
metadata = {
    "pipeline": pipeline,
    "numerical_features": NUMERICAL_FEATURES,
    "categorical_features": CATEGORICAL_FEATURES,
    "all_features": ALL_FEATURES,
    "metrics": {
        "auc": round(auc, 4),
        "recall": round(recall, 4),
        "precision": round(precision, 4),
        "f1": round(f1, 4),
    },
    "model_name": "Régression Logistique (class_weight=balanced)",
    "dataset_rows": df.shape[0],
}
joblib.dump(metadata, MODEL_PATH)
print(f"\n✅ Modèle sauvegardé → '{MODEL_PATH}'")
print(f"   Taille du fichier : {os.path.getsize(MODEL_PATH) / 1024:.1f} Ko")
print("\nVous pouvez maintenant lancer l'application : streamlit run app.py\n")
