"""
routing_engine.py
-----------------

Safe Route Intelligence engine.

Combines:

1. Real flood-risk locations
2. Project road network
3. Dijkstra safer-route algorithm
4. OSRM real-road routing
5. OSRM route flood-risk mapping
6. Affected-road detection
7. Shifting-risk detection
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

from .osrm_client import (
    OSRMClient,
)

from .risk_mapper import (
    get_route_risk,
    calculate_route_cost,
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
    """
    Convert dataset locations into the format expected
    by RoadNetwork and frontend routing components.
    """

    normalized_locations = []

    for location in locations:

        normalized_locations.append({

            # RoadNetwork fields
            "id": location["location_id"],

            "name": location["location_name"],

            # Original dataset fields
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
# BUILD REAL RISK DATA
# ============================================================

def build_real_risk_data(
    forecast_minutes=0,
):
    """
    Build:

        location_id -> risk information

    from the prediction engine.
    """

    real_locations = get_all_locations()

    risk_data = {}

    for location in real_locations:

        location_id = location["location_id"]

        predictions = predict_from_dataset(
            location_id
        )

        selected_prediction = next(

            (
                prediction

                for prediction in predictions

                if prediction[
                    "forecast_minutes"
                ] == forecast_minutes
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
# LOCATION LOOKUP
# ============================================================

def _build_location_map(
    locations,
):
    """
    Build:

        location_id -> location
    """

    return {
        location["location_id"]: location
        for location in locations
    }


# ============================================================
# GET LOCATION COORDINATES
# ============================================================

def _get_coordinates(
    location_map,
    location_id,
):
    """
    Return:

        (latitude, longitude)

    """

    location = location_map.get(
        location_id
    )

    if not location:
        return None

    try:

        return (
            float(location["latitude"]),
            float(location["longitude"]),
        )

    except (
        KeyError,
        TypeError,
        ValueError,
    ):

        return None


# ============================================================
# GET OSRM ROUTE
# ============================================================

def build_osrm_route(
    start_id,
    end_id,
    locations,
    osrm_client=None,
):
    """
    Request real driving routes from OSRM.

    Returns the best OSRM route together with alternatives.
    """

    location_map = _build_location_map(
        locations
    )

    start_coordinates = _get_coordinates(
        location_map,
        start_id,
    )

    end_coordinates = _get_coordinates(
        location_map,
        end_id,
    )

    if (
        start_coordinates is None
        or end_coordinates is None
    ):

        return {
            "found": False,
            "reason": "invalid start/end coordinates",
            "routes": [],
        }

    if osrm_client is None:

        osrm_client = OSRMClient()

    start_lat, start_lon = (
        start_coordinates
    )

    end_lat, end_lon = (
        end_coordinates
    )

    try:

        routes = osrm_client.get_route(

            start_lat=start_lat,

            start_lon=start_lon,

            end_lat=end_lat,

            end_lon=end_lon,

            alternatives=True,
        )

    except Exception as error:

        return {

            "found": False,

            "reason":
                str(error),

            "routes": [],
        }

    if not routes:

        return {

            "found": False,

            "reason":
                "OSRM returned no routes",

            "routes": [],
        }

    # Best/default OSRM route
    best_route = routes[0]

    return {

        "found": True,

        "distance_km":
            best_route[
                "distance_km"
            ],

        "duration_minutes":
            best_route[
                "duration_minutes"
            ],

        "geometry":
            best_route[
                "geometry"
            ],

        "legs":
            best_route[
                "legs"
            ],

        "route_index":
            best_route[
                "route_index"
            ],

        # Keep alternatives
        "routes":
            routes,
    }


# ============================================================
# BUILD REAL ROAD RISK DATA
# ============================================================

def build_osrm_route_risk(
    osrm_route,
    locations,
    risk_data,
):
    """
    Map OSRM road geometry to the project's flood-risk
    locations.
    """

    if not osrm_route.get("found"):

        return {

            "risk_level": "Low",

            "risk_score": 0,

            "affected_locations": [],

            "critical_locations": [],

            "high_risk_locations": [],
        }

    geometry = osrm_route.get(
        "geometry",
        []
    )

    return get_route_risk(

        geometry=geometry,

        locations=locations,

        risk_data=risk_data,

        sample_every=10,
    )


# ============================================================
# LOAD ROUTING INPUTS
# ============================================================

def load_routing_inputs(
    forecast_minutes=0,
):
    """
    Load:

        locations
        roads
        risk_data
    """

    real_locations = (
        get_all_locations()
    )

    locations = (
        normalize_locations_for_routing(
            real_locations
        )
    )

    roads = (
        build_real_roads(
            real_locations,
            max_distance_km=2.0,
        )
    )

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
# ENRICH ROAD DATA
# ============================================================

def enrich_roads(
    roads,
    network,
):
    """
    Add readable endpoint names to road objects.
    """

    enriched_roads = []

    for road in roads:

        road_copy = dict(road)

        road_id = (
            road.get("road_id")
            or road.get("id")
        )

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
                "from_id"
            ] = from_id

            road_copy[
                "to_id"
            ] = to_id

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

            if "road_name" not in road_copy:

                road_copy[
                    "road_name"
                ] = road_id

        enriched_roads.append(
            road_copy
        )

    return enriched_roads


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
    osrm_client=None,
):
    """
    Build complete routing intelligence report.
    """

    # --------------------------------------------------------
    # LOAD DATA
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
    # DIJKSTRA SAFER ROUTE
    # --------------------------------------------------------

    safer_route = (
        find_safer_route(

            network,

            risk_data,

            start_id,

            end_id,
        )
    )

    # --------------------------------------------------------
    # ENRICH PROJECT ROAD NETWORK
    # --------------------------------------------------------

    enriched_roads = enrich_roads(
        roads,
        network,
    )

    # --------------------------------------------------------
    # OSRM REAL ROAD ROUTE
    # --------------------------------------------------------

    osrm_route = build_osrm_route(

        start_id=start_id,

        end_id=end_id,

        locations=locations,

        osrm_client=osrm_client,
    )

    # --------------------------------------------------------
    # OSRM ROUTE RISK
    # --------------------------------------------------------

    osrm_route_risk = (
        build_osrm_route_risk(

            osrm_route,

            locations,

            risk_data,
        )
    )

    # --------------------------------------------------------
    # RISK-ADJUSTED OSRM COST
    # --------------------------------------------------------

    osrm_route_cost = None

    if osrm_route.get("found"):

        osrm_route_cost = (
            calculate_route_cost(

                osrm_route,

                osrm_route_risk,
            )
        )

    # --------------------------------------------------------
    # RETURN COMPLETE REPORT
    # --------------------------------------------------------

    return {

        # Forecast
        "forecast_minutes":
            forecast_minutes,

        # Flood affected roads
        "affected_roads":
            affected,

        # Locations whose risk is changing
        "shifting_risk_locations":
            shifting,

        # Project's flood-aware route
        "safer_route":
            safer_route,

        # Actual OSM/OSRM route
        "osrm_route":
            osrm_route,

        # Flood risk mapped onto actual route
        "osrm_route_risk":
            osrm_route_risk,

        # Risk-adjusted OSRM cost
        "osrm_route_cost":
            (
                round(
                    osrm_route_cost,
                    3,
                )
                if osrm_route_cost is not None
                else None
            ),

        # Project road network
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

            forecast_minutes=0,
        )
    )

    print(
        json.dumps(
            report,
            indent=2,
        )
    )