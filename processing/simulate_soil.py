import os
import pandas as pd
import numpy as np

# Base directory (project root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

WEATHER_PATH = os.path.join(
    BASE_DIR, "ingestion", "data", "raw", "district_weather_daily.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "district_soil_simulated.csv"
)


# Model parameters (physically reasonable)
ALPHA = 0.6    # rainfall infiltration
BETA  = 0.02   # evaporation (temperature driven)

START_DATE = "2015-01-01"
END_DATE   = "2024-12-31"


def simulate_soil_moisture(df):
    df = df.sort_values("date").copy()
    soil = []

    sm_prev = 0.3  # initial moderate wetness

    for _, row in df.iterrows():
        rain = row["rainfall_mm"]
        temp = row["temperature_2m_mean"]

        sm = sm_prev + ALPHA * rain / 100 - BETA * temp / 50
        sm = np.clip(sm, 0, 1)

        soil.append(sm)
        sm_prev = sm

    df["soil_moisture_simulated"] = soil
    df["soil_moisture_source"] = "simulated"
    return df


def main():
    print("Simulating soil moisture (2015–2018)...")

    df = pd.read_csv(WEATHER_PATH)
    df["date"] = pd.to_datetime(df["date"])

    df = df[(df["date"] >= START_DATE) & (df["date"] <= END_DATE)]

    results = []

    for district, group in df.groupby("district"):
        print(f"  → {district}")
        sim = simulate_soil_moisture(group)
        results.append(sim[[
            "date", "district",
            "soil_moisture_simulated",
            "soil_moisture_source"
        ]])

    final_df = pd.concat(results, ignore_index=True)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    final_df.to_csv(OUTPUT_PATH, index=False)

    print("✅ Simulated soil moisture saved")
    print("Rows:", len(final_df))

    print("Simulated soil date range:")
    print(df["date"].min(), "→", df["date"].max())
    print("Total rows:", len(df))


if __name__ == "__main__":
    main()

