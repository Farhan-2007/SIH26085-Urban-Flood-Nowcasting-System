from flask import Blueprint, request, jsonify

from .validator import validate_flood_input
from flood_engine import predict_flood_risk


api = Blueprint("api", __name__)


@api.route("/predict", methods=["POST"])
def predict():

    # Get JSON data from the request
    data = request.get_json()

    # Check if request contains data
    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    # Validate input data
    valid, error = validate_flood_input(data)

    if not valid:
        return jsonify({
            "error": error
        }), 400

    # Send validated data to Flood Engine
    result = predict_flood_risk(
        rainfall=data["rainfall"],
        rainfall_intensity=data["rainfall_intensity"],
        water_level=data["water_level"],
        forecast_rainfall=data["forecast_rainfall"]
    )

    # Return prediction
    return jsonify(result), 200