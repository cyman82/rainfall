import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import (
    Dense, Dropout, LayerNormalization,
    MultiHeadAttention, GlobalAveragePooling1D, Input
)
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, recall_score, precision_score
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
    "flood_transformer_model.keras"
)

SCALER_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "flood_transformer_scaler.pkl"
)

TIME_STEPS = 14

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


def build_sequences(df):
    X, y = [], []

    for district in df["district"].unique():
        sub = df[df["district"] == district].sort_values("date")
        data = sub[FEATURES].values
        labels = sub[TARGET].values

        for i in range(TIME_STEPS, len(sub)):
            X.append(data[i - TIME_STEPS:i])
            y.append(labels[i])

    return np.array(X), np.array(y)


def transformer_block(x, head_size=32, num_heads=2, ff_dim=64, dropout=0.2):
    attn = MultiHeadAttention(
        num_heads=num_heads,
        key_dim=head_size,
        dropout=dropout
    )(x, x)

    x = LayerNormalization(epsilon=1e-6)(x + attn)

    ff = Dense(ff_dim, activation="relu")(x)
    ff = Dropout(dropout)(ff)
    ff = Dense(x.shape[-1])(ff)

    return LayerNormalization(epsilon=1e-6)(x + ff)


def main():
    print("🤖 Training Transformer flood prediction model")

    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    train_df = df[df["year"] <= 2020]
    test_df  = df[(df["year"] >= 2021) & (df["year"] <= 2022)]

    # Scale features
    scaler = StandardScaler()
    train_df[FEATURES] = scaler.fit_transform(train_df[FEATURES])
    test_df[FEATURES]  = scaler.transform(test_df[FEATURES])
    joblib.dump(scaler, SCALER_PATH)

    # Build sequences
    X_train, y_train = build_sequences(train_df)
    X_test, y_test   = build_sequences(test_df)

    # Class weights
    neg, pos = np.bincount(y_train)
    class_weight = {0: 1.0, 1: neg / pos}

    # Model
    inputs = Input(shape=(TIME_STEPS, len(FEATURES)))
    x = transformer_block(inputs)
    x = transformer_block(x)
    x = GlobalAveragePooling1D()(x)
    x = Dense(32, activation="relu")(x)
    x = Dropout(0.3)(x)
    outputs = Dense(1, activation="sigmoid")(x)

    model = Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    model.summary()

    model.fit(
        X_train,
        y_train,
        epochs=40,
        batch_size=64,
        validation_split=0.2,
        class_weight=class_weight,
        callbacks=[EarlyStopping(patience=5, restore_best_weights=True)],
        verbose=1
    )

    # Evaluate
    y_prob = model.predict(X_test).ravel()

    print("\nThreshold tuning:")
    for t in np.linspace(0.05, 0.5, 10):
        preds = (y_prob >= t).astype(int)
        r = recall_score(y_test, preds, zero_division=0)
        p = precision_score(y_test, preds, zero_division=0)
        print(f"{t:0.2f} | Recall: {r:.3f} | Precision: {p:.3f}")

    THRESHOLD = 0.30
    y_pred = (y_prob >= THRESHOLD).astype(int)

    print("\n=== Classification Report (Transformer) ===")
    print(classification_report(y_test, y_pred, digits=3))
    print(confusion_matrix(y_test, y_pred))

    model.save(MODEL_PATH)
    print(f"\n✅ Transformer model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
