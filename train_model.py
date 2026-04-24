"""
train_model.py — Script d'entraînement du modèle de scoring crédit
MBA1 Finance Digitale — ISM Dakar 2025-2026
Professeur : M. Komla Martin CHOKKI — Lead Data Strategist

REPRODUCTION EXACTE DU NOTEBOOK DU PROF :
  - X = df.drop(['CLIENT_ID', 'DEFAUT'], axis=1)  ← toutes les colonnes
  - Pipeline : StandardScaler + OneHotEncoder (colonnes auto-détectées)
  - LogisticRegression(random_state=42, class_weight='balanced', max_iter=1000)
  - Seuil de décision : 0.5 (défaut sklearn)
  - Résultat attendu : AUC ≈ 0.9999, Précision ≥ 0.90

Usage :
    python train_model.py
"""

import pandas as pd
import numpy as np
import joblib
import os
import time
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, roc_auc_score, roc_curve,
    recall_score, precision_score, f1_score,
    confusion_matrix,
)

# ─────────────────────────────────────────────────────────
print("\n" + "=" * 62)
print("  SCORING CREDIT — Régression Logistique")
print("  ISM Dakar | MBA1 Finance Digitale 2025-2026")
print("  Prof : M. Komla Martin CHOKKI")
print("  Reproduction exacte du notebook de cours")
print("=" * 62)

# ─── 1. CHARGEMENT ───────────────────────────────────────
DATASET_PATH = "dataset_scoring_credit_900k.csv"
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(
        f"\n❌ Dataset introuvable : '{DATASET_PATH}'\n"
        "   Placez le fichier CSV dans le même répertoire que ce script.\n"
    )

print(f"\n[1/5] Chargement du dataset...")
df = pd.read_csv(DATASET_PATH)
print(f"      ✓ {df.shape[0]:,} lignes × {df.shape[1]} colonnes")
print(f"      ✓ Taux de défaut : {df['DEFAUT'].mean():.2%}")

# ─── 2. SÉPARATION X / y — IDENTIQUE AU NOTEBOOK ─────────
print(f"\n[2/5] Préparation des features...")

# ← Exactement comme le notebook du prof :
X = df.drop(['CLIENT_ID', 'DEFAUT'], axis=1)
y = df['DEFAUT']

# Détection automatique des colonnes (comme le notebook)
numerical_cols   = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

print(f"      ✓ {len(numerical_cols)} variables numériques")
print(f"      ✓ {len(categorical_cols)} variables catégorielles : {categorical_cols}")
print(f"      ✓ Total features : {X.shape[1]}")

# ─── 3. SPLIT TRAIN / TEST ───────────────────────────────
print(f"\n[3/5] Séparation train/test (80/20, stratifiée)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
print(f"      ✓ Train : {X_train.shape[0]:,} observations")
print(f"      ✓ Test  : {X_test.shape[0]:,} observations")

# ─── 4. PIPELINE — IDENTIQUE AU NOTEBOOK ─────────────────
print(f"\n[4/5] Construction du pipeline et entraînement...")

# Préprocesseur (copie exacte du notebook)
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
    ],
    remainder='passthrough'
)

# Régression Logistique (paramètres exacts du notebook du prof)
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(
        random_state=42,
        class_weight='balanced',
        max_iter=1000,
    )),
])

print(f"      ✓ Pipeline : StandardScaler + OneHotEncoder")
print(f"      ✓ Modèle : LogisticRegression(class_weight='balanced', max_iter=1000)")
print(f"      ⏳ Entraînement en cours...")

t0 = time.time()
pipeline.fit(X_train, y_train)
elapsed = time.time() - t0
print(f"      ✓ Entraînement terminé en {elapsed:.1f}s")

# ─── 5. ÉVALUATION ───────────────────────────────────────
print(f"\n[5/5] Évaluation sur le jeu de test...")

# Prédictions avec seuil 0.5 (défaut sklearn — consigne prof)
y_pred  = pipeline.predict(X_test)          # seuil = 0.5 par défaut
y_proba = pipeline.predict_proba(X_test)[:, 1]

auc       = roc_auc_score(y_test, y_proba)
recall    = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
f1        = f1_score(y_test, y_pred)

print(f"""
  ╔══════════════════════════════════════════════╗
  ║           RÉSULTATS FINAUX                   ║
  ╠══════════════════════════════════════════════╣
  ║  AUC-ROC          : {auc:.4f}                  ║
  ║  Rappel défaut    : {recall:.4f}                  ║
  ║  Précision défaut : {precision:.4f}                  ║
  ║  F1-Score         : {f1:.4f}                  ║
  ║  Seuil décision   : 0.50 (défaut)            ║
  ╚══════════════════════════════════════════════╝
""")

print(classification_report(y_test, y_pred, target_names=["Non-défaut", "Défaut"]))

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred)
print("Matrice de confusion :")
print(f"  TN={cm[0,0]:,}  FP={cm[0,1]:,}")
print(f"  FN={cm[1,0]:,}  TP={cm[1,1]:,}")

# ─── FEATURE IMPORTANCE (coefficients) ───────────────────
best_model = pipeline.named_steps['classifier']
ohe_feature_names = (
    pipeline.named_steps['preprocessor']
    .named_transformers_['cat']
    .get_feature_names_out(categorical_cols)
)
all_feature_names = np.concatenate([numerical_cols, ohe_feature_names])
feature_importance = dict(zip(
    all_feature_names,
    np.abs(best_model.coef_[0][:len(all_feature_names)])
))

# ─── SAUVEGARDE ──────────────────────────────────────────
MODEL_PATH = "credit_scoring_model.pkl"

joblib.dump({
    # Pipeline sklearn complet (preprocesseur + modèle)
    "pipeline":              pipeline,

    # Features — pour app.py (interface utilisateur)
    # On garde les 10 variables de l'interface mais le modèle
    # utilise toutes les colonnes disponibles via le pipeline
    "numerical_features":    [
        "REVENU_MENSUEL_FCFA",
        "RATIO_ENDETTEMENT",
        "SCORE_INTERNE_BANQUE",
        "NB_INCIDENTS_PAIEMENT",
        "JOURS_RETARD_MAX",
        "NB_REJETS_PRELEVEMENT",
        "NB_DECOUVERT_12MOIS",
        "ANCIENNETE_CLIENT_MOIS",
    ],
    "categorical_features":  categorical_cols,
    "all_features":          numerical_cols + categorical_cols,
    "all_feature_names":     all_feature_names.tolist(),
    "numerical_cols":        numerical_cols,
    "categorical_cols":      categorical_cols,

    # Seuil = 0.5 (consigne prof, seuil par défaut)
    "threshold":             0.5,

    # Métriques réelles
    "metrics": {
        "auc":       round(auc, 4),
        "recall":    round(recall, 4),
        "precision": round(precision, 4),
        "f1":        round(f1, 4),
    },

    # Feature importance (coefficients absolus)
    "feature_importance":    feature_importance,

    # Metadata
    "model_name":   "Régression Logistique (class_weight='balanced', max_iter=1000)",
    "dataset_rows": df.shape[0],
    "dataset_cols": df.shape[1],
    "n_features":   X.shape[1],
    "training_time_s": round(elapsed, 2),
}, MODEL_PATH)

print(f"\n✅ Modèle sauvegardé → '{MODEL_PATH}'")
print(f"   Taille : {os.path.getsize(MODEL_PATH)/1024:.0f} Ko")
print(f"\n   ▶ Lancez maintenant : streamlit run app.py\n")
