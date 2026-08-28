import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------------
# SAMPLE / IMAGINARY INPUT DATA   (TODO: replace with real input later)
# ---------------------------------------------------------------------------

# One fictional street, used to test the module end-to-end today.
# SAMPLE_STREET = {
#     "location_id": "RD-001",
#     "location_name": "Sample Street A (imaginary)",
#     "latitude": 19.0000,
#     "longitude": 72.8000,
#     "age_years": 2,                    # constructed 2 years ago
#     "years_since_maintenance": 2,      # never repaired since creation
#     "population_density": 18500,       # people / sq.km
#     "avg_population_density": 12000,   # city average, for comparison
#     "elevation": 8,                    # metres (low-lying)
#     "slope": 1.2,                      # percent (very flat -> poor natural drainage)
#     "imperviousness": 0.82,            # 82% paved / built-up surface
#     "drainage_capacity": 50,           # design capacity, mm/hr, before degradation
# }

# # Imaginary weather snapshot for "now". TODO: replace with live rainfall input.
# SAMPLE_WEATHER = {
#     "rainfall": 100,          # mm (heavy rainfall event)
#     "lightning": True,        # flag only -> used for alert severity, not risk math
#     "water_level": 0.6,       # 0-1, fraction of drain/channel already full
#     "soil_saturation": 0.55,  # 0-1, how saturated the ground already is
# }

FORECAST_INTERVALS = [0, 30, 60, 120, 180]  # minutes: Now, 30, 60, 120, 180

# ---------------------------------------------------------------------------
# DATASET LOADER
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FEATURES_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "processed"
    / "flood_features.csv"
)

FORECAST_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "sample_forecast.csv"
)


class DatasetLoader:
    """
    Loads location/environmental data and forecast data
    from the project CSV files.
    """

    def __init__(self):
        self.features_df = pd.read_csv(FEATURES_FILE)
        self.forecast_df = pd.read_csv(FORECAST_FILE)

    def get_street(self, location_id: str) -> dict:
        """
        Returns static/location information for one location.
        """

        row = self.features_df[
            self.features_df["location_id"] == location_id
        ]

        if row.empty:
            raise ValueError(
                f"Location {location_id} not found in dataset"
            )

        row = row.iloc[0]

        return {
            "location_id": row["location_id"],
            "location_name": row["location_name"],
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),

            "elevation": float(row["elevation"]),
            "slope": float(row["slope"]),
            "imperviousness": float(row["imperviousness"]),
            "drainage_capacity": float(row["drainage_capacity"]),

            # These fields are not currently available
            # in the dataset, so safe default values are used.
            "years_since_maintenance": 2,
            "population_density": 12000,
            "avg_population_density": 12000,
        }

    def get_current_weather(self, location_id: str) -> dict:
        """
        Gets current environmental/weather values
        from flood_features.csv.
        """

        row = self.features_df[
            self.features_df["location_id"] == location_id
        ]

        if row.empty:
            raise ValueError(
                f"Location {location_id} not found in dataset"
            )

        row = row.iloc[0]

        return {
            "rainfall": float(row["rainfall"]),
            "water_level": float(row["water_level"]),
            "soil_saturation": float(
                row["soil_saturation"]
            ),

            # Dataset currently has no lightning field.
            "lightning": False,
        }

    def get_forecast(self, location_id: str) -> list:
        """
        Returns actual forecast rainfall values
        for one location.
        """

        rows = self.forecast_df[
            self.forecast_df["location_id"] == location_id
        ].sort_values("forecast_minutes")

        return rows.to_dict(
            orient="records"
        )

# ---------------------------------------------------------------------------
# CLASS 1 -- FactorAnalyzer
# Computes every contributing factor's VALUE and IMPORTANCE (weight).
# ---------------------------------------------------------------------------
class FactorAnalyzer:
    """
    Turns raw street + weather data into normalized (0-1) factors, each
    with a weight (importance) reflecting how much it influences the final
    risk score -- the weighted-average design decided at ideation.
    """

    # Weights must sum to 1.0. Tune these as the team calibrates the model.
    WEIGHTS = {
        "rainfall_intensity": 0.25,
        "runoff_ratio": 0.20,
        "drainage_deficit": 0.20,
        "soil_saturation": 0.10,
        "imperviousness": 0.10,
        "infrastructure_condition": 0.10,
        "population_density_impact": 0.05,
    }

    def __init__(self, street: dict, weather: dict):
        self.street = street
        self.weather = weather

    def _maintenance_factor(self) -> float:
        """Drains lose effective capacity ~5%/year without maintenance."""
        deficit = 0.05 * self.street["years_since_maintenance"]
        return max(1 - deficit, 0.5)  # floor at 50% capacity

    def compute(self, rainfall: float, soil_saturation: float) -> dict:
        """Returns {factor_name: {value, weight}} for one point in time."""
        street = self.street

        # Simplified Rational Method: runoff coefficient C as a weighted mix
        # of imperviousness, slope (flatter = worse natural drainage) and
        # existing soil saturation.
        slope_factor = 1 - min(street["slope"] / 10, 1)
        runoff_coeff = min(
            0.5 * street["imperviousness"] + 0.2 * slope_factor + 0.3 * soil_saturation,
            1.0,
        )
        surface_runoff = rainfall * runoff_coeff

        maintenance_factor = self._maintenance_factor()
        effective_drainage_capacity = street["drainage_capacity"] * maintenance_factor
        drainage_capacity_used = (
            min(surface_runoff / effective_drainage_capacity, 2.0)
            if effective_drainage_capacity else 2.0
        )
        excess_water = max(surface_runoff - effective_drainage_capacity, 0)

        # Normalize each factor to 0-1 so they can be weighted-averaged together
        values = {
            "rainfall_intensity": min(rainfall / 150, 1.0),        # 150mm treated as extreme
            "runoff_ratio": min(surface_runoff / 150, 1.0),
            "drainage_deficit": min(excess_water / 100, 1.0),
            "soil_saturation": soil_saturation,
            "imperviousness": street["imperviousness"],
            "infrastructure_condition": min((1 - maintenance_factor) / 0.5, 1.0),
            "population_density_impact": min(
                street["population_density"] / street["avg_population_density"] / 2, 1.0
            ),
        }

        factors = {name: {"value": val, "weight": self.WEIGHTS[name]} for name, val in values.items()}

        # Raw physical numbers, kept for display / downstream use
        factors["_raw"] = {
            "surface_runoff": round(surface_runoff, 2),
            "drainage_capacity_used": round(drainage_capacity_used, 2),
            "effective_drainage_capacity": round(effective_drainage_capacity, 2),
            "excess_water": round(excess_water, 2),
        }
        return factors


# ---------------------------------------------------------------------------
# CLASS 2 -- RiskAggregator
# Weighted average -> risk_score / risk_level, plus forecast + trend status
# ---------------------------------------------------------------------------
class RiskAggregator:
    def __init__(self,analyzer: FactorAnalyzer,forecast_data=None):
        self.analyzer = analyzer

        self.forecast_data = {
            row["forecast_minutes"]: row["rainfall"]
            for row in (forecast_data or [])

    @staticmethod
    def _classify(risk_score: float) -> str:
        if risk_score < 25:
            return "Low"
        elif risk_score < 50:
            return "Moderate"
        elif risk_score < 75:
            return "High"
        return "Critical"

   def _rainfall_at(self,base_rainfall: float,minutes: int) -> float:
        """Uses dataset forecast rainfall when available.
        Falls back to current rainfall otherwise."""

        if minutes in self.forecast_data:
            return float(
                self.forecast_data[minutes]
            )

        return float(base_rainfall)

    @staticmethod
    def _soil_saturation_at(base_saturation: float, minutes: int) -> float:
        """Soil keeps saturating while it's still raining, then plateaus."""
        increment = {0: 0.0, 30: 0.05, 60: 0.10, 120: 0.15, 180: 0.18}
        return min(base_saturation + increment.get(minutes, 0.18), 1.0)

    def score_at(self, minutes: int) -> dict:
        rainfall = self._rainfall_at(self.analyzer.weather["rainfall"], minutes)
        soil_saturation = self._soil_saturation_at(self.analyzer.weather["soil_saturation"], minutes)
        factors = self.analyzer.compute(rainfall, soil_saturation)

        risk_score = round(
            sum(f["value"] * f["weight"] for name, f in factors.items() if name != "_raw") * 100, 1
        )
        risk_level = self._classify(risk_score)

        return {
            "forecast_minutes": minutes,
            "rainfall": rainfall,
            "risk_score": risk_score,
            "risk_level": risk_level,
            **factors["_raw"],
        }

    def forecast(self, intervals=None) -> list:
        intervals = intervals or FORECAST_INTERVALS
        results = [self.score_at(m) for m in intervals]

        for i, row in enumerate(results):
            if i == 0:
                row["prediction_status"] = "Stable"  # "now" has no prior point to compare
                continue
            delta = row["risk_score"] - results[i - 1]["risk_score"]
            if delta > 3:
                row["prediction_status"] = "Intensifying"
            elif delta < -3:
                row["prediction_status"] = "Receding"
            else:
                row["prediction_status"] = "Stable"
            # NOTE: "Shifting" (risk moving to a different location) can only
            # be detected once multiple locations are compared side by side --
            # not meaningful for a single-street test. Comes with multi-road support.
        return results


# ---------------------------------------------------------------------------
# CLASS 3 -- PredictorIO
# Input/output handling using pandas. Orchestrates Class 1 + Class 2.
# ---------------------------------------------------------------------------
class PredictorIO:
    def __init__(self, street: dict, weather: dict,forecast_data=None):
        self.street = street
        self.weather = weather
        self.analyzer = FactorAnalyzer(street, weather)
        self.aggregator = RiskAggregator(self.analyzer,forecast_data)

    def run(self) -> pd.DataFrame:
        """Runs the full forecast and returns a tidy pandas DataFrame,
        using the shared field-naming convention for the team."""
        rows = self.aggregator.forecast()
        df = pd.DataFrame(rows)
        df.insert(0, "location_name", self.street["location_name"])
        df.insert(0, "location_id", self.street["location_id"])
        df["lightning"] = self.weather["lightning"]  # metadata for alert module

        cols = [
            "location_id", "location_name", "forecast_minutes", "rainfall",
            "surface_runoff", "drainage_capacity_used", "excess_water",
            "risk_score", "risk_level", "prediction_status", "lightning",
        ]
        return df[cols]

    def to_dict_records(self) -> list:
        """Same output as a list of dicts -- e.g. for a Flask API response."""
        return self.run().to_dict(orient="records")

# ---------------------------------------------------------------------------
# API helper
# ---------------------------------------------------------------------------

def predict_flood_forecast(street: dict, weather: dict) -> list:
    """
    Generate the complete flood forecast for a street/location.
    Used by the Flask API.
    """
    predictor = PredictorIO(street, weather)
    return predictor.to_dict_records()

def predict_from_dataset(location_id: str) -> list:
    """Main dataset-based prediction function.

    Usage:
        predict_from_dataset("L001")
    """

    loader = DatasetLoader()

    street = loader.get_street(location_id)

    weather = loader.get_current_weather(location_id)

    forecast_data = loader.get_forecast(location_id)

    predictor = PredictorIO(street=street,weather=weather,forecast_data=forecast_data)

    return predictor.to_dict_records()
# ---------------------------------------------------------------------------
# DEMO -- run standalone to sanity-check today's output
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    result = predict_from_dataset("L001")
    print(pd.DataFrame(result).to_string(index=False))
