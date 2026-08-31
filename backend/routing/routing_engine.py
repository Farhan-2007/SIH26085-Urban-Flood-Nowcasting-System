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

from .safer_route import (
    find_safer_route,
)

from .real_road_data import (
    build_real_roads,
)

from backend.predictor import (
    predict_from_dataset,
)

from backend.data_loader import (
    get_all_locations,
)


# ============================================================
# NORMALIZE REAL LOCATIONS
# ============================================================

def normalize_locations_for_routing(
    locations,
):

    normalized_locations = []


    for location in locations:

        normalized_locations.append(

            {

                # RoadNetwork fields
                "id":
                    location[
                        "location_id"
                    ],

                "name":
                    location[
                        "location_name"
                    ],


                # Original fields
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

            }

        )


    return normalized_locations


# ============================================================
# BUILD REAL RISK DATA
# ============================================================

def build_real_risk_data(
    forecast_minutes=0,
):

    real_locations = (
        get_all_locations()
    )


    risk_data = {}


    for location in real_locations:

        location_id = location[
            "location_id"
        ]


        predictions = (
            predict_from_dataset(
                location_id
            )
        )


        # Select requested forecast time
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

def load_routing_inputs(
    forecast_minutes=0,
):

    # --------------------------------------------------------
    # LOAD REAL LOCATIONS
    # --------------------------------------------------------

    real_locations = (
        get_all_locations()
    )


    # --------------------------------------------------------
    # NORMALIZE LOCATIONS
    # --------------------------------------------------------

    locations = (
        normalize_locations_for_routing(
            real_locations
        )
    )


    # --------------------------------------------------------
    # BUILD REAL ROAD NETWORK
    # --------------------------------------------------------

    roads = (
        build_real_roads(
            real_locations,
            max_distance_km=2.0,
        )
    )


    # --------------------------------------------------------
    # BUILD RISK DATA
    # --------------------------------------------------------

    risk_data = (
        build_real_risk_data(
            forecast_minutes
        )
    )


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

    # --------------------------------------------------------
    # LOAD DATA IF NOT PROVIDED
    # --------------------------------------------------------

    if (
        locations is None
        or roads is None
        or risk_data is None
    ):

        (
            locations,
            roads,
            risk_data,
        ) = load_routing_inputs(
            forecast_minutes
        )


    # --------------------------------------------------------
    # BUILD NETWORK
    # --------------------------------------------------------

    network = RoadNetwork(
        locations,
        roads,
    )


    # --------------------------------------------------------
    # AFFECTED ROADS
    # --------------------------------------------------------

    affected = (
        get_affected_roads(
            network,
            risk_data,
        )
    )


    # --------------------------------------------------------
    # SHIFTING RISK
    # --------------------------------------------------------

    shifting = (
        get_shifting_risk(
            risk_data
        )
    )


    # --------------------------------------------------------
    # FIND SAFER ROUTE
    # --------------------------------------------------------

    route = (
        find_safer_route(
            network,
            risk_data,
            start_id,
            end_id,
        )
    )


    # --------------------------------------------------------
    # ENRICH ROAD DATA
    #
    # This keeps the original road objects but adds readable
    # names wherever endpoint IDs can be determined.
    # --------------------------------------------------------

    enriched_roads = []


    for road in roads:

        road_copy = dict(road)


        road_id = (
            road.get("road_id")
            or road.get("id")
        )


        # Try different possible endpoint fields
        from_id = (
            road.get("from_id")
            or road.get("from")
            or road.get("start_id")
        )


        to_id = (
            road.get("to_id")
            or road.get("to")
            or road.get("end_id")
        )


        # ----------------------------------------------------
        # Add readable road name
        # ----------------------------------------------------

        if (
            from_id in network.locations
            and to_id in network.locations
        ):

            try:

                from_name = (
                    network.location_name(
                        from_id
                    )
                )

            except Exception:

                from_name = str(
                    from_id
                )


            try:

                to_name = (
                    network.location_name(
                        to_id
                    )
                )

            except Exception:

                to_name = str(
                    to_id
                )


            road_copy[
                "from_name"
            ] = from_name


            road_copy[
                "to_name"
            ] = to_name


            road_copy[
                "road_name"
            ] = (
                f"{from_name} → {to_name}"
            )


        else:

            # Preserve existing name if available
            if "road_name" not in road_copy:

                road_copy[
                    "road_name"
                ] = road_id


        enriched_roads.append(
            road_copy
        )


    # --------------------------------------------------------
    # RETURN COMPLETE REPORT
    # --------------------------------------------------------

    return {

        "forecast_minutes":
            forecast_minutes,

        "affected_roads":
            affected,

        "shifting_risk_locations":
            shifting,

        "safer_route":
            route,

        # React uses this to display
        # road names and draw the network.
        "roads":
            enriched_roads,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    import json


    report = (
        build_routing_report(
            start_id="L001",
            end_id="L010",
        )
    )


    print(
        json.dumps(
            report,
            indent=2,
        )
    )