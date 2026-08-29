import pandas as pd


# ---------------------------------------------------------------------------
# SAMPLE / IMAGINARY INPUT DATA
# TODO: Replace with real data / API data later
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


# Forecast points
FORECAST_INTERVALS = [
    0,
    30,
    60,
    120,
    180,
]


# ---------------------------------------------------------------------------
# CLASS 1 -- FactorAnalyzer
# ---------------------------------------------------------------------------

class FactorAnalyzer:

    """
    Converts street and weather data into
    normalized flood-risk factors.
    """

    WEIGHTS = {
        "rainfall_intensity": 0.25,
        "runoff_ratio": 0.20,
        "drainage_deficit": 0.20,
        "soil_saturation": 0.10,
        "imperviousness": 0.10,
        "infrastructure_condition": 0.10,
        "population_density_impact": 0.05,
    }


    def __init__(
        self,
        street: dict,
        weather: dict,
    ):

        self.street = street
        self.weather = weather


    def _maintenance_factor(self) -> float:

        """
        Drainage capacity decreases when
        maintenance has not been performed.
        """

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
        # NORMALIZED RISK FACTORS
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
                    self.WEIGHTS[
                        name
                    ],

            }

            for name, value

            in values.items()

        }


        # ------------------------------------------------
        # RAW PHYSICAL VALUES
        # ------------------------------------------------

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
# CLASS 2 -- RiskAggregator
# ---------------------------------------------------------------------------

class RiskAggregator:


    def __init__(
        self,
        analyzer: FactorAnalyzer,
    ):

        self.analyzer = analyzer


    # ------------------------------------------------
    # CLASSIFY RISK
    # ------------------------------------------------

    @staticmethod
    def _classify(
        risk_score: float,
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
        Dynamic rainfall forecast.

        Severe conditions can continue increasing,
        while low rainfall conditions recede.
        """

        street = self.analyzer.street

        weather = self.analyzer.weather


        drainage_pressure = (

            weather["water_level"]

            +

            weather["soil_saturation"]

            +

            street["imperviousness"]

        ) / 3


        # ---------------------------------------------
        # SEVERE CONDITIONS
        # ---------------------------------------------

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


        # ---------------------------------------------
        # MODERATE CONDITIONS
        # ---------------------------------------------

        elif base_rainfall >= 40:

            trend = {

                0: 1.00,

                30: 1.02,

                60: 1.05,

                120: 0.95,

                180: 0.80,

            }


        # ---------------------------------------------
        # LOW CONDITIONS
        # ---------------------------------------------

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
    # CALCULATE RISK AT A SPECIFIC TIME
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


        # ---------------------------------------------
        # BASE WEIGHTED RISK SCORE
        # ---------------------------------------------

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


        # ---------------------------------------------
        # FLOOD ACCUMULATION PRESSURE
        # ---------------------------------------------

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


        # Drainage overload

        if drainage_used >= 1.0:

            accumulation_pressure += min(

                (
                    drainage_used
                    - 1.0
                )

                * 15,

                15,

            )


        # Excess water accumulation

        if excess_water >= 20:

            accumulation_pressure += min(

                excess_water / 10,

                10,

            )


        # Longer flooding duration

        if minutes >= 60:

            accumulation_pressure += 3


        if minutes >= 120:

            accumulation_pressure += 5


        if minutes >= 180:

            accumulation_pressure += 5


        # ---------------------------------------------
        # FINAL SCORE
        # ---------------------------------------------

        risk_score += (

            accumulation_pressure

        )


        risk_score = round(

            min(
                risk_score,
                100,
            ),

            1,

        )


        risk_level = (

            self._classify(
                risk_score
            )

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
    # GENERATE COMPLETE FORECAST
    # ------------------------------------------------

    def forecast(
        self,
        intervals=None,
    ) -> list:

        intervals = (

            intervals

            or

            FORECAST_INTERVALS

        )


        results = [

            self.score_at(
                minutes
            )

            for minutes

            in intervals

        ]


        # ---------------------------------------------
        # DETERMINE TREND
        # ---------------------------------------------

        for i, row in enumerate(
            results
        ):

            # NOW

            if i == 0:

                row[
                    "prediction_status"
                ] = "Stable"

                continue


            previous = (

                results[
                    i - 1
                ]

            )


            delta = (

                row[
                    "risk_score"
                ]

                -

                previous[
                    "risk_score"
                ]

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
# CLASS 3 -- PredictorIO
# ---------------------------------------------------------------------------

class PredictorIO:


    def __init__(
        self,
        street: dict,
        weather: dict,
    ):

        self.street = street

        self.weather = weather


        self.analyzer = (

            FactorAnalyzer(
                street,
                weather,
            )

        )


        self.aggregator = (

            RiskAggregator(
                self.analyzer
            )

        )


    def run(
        self,
    ) -> pd.DataFrame:

        """
        Runs the complete flood prediction
        and returns a pandas DataFrame.
        """

        rows = (

            self.aggregator.forecast()

        )


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

            self.weather[
                "lightning"
            ]

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
        self,
    ) -> list:

        """
        Returns prediction as list of dictionaries.
        Used by Flask API.
        """

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
) -> list:

    """
    Generate complete flood forecast
    for one location.
    """

    predictor = PredictorIO(
        street,
        weather,
    )


    return (

        predictor
        .to_dict_records()

    )


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    predictor = PredictorIO(

        SAMPLE_STREET,

        SAMPLE_WEATHER,

    )


    forecast_df = (

        predictor.run()

    )


    pd.set_option(
        "display.max_columns",
        None,
    )


    pd.set_option(
        "display.width",
        140,
    )


    print(

        forecast_df.to_string(
            index=False
        )

    )