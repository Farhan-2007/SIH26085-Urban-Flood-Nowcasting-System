"""
safer_route.py
---------------

Finds a "safer route" between two locations using Dijkstra's algorithm.

Each road is assigned an effective cost:

    distance × risk penalty

This makes the algorithm prefer safer roads when a reasonable
alternative exists.
"""

import heapq


# ============================================================
# RISK PENALTIES
# ============================================================

RISK_PENALTY = {
    "Low": 1.0,
    "Moderate": 1.5,
    "High": 3.0,
    "Critical": 8.0,
}


# ============================================================
# RISK LEVEL HELPER
# ============================================================

def _road_risk_level(
    road_id,
    from_id,
    to_id,
    risk_data,
    network,
):
    """
    Assign a road risk level based on the worse risk level
    of its two endpoint locations.
    """

    risk_a = (
        risk_data
        .get(from_id, {})
        .get("risk_level", "Low")
    )

    risk_b = (
        risk_data
        .get(to_id, {})
        .get("risk_level", "Low")
    )

    order = [
        "Low",
        "Moderate",
        "High",
        "Critical",
    ]

    if risk_a not in order:
        risk_a = "Low"

    if risk_b not in order:
        risk_b = "Low"

    return (
        risk_a
        if order.index(risk_a) >= order.index(risk_b)
        else risk_b
    )


# ============================================================
# ROAD NAME HELPER
# ============================================================

def _get_road_name(
    road_id,
    from_id,
    to_id,
    network,
):
    """
    Convert a road ID such as REAL_R001 into a readable name.

    Example:
        REAL_R001
        ->
        Dadar → Mahim
    """

    try:
        from_name = network.location_name(from_id)
    except Exception:
        from_name = str(from_id)

    try:
        to_name = network.location_name(to_id)
    except Exception:
        to_name = str(to_id)

    return f"{from_name} → {to_name}"


# ============================================================
# FIND SAFER ROUTE
# ============================================================

def find_safer_route(
    network,
    risk_data,
    start_id,
    end_id,
):
    """
    Returns:

    {
        path: [location_id, ...],
        path_names: [location_name, ...],

        roads_used: [road_id, ...],

        road_names: [
            "Dadar → Mahim",
            "Mahim → Shivaji Park"
        ],

        total_distance_km: float,

        avoided_high_risk_roads: [road_id, ...],

        avoided_high_risk_road_names: [
            "Prabhadevi → Parel"
        ],

        found: bool
    }
    """

    # --------------------------------------------------------
    # VALIDATE LOCATIONS
    # --------------------------------------------------------

    if (
        start_id not in network.locations
        or end_id not in network.locations
    ):
        return {
            "found": False,
            "reason": "invalid start/end location",
        }


    # --------------------------------------------------------
    # DIJKSTRA INITIALIZATION
    # --------------------------------------------------------

    dist = {
        loc_id: float("inf")
        for loc_id in network.locations
    }

    prev = {}

    prev_road = {}

    dist[start_id] = 0

    visited = set()

    heap = [
        (0, start_id)
    ]


    # --------------------------------------------------------
    # DIJKSTRA
    # --------------------------------------------------------

    while heap:

        current_cost, node = heapq.heappop(
            heap
        )

        if node in visited:
            continue

        visited.add(node)


        # Destination reached
        if node == end_id:
            break


        # Explore neighbours
        for (
            neighbor_id,
            road_id,
            distance_km,
        ) in network.get_neighbors(node):

            risk_level = _road_risk_level(
                road_id,
                node,
                neighbor_id,
                risk_data,
                network,
            )


            penalty = RISK_PENALTY.get(
                risk_level,
                1.0,
            )


            edge_cost = (
                distance_km * penalty
            )


            new_cost = (
                current_cost + edge_cost
            )


            if (
                new_cost
                < dist.get(
                    neighbor_id,
                    float("inf"),
                )
            ):

                dist[neighbor_id] = new_cost

                prev[neighbor_id] = node

                prev_road[neighbor_id] = (
                    road_id,
                    distance_km,
                    risk_level,
                )

                heapq.heappush(
                    heap,
                    (
                        new_cost,
                        neighbor_id,
                    ),
                )


    # --------------------------------------------------------
    # NO ROUTE
    # --------------------------------------------------------

    if (
        end_id not in prev
        and start_id != end_id
    ):
        return {
            "found": False,
            "reason": (
                "no route found between "
                "these locations"
            ),
        }


    # --------------------------------------------------------
    # RECONSTRUCT PATH
    # --------------------------------------------------------

    path = [
        end_id
    ]

    roads_used = []

    road_details = []

    total_distance = 0.0

    node = end_id


    while node != start_id:

        (
            road_id,
            distance_km,
            risk_level,
        ) = prev_road[node]


        previous_node = prev[node]


        roads_used.append(
            road_id
        )


        road_details.append(
            {
                "road_id": road_id,

                "from_id": previous_node,

                "to_id": node,

                "road_name": _get_road_name(
                    road_id,
                    previous_node,
                    node,
                    network,
                ),

                "distance_km": round(
                    distance_km,
                    3,
                ),

                "risk_level": risk_level,
            }
        )


        total_distance += (
            distance_km
        )


        node = previous_node

        path.append(node)


    # Reverse everything
    path.reverse()

    roads_used.reverse()

    road_details.reverse()


    # --------------------------------------------------------
    # LOCATION NAMES
    # --------------------------------------------------------

    path_names = []

    for loc_id in path:

        try:
            name = network.location_name(
                loc_id
            )
        except Exception:
            name = str(loc_id)

        path_names.append(name)


    # --------------------------------------------------------
    # AFFECTED ROADS
    # --------------------------------------------------------

    from .affected_roads import (
        get_affected_roads
    )


    all_affected = (
        get_affected_roads(
            network,
            risk_data,
        )
    )


    affected_ids = {
        road["road_id"]
        for road in all_affected
    }


    avoided = list(
        affected_ids
        - set(roads_used)
    )


    # --------------------------------------------------------
    # BUILD READABLE NAMES FOR AVOIDED ROADS
    # --------------------------------------------------------

    avoided_high_risk_road_names = []


    # First try names from affected-road data
    affected_name_map = {}


    for road in all_affected:

        road_id = road.get(
            "road_id"
        )

        from_name = road.get(
            "from_name"
        )

        to_name = road.get(
            "to_name"
        )


        if (
            from_name
            and to_name
        ):

            affected_name_map[
                road_id
            ] = (
                f"{from_name} → {to_name}"
            )


    for road_id in avoided:

        if road_id in affected_name_map:

            avoided_high_risk_road_names.append(
                affected_name_map[
                    road_id
                ]
            )

        else:

            # Fallback if affected_roads
            # does not contain names
            road_name = road_id

            for detail in road_details:

                if (
                    detail["road_id"]
                    == road_id
                ):

                    road_name = detail[
                        "road_name"
                    ]

                    break

            avoided_high_risk_road_names.append(
                road_name
            )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "found": True,

        "path": path,

        "path_names": path_names,

        "roads_used": roads_used,

        # NEW: readable road names
        "road_names": [
            detail["road_name"]
            for detail in road_details
        ],

        # NEW: detailed road information
        "road_details": road_details,

        "total_distance_km": round(
            total_distance,
            2,
        ),

        "avoided_high_risk_roads": avoided,

        # NEW: readable avoided-road names
        "avoided_high_risk_road_names":
            avoided_high_risk_road_names,
    }