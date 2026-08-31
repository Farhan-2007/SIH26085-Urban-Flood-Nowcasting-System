"""
routing_engine.py
-----------------

Main real-road flood-aware routing engine.

Flow:

Start + Destination
        ↓
OSRM / OpenStreetMap
        ↓
Real road alternatives
        ↓
Flood-risk data from Predictor
        ↓
Risk mapping
        ↓
Risk-adjusted route selection
        ↓
Safe route JSON
"""


from backend.data_loader import (
    get_all_locations,
)

from backend.predictor import (
    predict_from_dataset,
)

from .road_network import RoadNetwork

from .affected_roads import (
    get_affected_roads,
    get_shifting_risk,
)

from .safer_route import (
    find_safer_route,
)


# ============================================================
# LOAD REAL FLOOD-RISK DATA
# ============================================================

def build_real_risk_data(
    forecast_minutes=0
):

    locations = get_all_locations()

    risk_data = {}

    for location in locations:

        location_id = (
            location["location_id"]
        )

        predictions = predict_from_dataset(
            location_id
        )

        selected_prediction = next(

            (

                prediction

                for prediction
                in predictions

                if prediction[
                    "forecast_minutes"
                ]
                == forecast_minutes

            ),

            None

        )

        if selected_prediction is None:
            continue

        risk_data[
            location_id
        ] = {

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

def load_routing_inputs(
    forecast_minutes=0
):

    locations = get_all_locations()

    risk_data = build_real_risk_data(
        forecast_minutes
    )

    return (
        locations,
        risk_data,
    )


# ============================================================
# FIND LOCATION BY ID
# ============================================================

def get_location_by_id(
    locations,
    location_id
):

    for location in locations:

        if (
            location[
                "location_id"
            ]
            == location_id
        ):

            return location

    return None


# ============================================================
# BUILD ROUTING REPORT
# ============================================================

def build_routing_report(

    start_lat=None,
    start_lon=None,

    end_lat=None,
    end_lon=None,

    forecast_minutes=0,

    start_id=None,
    end_id=None,

    locations=None,
    risk_data=None,

):

    # --------------------------------------------------------
    # Load routing data
    # --------------------------------------------------------

    if locations is None:

        locations = get_all_locations()

    if risk_data is None:

        risk_data = build_real_risk_data(
            forecast_minutes
        )

    # --------------------------------------------------------
    # Support location IDs for backend compatibility
    # --------------------------------------------------------

    if start_id:

        start_location = (
            get_location_by_id(
                locations,
                start_id
            )
        )

        if start_location is None:

            return {

                "found": False,

                "error":
                    f"Start location '{start_id}' "
                    f"not found",

            }

        start_lat = (
            start_location[
                "latitude"
            ]
        )

        start_lon = (
            start_location[
                "longitude"
            ]
        )

    if end_id:

        end_location = (
            get_location_by_id(
                locations,
                end_id
            )
        )

        if end_location is None:

            return {

                "found": False,

                "error":
                    f"Destination location '{end_id}' "
                    f"not found",

            }

        end_lat = (
            end_location[
                "latitude"
            ]
        )

        end_lon = (
            end_location[
                "longitude"
            ]
        )

    # --------------------------------------------------------
    # Validate coordinates
    # --------------------------------------------------------

    if (
        start_lat is None
        or start_lon is None
        or end_lat is None
        or end_lon is None
    ):

        return {

            "found": False,

            "error":
                (
                    "Start and destination "
                    "coordinates are required"
                ),

        }

    # --------------------------------------------------------
    # Real OSRM routing
    # --------------------------------------------------------

    network = RoadNetwork()

    routes = network.get_routes(

        start_lat=float(
            start_lat
        ),

        start_lon=float(
            start_lon
        ),

        end_lat=float(
            end_lat
        ),

        end_lon=float(
            end_lon
        ),

    )

    if not routes:

        return {

            "found": False,

            "error":
                "No real road route found",

        }

    # --------------------------------------------------------
    # Flood affected locations
    # --------------------------------------------------------

    affected = get_affected_roads(

        locations=locations,

        risk_data=risk_data,

    )

    # --------------------------------------------------------
    # Shifting risk
    # --------------------------------------------------------

    shifting = get_shifting_risk(
        risk_data
    )

    # --------------------------------------------------------
    # Select safest route
    # --------------------------------------------------------

    safer_route = find_safer_route(

        routes=routes,

        locations=locations,

        risk_data=risk_data,

    )

    # --------------------------------------------------------
    # Final JSON
    # --------------------------------------------------------

    return {

        "found":
            safer_route[
                "found"
            ],

        "forecast_minutes":
            forecast_minutes,

        "start":
            {

                "latitude":
                    float(
                        start_lat
                    ),

                "longitude":
                    float(
                        start_lon
                    ),

                "location_id":
                    start_id,

            },

        "destination":
            {

                "latitude":
                    float(
                        end_lat
                    ),

                "longitude":
                    float(
                        end_lon
                    ),

                "location_id":
                    end_id,

            },

        "route":
            safer_route,

        "affected_roads":
            affected,

        "shifting_risk_locations":
            shifting,

        "routing_provider":
            "OSRM + OpenStreetMap",

        "route_count_considered":
            len(routes),

    }
