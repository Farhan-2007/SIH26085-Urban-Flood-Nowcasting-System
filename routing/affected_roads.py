"""
affected_roads.py
------------------
Identifies which roads are "affected" (unsafe/high-risk) based on the
risk level of the locations they connect.

Input risk_data is expected to come from the Predictor/Analyser
(risk_score, risk_level, trend per location) — currently mocked in
mock_data.py, later this will be real output from your own predictor code.
"""

# Roads touching a location at this risk level or higher are flagged
RISK_ORDER = ["Low", "Moderate", "High", "Critical"]
AFFECTED_THRESHOLD = "High"  # High or Critical => road considered affected


def _risk_rank(level):
    return RISK_ORDER.index(level) if level in RISK_ORDER else 0


def get_affected_roads(network, risk_data):
    """
    network: RoadNetwork instance
    risk_data: dict of location_id -> {risk_score, risk_level, trend}

    Returns a list of affected-road dicts, frontend-friendly:
    {
        road_id, from_id, from_name, to_id, to_name,
        distance_km, risk_level, trend, status
    }
    """
    affected = []
    threshold_rank = _risk_rank(AFFECTED_THRESHOLD)

    for road in network.all_roads():
        a, b = road["from"], road["to"]
        risk_a = risk_data.get(a, {})
        risk_b = risk_data.get(b, {})

        level_a = risk_a.get("risk_level", "Low")
        level_b = risk_b.get("risk_level", "Low")

        # a road is affected if EITHER endpoint is High/Critical
        worst_level = level_a if _risk_rank(level_a) >= _risk_rank(level_b) else level_b
        worst_trend = risk_a.get("trend") if worst_level == level_a else risk_b.get("trend")

        if _risk_rank(worst_level) >= threshold_rank:
            status = "Critical - avoid" if worst_level == "Critical" else "High risk - caution"
            affected.append({
                "road_id": road["road_id"],
                "from_id": a,
                "from_name": network.location_name(a),
                "to_id": b,
                "to_name": network.location_name(b),
                "distance_km": road["distance_km"],
                "risk_level": worst_level,
                "trend": worst_trend,
                "status": status,
            })

    return affected


def get_shifting_risk(risk_data):
    """
    Basic 'shifting' detection across multiple locations — flags locations
    where risk is Intensifying, ranked by risk_score so the frontend can
    show which areas risk is currently moving toward.

    Returns a list sorted by risk_score descending, intensifying-only.
    """
    shifting = [
        {"location_id": loc_id, **data}
        for loc_id, data in risk_data.items()
        if data.get("trend") == "Intensifying"
    ]
    shifting.sort(key=lambda x: x["risk_score"], reverse=True)
    return shifting