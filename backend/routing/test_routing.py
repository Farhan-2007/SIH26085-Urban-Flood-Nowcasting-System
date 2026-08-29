"""
test_routing.py
----------------
Quick sanity tests using mock data. Run: python3 test_routing.py
"""

from routing_engine import build_routing_report


def test_basic_route():
    report = build_routing_report(start_id="L001", end_id="L005")
    assert report["safer_route"]["found"] is True
    assert report["safer_route"]["path"][0] == "L001"
    assert report["safer_route"]["path"][-1] == "L005"
    print("PASS: basic route L001 -> L005 found")


def test_avoids_critical_roads():
    report = build_routing_report(start_id="L001", end_id="L005")
    roads_used = set(report["safer_route"]["roads_used"])
    # R1 (L001-L002) and R4 (L002-L004) are Critical; R2/R5/R12/R8 route around them
    assert "R1" not in roads_used, "safer route should avoid Critical road R1"
    print("PASS: safer route avoids Critical-risk road R1")


def test_invalid_location():
    report = build_routing_report(start_id="L001", end_id="L099")
    assert report["safer_route"]["found"] is False
    print("PASS: invalid destination handled gracefully")


def test_affected_roads_present():
    report = build_routing_report(start_id="L001", end_id="L005")
    assert len(report["affected_roads"]) > 0
    print("PASS: affected roads list populated")


def test_shifting_risk_sorted():
    report = build_routing_report(start_id="L001", end_id="L005")
    scores = [loc["risk_score"] for loc in report["shifting_risk_locations"]]
    assert scores == sorted(scores, reverse=True)
    print("PASS: shifting risk locations sorted by score descending")


if __name__ == "__main__":
    test_basic_route()
    test_avoids_critical_roads()
    test_invalid_location()
    test_affected_roads_present()
    test_shifting_risk_sorted()
    print("\nAll tests passed.")