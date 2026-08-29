from flask import Blueprint, request, jsonify
from routing.routing_engine import build_routing_report
from .validator import validate_flood_input
from backend.flood_engine import predict_flood_risk
from backend.data_loader import get_location, get_all_locations

from backend.predictor import (
    SAMPLE_STREET,
    SAMPLE_WEATHER,
    predict_flood_forecast,
)

from backend.Analyser import RealtimeAnalyser

api = Blueprint("api", __name__)

# Store one persistent analyser for each location
analysers = {}

# Existing single-point prediction endpoint

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

# Full 0–3 hour forecast using predictor.py

@api.route("/forecast", methods=["GET"])
def forecast():

    location_id = request.args.get("location_id")

    try:

        # If location_id is provided, load that location
        if location_id:

            street_data = get_location(location_id)

            if not street_data:
                return jsonify({
                    "error": f"Location '{location_id}' not found"
                }), 404

            weather = {
                "rainfall": street_data["rainfall"],
                "lightning": False,
                "water_level": street_data["water_level"],
                "soil_saturation": street_data["soil_saturation"],
            }

            results = predict_flood_forecast(
                street=street_data,
                weather=weather
            )

            return jsonify({
                "location": {
                    "location_id": street_data["location_id"],
                    "location_name": street_data["location_name"],
                    "latitude": street_data["latitude"],
                    "longitude": street_data["longitude"],
                },
                "forecast": results
            }), 200

        # Default behaviour if no location_id is provided
        results = predict_flood_forecast(
            street=SAMPLE_STREET,
            weather=SAMPLE_WEATHER
        )

        return jsonify({
            "location": SAMPLE_STREET["location_name"],
            "forecast": results
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500
    
@api.route("/analyse", methods=["POST"])
def analyse():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    try:
        # ---------------------------------------------
        # STEP 1: Get selected location ID
        # ---------------------------------------------
        location_id = data.get(
            "location_id",
            "L001"
        )

        # ---------------------------------------------
        # STEP 2: Load selected location data
        # ---------------------------------------------
        street_data = get_location(
            location_id
        )

        if not street_data:
            return jsonify({
                "error":
                    f"Location '{location_id}' not found"
            }), 404

        # ---------------------------------------------
        # STEP 3: Create/get persistent analyser
        # ---------------------------------------------
        analyser_key = street_data[
            "location_id"
        ]

        if analyser_key not in analysers:
            analysers[analyser_key] = (
                RealtimeAnalyser(
                    street_data,
                    alpha=0.4
                )
            )

        analyser = analysers[
            analyser_key
        ]

        # ---------------------------------------------
        # STEP 4: Start with selected location's data
        # ---------------------------------------------
        analysis_input = {
            "rainfall":
                street_data.get(
                    "rainfall",
                    0
                ),

            "water_level":
                street_data.get(
                    "water_level",
                    0
                ),

            "soil_saturation":
                street_data.get(
                    "soil_saturation",
                    0
                ),

            "lightning": False,
        }

        # ---------------------------------------------
        # STEP 5: Allow live values from frontend
        # ---------------------------------------------
        allowed_fields = [
            "rainfall",
            "water_level",
            "soil_saturation",
            "lightning",
        ]

        for field in allowed_fields:

            if field in data:
                analysis_input[field] = (
                    data[field]
                )

        # ---------------------------------------------
        # STEP 6: Analyse current conditions
        # ---------------------------------------------
        analysis_result = (
            analyser.analyse(
                analysis_input
            )
        )

        # ---------------------------------------------
        # STEP 7: Use analysed values for prediction
        # ---------------------------------------------
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

        # ---------------------------------------------
        # STEP 8: Generate location-specific forecast
        # ---------------------------------------------
        forecast_result = (
            predict_flood_forecast(
                street=street_data,
                weather=analysed_weather
            )
        )

        # ---------------------------------------------
        # STEP 9: Return complete result
        # ---------------------------------------------
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

@api.route("/routing", methods=["GET"])
def routing():

    start_id = request.args.get("start_id")
    end_id = request.args.get("end_id")

    if not start_id or not end_id:
        return jsonify({
            "error": "start_id and end_id are required"
        }), 400

    try:
        report = build_routing_report(
            start_id=start_id,
            end_id=end_id
        )

        return jsonify(report), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500
    
@api.route("/locations/risk", methods=["GET"])
def get_locations_risk():

    try:
        # Get selected forecast time from frontend
        forecast_minutes = request.args.get(
            "forecast_minutes",
            default=0,
            type=int
        )

        # Only allow dashboard forecast intervals
        valid_intervals = [0, 60, 120, 180]

        if forecast_minutes not in valid_intervals:
            return jsonify({
                "error": (
                    "forecast_minutes must be one of "
                    "0, 60, 120, or 180"
                )
            }), 400


        locations = get_all_locations()

        results = []


        for location in locations:

            weather = {
                "rainfall": location["rainfall"],
                "water_level": location["water_level"],
                "soil_saturation":
                    location["soil_saturation"],
                "lightning": False,
            }


            # Generate complete forecast
            forecast = predict_flood_forecast(
                street=location,
                weather=weather
            )


            # Select prediction for requested time
            selected_prediction = next(
                (
                    item
                    for item in forecast
                    if item["forecast_minutes"]
                    == forecast_minutes
                ),
                None
            )


            if selected_prediction:

                results.append({

                    "location_id":
                        location["location_id"],

                    "location_name":
                        location["location_name"],

                    "latitude":
                        location["latitude"],

                    "longitude":
                        location["longitude"],


                    # Dynamic risk values
                    "risk_score":
                        selected_prediction["risk_score"],

                    "risk_level":
                        selected_prediction["risk_level"],


                    # Dynamic forecast values
                    "rainfall":
                        selected_prediction["rainfall"],

                    "surface_runoff":
                        selected_prediction[
                            "surface_runoff"
                        ],

                    "drainage_capacity_used":
                        selected_prediction[
                            "drainage_capacity_used"
                        ],

                    # Useful for frontend
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
    
@api.route("/rainfall/history", methods=["GET"])
def get_rainfall_history():

    try:
        location_id = request.args.get(
            "location_id",
            default="L001",
            type=str
        )

        location = get_location(location_id)

        if not location:
            return jsonify({
                "error": f"Location '{location_id}' not found"
            }), 404


        current_rainfall = location["rainfall"]


        # Historical rainfall pattern.
        # Rainfall was higher earlier and has
        # decreased toward the current value.
        history = [

            {
                "time": "-6h",
                "intensity": round(
                    current_rainfall * 1.8,
                    1
                )
            },

            {
                "time": "-5h",
                "intensity": round(
                    current_rainfall * 2.2,
                    1
                )
            },

            {
                "time": "-4h",
                "intensity": round(
                    current_rainfall * 2.6,
                    1
                )
            },

            {
                "time": "-3h",
                "intensity": round(
                    current_rainfall * 2.3,
                    1
                )
            },

            {
                "time": "-2h",
                "intensity": round(
                    current_rainfall * 1.9,
                    1
                )
            },

            {
                "time": "-1h",
                "intensity": round(
                    current_rainfall * 1.4,
                    1
                )
            },

            {
                "time": "NOW",
                "intensity": current_rainfall
            },

        ]


        return jsonify({
            "location_id": location_id,
            "history": history
        }), 200


    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500