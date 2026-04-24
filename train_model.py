"""
train_model.py
Entraîne la Régression Logistique exactement comme dans le notebook du prof
et sauvegarde le pipeline complet dans credit_scoring_model.pkl
"""

import pandas as pd
import numpy as np
import joblib
import time
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    roc_auc_score, recall_score, precision_score,
    f1_score, classification_report, confusion_matrix
)

# ── 1. Chargement du dataset ─────────────────────────────────────────────────
print("Chargement du dataset...")
df = pd.read_csv('dataset_scoring_credit_900k.xls')
print(f"Dataset : {df.shape[0]:,} lignes × {df.shape[1]} colonnes")
print(f"Taux de défaut : {df['DEFAUT'].mean():.4%}")

# ── 2. Séparation X / y ──────────────────────────────────────────────────────
X = df.drop(['CLIENT_ID', 'DEFAUT'], axis=1)
y = df['DEFAUT']

# ── 3. Identification des types de colonnes ──────────────────────────────────
numerical_cols   = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object', 'str']).columns.tolist()
print(f"\nVariables numériques  : {len(numerical_cols)}")
print(f"Variables catégorielles : {len(categorical_cols)}")
print(f"  → {categorical_cols}")

# ── 4. Prétraitement (identique au notebook) ─────────────────────────────────
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough'
)

# ── 5. Split train/test (identique au notebook) ──────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain : {X_train.shape[0]:,}   Test : {X_test.shape[0]:,}")

# ── 6. Pipeline Régression Logistique (identique au notebook) ────────────────
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(
        random_state=42,
        class_weight='balanced',
        max_iter=1000
    ))
])

print("\nEntraînement de la Régression Logistique...", end=' ', flush=True)
t0 = time.time()
pipeline.fit(X_train, y_train)
print(f"Terminé en {time.time()-t0:.1f}s")

# ── 7. Évaluation ────────────────────────────────────────────────────────────
y_pred  = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

auc       = roc_auc_score(y_test, y_proba)
recall    = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
f1        = f1_score(y_test, y_pred)

print("\n" + "="*45)
print("   PERFORMANCES — Régression Logistique")
print("="*45)
print(f"  AUC                 : {auc:.4f}")
print(f"  Rappel   (Défaut)   : {recall:.4f}")
print(f"  Précision (Défaut)  : {precision:.4f}")
print(f"  F1-Score  (Défaut)  : {f1:.4f}")
print("="*45)

print("\nClassification report :")
print(classification_report(y_test, y_pred, target_names=['Non-Défaut', 'Défaut']))

# ── 8. Sauvegarde du pipeline ────────────────────────────────────────────────
# On enrichit le pipeline avec les métadonnées utiles pour app.py
model_data = {
    'pipeline':         pipeline,
    'numerical_cols':   numerical_cols,
    'categorical_cols': categorical_cols,
    'auc':              auc,
    'recall':           recall,
    'precision':        precision,
    'f1':               f1,
    'feature_names':    numerical_cols + categorical_cols,
}

joblib.dump(model_data, 'credit_scoring_model.pkl')
print("\ncredit_scoring_model.pkl sauvegardé avec succès !")

# ── 9. Top 10 features (pour l'affichage dans app.py) ────────────────────────
model      = pipeline.named_steps['classifier']
ohe_names  = pipeline.named_steps['preprocessor'] \
              .named_transformers_['cat'] \
              .get_feature_names_out(categorical_cols)
all_names  = np.concatenate([numerical_cols, ohe_names])
coef_abs   = np.abs(model.coef_[0])

top10 = pd.DataFrame({'feature': all_names, 'importance': coef_abs}) \
          .sort_values('importance', ascending=False).head(10)
print("\nTop 10 variables les plus importantes :")
print(top10.to_string(index=False))
