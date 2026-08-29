from flask import Blueprint, request, jsonify

from backend.routing.routing_engine import build_routing_report
from .validator import validate_flood_input
from backend.flood_engine import predict_flood_risk

from backend.data_loader import (
    get_location,
    get_all_locations,
)

from backend.predictor import (
    SAMPLE_STREET,
    SAMPLE_WEATHER,
    DatasetLoader,
    predict_from_dataset,
    predict_flood_forecast,
)

from backend.Analyser import (
    AnalyserDatasetLoader,
    RealtimeAnalyser,
)


api = Blueprint("api", __name__)


# Store one persistent analyser for each location
analysers = {}


# ============================================================
# SINGLE-POINT FLOOD PREDICTION
# ============================================================

@api.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    valid, error = validate_flood_input(data)

    if not valid:
        return jsonify({
            "error": error
        }), 400

    result = predict_flood_risk(
        rainfall=data["rainfall"],
        rainfall_intensity=data["rainfall_intensity"],
        water_level=data["water_level"],
        forecast_rainfall=data["forecast_rainfall"]
    )

    return jsonify(result), 200


# ============================================================
# FULL FLOOD FORECAST
# ============================================================

@api.route("/forecast", methods=["GET"])
def forecast():

    location_id = request.args.get("location_id")

    try:

        # ----------------------------------------------------
        # LOCATION-SPECIFIC DATASET FORECAST
        # ----------------------------------------------------

        if location_id:

            results = predict_from_dataset(
                location_id
            )

            return jsonify({
                "location_id": location_id,
                "forecast": results
            }), 200

        # ----------------------------------------------------
        # DEFAULT SAMPLE FORECAST
        # ----------------------------------------------------

        results = predict_flood_forecast(
            street=SAMPLE_STREET,
            weather=SAMPLE_WEATHER
        )

        return jsonify({
            "location_id":
                SAMPLE_STREET["location_id"],

            "forecast":
                results
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# ANALYSE CURRENT CONDITIONS
# ============================================================

@api.route("/analyse", methods=["POST"])
def analyse():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    location_id = data.get(
        "location_id",
        "L001"
    )

    try:

        # ----------------------------------------------------
        # STEP 1: Load location from dataset
        # ----------------------------------------------------

        analyser_loader = AnalyserDatasetLoader()

        predictor_loader = DatasetLoader()

        # Full street data required by Predictor
        street_data = predictor_loader.get_street(
            location_id
        )

        # ----------------------------------------------------
        # STEP 2: Create/get persistent analyser
        # ----------------------------------------------------

        if location_id not in analysers:

            analysers[location_id] = (
                RealtimeAnalyser(
                    street=street_data,
                    alpha=0.4
                )
            )

        analyser = analysers[
            location_id
        ]

        # ----------------------------------------------------
        # STEP 3: Load dataset observation
        # ----------------------------------------------------

        dataset_observation = (
            analyser_loader.get_observation(
                location_id
            )
        )

        # ----------------------------------------------------
        # STEP 4: Allow frontend to override live values
        # ----------------------------------------------------

        observation = {

            "timestamp":
                data.get(
                    "timestamp",
                    dataset_observation.get(
                        "timestamp"
                    )
                ),

            "rainfall":
                data.get(
                    "rainfall",
                    dataset_observation[
                        "rainfall"
                    ]
                ),

            "water_level":
                data.get(
                    "water_level",
                    dataset_observation[
                        "water_level"
                    ]
                ),

            "soil_saturation":
                data.get(
                    "soil_saturation",
                    dataset_observation[
                        "soil_saturation"
                    ]
                ),

            "lightning":
                data.get(
                    "lightning",
                    dataset_observation.get(
                        "lightning",
                        False
                    )
                ),
        }

        # ----------------------------------------------------
        # STEP 5: Analyse conditions
        # ----------------------------------------------------

        analysis_result = (
            analyser.analyse(
                observation
            )
        )

        # ----------------------------------------------------
        # STEP 6: Convert analysed output to weather input
        # ----------------------------------------------------

        analysed_weather = {

            "rainfall":
                analysis_result[
                    "rainfall_smoothed"
                ],

            "water_level":
                analysis_result[
                    "water_level_smoothed"
                ],

            "soil_saturation":
                analysis_result[
                    "soil_saturation_smoothed"
                ],

            "lightning":
                analysis_result.get(
                    "lightning",
                    False
                ),
        }

        # ----------------------------------------------------
        # STEP 7: Load actual forecast rainfall
        # ----------------------------------------------------

        forecast_data = (
            predictor_loader.get_forecast(
                location_id
            )
        )

        # ----------------------------------------------------
        # STEP 8: Generate flood forecast
        # ----------------------------------------------------

        forecast_result = (
            predict_flood_forecast(
                street=street_data,
                weather=analysed_weather,
                forecast_data=forecast_data
            )
        )

        # ----------------------------------------------------
        # STEP 9: Return result
        # ----------------------------------------------------

        return jsonify({

            "location": {

                "location_id":
                    street_data[
                        "location_id"
                    ],

                "location_name":
                    street_data[
                        "location_name"
                    ],

                "latitude":
                    street_data[
                        "latitude"
                    ],

                "longitude":
                    street_data[
                        "longitude"
                    ],
            },

            "analysis":
                analysis_result,

            "forecast":
                forecast_result,

        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# ROUTING ENDPOINT
# ============================================================

@api.route("/routing", methods=["GET"])
def routing():

    start_id = request.args.get(
        "start_id"
    )

    end_id = request.args.get(
        "end_id"
    )

    forecast_minutes = request.args.get(
    "forecast_minutes",
    default=0,
    type=int
)

    if not start_id or not end_id:

        return jsonify({
            "error":
                "start_id and end_id are required"
        }), 400

    try:

        report = (
            build_routing_report(
                start_id=start_id,
                end_id=end_id,
                forecast_minutes=forecast_minutes
            )
        )

        valid_intervals = [
            0,
            30,
            60,
            120,
            180,
        ]

        if forecast_minutes not in valid_intervals:

            return jsonify({

                "error":
                    (
                        "forecast_minutes must be "
                        "0, 30, 60, 120, or 180"
                    )

            }), 400

        return jsonify(
            report
        ), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# ALL LOCATIONS RISK
# ============================================================

@api.route(
    "/locations/risk",
    methods=["GET"]
)
def get_locations_risk():

    try:

        forecast_minutes = (
            request.args.get(
                "forecast_minutes",
                default=0,
                type=int
            )
        )

        valid_intervals = [
            0,
            30,
            60,
            120,
            180
        ]

        if (
            forecast_minutes
            not in valid_intervals
        ):

            return jsonify({

                "error":
                    (
                        "forecast_minutes must be "
                        "one of 0, 30, 60, 120, or 180"
                    )

            }), 400

        locations = (
            get_all_locations()
        )

        results = []

        for location in locations:

            weather = {

                "rainfall":
                    location[
                        "rainfall"
                    ],

                "water_level":
                    location[
                        "water_level"
                    ],

                "soil_saturation":
                    location[
                        "soil_saturation"
                    ],

                "lightning":
                    False,
            }

            forecast = (
                predict_flood_forecast(
                    street=location,
                    weather=weather
                )
            )

            selected_prediction = (
                next(

                    (
                        item

                        for item in forecast

                        if item[
                            "forecast_minutes"
                        ]
                        == forecast_minutes
                    ),

                    None

                )
            )

            if selected_prediction:

                results.append({

                    "location_id":
                        location[
                            "location_id"
                        ],

                    "location_name":
                        location[
                            "location_name"
                        ],

                    "latitude":
                        location[
                            "latitude"
                        ],

                    "longitude":
                        location[
                            "longitude"
                        ],

                    "risk_score":
                        selected_prediction[
                            "risk_score"
                        ],

                    "risk_level":
                        selected_prediction[
                            "risk_level"
                        ],

                    "rainfall":
                        selected_prediction[
                            "rainfall"
                        ],

                    "surface_runoff":
                        selected_prediction[
                            "surface_runoff"
                        ],

                    "drainage_capacity_used":
                        selected_prediction[
                            "drainage_capacity_used"
                        ],

                    "forecast_minutes":
                        forecast_minutes,

                    "prediction_status":
                        selected_prediction[
                            "prediction_status"
                        ],
                })

        return jsonify({

            "forecast_minutes":
                forecast_minutes,

            "locations":
                results

        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# RAINFALL HISTORY
# ============================================================

@api.route(
    "/rainfall/history",
    methods=["GET"]
)
def get_rainfall_history():

    try:

        location_id = (
            request.args.get(
                "location_id",
                default="L001",
                type=str
            )
        )

        location = (
            get_location(
                location_id
            )
        )

        if not location:

            return jsonify({
                "error":
                    f"Location '{location_id}' not found"
            }), 404

        current_rainfall = (
            location["rainfall"]
        )

        history = [

            {
                "time": "-6h",
                "intensity":
                    round(
                        current_rainfall * 1.8,
                        1
                    )
            },

            {
                "time": "-5h",
                "intensity":
                    round(
                        current_rainfall * 2.2,
                        1
                    )
            },

            {
                "time": "-4h",
                "intensity":
                    round(
                        current_rainfall * 2.6,
                        1
                    )
            },

            {
                "time": "-3h",
                "intensity":
                    round(
                        current_rainfall * 2.3,
                        1
                    )
            },

            {
                "time": "-2h",
                "intensity":
                    round(
                        current_rainfall * 1.9,
                        1
                    )
            },

            {
                "time": "-1h",
                "intensity":
                    round(
                        current_rainfall * 1.4,
                        1
                    )
            },

            {
                "time": "NOW",
                "intensity":
                    current_rainfall
            },
        ]

        return jsonify({

            "location_id":
                location_id,

            "history":
                history

        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500