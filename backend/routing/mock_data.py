"""
mock_data.py
------------
Mumbai mock routing data.

IMPORTANT:
Location IDs match flood_features.csv and GIS locations.
"""

# ============================================================
# LOCATIONS
# ============================================================

# ============================================================
# LOCATIONS
#
# IMPORTANT:
# These IDs and coordinates must match
# sample_environmental_data.csv exactly.
# ============================================================

MOCK_LOCATIONS = [

    {
        "id": "L001",
        "name": "Dadar",
        "lat": 19.0760,
        "lon": 72.8777
    },

    {
        "id": "L002",
        "name": "Mahim",
        "lat": 19.0780,
        "lon": 72.8800
    },

    {
        "id": "L003",
        "name": "Worli",
        "lat": 19.0800,
        "lon": 72.8820
    },

    {
        "id": "L004",
        "name": "Prabhadevi",
        "lat": 19.0820,
        "lon": 72.8850
    },

    {
        "id": "L005",
        "name": "Matunga",
        "lat": 19.0740,
        "lon": 72.8750
    },

    {
        "id": "L006",
        "name": "Parel",
        "lat": 19.0850,
        "lon": 72.8900
    },

    {
        "id": "L007",
        "name": "Dharavi",
        "lat": 19.0700,
        "lon": 72.8720
    },

    {
        "id": "L008",
        "name": "Shivaji Park",
        "lat": 19.0880,
        "lon": 72.8950
    },

    {
        "id": "L009",
        "name": "Sion",
        "lat": 19.0680,
        "lon": 72.8680
    },

    {
        "id": "L010",
        "name": "Bandra East",
        "lat": 19.0920,
        "lon": 72.9000
    },

]

# ============================================================
# RISK DATA
# ============================================================

MOCK_RISK_DATA = {

    "L001": {
        "risk_score": 30,
        "risk_level": "Moderate",
        "trend": "Stable"
    },

    "L002": {
        "risk_score": 45,
        "risk_level": "Moderate",
        "trend": "Intensifying"
    },

    "L003": {
        "risk_score": 75,
        "risk_level": "High",
        "trend": "Intensifying"
    },

    "L004": {
        "risk_score": 90,
        "risk_level": "Critical",
        "trend": "Intensifying"
    },

    "L005": {
        "risk_score": 55,
        "risk_level": "Moderate",
        "trend": "Stable"
    },

    "L006": {
        "risk_score": 25,
        "risk_level": "Low",
        "trend": "Stable"
    },

    "L007": {
        "risk_score": 70,
        "risk_level": "High",
        "trend": "Intensifying"
    },

    "L008": {
        "risk_score": 20,
        "risk_level": "Low",
        "trend": "Receding"
    },

    "L009": {
        "risk_score": 60,
        "risk_level": "High",
        "trend": "Stable"
    },

    "L010": {
        "risk_score": 35,
        "risk_level": "Moderate",
        "trend": "Stable"
    },
}


# ============================================================
# ROAD NETWORK
# ============================================================

# ============================================================
# ROAD NETWORK
#
# IMPORTANT:
# Location IDs below match the REAL locations returned by
# backend.data_loader.get_all_locations()
# ============================================================

MOCK_ROADS = [

    # --------------------------------------------------------
    # SHIVAJI PARK ↔ DADAR
    # --------------------------------------------------------
    {
        "road_id": "R1",
        "from": "L008",   # Shivaji Park
        "to": "L001",     # Dadar
        "distance_km": 2.0
    },


    # --------------------------------------------------------
    # DADAR ↔ MAHIM
    # --------------------------------------------------------
    {
        "road_id": "R2",
        "from": "L001",   # Dadar
        "to": "L002",     # Mahim
        "distance_km": 3.0
    },


    # --------------------------------------------------------
    # MAHIM ↔ BANDRA EAST
    # --------------------------------------------------------
    {
        "road_id": "R3",
        "from": "L002",   # Mahim
        "to": "L010",     # Bandra East
        "distance_km": 4.5
    },


    # --------------------------------------------------------
    # DADAR ↔ PRABHADEVI
    # --------------------------------------------------------
    {
        "road_id": "R4",
        "from": "L001",   # Dadar
        "to": "L004",     # Prabhadevi
        "distance_km": 2.0
    },


    # --------------------------------------------------------
    # PRABHADEVI ↔ WORLI
    # --------------------------------------------------------
    {
        "road_id": "R5",
        "from": "L004",   # Prabhadevi
        "to": "L003",     # Worli
        "distance_km": 2.1
    },


    # --------------------------------------------------------
    # DADAR ↔ MATUNGA
    # --------------------------------------------------------
    {
        "road_id": "R6",
        "from": "L001",   # Dadar
        "to": "L005",     # Matunga
        "distance_km": 2.5
    },


    # --------------------------------------------------------
    # MATUNGA ↔ SION
    # --------------------------------------------------------
    {
        "road_id": "R7",
        "from": "L005",   # Matunga
        "to": "L009",     # Sion
        "distance_km": 3.0
    },


    # --------------------------------------------------------
    # MATUNGA ↔ PAREL
    # --------------------------------------------------------
    {
        "road_id": "R8",
        "from": "L005",   # Matunga
        "to": "L006",     # Parel
        "distance_km": 3.2
    },


    # --------------------------------------------------------
    # PAREL ↔ PRABHADEVI
    # --------------------------------------------------------
    {
        "road_id": "R9",
        "from": "L006",   # Parel
        "to": "L004",     # Prabhadevi
        "distance_km": 3.5
    },


    # --------------------------------------------------------
    # PAREL ↔ WORLI
    # --------------------------------------------------------
    {
        "road_id": "R10",
        "from": "L006",   # Parel
        "to": "L003",     # Worli
        "distance_km": 3.8
    },


    # --------------------------------------------------------
    # WORLI ↔ PRABHADEVI ↔ DADAR ALTERNATIVE
    # --------------------------------------------------------
    {
        "road_id": "R11",
        "from": "L003",   # Worli
        "to": "L001",     # Dadar
        "distance_km": 4.0
    },


    # --------------------------------------------------------
    # PAREL ↔ BANDRA EAST
    #
    # Longer alternate route connection
    # --------------------------------------------------------
    {
        "road_id": "R12",
        "from": "L006",   # Parel
        "to": "L010",     # Bandra East
        "distance_km": 7.5
    },

]