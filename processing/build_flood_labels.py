import pandas as pd
import os

# ---------------- CONFIG ---------------- #

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FEATURES_PATH = os.path.join(
    PROJECT_ROOT,
    "ingestion", "data", "processed",
    "district_weather_soil_features_clean.csv"
)

IFI_PATH = os.path.join(
    PROJECT_ROOT,
    "ingestion", "data", "labels",
    "India_Flood_Inventory.csv"
)

OUTPUT_PATH = os.path.join(
    PROJECT_ROOT,
    "ingestion", "data", "processed",
    "district_flood_ml_dataset.csv"
)

MODEL_DISTRICTS = [
    "Chennai",
    "Tiruvallur",
    "Chengalpattu",
    "Kancheepuram",
    "Cuddalore",
    "Nagapattinam",
]

# ---------------------------------------- #

def main():
    print("🚀 Building flood labels...")

    # Load feature dataset
    df = pd.read_csv(FEATURES_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["district", "date"])

    print(f"Feature rows: {len(df)}")

    # Load IFI dataset
    ifi = pd.read_csv(IFI_PATH)

    # Parse dates
    ifi["Start Date"] = pd.to_datetime(
        ifi["Start Date"], errors="coerce", dayfirst=True
    )
    ifi["End Date"] = pd.to_datetime(
        ifi["End Date"], errors="coerce", dayfirst=True
    )

    ifi = ifi.dropna(subset=["Start Date", "End Date"])

    # Filter Tamil Nadu
    ifi = ifi[
        ifi["State"].str.contains("Tamil Nadu", case=False, na=False)
    ]

    print(f"TN flood events: {len(ifi)}")

    # Extract district-wise flood events
    records = []

    for _, row in ifi.iterrows():
        district_text = str(row.get("Districts", "")).lower()
        for d in MODEL_DISTRICTS:
            if d.lower() in district_text:
                records.append({
                    "district": d,
                    "start_date": row["Start Date"],
                    "end_date": row["End Date"],
                })

    flood_events = pd.DataFrame(records)

    print("Flood events by district:")
    print(flood_events["district"].value_counts())

    # Expand flood ranges into daily labels
    daily = []

    for _, r in flood_events.iterrows():
        for d in pd.date_range(r["start_date"], r["end_date"]):
            daily.append({
                "district": r["district"],
                "date": d,
                "flood_risk": 1
            })

    flood_days = pd.DataFrame(daily)

    print(f"Total flood-labeled days: {len(flood_days)}")

    # Merge labels
    df = df.merge(
        flood_days,
        on=["district", "date"],
        how="left"
    )

    df["flood_risk"] = df["flood_risk"].fillna(0).astype(int)

    # Final sanity check
    print("\nFlood label distribution:")
    print(df["flood_risk"].value_counts())

    # Save
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n✅ Saved ML dataset to:\n{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
