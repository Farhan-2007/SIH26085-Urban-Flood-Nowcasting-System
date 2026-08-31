import math
import requests


OSRM_URL = "https://router.project-osrm.org"


def calculate_distance_km(lat1, lon1, lat2, lon2):
    """
    Calculate geographical distance using Haversine formula.
    """

    earth_radius = 6371

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
        math.sqrt(1 - a)
    )

    return earth_radius * c


def get_osrm_geometry(
    start_lat,
    start_lon,
    end_lat,
    end_lon,
):
    """
    Get actual road geometry from OSRM.

    Returns GeoJSON LineString coordinates:

        [
            [longitude, latitude],
            ...
        ]
    """

    coordinates = (
        f"{float(start_lon)},{float(start_lat)};"
        f"{float(end_lon)},{float(end_lat)}"
    )

    url = (
        f"{OSRM_URL}/route/v1/driving/"
        f"{coordinates}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
        "alternatives": "false",
    }

    response = requests.get(
        url,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok":
        raise RuntimeError(
            f"OSRM error: {data.get('code')}"
        )

    routes = data.get("routes", [])

    if not routes:
        raise RuntimeError(
            "OSRM returned no route"
        )

    geometry = (
        routes[0]
        .get("geometry", {})
        .get("coordinates", [])
    )

    return geometry


def build_real_roads(
    locations,
    max_distance_km=2.0,
):
    """
    Build project road connections.

    Nearby flood locations are connected and
    OSRM provides the actual road geometry.

    Each road contains:

        road_id
        from
        to
        distance_km
        geometry
    """

    roads = []

    road_number = 1

    for i, location_a in enumerate(locations):

        for j, location_b in enumerate(locations):

            # Don't connect location to itself
            if i >= j:
                continue

            distance = calculate_distance_km(
                location_a["latitude"],
                location_a["longitude"],
                location_b["latitude"],
                location_b["longitude"],
            )

            # Only connect nearby locations
            if distance > max_distance_km:
                continue

            try:

                geometry = get_osrm_geometry(
                    start_lat=location_a["latitude"],
                    start_lon=location_a["longitude"],
                    end_lat=location_b["latitude"],
                    end_lon=location_b["longitude"],
                )

            except Exception as error:

                print(
                    f"OSRM failed for "
                    f"{location_a['location_id']} -> "
                    f"{location_b['location_id']}: "
                    f"{error}"
                )

                # Skip this road instead of creating
                # a fake straight-line road.
                continue

            roads.append({

                "road_id":
                    f"REAL_R{road_number:03d}",

                "from":
                    location_a["location_id"],

                "to":
                    location_b["location_id"],

                "distance_km":
                    round(distance, 3),

                "geometry":
                    geometry,
            })

            road_number += 1

    return roads