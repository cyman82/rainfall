import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, recall_score, precision_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
import joblib

# ================= CONFIG ================= #

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "ingestion", "data", "processed",
    "district_flood_ml_dataset.csv"
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "flood_lstm_model.keras"
)

SCALER_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "flood_lstm_scaler.pkl"
)

TIME_STEPS = 14   # 2-week temporal window

FEATURES = [
    "rainfall_mm",
    "soil_moisture",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "surface_pressure_mean",
    "wind_speed_10m_mean",
    "cloud_cover_mean",
    "is_monsoon",
]

TARGET = "flood_risk"

# ========================================= #


def build_sequences(df, features, target, time_steps):
    """
    Build LSTM sequences district-wise to avoid leakage
    """
    X, y = [], []

    for district in df["district"].unique():
        sub = df[df["district"] == district].sort_values("date")

        data = sub[features].values
        labels = sub[target].values

        for i in range(time_steps, len(sub)):
            X.append(data[i - time_steps:i])
            y.append(labels[i])

    return np.array(X), np.array(y)


def main():
    print("🧠 Training LSTM flood prediction model")

    # Load data
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    print("Total rows:", len(df))
    print("Flood distribution:")
    print(df[TARGET].value_counts())

    # Time-based split
    train_df = df[df["year"] <= 2020]
    test_df  = df[(df["year"] >= 2021) & (df["year"] <= 2022)]

    print("\nTrain period:", train_df["date"].min(), "→", train_df["date"].max())
    print("Test period :", test_df["date"].min(),  "→", test_df["date"].max())

    print("Train floods:", train_df[TARGET].sum())
    print("Test floods :", test_df[TARGET].sum())

    # Scale features (fit ONLY on training)
    scaler = StandardScaler()
    train_df[FEATURES] = scaler.fit_transform(train_df[FEATURES])
    test_df[FEATURES]  = scaler.transform(test_df[FEATURES])

    # Save scaler
    joblib.dump(scaler, SCALER_PATH)

    # Build sequences
    X_train, y_train = build_sequences(train_df, FEATURES, TARGET, TIME_STEPS)
    X_test, y_test   = build_sequences(test_df,  FEATURES, TARGET, TIME_STEPS)

    print("\nSequence shapes:")
    print("X_train:", X_train.shape)
    print("X_test :", X_test.shape)

    # Handle class imbalance
    neg, pos = np.bincount(y_train)
    class_weight = {
        0: 1.0,
        1: neg / pos
    }

    print("Class weights:", class_weight)

    # Model
    model = Sequential([
        LSTM(32, input_shape=(TIME_STEPS, len(FEATURES))),
        Dropout(0.3),
        Dense(16, activation="relu"),
        Dropout(0.3),
        Dense(1, activation="sigmoid")
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    model.summary()

    # Train
    model.fit(
        X_train,
        y_train,
        epochs=40,
        batch_size=64,
        validation_split=0.2,
        class_weight=class_weight,
        callbacks=[
            EarlyStopping(
                monitor="val_loss",
                patience=5,
                restore_best_weights=True
            )
        ],
        verbose=1
    )

    # Predict probabilities
    y_prob = model.predict(X_test).ravel()

    # Threshold tuning
    print("\nThreshold tuning:")
    print("Threshold | Recall (Flood) | Precision (Flood)")

    for t in np.linspace(0.05, 0.5, 10):
        preds = (y_prob >= t).astype(int)
        r = recall_score(y_test, preds, zero_division=0)
        p = precision_score(y_test, preds, zero_division=0)
        print(f"{t:0.2f}      | {r:0.3f}         | {p:0.3f}")

    # Default threshold evaluation
    THRESHOLD = 0.25
    y_pred = (y_prob >= THRESHOLD).astype(int)

    print("\n=== Classification Report (LSTM) ===")
    print(classification_report(y_test, y_pred, digits=3))

    print("=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))

    # Save model
    model.save(MODEL_PATH)
    print(f"\n✅ LSTM model saved to: {MODEL_PATH}")
    print(f"✅ Scaler saved to: {SCALER_PATH}")


if __name__ == "__main__":
    main()
