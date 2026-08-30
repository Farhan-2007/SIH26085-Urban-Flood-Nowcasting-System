from data_loader import get_all_locations

locations = get_all_locations()

for location in locations:
    print(
        location["location_id"],
        "|",
        location["location_name"],
        "|",
        location["latitude"],
        "|",
        location["longitude"],
    )