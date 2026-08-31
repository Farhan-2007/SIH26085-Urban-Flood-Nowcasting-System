"""
test_routing.py
---------------

Tests the real-road flood-aware routing engine.

These tests require internet access because
OSRM is an external routing service.
"""

from backend.routing.routing_engine import (
    build_routing_report,
)


# ============================================================
# TEST 1
# ============================================================

def test_route_1():

    report = build_routing_report(

        start_lat=19.0760,
        start_lon=72.8777,

        end_lat=19.0820,
        end_lon=72.8850,

        forecast_minutes=0,

    )

    assert report["found"] is True

    route = report["route"]

    assert route["found"] is True

    assert len(
        route["geometry"]
    ) > 0

    print(
        "PASS: Route 1"
    )

    print(
        "Distance:",
        route["distance_km"],
        "km"
    )

    print(
        "Risk:",
        route["risk_level"]
    )


# ============================================================
# TEST 2
# ============================================================

def test_route_2():

    report = build_routing_report(

        start_lat=19.0700,
        start_lon=72.8720,

        end_lat=19.0880,
        end_lon=72.8950,

        forecast_minutes=30,

    )

    assert report["found"] is True

    route = report["route"]

    assert route["found"] is True

    print(
        "PASS: Route 2"
    )

    print(
        "Distance:",
        route["distance_km"],
        "km"
    )

    print(
        "Risk:",
        route["risk_level"]
    )


# ============================================================
# TEST 3
# ============================================================

def test_route_3():

    report = build_routing_report(

        start_lat=19.0740,
        start_lon=72.8750,

        end_lat=19.0920,
        end_lon=72.9000,

        forecast_minutes=60,

    )

    assert report["found"] is True

    route = report["route"]

    assert route["found"] is True

    print(
        "PASS: Route 3"
    )

    print(
        "Distance:",
        route["distance_km"],
        "km"
    )

    print(
        "Risk:",
        route["risk_level"]
    )


# ============================================================
# TEST LOCATION-ID COMPATIBILITY
# ============================================================

def test_location_ids():

    report = build_routing_report(

        start_id="L001",

        end_id="L004",

        forecast_minutes=0,

    )

    assert report["found"] is True

    assert (
        report["route"]["found"]
        is True
    )

    print(
        "PASS: Location ID routing"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "REAL ROAD ROUTING TESTS"
    )

    print(
        "==============================\n"
    )

    test_route_1()

    test_route_2()

    test_route_3()

    test_location_ids()

    print(
        "\nAll routing tests passed."
    )
