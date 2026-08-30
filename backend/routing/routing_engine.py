"""
routing_engine.py
------------------

Safe Route Intelligence engine.

Uses real Urban Flood dataset locations while keeping the
existing road network and risk-routing logic.
"""

from .road_network import RoadNetwork
from .affected_roads import (
    get_affected_roads,
    get_shifting_risk,
)
from .safer_route import find_safer_route

from .mock_data import MOCK_ROADS

from backend.predictor import (
    predict_from_dataset,
)

from backend.data_loader import (
    get_all_locations,
)


# ============================================================
# NORMALIZE REAL LOCATIONS FOR ROUTING ENGINE
# ============================================================

def normalize_locations_for_routing(locations):

    normalized_locations = []

    for location in locations:

        normalized_locations.append({

            # RoadNetwork expects these fields
            "id":
                location["location_id"],

            "name":
                location["location_name"],


            # Keep original fields as well
            "location_id":
                location["location_id"],

            "location_name":
                location["location_name"],

            "latitude":
                location["latitude"],

            "longitude":
                location["longitude"],

        })

    return normalized_locations


# ============================================================
# BUILD REAL RISK DATA FROM PREDICTOR
# ============================================================

def build_real_risk_data(
    forecast_minutes=0
):

    real_locations = get_all_locations()

    risk_data = {}

    for location in real_locations:

        location_id = location["location_id"]

        predictions = predict_from_dataset(
            location_id
        )

        # Select prediction for requested time
        selected_prediction = next(
            (
                prediction
                for prediction in predictions
                if prediction["forecast_minutes"]
                == forecast_minutes
            ),
            None,
        )

        if selected_prediction is None:
            continue

        risk_data[location_id] = {

            "risk_score":
                selected_prediction[
                    "risk_score"
                ],

            "risk_level":
                selected_prediction[
                    "risk_level"
                ],

            "trend":
                selected_prediction[
                    "prediction_status"
                ],
        }

    return risk_data

# ============================================================
# LOAD ROUTING INPUTS
# ============================================================

def load_routing_inputs(forecast_minutes=0):

    # Load actual Mumbai locations
    real_locations = get_all_locations()


    # Convert location_id -> id
    locations = (
        normalize_locations_for_routing(
            real_locations
        )
    )


    # Existing road topology
    roads = MOCK_ROADS


    # Existing routing risk data
    # Build real risk data from Predictor
    risk_data = build_real_risk_data(forecast_minutes)  


    return (
        locations,
        roads,
        risk_data,
    )


# ============================================================
# BUILD ROUTING REPORT
# ============================================================

def build_routing_report(
    start_id,
    end_id,
    forecast_minutes=0,
    locations=None,
    roads=None,
    risk_data=None,
):

    if (
        locations is None
        or roads is None
        or risk_data is None
    ):

        (
            locations,
            roads,
            risk_data,
        ) = load_routing_inputs(forecast_minutes)


    # Build network
    network = RoadNetwork(
        locations,
        roads,
    )


    # Find affected roads
    affected = get_affected_roads(
        network,
        risk_data,
    )


    # Find changing risk
    shifting = get_shifting_risk(
        risk_data
    )


    # Find safer route
    route = find_safer_route(
        network,
        risk_data,
        start_id,
        end_id,
    )


    return {

    "forecast_minutes":forecast_minutes,
    
    "affected_roads": affected,

    "shifting_risk_locations": shifting,

    "safer_route": route,

    # Send all roads so React can draw
    # roads that are part of the safe route.
    "roads": roads,
}


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    import json


    report = build_routing_report(
        start_id="L001",
        end_id="L010",
    )


    print(
        json.dumps(
            report,
            indent=2,
        )
    )