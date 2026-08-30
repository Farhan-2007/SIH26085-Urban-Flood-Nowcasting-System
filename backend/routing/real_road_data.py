import math


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
        *
        math.cos(lat2)
        *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


def build_real_roads(locations, max_distance_km=2.0):
    """
    Build road connections using real location coordinates.

    Each nearby location is connected to another nearby location.
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

            # Connect nearby locations
            if distance <= max_distance_km:

                roads.append({
                    "road_id": f"REAL_R{road_number:03d}",

                    "from":
                        location_a["location_id"],

                    "to":
                        location_b["location_id"],

                    "distance_km":
                        round(distance, 3),
                })

                road_number += 1

    return roads
