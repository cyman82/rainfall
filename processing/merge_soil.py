import os
import pandas as pd

# Project root (rainfall/)
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# Correct paths based on your folder structure
SIM_PATH = os.path.join(
    BASE_DIR,
    "ingestion",
    "data",
    "processed",
    "district_soil_simulated.csv"
)

REAL_PATH = os.path.join(
    BASE_DIR,
    "ingestion",
    "data",
    "raw",
    "district_weather_daily.csv"  # temporary, we’ll extract soil later
)

OUT_PATH = os.path.join(
    BASE_DIR,
    "ingestion",
    "data",
    "processed",
    "district_soil_continuous.csv"
)



def main():
    print("Merging simulated soil moisture (2015–present placeholder)...")

    sim = pd.read_csv(SIM_PATH)
    sim["date"] = pd.to_datetime(sim["date"])
    sim = sim.rename(columns={
        "soil_moisture_simulated": "soil_moisture"
    })
    sim["soil_source"] = "simulated"

    sim = sim.sort_values(
        ["district", "date"]
    ).reset_index(drop=True)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    sim.to_csv(OUT_PATH, index=False)

    print("✅ Continuous soil file created (simulated)")
    print("Rows:", len(sim))
    print("Date range:", sim["date"].min(), "→", sim["date"].max())



if __name__ == "__main__":
    main()
