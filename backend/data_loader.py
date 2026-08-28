import pandas as pd
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "locations.csv"


def get_location(location_id: str):

    df = pd.read_csv(DATA_PATH)

    location = df[
        df["location_id"] == location_id
    ]

    if location.empty:
        return None

    row = location.iloc[0]

    return {
        "location_id": row["location_id"],
        "location_name": row["location_name"],
        "latitude": float(row["latitude"]),
        "longitude": float(row["longitude"]),

        # Temporary default infrastructure values
        "age_years": 2,
        "years_since_maintenance": 2,
        "population_density": 18500,
        "avg_population_density": 12000,
        "elevation": 8,
        "slope": 1.2,
        "imperviousness": 0.82,
        "drainage_capacity": 50,
    }