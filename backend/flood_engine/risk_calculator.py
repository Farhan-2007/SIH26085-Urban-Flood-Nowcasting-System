from .threshold import (
    RAINFALL_REFERENCE,
    INTENSITY_REFERENCE,
    WATER_LEVEL_REFERENCE,
    FORECAST_REFERENCE,
    RAINFALL_WEIGHT,
    WATER_LEVEL_WEIGHT,
    INTENSITY_WEIGHT,
    FORECAST_WEIGHT
)


def normalize(value, reference):
    """
    Convert input into a 0-100 score.
    """
    return min((value / reference) * 100, 100)


def calculate_risk_score(
    rainfall,
    rainfall_intensity,
    water_level,
    forecast_rainfall
):
    """
    Calculate flood risk score from 0 to 100.
    """

    rainfall_score = normalize(
        rainfall,
        RAINFALL_REFERENCE
    )

    intensity_score = normalize(
        rainfall_intensity,
        INTENSITY_REFERENCE
    )

    water_level_score = normalize(
        water_level,
        WATER_LEVEL_REFERENCE
    )

    forecast_score = normalize(
        forecast_rainfall,
        FORECAST_REFERENCE
    )

    risk_score = (
        rainfall_score * RAINFALL_WEIGHT
        + intensity_score * INTENSITY_WEIGHT
        + water_level_score * WATER_LEVEL_WEIGHT
        + forecast_score * FORECAST_WEIGHT
    )

    return round(risk_score, 2)


def determine_risk_level(risk_score):
    """
    Convert risk score into a flood risk level.
    """

    if risk_score < 25:
        return "LOW"

    elif risk_score < 50:
        return "MEDIUM"

    elif risk_score < 75:
        return "HIGH"

    else:
        return "CRITICAL"


def calculate_flood_risk(
    rainfall,
    rainfall_intensity,
    water_level,
    forecast_rainfall
):
    """
    Main Flood Engine function.
    """

    risk_score = calculate_risk_score(
        rainfall,
        rainfall_intensity,
        water_level,
        forecast_rainfall
    )

    risk_level = determine_risk_level(risk_score)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level
    }