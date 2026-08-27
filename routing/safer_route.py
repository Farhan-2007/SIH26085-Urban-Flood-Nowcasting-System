"""
safer_route.py
---------------
Finds a "safer route" between two locations: a shortest-path search
(Dijkstra) where edge cost is distance multiplied by a risk penalty, so
the algorithm naturally prefers lower-risk roads over the raw-shortest
path when a safer alternative exists.
"""

import heapq

# how much a road's risk level inflates its effective "cost" for routing
RISK_PENALTY = {
    "Low": 1.0,
    "Moderate": 1.5,
    "High": 3.0,
    "Critical": 8.0,   # heavily penalized so Dijkstra avoids it unless it's the only path
}


def _road_risk_level(road_id, from_id, to_id, risk_data, network):
    """Assign a road's risk level as the worse of its two endpoints."""
    risk_a = risk_data.get(from_id, {}).get("risk_level", "Low")
    risk_b = risk_data.get(to_id, {}).get("risk_level", "Low")
    order = ["Low", "Moderate", "High", "Critical"]
    return risk_a if order.index(risk_a) >= order.index(risk_b) else risk_b


def find_safer_route(network, risk_data, start_id, end_id):
    """
    Returns dict:
    {
        path: [location_id, ...],
        path_names: [location_name, ...],
        roads_used: [road_id, ...],
        total_distance_km: float,
        avoided_high_risk_roads: [road_id, ...],
        found: bool
    }
    """
    if start_id not in network.locations or end_id not in network.locations:
        return {"found": False, "reason": "invalid start/end location"}

    # Dijkstra with risk-adjusted edge weight
    dist = {loc_id: float("inf") for loc_id in network.locations}
    prev = {}
    prev_road = {}
    dist[start_id] = 0
    visited = set()
    heap = [(0, start_id)]

    while heap:
        current_cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)

        if node == end_id:
            break

        for neighbor_id, road_id, distance_km in network.get_neighbors(node):
            risk_level = _road_risk_level(road_id, node, neighbor_id, risk_data, network)
            penalty = RISK_PENALTY.get(risk_level, 1.0)
            edge_cost = distance_km * penalty

            new_cost = current_cost + edge_cost
            if new_cost < dist.get(neighbor_id, float("inf")):
                dist[neighbor_id] = new_cost
                prev[neighbor_id] = node
                prev_road[neighbor_id] = (road_id, distance_km, risk_level)
                heapq.heappush(heap, (new_cost, neighbor_id))

    if end_id not in prev and start_id != end_id:
        return {"found": False, "reason": "no route found between these locations"}

    # reconstruct path
    path = [end_id]
    roads_used = []
    total_distance = 0.0
    node = end_id
    while node != start_id:
        road_id, distance_km, risk_level = prev_road[node]
        roads_used.append(road_id)
        total_distance += distance_km
        node = prev[node]
        path.append(node)

    path.reverse()
    roads_used.reverse()

    # figure out which affected (high-risk) roads were successfully avoided
    from affected_roads import get_affected_roads
    all_affected = {r["road_id"] for r in get_affected_roads(network, risk_data)}
    avoided = list(all_affected - set(roads_used))

    return {
        "found": True,
        "path": path,
        "path_names": [network.location_name(loc_id) for loc_id in path],
        "roads_used": roads_used,
        "total_distance_km": round(total_distance, 2),
        "avoided_high_risk_roads": avoided,
    }