# Routing Module — Flood-Safe Route Planning

The Routing Module finds safer paths through flood-affected areas by analyzing real-time risk data and applying intelligent path optimization.

## Overview

This module provides a complete routing engine that:
- Identifies roads affected by high flood risk
- Detects locations where risk is intensifying
- Computes safer routes using a risk-weighted Dijkstra algorithm
- Avoids or penalizes high-risk roads while finding practical alternatives

**Design Philosophy:** Modular, zero external dependencies (uses only Python stdlib), and designed to integrate seamlessly with the Analyser's output.

---

## Files and Components

### Core Modules

| Module | Purpose |
|--------|---------|
| **routing_engine.py** | Main entry point; orchestrates all components and returns a comprehensive routing report |
| **road_network.py** | Graph abstraction using adjacency lists; no external dependencies |
| **affected_roads.py** | Identifies which roads are unsafe (touching High/Critical risk locations); detects shifting risk |
| **safer_route.py** | Implements Dijkstra with risk-weighted edge costs to find safer paths |

### Data & Testing

| File | Purpose |
|------|---------|
| **mock_data.py** | Mock locations, roads, and risk data for standalone development and testing |
| **test_routing.py** | 5 basic sanity tests; run with `python3 test_routing.py` |

---

## Quick Start

### 1. Run Demo

```bash
cd routing
python3 routing_engine.py
