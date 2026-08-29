import math
import pandas as pd
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# MOCK / SAMPLE DATA
# Same structure as Predictor.py for standalone testing.
# Later this will come from APIs, sensors, or databases.
# ---------------------------------------------------------------------------

# SAMPLE_STREET = {
#     "location_id": "RD-001",
#     "location_name": "Sample Street A (imaginary)",
#     "latitude": 19.0000,
#     "longitude": 72.8000,
#     "age_years": 2,
#     "years_since_maintenance": 2,
#     "population_density": 18500,
#     "avg_population_density": 12000,
#     "elevation": 8,
#     "slope": 1.2,
#     "imperviousness": 0.82,
#     "drainage_capacity": 50,
# }


# ---------------------------------------------------------------------------
# SIMULATED REAL-TIME WEATHER DATA
#
# Each dictionary represents a new observation.
# Today: mock data
# Future: Weather API / sensors / government database
# ---------------------------------------------------------------------------

# MOCK_REALTIME_DATA = [
#     {
#         "timestamp": "10:00",
#         "rainfall": 70,
#         "water_level": 0.35,
#         "soil_saturation": 0.40,
#         "lightning": False,
#     },
#     {
#         "timestamp": "10:10",
#         "rainfall": 85,
#         "water_level": 0.42,
#         "soil_saturation": 0.46,
#         "lightning": False,
#     },
#     {
#         "timestamp": "10:20",
#         "rainfall": 100,
#         "water_level": 0.60,
#         "soil_saturation": 0.55,
#         "lightning": True,
#     },
# ]

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


class AnalyserDatasetLoader:
    """
    Loads location and environmental observations
    from flood_features.csv.
    """

    def __init__(self):
        self.df = pd.read_csv(
            FEATURES_FILE
        )

    def get_street(
        self,
        location_id: str
    ) -> dict:

        row = self.df[
            self.df["location_id"] == location_id
        ]

        if row.empty:
            raise ValueError(
                f"Location {location_id} not found"
            )

        row = row.iloc[0]

        return {
            "location_id": row["location_id"],
            "location_name": row["location_name"],

            "slope": float(row["slope"]),
            "imperviousness": float(
                row["imperviousness"]
            ),
            "drainage_capacity": float(
                row["drainage_capacity"]
            ),

            # Temporary defaults until the final
            # infrastructure dataset is available.
            "years_since_maintenance": 2,
        }

    def get_observation(
        self,
        location_id: str
    ) -> dict:

        row = self.df[
            self.df["location_id"] == location_id
        ]

        if row.empty:
            raise ValueError(
                f"Location {location_id} not found"
            )

        row = row.iloc[0]

        return {
            "timestamp":
                datetime.now().isoformat(),

            "rainfall":
                float(row["rainfall"]),

            "water_level":
                float(row["water_level"]),

            "soil_saturation":
                float(row["soil_saturation"]),

            # Not currently present in dataset.
            "lightning": False,
        }

    def get_all_observations(self) -> list:
        """
        Returns observations for all locations.
        Useful for multi-location analysis later.
        """

        observations = []

        for _, row in self.df.iterrows():

            observations.append({
                "location_id":
                    row["location_id"],

                "timestamp":
                    datetime.now().isoformat(),

                "rainfall":
                    float(row["rainfall"]),

                "water_level":
                    float(row["water_level"]),

                "soil_saturation":
                    float(
                        row["soil_saturation"]
                    ),

                "lightning": False,
            })

        return observations

# ---------------------------------------------------------------------------
# CLASS 1 -- DataValidator
# Checks that incoming real-time data is valid before analysis.
# ---------------------------------------------------------------------------

class DataValidator:

    @staticmethod
    def validate_weather(data: dict) -> bool:

        required_fields = [
            "rainfall",
            "water_level",
            "soil_saturation",
            "lightning",
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing weather field: {field}")

        if data["rainfall"] < 0:
            raise ValueError("Rainfall cannot be negative")

        if not 0 <= data["water_level"] <= 1:
            raise ValueError("Water level must be between 0 and 1")

        if not 0 <= data["soil_saturation"] <= 1:
            raise ValueError("Soil saturation must be between 0 and 1")

        return True


# ---------------------------------------------------------------------------
# CLASS 2 -- EMAProcessor
#
# Exponential Moving Average:
#
# EMA(t) = alpha * current_value
#          + (1 - alpha) * previous_EMA
#
# Used to reduce noise in continuously arriving real-time data.
# ---------------------------------------------------------------------------

class EMAProcessor:

    def __init__(self, alpha=0.4):
        self.alpha = alpha
        self.previous_values = {}

    def update(self, name: str, current_value: float) -> float:

        # First observation:
        # No previous value exists, so current value becomes EMA.
        if name not in self.previous_values:

            ema = current_value

        else:

            previous_ema = self.previous_values[name]

            ema = (
                self.alpha * current_value
                + (1 - self.alpha) * previous_ema
            )

        self.previous_values[name] = ema

        return round(ema, 3)


# ---------------------------------------------------------------------------
# CLASS 3 -- TrendAnalyzer
#
# Calculates Rate of Change:
#
# rate = current_value - previous_value
#
# Classifies:
# Rising / Falling / Stable
# ---------------------------------------------------------------------------

class TrendAnalyzer:

    def __init__(self, threshold=0.02):
        self.previous_values = {}
        self.threshold = threshold

    def analyze(self, name: str, current_value: float) -> dict:

        if name not in self.previous_values:

            self.previous_values[name] = current_value

            return {
                "change": 0,
                "trend": "Initial"
            }

        previous_value = self.previous_values[name]

        change = current_value - previous_value

        if change > self.threshold:
            trend = "Rising"

        elif change < -self.threshold:
            trend = "Falling"

        else:
            trend = "Stable"

        self.previous_values[name] = current_value

        return {
            "change": round(change, 3),
            "trend": trend
        }


# ---------------------------------------------------------------------------
# CLASS 4 -- FloodConditionAnalyzer
#
# Creates a scientific Flood Condition Index (FCI).
#
# Formula:
#
# FCI =
# rainfall_score * 0.35
# water_level    * 0.30
# soil_sat       * 0.20
# drainage_stress* 0.15
#
# Final value = 0 to 100
# ---------------------------------------------------------------------------

class FloodConditionAnalyzer:

    def __init__(self, street: dict):
        self.street = street

    def calculate_drainage_stress(
        self,
        rainfall: float,
        soil_saturation: float
    ) -> dict:

        # Flatter roads retain more surface water.
        slope_factor = 1 - min(
            self.street["slope"] / 10,
            1
        )

        # Simplified runoff coefficient.
        runoff_coefficient = min(
            0.5 * self.street["imperviousness"]
            + 0.2 * slope_factor
            + 0.3 * soil_saturation,
            1.0
        )

        # Estimated surface runoff.
        surface_runoff = rainfall * runoff_coefficient

        # Drainage loses 5% capacity per year without maintenance.
        maintenance_loss = (
            0.05
            * self.street["years_since_maintenance"]
        )

        maintenance_factor = max(
            1 - maintenance_loss,
            0.5
        )

        effective_capacity = (
            self.street["drainage_capacity"]
            * maintenance_factor
        )

        # How much of drainage capacity is being used.
        drainage_stress = min(
            surface_runoff / effective_capacity,
            1.0
        )

        excess_water = max(
            surface_runoff - effective_capacity,
            0
        )

        return {
            "runoff_coefficient":
                round(runoff_coefficient, 3),

            "surface_runoff":
                round(surface_runoff, 2),

            "effective_drainage_capacity":
                round(effective_capacity, 2),

            "drainage_stress":
                round(drainage_stress, 3),

            "excess_water":
                round(excess_water, 2)
        }

    @staticmethod
    def calculate_fci(
        rainfall: float,
        water_level: float,
        soil_saturation: float,
        drainage_stress: float
    ) -> float:

        # Normalize rainfall.
        rainfall_score = min(
            rainfall / 150,
            1.0
        )

        # Flood Condition Index.
        fci = (
            rainfall_score * 0.35
            + water_level * 0.30
            + soil_saturation * 0.20
            + drainage_stress * 0.15
        ) * 100

        return round(fci, 2)

    @staticmethod
    def classify_condition(fci: float) -> str:

        if fci < 25:
            return "Normal"

        elif fci < 50:
            return "Watch"

        elif fci < 75:
            return "Warning"

        return "Severe"


# ---------------------------------------------------------------------------
# CLASS 5 -- RealtimeAnalyser
#
# Main orchestrator.
#
# Input:
#     new real-time weather observation
#
# Processing:
#     Validation
#     ↓
#     EMA smoothing
#     ↓
#     Trend detection
#     ↓
#     Drainage analysis
#     ↓
#     Flood Condition Index
#
# Output:
#     Clean analysed data
#
# Tomorrow:
#     This output will be passed directly to Predictor.py
# ---------------------------------------------------------------------------

class RealtimeAnalyser:

    def __init__(
        self,
        street: dict,
        alpha=0.4
    ):

        self.street = street

        self.validator = DataValidator()

        self.ema = EMAProcessor(
            alpha=alpha
        )

        self.trend_analyzer = TrendAnalyzer()

        self.flood_analyzer = (
            FloodConditionAnalyzer(street)
        )

    def analyse(
        self,
        realtime_data: dict
    ) -> dict:

        # ---------------------------------------------------------------
        # STEP 1 -- Validate incoming data
        # ---------------------------------------------------------------

        self.validator.validate_weather(
            realtime_data
        )

        # ---------------------------------------------------------------
        # STEP 2 -- Smooth real-time data using EMA
        # ---------------------------------------------------------------

        rainfall_smoothed = self.ema.update(
            "rainfall",
            realtime_data["rainfall"]
        )

        water_level_smoothed = self.ema.update(
            "water_level",
            realtime_data["water_level"]
        )

        soil_saturation_smoothed = self.ema.update(
            "soil_saturation",
            realtime_data["soil_saturation"]
        )

        # ---------------------------------------------------------------
        # STEP 3 -- Analyze trends
        # ---------------------------------------------------------------

        rainfall_trend = (
            self.trend_analyzer.analyze(
                "rainfall",
                rainfall_smoothed
            )
        )

        water_level_trend = (
            self.trend_analyzer.analyze(
                "water_level",
                water_level_smoothed
            )
        )

        soil_trend = (
            self.trend_analyzer.analyze(
                "soil_saturation",
                soil_saturation_smoothed
            )
        )

        # ---------------------------------------------------------------
        # STEP 4 -- Analyze drainage
        # ---------------------------------------------------------------

        drainage_analysis = (
            self.flood_analyzer
            .calculate_drainage_stress(
                rainfall_smoothed,
                soil_saturation_smoothed
            )
        )

        # ---------------------------------------------------------------
        # STEP 5 -- Calculate Flood Condition Index
        # ---------------------------------------------------------------

        fci = (
            self.flood_analyzer
            .calculate_fci(
                rainfall=rainfall_smoothed,
                water_level=water_level_smoothed,
                soil_saturation=soil_saturation_smoothed,
                drainage_stress=
                    drainage_analysis[
                        "drainage_stress"
                    ]
            )
        )

        condition = (
            self.flood_analyzer
            .classify_condition(fci)
        )

        # ---------------------------------------------------------------
        # STEP 6 -- Overall trend
        # ---------------------------------------------------------------

        rising_count = sum([
            rainfall_trend["trend"] == "Rising",
            water_level_trend["trend"] == "Rising",
            soil_trend["trend"] == "Rising",
        ])

        falling_count = sum([
            rainfall_trend["trend"] == "Falling",
            water_level_trend["trend"] == "Falling",
            soil_trend["trend"] == "Falling",
        ])

        if rising_count >= 2:
            overall_trend = "Deteriorating"

        elif falling_count >= 2:
            overall_trend = "Improving"

        else:
            overall_trend = "Stable"

        # ---------------------------------------------------------------
        # FINAL ANALYSED OUTPUT
        # ---------------------------------------------------------------

        return {

            "location_id":
                self.street["location_id"],

            "timestamp":
                realtime_data.get(
                    "timestamp",
                    datetime.now().isoformat()
                ),

            # -----------------------------------------------------------
            # Raw data
            # -----------------------------------------------------------

            "rainfall_raw":
                realtime_data["rainfall"],

            "water_level_raw":
                realtime_data["water_level"],

            "soil_saturation_raw":
                realtime_data["soil_saturation"],

            "lightning":
                realtime_data["lightning"],

            # -----------------------------------------------------------
            # Smoothed data
            # -----------------------------------------------------------

            "rainfall_smoothed":
                rainfall_smoothed,

            "water_level_smoothed":
                water_level_smoothed,

            "soil_saturation_smoothed":
                soil_saturation_smoothed,

            # -----------------------------------------------------------
            # Trends
            # -----------------------------------------------------------

            "rainfall_trend":
                rainfall_trend["trend"],

            "rainfall_change":
                rainfall_trend["change"],

            "water_level_trend":
                water_level_trend["trend"],

            "water_level_change":
                water_level_trend["change"],

            "soil_saturation_trend":
                soil_trend["trend"],

            "soil_saturation_change":
                soil_trend["change"],

            # -----------------------------------------------------------
            # Drainage analysis
            # -----------------------------------------------------------

            **drainage_analysis,

            # -----------------------------------------------------------
            # Flood condition
            # -----------------------------------------------------------

            "flood_condition_index":
                fci,

            "condition":
                condition,

            "overall_trend":
                overall_trend
        }

def analyse_location_from_dataset(location_id:str)-> dict:
    """Analyse one location directly
       from flood_features.csv"""

    loader= AnalyserDatasetLoader()
    street= loader.get_street(location_id)

    observation = loader.get_observation(location_id)

    analyser=RealtimeAnalyser(street=street,alpha=0.4)

    return analyser.analyse(observation)
# ---------------------------------------------------------------------------
# DEMO
#
# Simulates data continuously arriving at the analyser.
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    result=analyse_location_from_dataset("L001")

    print("\n ANALYSIS RESULT\n")

    for key,value in result.items():
        print(f"{key}:{value}")
   
