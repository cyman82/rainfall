import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import precision_score, recall_score
import joblib

# 🔹 ADDED: calibration import
from sklearn.calibration import CalibratedClassifierCV

# 🔹 ADDED: train/calibration split
from sklearn.model_selection import train_test_split


# ---------------- CONFIG ---------------- #

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "ingestion", "data", "processed",
    "district_flood_ml_dataset.csv"
)

# 🔹 CHANGED: save calibrated model (not raw RF)
MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "flood_rf_calibrated.pkl"
)

FEATURES = [
    "rainfall_mm",
    "rain_3d",
    "rain_7d",
    "rain_14d",
    "soil_moisture",
    "soil_7d_avg",
    "soil_14d_avg",
    "wetness_index",
    "rain_intensity",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "surface_pressure_mean",
    "wind_speed_10m_mean",
    "cloud_cover_mean",
    "is_monsoon",
]

TARGET = "flood_risk"

# ---------------------------------------- #

def main():
    print("🌲 Training Random Forest flood model")

    # Load data
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    print("Total rows:", len(df))
    print("Flood label distribution:")
    print(df[TARGET].value_counts())

    # Time-based split
    train_df = df[df["year"] <= 2020]
    test_df = df[(df["year"] >= 2021) & (df["year"] <= 2022)]

    print("\nTrain period:", train_df["date"].min(), "→", train_df["date"].max())
    print("Test period :", test_df["date"].min(),  "→", test_df["date"].max())

    print("Train floods:", train_df[TARGET].sum())
    print("Test floods :", test_df[TARGET].sum())

    # -------------------------------
    # 🔹 CHANGED: split train → train + calibration
    # -------------------------------
    X_full = train_df[FEATURES]
    y_full = train_df[TARGET]

    X_train, X_calib, y_train, y_calib = train_test_split(
        X_full,
        y_full,
        test_size=0.2,
        stratify=y_full,
        random_state=42
    )

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    # Model
    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    # -------------------------------
    # 🔹 CHANGED: train RF on TRAIN ONLY
    # -------------------------------
    rf.fit(X_train, y_train)

    # -------------------------------
    # 🔹 ADDED: Platt calibration
    # -------------------------------
    # 🔹 CHANGED: Calibrated RF with internal CV (Platt scaling)
    calibrated_rf = CalibratedClassifierCV(
        estimator=rf,
        method="sigmoid",
        cv=5  # 5-fold CV on training data
    )

    # 🔹 CHANGED: fit on FULL training data
    calibrated_rf.fit(X_full, y_full)

    # -------------------------------
    # 🔹 CHANGED: use CALIBRATED probabilities
    # -------------------------------
    y_prob = calibrated_rf.predict_proba(X_test)[:, 1]

    THRESHOLD = 0.10
    y_pred = (y_prob >= THRESHOLD).astype(int)

    # Evaluation
    print("\n=== Classification Report (Calibrated RF) ===")
    print(classification_report(y_test, y_pred, digits=3, zero_division=0))

    print("=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))

    # Threshold tuning
    thresholds = np.linspace(0.05, 0.5, 10)

    print("\nThreshold tuning:")
    print("Threshold | Recall (Flood) | Precision (Flood)")

    for t in thresholds:
        preds = (y_prob >= t).astype(int)
        r = recall_score(y_test, preds, pos_label=1, zero_division=0)
        p = precision_score(y_test, preds, pos_label=1, zero_division=0)
        print(f"{t:0.2f}      | {r:0.3f}         | {p:0.3f}")

    # Feature importance (from base RF)
    importances = pd.Series(
        rf.feature_importances_,
        index=FEATURES
    ).sort_values(ascending=False)

    print("\n=== Feature Importances ===")
    print(importances)

    # -------------------------------
    # 🔹 CHANGED: save CALIBRATED model
    # -------------------------------
    joblib.dump(calibrated_rf, MODEL_PATH)
    print(f"\n✅ Calibrated model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
