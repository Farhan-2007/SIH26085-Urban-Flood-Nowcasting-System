from flask import Blueprint, request, jsonify
from routing.routing_engine import build_routing_report
from .validator import validate_flood_input
from backend.flood_engine import predict_flood_risk

from backend.predictor import (
    DatasetLoader,
    predict_from_dataset,
    predict_flood_forecast,
)

from backend.Analyser import (
    AnalyserDatasetLoader,
    RealtimeAnalyser,
)


api = Blueprint("api", __name__)


# Persistent analyser for each location.
# This preserves EMA and trend history between requests.
analysers = {}


# ---------------------------------------------------------------------------
# Existing single-point flood prediction endpoint
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Full 0/30/60/120/180 minute forecast from dataset
# ---------------------------------------------------------------------------

@api.route("/forecast", methods=["GET"])
def forecast():

    location_id = request.args.get("location_id")

    if not location_id:
        return jsonify({
            "error": "location_id is required"
        }), 400

    try:

        results = predict_from_dataset(location_id)

        return jsonify({
            "location_id": location_id,
            "forecast": results
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ---------------------------------------------------------------------------
# Analyse current conditions and generate forecast
# ---------------------------------------------------------------------------

@api.route("/analyse", methods=["POST"])
def analyse():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    location_id = data.get("location_id")

    if not location_id:
        return jsonify({
            "error": "location_id is required"
        }), 400

    try:

        # ---------------------------------------------------------------
        # STEP 1: Load location data from dataset
        # ---------------------------------------------------------------

        analyser_loader = AnalyserDatasetLoader()

        street_data = analyser_loader.get_street(
            location_id
        )

        # ---------------------------------------------------------------
        # STEP 2: Get persistent analyser for this location
        # ---------------------------------------------------------------

        if location_id not in analysers:

            analysers[location_id] = RealtimeAnalyser(
                street=street_data,
                alpha=0.4
            )

        analyser = analysers[location_id]

        # ---------------------------------------------------------------
        # STEP 3: Use observation sent by API
        #
        # If rainfall/water_level/soil_saturation are not sent,
        # use the dataset values.
        # ---------------------------------------------------------------

        dataset_observation = (
            analyser_loader.get_observation(
                location_id
            )
        )

        observation = {
            "timestamp": data.get(
                "timestamp",
                dataset_observation["timestamp"]
            ),

            "rainfall": data.get(
                "rainfall",
                dataset_observation["rainfall"]
            ),

            "water_level": data.get(
                "water_level",
                dataset_observation["water_level"]
            ),

            "soil_saturation": data.get(
                "soil_saturation",
                dataset_observation["soil_saturation"]
            ),

            "lightning": data.get(
                "lightning",
                dataset_observation["lightning"]
            ),
        }

        # ---------------------------------------------------------------
        # STEP 4: Analyse current conditions
        # ---------------------------------------------------------------

        analysis_result = analyser.analyse(
            observation
        )

        # ---------------------------------------------------------------
        # STEP 5: Convert analysed output into Predictor weather input
        # ---------------------------------------------------------------

        analysed_weather = {
            "rainfall":
                analysis_result["rainfall_smoothed"],

            "water_level":
                analysis_result["water_level_smoothed"],

            "soil_saturation":
                analysis_result[
                    "soil_saturation_smoothed"
                ],

            "lightning":
                analysis_result["lightning"],
        }

        # ---------------------------------------------------------------
        # STEP 6: Load actual forecast rainfall data
        # ---------------------------------------------------------------

        predictor_loader = DatasetLoader()

        forecast_data = (
            predictor_loader.get_forecast(
                location_id
            )
        )

        # ---------------------------------------------------------------
        # STEP 7: Generate flood forecast
        # ---------------------------------------------------------------

        forecast_result = predict_flood_forecast(
            street=street_data,
            weather=analysed_weather,
            forecast_data=forecast_data
        )

        # ---------------------------------------------------------------
        # STEP 8: Return results
        # ---------------------------------------------------------------

        return jsonify({
            "location_id": location_id,
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


# ---------------------------------------------------------------------------
# Routing endpoint
#
# Keep unchanged for now.
# It still uses routing mock data until the GIS member provides
# real road connectivity data.
# ---------------------------------------------------------------------------

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
