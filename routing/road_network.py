"""
road_network.py
----------------
Builds a basic road network graph from location + road data.

No external dependencies (no networkx) so this drops straight into the
Flask backend later without adding a new requirement.
"""


class RoadNetwork:
    def __init__(self, locations, roads):
        """
        locations: list of dicts like MOCK_LOCATIONS
        roads: list of dicts like MOCK_ROADS
        """
        self.locations = {loc["id"]: loc for loc in locations}
        self.roads = roads
        # adjacency list: node_id -> list of (neighbor_id, road_id, distance_km)
        self.adjacency = {loc_id: [] for loc_id in self.locations}
        self._build_graph()

    def _build_graph(self):
        for road in self.roads:
            a, b = road["from"], road["to"]
            dist = road["distance_km"]
            road_id = road["road_id"]
            # undirected: roads can be travelled both ways
            self.adjacency[a].append((b, road_id, dist))
            self.adjacency[b].append((a, road_id, dist))

    def get_neighbors(self, location_id):
        return self.adjacency.get(location_id, [])

    def get_road_between(self, loc_a, loc_b):
        for neighbor_id, road_id, dist in self.adjacency.get(loc_a, []):
            if neighbor_id == loc_b:
                return road_id, dist
        return None, None

    def all_roads(self):
        return self.roads

    def location_name(self, location_id):
        loc = self.locations.get(location_id)
        return loc["name"] if loc else location_id