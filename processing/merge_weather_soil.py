import os
import pandas as pd

# Resolve project root
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

WEATHER_PATH = os.path.join(
    BASE_DIR,
    "ingestion",
    "data",
    "raw",
    "district_weather_daily.csv"
)

SOIL_PATH = os.path.join(
    BASE_DIR,
    "ingestion",
    "data",
    "processed",
    "district_soil_continuous.csv"
)

OUT_PATH = os.path.join(
    BASE_DIR,
    "ingestion",
    "data",
    "processed",
    "district_weather_soil_daily.csv"
)

def main():
    print("Loading weather data...")
    weather = pd.read_csv(WEATHER_PATH)
    weather["date"] = pd.to_datetime(weather["date"])

    print("Loading soil data...")
    soil = pd.read_csv(SOIL_PATH)
    soil["date"] = pd.to_datetime(soil["date"])

    print("Merging on (district, date)...")
    df = weather.merge(
        soil,
        on=["district", "date"],
        how="left"
    )

    # Sort + clean
    df = df.sort_values(
        ["district", "date"]
    ).reset_index(drop=True)

    # Safety check
    missing_soil = df["soil_moisture"].isna().sum()
    print(f"Missing soil rows: {missing_soil}")

    # Save
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print("✅ Weather + soil merged successfully")
    print("Rows:", len(df))
    print("Date range:", df["date"].min(), "→", df["date"].max())
    print("Districts:", df["district"].nunique())

if __name__ == "__main__":
    main()
