# Urban Flood Nowcasting System

## Problem Statement

Develop an Urban Flood Nowcasting System that provides real-time flood risk prediction, visualization, analysis, and safer route suggestions during urban flooding.

## Project Overview

The system aims to help citizens and authorities monitor potential flood situations using real-time and historical data. It will analyze factors such as rainfall, water levels, weather conditions, and geographical information to predict flood risk.

The platform will provide:

- Real-time flood risk monitoring
- Interactive GIS-based map visualization
- Flood prediction and analysis
- Risk zone identification
- Safe route suggestions
- Dashboard for monitoring important information
- Data collection and dataset preparation

## Team Members & Responsibilities

Member 1 : Frontend & Dashboard | Develop the web dashboard, user interface, risk visualization components, and frontend-backend integration

Member 2 : Map & GIS Visualization | Handle GIS data, map layers, terrain/DEM analysis, flood-zone visualization, and spatial processing

Member 3 : Backend & Flood Risk Engine | Develop backend APIs, flood-risk calculations, runoff analysis, drainage-capacity comparison, and hydraulic logic

Member 4 : Predictor–Analyser & Routing | Develop the Predictor–Analyser architecture, risk updates, prediction logic, affected-road detection, and safer route suggestions

Member 5 : Data Collection & Dataset Preparation | Collect rainfall, weather, terrain, drainage, and historical flood data; clean, process, and prepare datasets

Member 6 :  Testing, Documentation & Presentation | Perform system testing, validation, documentation, project reports, presentation preparation, and final demonstration

## Technology Stack

The technologies may include:

- Python
- Flask / FastAPI
- JavaScript
- HTML & CSS
- GIS and mapping tools
- Machine Learning
- Pandas and NumPy
- APIs for weather and rainfall data

## Project Structure

```text
SIH26085-Urban-Flood-Nowcasting-System/
│
├── frontend/       # Dashboard and user interface
├── gis/            # Maps and GIS visualization
├── backend/        # Backend services and APIs
├── flood_engine/   # Flood risk analysis engine
├── predictor/      # Prediction and analysis models
├── routing/        # Safe route suggestions
├── data/           # Collected data
├── datasets/       # Prepared datasets
├── tests/          # Testing
├── docs/           # Documentation
│
├── README.md
├── requirements.txt
└── .gitignore
