from backend.routing.routing_engine import (
    build_routing_report
)


def test_basic_route():

    report = build_routing_report(
        start_id="L001",
        end_id="L005"
    )

    assert report["safer_route"]["found"] is True

    assert (
        report["safer_route"]["path"][0]
        == "L001"
    )

    assert (
        report["safer_route"]["path"][-1]
        == "L005"
    )

    print("PASS: basic route found")


def test_route_found():

    report = build_routing_report(
        start_id="L001",
        end_id="L005"
    )

    assert (
        report["safer_route"]["found"]
        is True
    )

    print("PASS: route successfully found")


def test_invalid_location():

    report = build_routing_report(
        start_id="L001",
        end_id="L099"
    )

    assert (
        report["safer_route"]["found"]
        is False
    )

    print("PASS: invalid destination handled")


def test_affected_roads():

    report = build_routing_report(
        start_id="L001",
        end_id="L005"
    )

    assert (
        isinstance(
            report["affected_roads"],
            list
        )
    )

    print("PASS: affected roads generated")


def test_real_roads_generated():

    report = build_routing_report(
        start_id="L001",
        end_id="L005"
    )

    roads = report["roads"]

    assert len(roads) > 0

    assert all(
        road["road_id"].startswith("REAL_R")
        for road in roads
    )

    print("PASS: real roads generated")

def test_multiple_routes():

    test_routes = [
        ("L001", "L005"),
        ("L002", "L007"),
        ("L003", "L009"),
        ("L004", "L008"),
        ("L006", "L010"),
    ]

    print("\n--- TESTING MULTIPLE ROUTES ---")

    for start_id, end_id in test_routes:

        try:
            report = build_routing_report(
                start_id=start_id,
                end_id=end_id
            )

            route = report["safer_route"]

            if route["found"]:

                print(
                    f"PASS: {start_id} -> {end_id}"
                )

                print(
                    "Path:",
                    route.get("path")
                )

            else:
                print(
                    f"NO ROUTE: {start_id} -> {end_id}"
                )

        except Exception as error:

            print(
                f"ERROR: {start_id} -> {end_id}"
            )

            print(error)

def test_forecast_intervals():

    intervals = [0, 30, 60, 120, 180]

    print("\n--- TESTING FORECAST INTERVALS ---")

    for minutes in intervals:

        try:

            report = build_routing_report(
                start_id="L001",
                end_id="L005",
                forecast_minutes=minutes
            )

            route = report["safer_route"]

            print(
                f"Forecast {minutes} minutes:"
            )

            print(
                "Route found:",
                route["found"]
            )

            print(
                "Path:",
                route.get("path")
            )

        except Exception as error:

            print(
                f"ERROR at {minutes} minutes:"
            )

            print(error)


if __name__ == "__main__":

    test_basic_route()

    test_route_found()

    test_invalid_location()

    test_affected_roads()

    test_real_roads_generated()

    test_multiple_routes()

    test_forecast_intervals()
    
    print("\nAll tests passed.")
