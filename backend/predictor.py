import pandas as pd
from pathlib import Path


# ---------------------------------------------------------------------------
# SAMPLE DATA
# Used as fallback/demo data
# ---------------------------------------------------------------------------

SAMPLE_STREET = {
    "location_id": "RD-001",
    "location_name": "Sample Street A (imaginary)",
    "latitude": 19.0000,
    "longitude": 72.8000,

    "age_years": 2,
    "years_since_maintenance": 2,

    "population_density": 18500,
    "avg_population_density": 12000,

    "elevation": 8,
    "slope": 1.2,

    "imperviousness": 0.82,

    "drainage_capacity": 50,
}


SAMPLE_WEATHER = {
    "rainfall": 100,
    "lightning": True,
    "water_level": 0.6,
    "soil_saturation": 0.55,
}


# ---------------------------------------------------------------------------
# FORECAST INTERVALS
# ---------------------------------------------------------------------------

FORECAST_INTERVALS = [
    0,
    30,
    60,
    120,
    180,
]


# ---------------------------------------------------------------------------
# DATASET PATHS
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


# ---------------------------------------------------------------------------
# DATASET LOADER
# ---------------------------------------------------------------------------

class DatasetLoader:

    """
    Loads location/environmental data and forecast data
    from project CSV files.
    """

    def __init__(self):

        self.features_df = pd.read_csv(
            FEATURES_FILE
        )

        self.forecast_df = pd.read_csv(
            FORECAST_FILE
        )


    def get_street(
        self,
        location_id: str
    ) -> dict:

        row = self.features_df[
            self.features_df["location_id"]
            == location_id
        ]

        if row.empty:

            raise ValueError(
                f"Location {location_id} not found in dataset"
            )

        row = row.iloc[0]

        return {

            "location_id":
                row["location_id"],

            "location_name":
                row["location_name"],

            "latitude":
                float(row["latitude"]),

            "longitude":
                float(row["longitude"]),


            "elevation":
                float(row["elevation"]),

            "slope":
                float(row["slope"]),

            "imperviousness":
                float(row["imperviousness"]),

            "drainage_capacity":
                float(row["drainage_capacity"]),


            # Default values until dataset contains them
            "years_since_maintenance":
                2,

            "population_density":
                12000,

            "avg_population_density":
                12000,

        }


    def get_current_weather(
        self,
        location_id: str
    ) -> dict:

        row = self.features_df[
            self.features_df["location_id"]
            == location_id
        ]

        if row.empty:

            raise ValueError(
                f"Location {location_id} not found in dataset"
            )

        row = row.iloc[0]

        return {

            "rainfall":
                float(row["rainfall"]),

            "water_level":
                float(row["water_level"]),

            "soil_saturation":
                float(row["soil_saturation"]),

            "lightning":
                False,

        }


    def get_forecast(
        self,
        location_id: str
    ) -> list:

        rows = self.forecast_df[
            self.forecast_df["location_id"]
            == location_id
        ].sort_values(
            "forecast_minutes"
        )

        return rows.to_dict(
            orient="records"
        )


# ---------------------------------------------------------------------------
# FACTOR ANALYZER
# ---------------------------------------------------------------------------

class FactorAnalyzer:

    WEIGHTS = {

        "rainfall_intensity":
            0.25,

        "runoff_ratio":
            0.20,

        "drainage_deficit":
            0.20,

        "soil_saturation":
            0.10,

        "imperviousness":
            0.10,

        "infrastructure_condition":
            0.10,

        "population_density_impact":
            0.05,

    }


    def __init__(
        self,
        street: dict,
        weather: dict,
    ):

        self.street = street
        self.weather = weather


    def _maintenance_factor(
        self
    ) -> float:

        deficit = (

            0.05

            * self.street[
                "years_since_maintenance"
            ]

        )

        return max(
            1 - deficit,
            0.5,
        )


    def compute(
        self,
        rainfall: float,
        soil_saturation: float,
    ) -> dict:

        street = self.street


        # ------------------------------------------------
        # RUNOFF CALCULATION
        # ------------------------------------------------

        slope_factor = (

            1

            - min(
                street["slope"] / 10,
                1,
            )

        )


        runoff_coeff = min(

            (
                0.5
                * street["imperviousness"]
            )

            +

            (
                0.2
                * slope_factor
            )

            +

            (
                0.3
                * soil_saturation
            ),

            1.0,

        )


        surface_runoff = (

            rainfall
            * runoff_coeff

        )


        # ------------------------------------------------
        # DRAINAGE CAPACITY
        # ------------------------------------------------

        maintenance_factor = (

            self._maintenance_factor()

        )


        effective_drainage_capacity = (

            street["drainage_capacity"]

            * maintenance_factor

        )


        if effective_drainage_capacity:

            drainage_capacity_used = min(

                surface_runoff
                / effective_drainage_capacity,

                2.0,

            )

        else:

            drainage_capacity_used = 2.0


        excess_water = max(

            surface_runoff

            - effective_drainage_capacity,

            0,

        )


        # ------------------------------------------------
        # NORMALIZED VALUES
        # ------------------------------------------------

        values = {

            "rainfall_intensity":

                min(
                    rainfall / 150,
                    1.0,
                ),


            "runoff_ratio":

                min(
                    surface_runoff / 150,
                    1.0,
                ),


            "drainage_deficit":

                min(
                    excess_water / 100,
                    1.0,
                ),


            "soil_saturation":

                soil_saturation,


            "imperviousness":

                street[
                    "imperviousness"
                ],


            "infrastructure_condition":

                min(

                    (
                        1
                        - maintenance_factor
                    )

                    / 0.5,

                    1.0,

                ),


            "population_density_impact":

                min(

                    street[
                        "population_density"
                    ]

                    /

                    street[
                        "avg_population_density"
                    ]

                    /

                    2,

                    1.0,

                ),

        }


        factors = {

            name: {

                "value":
                    value,

                "weight":
                    self.WEIGHTS[name],

            }

            for name, value

            in values.items()

        }


        factors["_raw"] = {

            "surface_runoff":

                round(
                    surface_runoff,
                    2,
                ),


            "drainage_capacity_used":

                round(
                    drainage_capacity_used,
                    2,
                ),


            "effective_drainage_capacity":

                round(
                    effective_drainage_capacity,
                    2,
                ),


            "excess_water":

                round(
                    excess_water,
                    2,
                ),

        }


        return factors


# ---------------------------------------------------------------------------
# RISK AGGREGATOR
# ---------------------------------------------------------------------------

class RiskAggregator:


    def __init__(
        self,
        analyzer: FactorAnalyzer,
        forecast_data=None,
    ):

        self.analyzer = analyzer


        # Convert forecast CSV rows into dictionary
        self.forecast_data = {

            int(
                row["forecast_minutes"]
            ):

            float(
                row["rainfall"]
            )

            for row

            in (
                forecast_data
                or []
            )

        }


    @staticmethod
    def _classify(
        risk_score: float
    ) -> str:

        if risk_score < 25:
            return "Low"

        elif risk_score < 50:
            return "Moderate"

        elif risk_score < 75:
            return "High"

        return "Critical"


    # ------------------------------------------------
    # FORECAST RAINFALL
    # ------------------------------------------------

    def _rainfall_at(
        self,
        base_rainfall: float,
        minutes: int,
    ) -> float:

        """
        Uses actual dataset forecast when available.

        Otherwise uses the existing dynamic
        rainfall trend model.
        """

        if minutes in self.forecast_data:

            return float(
                self.forecast_data[
                    minutes
                ]
            )


        street = self.analyzer.street

        weather = self.analyzer.weather


        drainage_pressure = (

            weather["water_level"]

            +

            weather["soil_saturation"]

            +

            street["imperviousness"]

        ) / 3


        if (

            base_rainfall >= 80

            or

            drainage_pressure >= 0.75

        ):

            trend = {

                0: 1.00,
                30: 1.05,
                60: 1.10,
                120: 1.20,
                180: 1.10,

            }


        elif base_rainfall >= 40:

            trend = {

                0: 1.00,
                30: 1.02,
                60: 1.05,
                120: 0.95,
                180: 0.80,

            }


        else:

            trend = {

                0: 1.00,
                30: 0.90,
                60: 0.75,
                120: 0.55,
                180: 0.35,

            }


        return round(

            base_rainfall

            * trend.get(
                minutes,
                0.5,
            ),

            1,

        )


    # ------------------------------------------------
    # FORECAST SOIL SATURATION
    # ------------------------------------------------

    def _soil_saturation_at(
        self,
        base_saturation: float,
        minutes: int,
    ) -> float:

        rainfall = self._rainfall_at(

            self.analyzer.weather[
                "rainfall"
            ],

            minutes,

        )


        base_rainfall = (

            self.analyzer.weather[
                "rainfall"
            ]

        )


        rainfall_factor = min(

            rainfall

            /

            max(
                base_rainfall,
                1,
            ),

            1.5,

        )


        time_factor = (

            minutes
            / 180

        )


        increase = (

            0.25

            * rainfall_factor

            * time_factor

        )


        return min(

            base_saturation
            + increase,

            1.0,

        )


    # ------------------------------------------------
    # SCORE AT TIME
    # ------------------------------------------------

    def score_at(
        self,
        minutes: int,
    ) -> dict:

        rainfall = self._rainfall_at(

            self.analyzer.weather[
                "rainfall"
            ],

            minutes,

        )


        soil_saturation = (

            self._soil_saturation_at(

                self.analyzer.weather[
                    "soil_saturation"
                ],

                minutes,

            )

        )


        factors = self.analyzer.compute(

            rainfall,
            soil_saturation,

        )


        risk_score = (

            sum(

                factor["value"]

                * factor["weight"]

                for name, factor

                in factors.items()

                if name != "_raw"

            )

            * 100

        )


        drainage_used = (

            factors["_raw"][
                "drainage_capacity_used"
            ]

        )


        excess_water = (

            factors["_raw"][
                "excess_water"
            ]

        )


        accumulation_pressure = 0


        if drainage_used >= 1.0:

            accumulation_pressure += min(

                (
                    drainage_used
                    - 1.0
                )

                * 15,

                15,

            )


        if excess_water >= 20:

            accumulation_pressure += min(

                excess_water / 10,

                10,

            )


        if minutes >= 60:
            accumulation_pressure += 3

        if minutes >= 120:
            accumulation_pressure += 5

        if minutes >= 180:
            accumulation_pressure += 5


        risk_score += accumulation_pressure


        risk_score = round(

            min(
                risk_score,
                100,
            ),

            1,

        )


        risk_level = self._classify(
            risk_score
        )


        return {

            "forecast_minutes":
                minutes,

            "rainfall":
                rainfall,

            "risk_score":
                risk_score,

            "risk_level":
                risk_level,

            **factors["_raw"],

        }


    # ------------------------------------------------
    # COMPLETE FORECAST
    # ------------------------------------------------

    def forecast(
        self,
        intervals=None,
    ) -> list:

        intervals = (

            intervals
            or FORECAST_INTERVALS

        )


        results = [

            self.score_at(
                minutes
            )

            for minutes

            in intervals

        ]


        for i, row in enumerate(
            results
        ):

            if i == 0:

                row[
                    "prediction_status"
                ] = "Stable"

                continue


            previous = results[
                i - 1
            ]


            delta = (

                row["risk_score"]

                -

                previous["risk_score"]

            )


            if delta > 3:

                row[
                    "prediction_status"
                ] = "Intensifying"

            elif delta < -3:

                row[
                    "prediction_status"
                ] = "Receding"

            else:

                row[
                    "prediction_status"
                ] = "Stable"


        return results


# ---------------------------------------------------------------------------
# PREDICTOR IO
# ---------------------------------------------------------------------------

class PredictorIO:


    def __init__(
        self,
        street: dict,
        weather: dict,
        forecast_data=None,
    ):

        self.street = street
        self.weather = weather


        self.analyzer = FactorAnalyzer(
            street,
            weather,
        )


        self.aggregator = RiskAggregator(

            self.analyzer,

            forecast_data,

        )


    def run(
        self
    ) -> pd.DataFrame:

        rows = self.aggregator.forecast()


        df = pd.DataFrame(
            rows
        )


        df.insert(

            0,

            "location_name",

            self.street[
                "location_name"
            ],

        )


        df.insert(

            0,

            "location_id",

            self.street[
                "location_id"
            ],

        )


        df[
            "lightning"
        ] = (

            self.weather.get(
                "lightning",
                False,
            )

        )


        cols = [

            "location_id",
            "location_name",
            "forecast_minutes",
            "rainfall",
            "surface_runoff",
            "drainage_capacity_used",
            "excess_water",
            "risk_score",
            "risk_level",
            "prediction_status",
            "lightning",

        ]


        return df[
            cols
        ]


    def to_dict_records(
        self
    ) -> list:

        return (

            self.run()

            .to_dict(
                orient="records"
            )

        )


# ---------------------------------------------------------------------------
# API HELPER
# ---------------------------------------------------------------------------

def predict_flood_forecast(

    street: dict,

    weather: dict,

    forecast_data=None,

) -> list:


    predictor = PredictorIO(

        street=street,

        weather=weather,

        forecast_data=forecast_data,

    )


    return predictor.to_dict_records()


# ---------------------------------------------------------------------------
# DATASET PREDICTION
# ---------------------------------------------------------------------------

def predict_from_dataset(
    location_id: str
) -> list:


    loader = DatasetLoader()


    street = loader.get_street(
        location_id
    )


    weather = loader.get_current_weather(
        location_id
    )


    forecast_data = loader.get_forecast(
        location_id
    )


    predictor = PredictorIO(

        street=street,

        weather=weather,

        forecast_data=forecast_data,

    )


    return predictor.to_dict_records()


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    result = predict_from_dataset(
        "L001"
    )


    print(

        pd.DataFrame(
            result
        ).to_string(
            index=False
        )

    )