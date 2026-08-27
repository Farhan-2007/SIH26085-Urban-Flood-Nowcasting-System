"""
routing_engine.py
------------------
Single entry point Member 3 can eventually call from Flask.

Today it runs entirely on MOCK_LOCATIONS / MOCK_ROADS / MOCK_RISK_DATA.
Tomorrow, swap `load_mock_inputs()` for real inputs (real locations/roads
from Member 5's dataset + real risk_data from your own Predictor/Analyser
output) — nothing else in this file needs to change, since everything
downstream only depends on the same dict shapes.
"""

from road_network import RoadNetwork
from affected_roads import get_affected_roads, get_shifting_risk
from safer_route import find_safer_route
from mock_data import MOCK_LOCATIONS, MOCK_ROADS, MOCK_RISK_DATA


def load_mock_inputs():
    """Swap this out later for real data pulled from the pipeline."""
    return MOCK_LOCATIONS, MOCK_ROADS, MOCK_RISK_DATA


def build_routing_report(start_id, end_id, locations=None, roads=None, risk_data=None):
    """
    Main function. Returns one frontend-friendly JSON-serializable dict
    with affected roads, shifting risk, and a safer route suggestion.
    """
    if locations is None or roads is None or risk_data is None:
        locations, roads, risk_data = load_mock_inputs()

    network = RoadNetwork(locations, roads)

    affected = get_affected_roads(network, risk_data)
    shifting = get_shifting_risk(risk_data)
    route = find_safer_route(network, risk_data, start_id, end_id)

    return {
        "affected_roads": affected,
        "shifting_risk_locations": shifting,
        "safer_route": route,
    }


if __name__ == "__main__":
    import json

    # demo run with mock data: route from Koramangala (L1) to Marathahalli (L5)
    report = build_routing_report(start_id="L1", end_id="L5")
    print(json.dumps(report, indent=2))