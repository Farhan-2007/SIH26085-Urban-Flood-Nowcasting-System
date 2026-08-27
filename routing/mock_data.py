"""
mock_data.py
------------
STANDALONE MOCK DATA for routing/analyser development.

This mirrors the shape of what will eventually come from:
  - Member 5's locations.csv / flood_features.csv
  - Member 4's own Predictor + Analyser output (risk_score, risk_level, trend)

⚠️ REPLACE LATER:
When Member 3 wires the real pipeline (Dataset -> Predictor -> Analyser -> Flask),
swap MOCK_LOCATIONS / MOCK_ROADS for real data pulled from the predictor's
output and Member 5's dataset. Everything downstream (affected_roads.py,
safer_route.py, routing_engine.py) only depends on this shape, not on how
the numbers were produced — so integration later should just mean deleting
this file's usage and injecting real data with the same keys.
"""

# 10 mock locations, same shape as Member 5's locations.csv is expected to have
MOCK_LOCATIONS = [
    {"id": "L1", "name": "Koramangala",     "lat": 12.9352, "lon": 77.6146},
    {"id": "L2", "name": "Silk Board",      "lat": 12.9172, "lon": 77.6228},
    {"id": "L3", "name": "BTM Layout",      "lat": 12.9166, "lon": 77.6101},
    {"id": "L4", "name": "HSR Layout",      "lat": 12.9121, "lon": 77.6446},
    {"id": "L5", "name": "Marathahalli",    "lat": 12.9569, "lon": 77.7011},
    {"id": "L6", "name": "Indiranagar",     "lat": 12.9784, "lon": 77.6408},
    {"id": "L7", "name": "MG Road",         "lat": 12.9757, "lon": 77.6069},
    {"id": "L8", "name": "Jayanagar",       "lat": 12.9308, "lon": 77.5838},
    {"id": "L9", "name": "Whitefield",      "lat": 12.9698, "lon": 77.7500},
    {"id": "L10", "name": "Electronic City", "lat": 12.8452, "lon": 77.6602},
]

# Mock output of the Predictor + Analyser (this is what YOUR modules already
# produce for a single location today). risk_score is 0-100, risk_level is
# Low/Moderate/High/Critical, trend is Intensifying/Stable/Receding
# (matches the "Intensifying / Receding / Stable logic" already built).
MOCK_RISK_DATA = {
    "L1": {"risk_score": 42, "risk_level": "Moderate", "trend": "Intensifying"},
    "L2": {"risk_score": 88, "risk_level": "Critical",  "trend": "Intensifying"},
    "L3": {"risk_score": 65, "risk_level": "High",      "trend": "Stable"},
    "L4": {"risk_score": 30, "risk_level": "Low",       "trend": "Receding"},
    "L5": {"risk_score": 55, "risk_level": "Moderate",  "trend": "Intensifying"},
    "L6": {"risk_score": 20, "risk_level": "Low",       "trend": "Stable"},
    "L7": {"risk_score": 15, "risk_level": "Low",       "trend": "Stable"},
    "L8": {"risk_score": 70, "risk_level": "High",      "trend": "Intensifying"},
    "L9": {"risk_score": 25, "risk_level": "Low",       "trend": "Receding"},
    "L10": {"risk_score": 60, "risk_level": "High",     "trend": "Stable"},
}

# Basic mock road network: which locations are directly connected by a road,
# plus a rough distance in km. Member 2/3 will eventually supply real road
# geometry; for now this is enough to run graph + routing logic end-to-end.
MOCK_ROADS = [
    {"road_id": "R1", "from": "L1", "to": "L2", "distance_km": 3.2},
    {"road_id": "R2", "from": "L1", "to": "L3", "distance_km": 2.5},
    {"road_id": "R3", "from": "L2", "to": "L3", "distance_km": 2.1},
    {"road_id": "R4", "from": "L2", "to": "L4", "distance_km": 4.0},
    {"road_id": "R5", "from": "L3", "to": "L8", "distance_km": 3.7},
    {"road_id": "R6", "from": "L1", "to": "L6", "distance_km": 5.5},
    {"road_id": "R7", "from": "L6", "to": "L7", "distance_km": 2.8},
    {"road_id": "R8", "from": "L4", "to": "L5", "distance_km": 6.1},
    {"road_id": "R9", "from": "L5", "to": "L9", "distance_km": 8.4},
    {"road_id": "R10", "from": "L4", "to": "L10", "distance_km": 9.0},
    {"road_id": "R11", "from": "L7", "to": "L1", "distance_km": 4.4},
    {"road_id": "R12", "from": "L8", "to": "L4", "distance_km": 4.9},
]