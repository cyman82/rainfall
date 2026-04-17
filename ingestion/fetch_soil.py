import requests
import pandas as pd
import time
from datetime import date

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

# Same districts you already used for rainfall
DISTRICTS = {
    "Chennai": (13.0827, 80.2707),
    "Tiruvallur": (13.2544, 80.0088),
    "Chengalpattu": (12.6845, 79.9830),
    "Kancheepuram": (12.8342, 79.7036),
    "Cuddalore": (11.7480, 79.7714),
    "Nagapattinam": (10.7660, 79.8434),
}

START_YEAR = 2015
END_YEAR = 2026          # we will auto-skip future dates
CHUNK_YEARS = 2          # critical for API stability

OUTPUT_PATH = "../data/raw/district_soil_daily.csv"


def fetch_soil_chunk(lat, lon, start_date, end_date, retries=3):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": (
            "soil_moisture_0_to_7cm,"
            "soil_moisture_7_to_28cm,"
            "soil_moisture_28_to_100cm"
        ),
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "Asia/Kolkata"
    }

    for attempt in range(retries):
        r = requests.get(BASE_URL, params=params, timeout=30)

        if r.status_code == 200:
            return r.json()["daily"]

        if r.status_code == 429:
            wait = (attempt + 1) * 5
            print(f"      Rate limited. Waiting {wait}s...")
            time.sleep(wait)
        else:
            r.raise_for_status()

    raise RuntimeError("Failed after retries")


def fetch_soil_for_district(name, lat, lon):
    print(f"    Fetching chunks for {name}")
    today = date.today()
    frames = []

    for year in range(START_YEAR, END_YEAR, CHUNK_YEARS):
        start = date(year, 1, 1)
        end = date(year + CHUNK_YEARS - 1, 12, 31)

        if start > today:
            print(f"        Skipping chunk {start} → {end}")
            continue

        if end > today:
            end = today

        print(f"      → {start} to {end}")

        data = fetch_soil_chunk(
            lat, lon,
            start.isoformat(),
            end.isoformat()
        )

        df = pd.DataFrame(data)
        df.rename(columns={"time": "date"}, inplace=True)
        df["date"] = pd.to_datetime(df["date"])
        df["district"] = name

        frames.append(df)
        time.sleep(1)  # safety pause

    return pd.concat(frames, ignore_index=True)


def main():
    print("Fetching soil moisture data...")
    all_data = []

    for name, (lat, lon) in DISTRICTS.items():
        print(f"  → {name}")
        df = fetch_soil_for_district(name, lat, lon)
        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv(OUTPUT_PATH, index=False)

    print(f"\n✅ Soil data saved to: {OUTPUT_PATH}")
    print("Rows:", len(final_df))
    print("Columns:", list(final_df.columns))


if __name__ == "__main__":
    main()
