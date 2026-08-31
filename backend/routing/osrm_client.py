"""
osrm_client.py
--------------

OSRM client for real-road routing.

OSRM uses OpenStreetMap road-network data to calculate
real driving routes between coordinates.
"""

import requests


DEFAULT_OSRM_URL = "https://router.project-osrm.org"


class OSRMClient:

    def __init__(
        self,
        base_url=DEFAULT_OSRM_URL,
        timeout=15
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # ========================================================
    # ROUTE REQUEST
    # ========================================================

    def get_route(
        self,
        start_lat,
        start_lon,
        end_lat,
        end_lon,
        alternatives=True
    ):
        """
        Get real driving route from OSRM.

        Coordinates are supplied as:
            latitude, longitude

        OSRM expects:
            longitude,latitude
        """

        coordinates = (
            f"{float(start_lon)},{float(start_lat)};"
            f"{float(end_lon)},{float(end_lat)}"
        )

        url = (
            f"{self.base_url}"
            f"/route/v1/driving/"
            f"{coordinates}"
        )

        params = {
            "overview": "full",
            "geometries": "geojson",
            "steps": "true",
            "alternatives": "true"
            if alternatives
            else "false",
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()

        except requests.RequestException as error:

            raise RuntimeError(
                f"OSRM routing request failed: {error}"
            )

        data = response.json()

        if data.get("code") != "Ok":

            raise RuntimeError(
                f"OSRM returned error: "
                f"{data.get('message', data.get('code'))}"
            )

        routes = data.get(
            "routes",
            []
        )

        if not routes:

            raise RuntimeError(
                "OSRM returned no routes"
            )

        return self._format_routes(routes)

    # ========================================================
    # FORMAT ROUTES
    # ========================================================

    def _format_routes(
        self,
        routes
    ):

        formatted_routes = []

        for index, route in enumerate(
            routes
        ):

            geometry = route.get(
                "geometry",
                {}
            )

            coordinates = geometry.get(
                "coordinates",
                []
            )

            formatted_routes.append({

                "route_index":
                    index,

                "distance_km":
                    round(
                        route.get(
                            "distance",
                            0
                        ) / 1000,
                        3
                    ),

                "duration_minutes":
                    round(
                        route.get(
                            "duration",
                            0
                        ) / 60,
                        2
                    ),

                "geometry":
                    coordinates,

                "legs":
                    route.get(
                        "legs",
                        []
                    ),

            })

        return formatted_routes