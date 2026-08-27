from flask import Blueprint, request, jsonify
from routing.routing_engine import build_routing_report
from .validator import validate_flood_input
from flood_engine import predict_flood_risk

from predictor import (
    SAMPLE_STREET,
    SAMPLE_WEATHER,
    predict_flood_forecast,
)


api = Blueprint("api", __name__)

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