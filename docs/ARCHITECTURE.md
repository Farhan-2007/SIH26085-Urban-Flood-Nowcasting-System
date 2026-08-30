## 1. SIH26085 – Urban Flood Nowcasting System
> A real-time environmental analysis, short-term flood forecasting, and risk-aware emergency routing platform.
> 
The Urban Flood Nowcasting System processes environmental, geographical, and meteorological data to estimate localized flood risks in urban environments. Beyond static risk mapping, the system continuously analyzes risk trends, projects dynamic short-term forecasts, detects impacted roadways, and calculates safer routes by factoring flood risk penalties into navigation algorithms.

## 2. Executive Summary
 * Real-time Assessment & Forecasting: Instant evaluation of surface risk with short-term projections up to 180 minutes.
 * Dynamic Trend Analysis: Continuous monitoring of risk shifts across locations (Increasing, Stable, Decreasing).
 * Risk-Aware Routing: Custom Dijkstra routing implementation that applies dynamic cost multipliers to flood-prone roads to prioritize safety over distance.
 * Modular Full-Stack Architecture: Powered by a Python/Flask analytics engine and a React visual dashboard.
## 3. High-Level Architecture
   
               [ Environmental & Rainfall Data ]
                              │
                              ▼
                      [ Data Processing ]
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
       [ Predictor ]                    [ Analyser ]
              │                               │
              └───────────────┬───────────────┘
                              ▼
                     [ Risk Assessment ]
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
        [ Forecast ]                     [ Routing ]
              │                               │
              ▼                               ▼
         [ Alerts ]                    [ Safer Route ]
              │                               │
              └───────────────┬───────────────┘
                              ▼
                         [ Flask API ]
                              │
                              ▼
                      [ React Dashboard ]
                              │
                              ▼
                   [ Map & Visualisation ]

## 4. System Components & Data Schema
### 4.1 Data Layer
The data layer ingests continuous metrics to generate terrain and runoff baselines.


| Field | Description | Purpose |
|---|---|---|
| Location ID / Name | Unique string identifier & label | Human-readable spatial mapping |
| Lat / Long | Geographic coordinates | Spatial positioning & distance math |
| Rainfall | Intensity measurement | Surface water input volume |
| Water Level | Absolute depth gauge | Accumulation tracking |
| Soil Saturation | Percentage absorption | Infiltration capacity calculation |
| Elevation / Slope | Digital Elevation Model parameters | Gravity flow & pooling estimation |
| Imperviousness | Urban surface ratio | Runoff coefficient calculation |
| Drainage Capacity | Infrastructure throughput rate | Discharge rate monitoring |


### 4.2 Predictor & Analyser Modules
The Predictor Module computes immediate surface risk scores and generates future projections across defined time intervals:

Intervals:  [ 0 Min ] ──► [ 30 Min ] ──► [ 60 Min ] ──► [ 120 Min ] ──► [ 180 Min ]

            Current       Immediate      Short-Term     Extended        Longer Term



The Analyser Module evaluates spatial temporal shifts by comparing state histories:
 * Decreasing: Water receding or absorption exceeding rainfall rate.
 * Stable: Steady-state runoff and drainage.
 * Increasing / Shifting: Escalating risk or active flood boundary expansion.
### 4.3 Risk Assessment Matrix
Combined predictor and analyzer outputs output a discrete classification level used across alerts and navigation:


| Risk Level | Meaning | Routing Action |
|---|---|---|
| Low | Normal conditions; minimal surface water | Standard routing |
| Moderate | Rising water potential; monitoring required | Minor cost penalty applied |
| High | Significant water buildup; local road hazard | Heavy route avoidance |
| Critical | Severe flooding; impassable hazards | Strict exclusion / Max penalty |
## 5. Risk-Aware Routing Engine

Standard navigation algorithms select the shortest physical path regardless of road hazards. This system adjusts the edge weights of the road graph dynamically using Risk Cost Multipliers before executing Dijkstra's Algorithm.
Risk Multiplier Matrix


| Risk Classification | Cost Multiplier (M) | Example (2.0 km Segment) | Calculated Route Weight |
|---|---|---|---|
| Low | 1.0x | 2.0 \times 1.0 | 2.0 |
| Moderate | 1.5x | 2.0 \times 1.5 | 3.0 |
| High | 3.0x | 2.0 \times 3.0 | 6.0 |
| Critical | 8.0x | 2.0 \times 8.0 | 16.0 |


    [ Start ] ════════════════════════════════════════════ [ Destination ]
        ║                                                        ▲
        ║ (Shortest Path: 2.0 km - HIGH RISK)                    ║
        ║ Weight: 2.0 x 3.0 = 6.0                                ║
        ▼                                                        ║
    [ High Risk Zone ] ──────────────────────────────────────────┘
        
        VS.
        
    [ Start ] ──────────────────────────────────────────── [ Destination ]
        ║                                                        ▲
        ║ (Detour Path: 3.5 km - LOW RISK)                       ║
        ║ Weight: 3.5 x 1.0 = 3.5  ◄── SELECTED (SAFEST)         ║
        ╚════════════════════════════════════════════════════════╝



### Project Structure

```text
SIH26085-Urban-Flood-Nowcasting-System/
│
├── backend/
│   │
│   ├── app.py
│   │   Main Flask application and API entry point.
│   │
│   ├── predictor/
│   │   └── predictor.py
│   │       Generates flood risk predictions and forecasts.
│   │
│   ├── analyser/
│   │   └── analyser.py
│   │       Analyses environmental conditions and flood-risk trends.
│   │
│   ├── routing/
|   |   │
|   |   ├── __init__.py
|   |   │   Makes the routing folder available as a Python package.
|   |   │
|   |   ├── routing_engine.py
|   |   │   Contains the main routing logic, risk penalties and
|   |   │   Dijkstra-based safer route calculation.
|   |   │
|   |   ├── real_road_data.py
|   |   │   Creates or loads road connections using location
|   |   │   coordinates and distance calculations.
|   |   │
|   |   ├── test_routing.py
|   |   │   Tests route generation, affected roads and different
|   |   │   start and destination combinations.
|   |   │
|   |   └── Other routing files
|   |   Supporting routing-related functionality.
│   └── Other backend modules
│       Supporting flood-risk calculations and API functionality.
│
├── frontend/
│   │
│   ├── Dashboard components
│   ├── Map components
│   ├── Forecast components
│   ├── Alert components
│   └── API integration
│
├── data/
│   │
│   └── Environmental and location-related data.
│
├── datasets/
│   │
│   └── Datasets used for flood prediction and analysis.
│
├── tests/
│   │
│   └── Testing files for different system components.
│
├── docs/
│   │
│   └── ARCHITECTURE.md
│       Project architecture and technical documentation.
│
├── requirements.txt
│   Python dependencies required by the project.
│
└── README.md
    Main project documentation and setup instructions.
```

---

### Module Responsibilities

| Module | Main Responsibility |
|---|---|
| Backend | Handles APIs and core application logic |
| Predictor | Calculates flood risk and future forecasts |
| Analyser | Detects changing flood conditions and trends |
| Routing | Finds safer routes based on flood risk |
| Frontend | Displays dashboard, maps, alerts and forecasts |
| Data | Provides environmental and geographical information |
| Tests | Validates system functionality |
| Docs | Stores project documentation |

---

### Backend Component Flow

```text
                    Flask Application
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
    Predictor           Analyser           Routing
        |                  |                  |
        +------------------+------------------+
                           |
                           v
                    Risk Information
                           |
                           v
                       API Response
```

---

### Routing Module Structure

| File | Responsibility |
|---|---|
| `routing_engine.py` | Builds the routing graph and calculates safer routes |
| `real_road_data.py` | Generates road connections using real location coordinates |
| `test_routing.py` | Tests routing behaviour and different route combinations |

---

### Module Communication

```text
Environmental Data
        |
        v
Data Processing
        |
        +-------------------+
        |                   |
        v                   v
   Predictor             Analyser
        |                   |
        +--------+----------+
                 |
                 v
          Risk Assessment
                 |
                 +------------------+
                 |                  |
                 v                  v
             Forecasting         Routing
                 |                  |
                 v                  v
               Alerts          Safer Route
                 |                  |
                 +--------+---------+
                          |
                          v
                      Flask API
                          |
                          v
                    React Frontend
```
## 6. Tech Stack
Frontend & Visualizations
 * React: Interactive user interface and layout components.
 * Vite: High-performance web development build tool.
 * JavaScript / HTML5 / CSS3: Core application logic and custom layout styling.
Backend & Analytics
 * Python: Data processing pipeline and routing execution.
 * Flask: REST API endpoint provider.
 * Pandas & NumPy: Linear algebra, spatial metrics, and data structures.


## 7. End-to-End Data Pipeline

The system processes environmental inputs through a sequential data pipeline, transforming raw sensor measurements into dynamic routing decisions displayed on the web interface.

### 7.1 Data Flow Architecture



    +------------------+     +-----------------------+     +---------------------+
    | Data Ingestion   | --> | Risk Assessment Engine| --> | Dynamic Road Graph  |
    | (Rain, Soil, DEM)|     | (Predictor & Analyser)|     | Cost Allocation     |
    +------------------+     +-----------------------+     +---------------------+
                                                                    |
                                                                    v
    +------------------+     +-----------------------+     +---------------------+
    | React Dashboard  | <-- | Flask REST API        | <-- | Safer Route Engine  |
    | & Visualisation  |     | (JSON Output)         |     | (Dijkstra Execution)|
    +------------------+     +-----------------------+     +---------------------+


### 7.2 Stage Breakdown

1. **Data Ingestion & Preprocessing**
   * Collects rainfall intensity, water levels, soil saturation, and digital elevation model (DEM) metrics.
   * Standardizes spatial coordinates and calculates surface runoff parameters.

2. **Risk Assessment & Trend Forecasting**
   * **Predictor:** Computes risk scores for time intervals from 0 to 180 minutes.
   * **Analyser:** Determines directional spatial trends (Increasing, Stable, Decreasing).

3. **Dynamic Graph Penalty Assignment**
   * Maps calculated risk scores onto connected road network edges.
   * Applies safety multipliers to physical edge weights based on risk level.

4. **Safer Path Calculation**
   * Executes Dijkstra's algorithm over the re-weighted road graph.
   * Resolves paths that balance total distance against flood hazard avoidance.

5. **API & Interface Delivery**
   * Transmits route geometries, affected road arrays, and forecast timelines via JSON REST endpoints.
   * Renders spatial overlays and alternative navigation paths on the React user dashboard.



## 8. Roadmap & Future Enhancements
 * Real-Time IoT Integration: Direct hookups to live rain gauge and water-level telemetry.
 * External GIS Networks: Import full OpenStreetMap (OSM) highway networks via OSMNx.
 * Dynamic Traffic Overlay: Merging live vehicular congestion speeds with flood delays.
 * Emergency Prioritization: Fast-path routing for emergency response vehicles (ambulances, fire engines).
