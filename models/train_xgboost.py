import pandas as pd
import numpy as np
import joblib

from xgboost import XGBClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score
)

# -----------------------
# CONFIG
# -----------------------
DATA_PATH = "../ingestion/data/processed/district_flood_ml_dataset.csv"
MODEL_PATH = "../models/flood_xgb_model.pkl"

THRESHOLD = 0.10   # start with same RF threshold
RANDOM_STATE = 42

FEATURES = [
    "rainfall_mm",
    "rain_3d",
    "rain_7d",
    "rain_14d",
    "rain_intensity",
    "soil_moisture",
    "soil_7d_avg",
    "soil_14d_avg",
    "wetness_index",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "surface_pressure_mean",
    "wind_speed_10m_mean",
    "cloud_cover_mean",
    "is_monsoon"
]

# -----------------------
# LOAD DATA
# -----------------------
print("⚡ Training XGBoost flood model")

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year

print(f"Total rows: {len(df)}")
print("Flood label distribution:")
print(df["flood_risk"].value_counts())

# -----------------------
# TIME-AWARE SPLIT
# -----------------------
train_df = df[df["year"] <= 2020]
test_df  = df[(df["year"] >= 2021) & (df["year"] <= 2022)]

print(f"\nTrain period: {train_df['date'].min()} → {train_df['date'].max()}")
print(f"Test period : {test_df['date'].min()} → {test_df['date'].max()}")

print(f"Train floods: {train_df['flood_risk'].sum()}")
print(f"Test floods : {test_df['flood_risk'].sum()}")

X_train = train_df[FEATURES]
y_train = train_df["flood_risk"]

X_test  = test_df[FEATURES]
y_test  = test_df["flood_risk"]

# -----------------------
# CLASS IMBALANCE HANDLING
# -----------------------
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()
scale_pos_weight = neg / pos

print(f"\nscale_pos_weight = {scale_pos_weight:.2f}")

# -----------------------
# MODEL
# -----------------------
model = XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=RANDOM_STATE,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -----------------------
# PREDICTION (PROBABILITY-BASED)
# -----------------------
y_prob = model.predict_proba(X_test)[:, 1]
y_pred = (y_prob >= THRESHOLD).astype(int)

print(f"\n=== Classification Report (XGBoost, threshold={THRESHOLD}) ===")
print(classification_report(y_test, y_pred, zero_division=0))

print("=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))

# -----------------------
# THRESHOLD SWEEP
# -----------------------
print("\nThreshold tuning:")
print("Threshold | Recall (Flood) | Precision (Flood)")

for t in np.linspace(0.05, 0.5, 10):
    preds = (y_prob >= t).astype(int)
    r = recall_score(y_test, preds, pos_label=1, zero_division=0)
    p = precision_score(y_test, preds, pos_label=1, zero_division=0)
    print(f"{t:0.2f}      | {r:0.3f}         | {p:0.3f}")

# -----------------------
# FEATURE IMPORTANCE
# -----------------------
importance = pd.Series(
    model.feature_importances_,
    index=FEATURES
).sort_values(ascending=False)

print("\n=== Feature Importances (XGBoost) ===")
print(importance)

# -----------------------
# SAVE MODEL
# -----------------------
joblib.dump(model, MODEL_PATH)
print(f"\n✅ Model saved to: {MODEL_PATH}")
