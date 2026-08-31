import json

from backend.data_loader import get_all_locations
from backend.routing.real_road_data import build_real_roads


OUTPUT_FILE = (
    "frontend/src/components/gis/geojson/roads.geojson"
)


def main():

    locations = get_all_locations()

    roads = build_real_roads(
        locations,
        max_distance_km=2.0
    )

    features = []

    for road in roads:

        geometry = road.get(
            "geometry",
            []
        )

        if not geometry:
            continue

        features.append({

            "type": "Feature",

            "properties": {

                "road_id":
                    road["road_id"],

                "from":
                    road["from"],

                "to":
                    road["to"],

                "distance_km":
                    road["distance_km"],

            },

            "geometry": {

                "type": "LineString",

                "coordinates":
                    geometry,

            },

        })

    geojson = {

        "type": "FeatureCollection",

        "features":
            features,

    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            geojson,
            file,
            indent=2
        )

    print(
        f"Generated {len(features)} roads"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()