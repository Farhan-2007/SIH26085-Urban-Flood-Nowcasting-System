# Flood Dataset

Dataset package for the SIH26085 Urban Flood Nowcasting System.

## Dataset Contents

### Sample / Prototype Datasets

The following datasets currently contain sample/mock values for prototype development:

- `data/raw/locations.csv`
- `data/raw/sample_environmental_data.csv`
- `data/raw/sample_forecast.csv`
- `datasets/processed/flood_features.csv`

These datasets contain 10 sample locations (L001–L010).

## Forecast Data

`sample_forecast.csv` contains rainfall forecast values for:

- 0 minutes
- 30 minutes
- 60 minutes
- 120 minutes
- 180 minutes

Each of the 10 sample locations has all 5 forecast intervals, giving 50 forecast rows in total.

## Common Fields

- `location_id`: Unique location identifier
- `location_name`: Location name
- `latitude`: Latitude in decimal degrees
- `longitude`: Longitude in decimal degrees
- `rainfall`: Rainfall intensity in mm/hr
- `water_level`: Water level in metres
- `soil_saturation`: Soil saturation from 0–1
- `elevation`: Elevation in metres
- `slope`: Slope in degrees
- `imperviousness`: Imperviousness from 0–1
- `drainage_capacity`: Drainage capacity in L/s
- `drainage_capacity_used`: Used drainage capacity in L/s
- `forecast_minutes`: Forecast interval in minutes

## Units

| Field | Unit |
|---|---|
| rainfall | mm/hr |
| water_level | m |
| soil_saturation | 0–1 |
| elevation | m |
| slope | degrees |
| imperviousness | 0–1 |
| drainage_capacity | L/s |
| drainage_capacity_used | L/s |
| forecast_minutes | minutes |

## Real Rainfall Source

A separate Mumbai rainfall dataset was obtained from the Government of India's Open Government Data platform.

File:

`data/raw/rainfall/mumbai_rainfall_2025.csv`

The source contains daily rainfall values and progressive cumulative rainfall for Mumbai City from 1 June 2025 to 13 August 2025.

The processed copy is:

`data/processed/rainfall/mumbai_daily_rainfall.csv`

The source rainfall is daily rainfall in mm and should NOT be treated as mm/hr.

## Data Status

The current 10-location environmental and forecast datasets are sample/mock values created for prototype integration.

Real/derived datasets can replace individual fields as they become available.

Real, derived, and assumed values must be clearly identified before final deployment.

## Purpose

The finalized dataset is intended to serve as the common input for the Predictor, Flood Risk Engine and Flask backend.