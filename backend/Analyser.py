import pandas as pd

from datetime import datetime
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)


FEATURES_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "processed"
    / "flood_features.csv"
)


# ============================================================
# DATASET LOADER
# ============================================================

class AnalyserDatasetLoader:

    """
    Loads environmental and flood data
    from flood_features.csv.
    """

    def __init__(self):

        if not FEATURES_FILE.exists():

            raise FileNotFoundError(

                f"flood_features.csv not found at:\n"
                f"{FEATURES_FILE}"

            )

        if FEATURES_FILE.stat().st_size == 0:

            raise ValueError(

                "flood_features.csv is empty. "
                "Please add the CSV data."

            )

        try:

            self.df = pd.read_csv(
                FEATURES_FILE
            )

        except pd.errors.EmptyDataError:

            raise ValueError(

                "No columns to parse from file. "
                "flood_features.csv is empty or invalid."

            )

        # Remove accidental empty rows
        self.df = self.df.dropna(
            how="all"
        )

        # Required columns
        required_columns = [

            "location_id",
            "location_name",

            "rainfall",
            "water_level",
            "soil_saturation",

            "slope",
            "imperviousness",
            "drainage_capacity",

        ]

        missing_columns = [

            column

            for column
            in required_columns

            if column
            not in self.df.columns

        ]

        if missing_columns:

            raise ValueError(

                "Missing required columns in "
                "flood_features.csv: "

                + ", ".join(
                    missing_columns
                )

            )


    # ========================================================
    # GET STREET DATA
    # ========================================================

    def get_street(
        self,
        location_id: str
    ) -> dict:

        row = self.df[

            self.df[
                "location_id"
            ].astype(str)

            == str(
                location_id
            )

        ]

        if row.empty:

            raise ValueError(

                f"Location "
                f"{location_id} "
                f"not found"

            )

        row = row.iloc[0]

        return {

            "location_id":

                str(
                    row[
                        "location_id"
                    ]
                ),

            "location_name":

                str(
                    row[
                        "location_name"
                    ]
                ),

            "slope":

                float(
                    row[
                        "slope"
                    ]
                ),

            "imperviousness":

                float(
                    row[
                        "imperviousness"
                    ]
                ),

            "drainage_capacity":

                float(
                    row[
                        "drainage_capacity"
                    ]
                ),

            # Temporary value
            # until maintenance dataset is added

            "years_since_maintenance":

                2,

        }


    # ========================================================
    # GET OBSERVATION
    # ========================================================

    def get_observation(
        self,
        location_id: str
    ) -> dict:

        row = self.df[

            self.df[
                "location_id"
            ].astype(str)

            == str(
                location_id
            )

        ]

        if row.empty:

            raise ValueError(

                f"Location "
                f"{location_id} "
                f"not found"

            )

        row = row.iloc[0]

        return {

            "timestamp":

                datetime.now().isoformat(),

            "rainfall":

                float(
                    row[
                        "rainfall"
                    ]
                ),

            "water_level":

                float(
                    row[
                        "water_level"
                    ]
                ),

            "soil_saturation":

                float(
                    row[
                        "soil_saturation"
                    ]
                ),

            "lightning":

                False,

        }


    # ========================================================
    # GET ALL OBSERVATIONS
    # ========================================================

    def get_all_observations(
        self
    ) -> list:

        observations = []

        for _, row in self.df.iterrows():

            observations.append({

                "location_id":

                    str(
                        row[
                            "location_id"
                        ]
                    ),

                "timestamp":

                    datetime.now().isoformat(),

                "rainfall":

                    float(
                        row[
                            "rainfall"
                        ]
                    ),

                "water_level":

                    float(
                        row[
                            "water_level"
                        ]
                    ),

                "soil_saturation":

                    float(
                        row[
                            "soil_saturation"
                        ]
                    ),

                "lightning":

                    False,

            })

        return observations


# ============================================================
# DATA VALIDATOR
# ============================================================

class DataValidator:


    @staticmethod

    def validate_weather(
        data: dict
    ) -> bool:


        required_fields = [

            "rainfall",
            "water_level",
            "soil_saturation",
            "lightning",

        ]


        for field in required_fields:

            if field not in data:

                raise ValueError(

                    f"Missing weather field: "
                    f"{field}"

                )


        if data[
            "rainfall"
        ] < 0:

            raise ValueError(

                "Rainfall cannot be negative"

            )


        if not (

            0
            <= data[
                "water_level"
            ]
            <= 1

        ):

            raise ValueError(

                "Water level must be between "
                "0 and 1"

            )


        if not (

            0
            <= data[
                "soil_saturation"
            ]
            <= 1

        ):

            raise ValueError(

                "Soil saturation must be between "
                "0 and 1"

            )


        return True


# ============================================================
# EMA PROCESSOR
# ============================================================

class EMAProcessor:


    def __init__(
        self,
        alpha=0.4
    ):

        self.alpha = alpha

        self.previous_values = {}


    def update(
        self,
        name: str,
        current_value: float
    ) -> float:


        if name not in self.previous_values:

            ema = current_value


        else:

            previous_ema = (

                self.previous_values[
                    name
                ]

            )


            ema = (

                self.alpha
                * current_value

                +

                (
                    1
                    - self.alpha
                )

                * previous_ema

            )


        self.previous_values[
            name
        ] = ema


        return round(
            ema,
            3
        )


# ============================================================
# TREND ANALYSER
# ============================================================

class TrendAnalyzer:


    def __init__(
        self,
        threshold=0.02
    ):

        self.previous_values = {}

        self.threshold = threshold


    def analyze(
        self,
        name: str,
        current_value: float
    ) -> dict:


        if name not in self.previous_values:


            self.previous_values[
                name
            ] = current_value


            return {

                "change":

                    0,

                "trend":

                    "Initial",

            }


        previous_value = (

            self.previous_values[
                name
            ]

        )


        change = (

            current_value
            - previous_value

        )


        if change > self.threshold:

            trend = "Rising"


        elif change < -self.threshold:

            trend = "Falling"


        else:

            trend = "Stable"


        self.previous_values[
            name
        ] = current_value


        return {

            "change":

                round(
                    change,
                    3
                ),

            "trend":

                trend,

        }


# ============================================================
# FLOOD CONDITION ANALYSER
# ============================================================

class FloodConditionAnalyzer:


    def __init__(
        self,
        street: dict
    ):

        self.street = street


    # ========================================================
    # DRAINAGE STRESS
    # ========================================================

    def calculate_drainage_stress(

        self,

        rainfall: float,

        soil_saturation: float

    ) -> dict:


        # Flatter roads
        # retain more water

        slope_factor = (

            1

            - min(

                self.street[
                    "slope"
                ]

                / 10,

                1

            )

        )


        # Runoff coefficient

        runoff_coefficient = min(

            (

                0.5

                * self.street[
                    "imperviousness"
                ]

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

            1.0

        )


        # Surface runoff

        surface_runoff = (

            rainfall
            * runoff_coefficient

        )


        # Maintenance loss

        maintenance_loss = (

            0.05

            * self.street[
                "years_since_maintenance"
            ]

        )


        maintenance_factor = max(

            1
            - maintenance_loss,

            0.5

        )


        effective_capacity = (

            self.street[
                "drainage_capacity"
            ]

            * maintenance_factor

        )


        drainage_stress = min(

            surface_runoff
            / effective_capacity,

            1.0

        )


        excess_water = max(

            surface_runoff
            - effective_capacity,

            0

        )


        return {


            "runoff_coefficient":

                round(
                    runoff_coefficient,
                    3
                ),


            "surface_runoff":

                round(
                    surface_runoff,
                    2
                ),


            "effective_drainage_capacity":

                round(
                    effective_capacity,
                    2
                ),


            "drainage_stress":

                round(
                    drainage_stress,
                    3
                ),


            "excess_water":

                round(
                    excess_water,
                    2
                ),

        }


    # ========================================================
    # FLOOD CONDITION INDEX
    # ========================================================

    @staticmethod

    def calculate_fci(

        rainfall: float,

        water_level: float,

        soil_saturation: float,

        drainage_stress: float

    ) -> float:


        rainfall_score = min(

            rainfall
            / 150,

            1.0

        )


        fci = (

            (

                rainfall_score
                * 0.35

            )

            +

            (

                water_level
                * 0.30

            )

            +

            (

                soil_saturation
                * 0.20

            )

            +

            (

                drainage_stress
                * 0.15

            )

        ) * 100


        return round(
            fci,
            2
        )


    # ========================================================
    # CLASSIFY CONDITION
    # ========================================================

    @staticmethod

    def classify_condition(
        fci: float
    ) -> str:


        if fci < 25:

            return "Normal"


        elif fci < 50:

            return "Watch"


        elif fci < 75:

            return "Warning"


        return "Severe"


# ============================================================
# REALTIME ANALYSER
# ============================================================

class RealtimeAnalyser:


    def __init__(

        self,

        street: dict,

        alpha=0.4

    ):


        self.street = street


        self.validator = (
            DataValidator()
        )


        self.ema = (

            EMAProcessor(
                alpha=alpha
            )

        )


        self.trend_analyzer = (
            TrendAnalyzer()
        )


        self.flood_analyzer = (

            FloodConditionAnalyzer(
                street
            )

        )


    # ========================================================
    # ANALYSE
    # ========================================================

    def analyse(
        self,
        realtime_data: dict
    ) -> dict:


        # ----------------------------------------------------
        # STEP 1
        # VALIDATE
        # ----------------------------------------------------

        self.validator.validate_weather(

            realtime_data

        )


        # ----------------------------------------------------
        # STEP 2
        # EMA SMOOTHING
        # ----------------------------------------------------

        rainfall_smoothed = (

            self.ema.update(

                "rainfall",

                realtime_data[
                    "rainfall"
                ]

            )

        )


        water_level_smoothed = (

            self.ema.update(

                "water_level",

                realtime_data[
                    "water_level"
                ]

            )

        )


        soil_saturation_smoothed = (

            self.ema.update(

                "soil_saturation",

                realtime_data[
                    "soil_saturation"
                ]

            )

        )


        # ----------------------------------------------------
        # STEP 3
        # TREND ANALYSIS
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # STEP 4
        # DRAINAGE ANALYSIS
        # ----------------------------------------------------

        drainage_analysis = (

            self.flood_analyzer
            .calculate_drainage_stress(

                rainfall_smoothed,

                soil_saturation_smoothed

            )

        )


        # ----------------------------------------------------
        # STEP 5
        # FLOOD CONDITION INDEX
        # ----------------------------------------------------

        fci = (

            self.flood_analyzer
            .calculate_fci(

                rainfall=

                    rainfall_smoothed,


                water_level=

                    water_level_smoothed,


                soil_saturation=

                    soil_saturation_smoothed,


                drainage_stress=

                    drainage_analysis[
                        "drainage_stress"
                    ]

            )

        )


        condition = (

            self.flood_analyzer
            .classify_condition(

                fci

            )

        )


        # ----------------------------------------------------
        # STEP 6
        # OVERALL TREND
        # ----------------------------------------------------

        rising_count = sum([

            rainfall_trend[
                "trend"
            ] == "Rising",


            water_level_trend[
                "trend"
            ] == "Rising",


            soil_trend[
                "trend"
            ] == "Rising",

        ])


        falling_count = sum([

            rainfall_trend[
                "trend"
            ] == "Falling",


            water_level_trend[
                "trend"
            ] == "Falling",


            soil_trend[
                "trend"
            ] == "Falling",

        ])


        if rising_count >= 2:

            overall_trend = (
                "Deteriorating"
            )


        elif falling_count >= 2:

            overall_trend = (
                "Improving"
            )


        else:

            overall_trend = (
                "Stable"
            )


        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        return {


            "location_id":

                self.street[
                    "location_id"
                ],


            "timestamp":

                realtime_data.get(

                    "timestamp",

                    datetime.now()
                    .isoformat()

                ),


            # RAW DATA

            "rainfall_raw":

                realtime_data[
                    "rainfall"
                ],


            "water_level_raw":

                realtime_data[
                    "water_level"
                ],


            "soil_saturation_raw":

                realtime_data[
                    "soil_saturation"
                ],


            "lightning":

                realtime_data[
                    "lightning"
                ],


            # SMOOTHED DATA

            "rainfall_smoothed":

                rainfall_smoothed,


            "water_level_smoothed":

                water_level_smoothed,


            "soil_saturation_smoothed":

                soil_saturation_smoothed,


            # TRENDS

            "rainfall_trend":

                rainfall_trend[
                    "trend"
                ],


            "rainfall_change":

                rainfall_trend[
                    "change"
                ],


            "water_level_trend":

                water_level_trend[
                    "trend"
                ],


            "water_level_change":

                water_level_trend[
                    "change"
                ],


            "soil_saturation_trend":

                soil_trend[
                    "trend"
                ],


            "soil_saturation_change":

                soil_trend[
                    "change"
                ],


            # DRAINAGE

            **drainage_analysis,


            # FLOOD CONDITION

            "flood_condition_index":

                fci,


            "condition":

                condition,


            "overall_trend":

                overall_trend,

        }


# ============================================================
# ANALYSE LOCATION DIRECTLY
# ============================================================

def analyse_location_from_dataset(
    location_id: str
) -> dict:


    loader = (
        AnalyserDatasetLoader()
    )


    street = (
        loader.get_street(
            location_id
        )
    )


    observation = (
        loader.get_observation(
            location_id
        )
    )


    analyser = (

        RealtimeAnalyser(

            street=street,

            alpha=0.4

        )

    )


    return analyser.analyse(
        observation
    )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":


    result = (

        analyse_location_from_dataset(

            "L001"

        )

    )


    print(

        "\nANALYSIS RESULT\n"

    )


    for key, value in result.items():

        print(

            f"{key}: {value}"

        )