"""
train_model.py — Script d'entraînement du modèle de scoring crédit
MBA1 Finance Digitale — ISM Dakar 2025-2026
Professeur : M. Komla Martin CHOKKI

Conformément aux consignes :
  - Régression Logistique avec class_weight='balanced'
  - Pipeline StandardScaler + OneHotEncoder
  - Sauvegarde dans credit_scoring_model.pkl avec joblib
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
    recall_score, precision_score, f1_score,
)

# ─── BANNER ───────────────────────────────────────────────
print("\n" + "=" * 62)
print("  SCORING CREDIT — Regression Logistique")
print("  ISM Dakar | MBA1 Finance Digitale 2025-2026")
print("  Prof : M. Komla Martin CHOKKI")
print("=" * 62)

# ─── 1. CHARGEMENT ────────────────────────────────────────
DATASET_PATH = "dataset_scoring_credit_900k.csv"
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(
        f"Dataset introuvable : '{DATASET_PATH}'\n"
        "Placez le fichier CSV dans le meme repertoire que ce script."
    )

print(f"\n[1/5] Chargement : {DATASET_PATH} ...")
df = pd.read_csv(DATASET_PATH)
print(f"      OK {df.shape[0]:,} lignes x {df.shape[1]} colonnes")
print(f"      OK Taux de defaut : {df['DEFAUT'].mean():.2%}")

# ─── 2. FEATURES (10 variables importantes) ───────────────
NUMERICAL_FEATURES = [
    "REVENU_MENSUEL_FCFA",      # Variable 1
    "RATIO_ENDETTEMENT",         # Variable 2
    "SCORE_INTERNE_BANQUE",      # Variable 3
    "NB_INCIDENTS_PAIEMENT",     # Variable 4
    "JOURS_RETARD_MAX",          # Variable 5
    "NB_REJETS_PRELEVEMENT",     # Variable 6
    "NB_DECOUVERT_12MOIS",       # Variable 7
    "ANCIENNETE_CLIENT_MOIS",    # Variable 8
]
CATEGORICAL_FEATURES = [
    "TYPE_EMPLOI",   # Variable 9
    "GARANTIE",      # Variable 10
]
ALL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
TARGET = "DEFAUT"

print(f"\n[2/5] Features selectionnees : {len(ALL_FEATURES)} variables")
print(f"      - {len(NUMERICAL_FEATURES)} numeriques : {', '.join(NUMERICAL_FEATURES)}")
print(f"      - {len(CATEGORICAL_FEATURES)} categorielles : {', '.join(CATEGORICAL_FEATURES)}")

X = df[ALL_FEATURES].copy()
y = df[TARGET].copy()

# ─── 3. SPLIT TRAIN / TEST ────────────────────────────────
print("\n[3/5] Separation train/test (80/20, stratifiee) ...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
print(f"      OK Train : {X_train.shape[0]:,} observations")
print(f"      OK Test  : {X_test.shape[0]:,} observations")

# ─── 4. PIPELINE (conforme consignes) ─────────────────────
print("\n[4/5] Construction du pipeline de pretraitement ...")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), NUMERICAL_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
    ],
    remainder="drop",
)

# Pipeline complet : preprocesseur + Régression Logistique
# class_weight='balanced' : conforme aux consignes du prof
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier",   LogisticRegression(
        class_weight="balanced",  # ← Consigne exacte du prof
        max_iter=2000,
        solver="lbfgs",
        C=1.0,
        random_state=42,
    )),
])

print("      OK Pipeline : StandardScaler + OneHotEncoder + LogisticRegression")
print("      OK class_weight='balanced' (consigne prof)")

# ─── 5. ENTRAÎNEMENT + ÉVALUATION ─────────────────────────
print("\n[5/5] Entrainement du modele ...")
pipeline.fit(X_train, y_train)
print("      OK Entrainement termine !")

# Seuil optimisé pour maximiser F1
print("      OK Optimisation du seuil de decision ...")
y_proba_train = pipeline.predict_proba(X_train)[:, 1]
best_f1, best_thr = 0, 0.5
for t in np.arange(0.10, 0.90, 0.01):
    f = f1_score(y_train, (y_proba_train >= t).astype(int), zero_division=0)
    if f > best_f1:
        best_f1, best_thr = f, t
print(f"      OK Seuil optimal : {best_thr:.2f}")

# Évaluation finale
y_proba = pipeline.predict_proba(X_test)[:, 1]
y_pred  = (y_proba >= best_thr).astype(int)

auc       = roc_auc_score(y_test, y_proba)
recall    = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
f1        = f1_score(y_test, y_pred)

# Coefficients pour Feature Importance
lr_coefs = pipeline.named_steps["classifier"].coef_[0]
ohe_features = list(
    pipeline.named_steps["preprocessor"]
    .named_transformers_["cat"]
    .get_feature_names_out(CATEGORICAL_FEATURES)
)
feature_names_all = NUMERICAL_FEATURES + ohe_features
feature_importance = dict(zip(feature_names_all, np.abs(lr_coefs)))

print(f"""
================= RESULTATS FINAUX =================
AUC-ROC        : {auc:.4f}
Rappel defaut  : {recall:.4f}
Precision      : {precision:.4f}
F1-score       : {f1:.4f}
Seuil optimal  : {best_thr:.2f}
====================================================
""")
print(classification_report(y_test, y_pred, target_names=["Non-defaut", "Defaut"]))

# ─── SAUVEGARDE ───────────────────────────────────────────
MODEL_PATH = "credit_scoring_model.pkl"
joblib.dump({
    "pipeline":              pipeline,          # Pipeline sklearn complet
    "numerical_features":    NUMERICAL_FEATURES,
    "categorical_features":  CATEGORICAL_FEATURES,
    "all_features":          ALL_FEATURES,
    "threshold":             float(best_thr),
    "feature_importance":    feature_importance,
    "feature_names_all":     feature_names_all,
    "metrics": {
        "auc":       round(auc, 4),
        "recall":    round(recall, 4),
        "precision": round(precision, 4),
        "f1":        round(f1, 4),
    },
    "model_name": "Regression Logistique (class_weight=balanced)",
    "dataset_rows": df.shape[0],
}, MODEL_PATH)

print(f"Modele sauvegarde -> '{MODEL_PATH}'  ({os.path.getsize(MODEL_PATH)/1024:.0f} Ko)")
print("Lancez maintenant : streamlit run app.py\n")
