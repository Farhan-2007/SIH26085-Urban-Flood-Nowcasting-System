def validate_flood_input(data):
    required_fields = [
        "rainfall",
        "rainfall_intensity",
        "water_level",
        "forecast_rainfall"
    ]

    for field in required_fields:

        # Check if field exists
        if field not in data:
            return False, f"Missing field: {field}"

        # Check if value is a number
        if not isinstance(data[field], (int, float)):
            return False, f"{field} must be a number"

        # Check if value is negative
        if data[field] < 0:
            return False, f"{field} cannot be negative"

    return True, None