import pandas as pd
from pathlib import Path


DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "sample_environmental_data.csv"
)


def format_location(row):
    """
    Convert one dataset row into the standard
    location/environment dictionary used by the backend.
    """

    return {
        # Location information
        "location_id": row["location_id"],
        "location_name": row["location_name"],

        "latitude": float(row["latitude"]),
        "longitude": float(row["longitude"]),

        # Environmental conditions
        "rainfall": float(row["rainfall"]),
        "water_level": float(row["water_level"]),
        "soil_saturation": float(
            row["soil_saturation"]
        ),

        # Terrain information
        "elevation": float(row["elevation"]),
        "slope": float(row["slope"]),
        "imperviousness": float(
            row["imperviousness"]
        ),

        # Drainage information
        "drainage_capacity": float(
            row["drainage_capacity"]
        ),
        "drainage_capacity_used": float(
            row["drainage_capacity_used"]
        ),

        # Temporary infrastructure information
        # Required by existing analyser/predictor logic
        "age_years": 2,
        "years_since_maintenance": 2,
        "population_density": 18500,
        "avg_population_density": 12000,
    }


def get_location(location_id: str):
    """
    Load environmental and geographic data
    for one specific location.
    """

    df = pd.read_csv(DATA_PATH)

    location = df[
        df["location_id"] == location_id
    ]

    if location.empty:
        return None

    row = location.iloc[0]

    return format_location(row)


def get_all_locations():
    """
    Load all locations with environmental,
    terrain and drainage data.
    """

    df = pd.read_csv(DATA_PATH)

    locations = []

    for _, row in df.iterrows():
        locations.append(
            format_location(row)
        )

    return locations