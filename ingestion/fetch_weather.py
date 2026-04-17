import requests
import time
import os
from datetime import datetime
import pandas as pd
from datetime import date, timedelta
from config.districts import DISTRICTS


# =========================
# CONFIG
# =========================
START_DATE = "2015-01-01"
END_DATE = date.today().isoformat()

OUTPUT_PATH = "data/raw/district_weather_daily.csv"


# =========================
# FETCH FUNCTION
# =========================
def fetch_weather_for_district(district, lat, lon):
    print(f"    Fetching chunks for {district}")

    all_chunks = []

    start_year = 2015
    end_year = datetime.today().year

    for year in range(start_year, end_year + 1, 2):
        chunk_start = f"{year}-01-01"
        chunk_end = f"{min(year + 1, end_year)}-12-31"

        print(f"      → {chunk_start} to {chunk_end}")

        url = (
            "https://archive-api.open-meteo.com/v1/archive"
            f"?latitude={lat}"
            f"&longitude={lon}"
            "&daily=precipitation_sum,"
            "temperature_2m_mean,"
            "relative_humidity_2m_mean,"
            "surface_pressure_mean,"
            "wind_speed_10m_mean,"
            "cloud_cover_mean"
            f"&start_date={chunk_start}"
            f"&end_date={chunk_end}"
            "&timezone=Asia/Kolkata"
        )

        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            print(f"        Skipping chunk {chunk_start} → {chunk_end}")
            time.sleep(5)
            continue

        data = response.json()
        daily = data["daily"]

        df_chunk = pd.DataFrame({
            "date": daily["time"],
            "district": district,
            "rainfall_mm": daily["precipitation_sum"],
            "temperature_2m_mean": daily["temperature_2m_mean"],
            "relative_humidity_2m_mean": daily["relative_humidity_2m_mean"],
            "surface_pressure_mean": daily["surface_pressure_mean"],
            "wind_speed_10m_mean": daily["wind_speed_10m_mean"],
            "cloud_cover_mean": daily["cloud_cover_mean"],
        })

        all_chunks.append(df_chunk)
        time.sleep(2)  # respect rate limit

    if not all_chunks:
        raise RuntimeError(f"No data fetched for {district}")

    return pd.concat(all_chunks, ignore_index=True)





# =========================
# MAIN PIPELINE
# =========================
def main():
    all_districts = []

    print("Fetching weather data...")

    for district, coords in DISTRICTS.items():
        print(f"  → {district}")
        df = fetch_weather_for_district(
            district,
            coords["lat"],
            coords["lon"]
        )
        all_districts.append(df)

        # IMPORTANT: Respect API limits
        time.sleep(2)  # 2 seconds between requests

    final_df = pd.concat(all_districts, ignore_index=True)

    # Ensure correct types
    final_df["date"] = pd.to_datetime(final_df["date"])

    # Sort for sanity
    final_df = final_df.sort_values(
        ["district", "date"]
    ).reset_index(drop=True)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Save raw data
    final_df.to_csv(OUTPUT_PATH, index=False)

    print("Done.")
    print(f"Saved to: {OUTPUT_PATH}")
    print("Rows:", len(final_df))
    print("Districts:", final_df["district"].unique())


if __name__ == "__main__":
    main()
