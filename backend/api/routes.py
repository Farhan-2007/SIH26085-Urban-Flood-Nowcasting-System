from flask import Blueprint, request, jsonify
from routing.routing_engine import build_routing_report
from .validator import validate_flood_input
from backend.flood_engine import predict_flood_risk
from backend.data_loader import get_location

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

    try:
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
        # Step 1: Get location/street data
        location_id = data.get("location_id")

        if location_id:
            street_data = get_location(location_id)

            if not street_data:
                return jsonify({
                    "error": f"Location '{location_id}' not found"
                }), 404
        else:
            street_data = data.get("street", SAMPLE_STREET)

        # Step 2: Create analyser for this location
        # Step 2: Get persistent analyser for this location
        analyser_key = street_data["location_id"]

        # Create analyser only if this location has not been analysed before
        if analyser_key not in analysers:
            analysers[analyser_key] = RealtimeAnalyser(
                street_data,
                alpha=0.4
            )

        # Reuse the existing analyser
        analyser = analysers[analyser_key]

        # Step 3: Analyse conditions
        analysis_result = analyser.analyse(data)

        # Step 4: Create weather data
        analysed_weather = {
            "rainfall": analysis_result["rainfall_smoothed"],
            "lightning": analysis_result["lightning"],
            "water_level": analysis_result["water_level_smoothed"],
            "soil_saturation": analysis_result["soil_saturation_smoothed"],
        }

        # Step 5: Generate forecast
        forecast_result = predict_flood_forecast(
            street=street_data,
            weather=analysed_weather
        )

        # Step 6: Return results
        return jsonify({
            "analysis": analysis_result,
            "forecast": forecast_result
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