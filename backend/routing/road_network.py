"""
road_network.py
---------------

Represents real-road routing results returned by OSRM.

The actual road graph is maintained by OSRM/OpenStreetMap.
"""

from .osrm_client import OSRMClient


class RoadNetwork:

    def __init__(
        self,
        osrm_client=None
    ):

        self.osrm = (
            osrm_client
            or OSRMClient()
        )

    def get_routes(
        self,
        start_lat,
        start_lon,
        end_lat,
        end_lon
    ):

        return self.osrm.get_route(

            start_lat=start_lat,
            start_lon=start_lon,

            end_lat=end_lat,
            end_lon=end_lon,

            alternatives=True

        )
