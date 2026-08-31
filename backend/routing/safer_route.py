"""
safer_route.py
--------------

Selects the safest practical route from real OSRM routes.

OSRM supplies real road routes.

This module evaluates those routes against
flood-risk information and selects the route
with the lowest practical risk-adjusted cost.
"""


from .risk_mapper import (
    get_route_risk,
    calculate_route_cost,
)


def find_safer_route(
    routes,
    locations,
    risk_data
):

    if not routes:

        return {

            "found": False,

            "reason":
                "No real road route found",

        }

    evaluated_routes = []

    for route in routes:

        risk_result = get_route_risk(

            geometry=route[
                "geometry"
            ],

            locations=locations,

            risk_data=risk_data,

        )

        risk_cost = calculate_route_cost(

            route=route,

            risk_result=risk_result,

        )

        evaluated_routes.append({

            "route":
                route,

            "risk":
                risk_result,

            "risk_adjusted_cost":
                round(
                    risk_cost,
                    3
                ),

        })

    # --------------------------------------------------------
    # Prefer routes without Critical risk.
    # --------------------------------------------------------

    non_critical = [

        item

        for item
        in evaluated_routes

        if item[
            "risk"
        ]["risk_level"]
        != "Critical"

    ]

    if non_critical:

        evaluated_routes = non_critical

    # --------------------------------------------------------
    # Choose lowest risk-adjusted route.
    # --------------------------------------------------------

    selected = min(

        evaluated_routes,

        key=lambda item:
            item[
                "risk_adjusted_cost"
            ]

    )

    route = selected["route"]
    risk = selected["risk"]

    avoided_locations = []

    for item in routes:

        if item is route:
            continue

        other_risk = get_route_risk(

            geometry=item[
                "geometry"
            ],

            locations=locations,

            risk_data=risk_data,

        )

        for location in (
            other_risk[
                "affected_locations"
            ]
        ):

            location_id = (
                location[
                    "location_id"
                ]
            )

            selected_ids = {

                x[
                    "location_id"
                ]

                for x in
                risk[
                    "affected_locations"
                ]

            }

            if location_id not in selected_ids:

                if location_id not in [
                    x[
                        "location_id"
                    ]

                    for x in
                    avoided_locations
                ]:

                    avoided_locations.append(
                        location
                    )

    # --------------------------------------------------------
    # Route status
    # --------------------------------------------------------

    if risk["risk_level"] == "Critical":

        route_status = (
            "Critical risk remains"
        )

    elif risk["risk_level"] == "High":

        route_status = (
            "High risk route - use caution"
        )

    elif risk["risk_level"] == "Moderate":

        route_status = (
            "Safer route - moderate risk"
        )

    else:

        route_status = (
            "Safer route"
        )

    return {

        "found":
            True,

        "route_status":
            route_status,

        "risk_level":
            risk[
                "risk_level"
            ],

        "risk_score":
            risk[
                "risk_score"
            ],

        "distance_km":
            route[
                "distance_km"
            ],

        "duration_minutes":
            route[
                "duration_minutes"
            ],

        "geometry":
            route[
                "geometry"
            ],

        "affected_locations":
            risk[
                "affected_locations"
            ],

        "critical_locations":
            risk[
                "critical_locations"
            ],

        "high_risk_locations":
            risk[
                "high_risk_locations"
            ],

        "avoided_roads":
            avoided_locations,

        "alternative_routes_considered":
            len(routes),

        "risk_adjusted_cost":
            selected[
                "risk_adjusted_cost"
            ],

    }
