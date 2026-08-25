from .risk_calculator import calculate_flood_risk


def predict_flood_risk(
    rainfall,
    rainfall_intensity,
    water_level,
    forecast_rainfall
):
    """
    Generate flood risk prediction.
    """

    return calculate_flood_risk(
        rainfall=rainfall,
        rainfall_intensity=rainfall_intensity,
        water_level=water_level,
        forecast_rainfall=forecast_rainfall
    )