"""
risk_mapper.py
--------------

Maps real OSRM route geometry to the project's
flood-risk locations.

The flood dataset contains risk information at
geographic locations rather than OSM road IDs.

Therefore, route coordinates are compared with
nearby flood-risk locations.
"""

import math


# ============================================================
# RISK CONFIGURATION
# ============================================================

RISK_ORDER = [
    "Low",
    "Moderate",
    "High",
    "Critical",
]


RISK_PENALTY = {
    "Low": 1.0,
    "Moderate": 1.25,
    "High": 3.0,
    "Critical": 8.0,
}


# Maximum distance from a route point within which
# a flood-risk location is considered relevant.
RISK_MATCH_DISTANCE_KM = 0.5


# ============================================================
# HAVERSINE DISTANCE
# ============================================================

def haversine_km(
    lat1,
    lon1,
    lat2,
    lon2,
):
    """
    Calculate distance between two latitude/longitude
    coordinates using the Haversine formula.
    """

    earth_radius = 6371.0

    lat1 = math.radians(float(lat1))
    lon1 = math.radians(float(lon1))

    lat2 = math.radians(float(lat2))
    lon2 = math.radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return earth_radius * c


# ============================================================
# FIND NEAREST RISK LOCATION
# ============================================================

def nearest_risk_location(
    latitude,
    longitude,
    locations,
):
    """
    Find the closest flood-risk location to a route point.
    """

    nearest = None
    nearest_distance = float("inf")

    for location in locations:

        try:

            distance = haversine_km(
                latitude,
                longitude,
                location["latitude"],
                location["longitude"],
            )

        except (
            KeyError,
            TypeError,
            ValueError,
        ):

            continue

        if distance < nearest_distance:

            nearest_distance = distance
            nearest = location

    if nearest is None:

        return None

    return {
        "location": nearest,
        "distance_km": nearest_distance,
    }


# ============================================================
# ROUTE RISK ANALYSIS
# ============================================================

def get_route_risk(
    geometry,
    locations,
    risk_data,
    sample_every=10,
):
    """
    Determine flood risk along an OSRM route.

    Parameters
    ----------
    geometry:
        OSRM GeoJSON coordinates:

        [
            [longitude, latitude],
            ...
        ]

    locations:
        Real flood-risk locations.

    risk_data:
        Dictionary:

        location_id -> risk information

    sample_every:
        Process every Nth route coordinate.
    """

    if not geometry:

        return {
            "risk_level": "Low",
            "risk_score": 0,
            "affected_locations": [],
            "critical_locations": [],
            "high_risk_locations": [],
        }

    affected = {}
    critical = {}
    high_risk = {}

    maximum_risk_score = 0

    # --------------------------------------------------------
    # Sample route geometry
    # --------------------------------------------------------

    step = max(
        1,
        int(sample_every),
    )

    sampled_points = geometry[::step]

    # --------------------------------------------------------
    # Check every sampled route point
    # --------------------------------------------------------

    for coordinate in sampled_points:

        if len(coordinate) < 2:
            continue

        longitude = coordinate[0]
        latitude = coordinate[1]

        nearest = nearest_risk_location(
            latitude,
            longitude,
            locations,
        )

        if nearest is None:
            continue

        nearest_distance = nearest[
            "distance_km"
        ]

        # Ignore locations that are too far away
        # from the actual road route.
        if (
            nearest_distance
            > RISK_MATCH_DISTANCE_KM
        ):
            continue

        location = nearest["location"]

        location_id = location[
            "location_id"
        ]

        risk = risk_data.get(
            location_id,
            {},
        )

        risk_level = risk.get(
            "risk_level",
            "Low",
        )

        risk_score = float(
            risk.get(
                "risk_score",
                0,
            )
        )

        maximum_risk_score = max(
            maximum_risk_score,
            risk_score,
        )

        # ----------------------------------------------------
        # High / Critical locations
        # ----------------------------------------------------

        if risk_level in (
            "High",
            "Critical",
        ):

            affected[
                location_id
            ] = {

                "location_id":
                    location_id,

                "location_name":
                    location[
                        "location_name"
                    ],

                "risk_level":
                    risk_level,

                "risk_score":
                    risk_score,

                "distance_from_route_km":
                    round(
                        nearest_distance,
                        3,
                    ),

            }

        # ----------------------------------------------------
        # Critical
        # ----------------------------------------------------

        if risk_level == "Critical":

            critical[
                location_id
            ] = affected[
                location_id
            ]

        # ----------------------------------------------------
        # High
        # ----------------------------------------------------

        elif risk_level == "High":

            high_risk[
                location_id
            ] = affected[
                location_id
            ]

    # ========================================================
    # DETERMINE OVERALL ROUTE RISK
    # ========================================================

    if critical:

        route_risk_level = "Critical"

    elif high_risk:

        route_risk_level = "High"

    else:

        moderate_found = False

        for location in locations:

            location_id = location[
                "location_id"
            ]

            risk = risk_data.get(
                location_id,
                {},
            )

            if (
                risk.get(
                    "risk_level"
                )
                == "Moderate"
            ):

                moderate_found = True
                break

        if moderate_found:

            route_risk_level = "Moderate"

        else:

            route_risk_level = "Low"

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "risk_level":
            route_risk_level,

        "risk_score":
            round(
                maximum_risk_score,
                2,
            ),

        "affected_locations":
            list(
                affected.values()
            ),

        "critical_locations":
            list(
                critical.values()
            ),

        "high_risk_locations":
            list(
                high_risk.values()
            ),
    }


# ============================================================
# CALCULATE RISK-ADJUSTED ROUTE COST
# ============================================================

def calculate_route_cost(
    route,
    risk_result,
):
    """
    Calculate practical routing cost.

    Distance remains the base cost.
    Flood risk increases the effective cost.
    """

    distance = float(
        route.get(
            "distance_km",
            0,
        )
    )

    risk_level = risk_result.get(
        "risk_level",
        "Low",
    )

    penalty = RISK_PENALTY.get(
        risk_level,
        1.0,
    )

    return distance * penalty