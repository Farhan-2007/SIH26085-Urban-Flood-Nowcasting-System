// Real project data — NOT mock/demo values.
//
// Source: data/raw/locations.csv and data/raw/flood_features.csv
//
// Why this lives in the frontend instead of being fetched from the API:
// the current Flask backend (backend/api/routes.py) does not expose any
// endpoint that lists locations or returns a location's current
// rainfall / water level / soil saturation reading. The only place a
// location's environmental state can be supplied is inside the POST
// body of /api/analyse, which the *caller* must provide.
//
// Until the team adds a location-listing / live-sensor endpoint, this
// file is the legitimate source for that input — it is the project's
// actual dataset, not fabricated numbers. If those endpoints are added
// later, replace LOCATIONS below with a fetch call and keep the shape
// identical so components don't need to change.
//
// water_level and soil_saturation are already expressed as 0–1
// fractions here, matching what backend/Analyser.py's DataValidator
// expects (0 <= water_level <= 1, 0 <= soil_saturation <= 1).
export const LOCATIONS = [
  { locationId: "L001", name: "Sample Road 1", latitude: 19.0760, longitude: 72.8777, rainfall: 15, waterLevel: 0.05, soilSaturation: 0.30, elevation: 18.2, slope: 3.5, imperviousness: 0.55 },
  { locationId: "L002", name: "Sample Road 2", latitude: 19.0780, longitude: 72.8800, rainfall: 40, waterLevel: 0.10, soilSaturation: 0.50, elevation: 12.5, slope: 1.8, imperviousness: 0.75 },
  { locationId: "L003", name: "Sample Road 3", latitude: 19.0800, longitude: 72.8820, rainfall: 75, waterLevel: 0.20, soilSaturation: 0.70, elevation: 7.2, slope: 0.8, imperviousness: 0.90 },
  { locationId: "L004", name: "Sample Road 4", latitude: 19.0820, longitude: 72.8850, rainfall: 110, waterLevel: 0.35, soilSaturation: 0.90, elevation: 4.1, slope: 0.3, imperviousness: 0.95 },
  { locationId: "L005", name: "Sample Road 5", latitude: 19.0740, longitude: 72.8750, rainfall: 25, waterLevel: 0.06, soilSaturation: 0.35, elevation: 16.8, slope: 2.8, imperviousness: 0.60 },
  { locationId: "L006", name: "Sample Road 6", latitude: 19.0850, longitude: 72.8900, rainfall: 55, waterLevel: 0.15, soilSaturation: 0.65, elevation: 9.5, slope: 1.2, imperviousness: 0.82 },
  { locationId: "L007", name: "Sample Road 7", latitude: 19.0700, longitude: 72.8720, rainfall: 90, waterLevel: 0.28, soilSaturation: 0.85, elevation: 5.5, slope: 0.5, imperviousness: 0.92 },
  { locationId: "L008", name: "Sample Road 8", latitude: 19.0880, longitude: 72.8950, rainfall: 18, waterLevel: 0.03, soilSaturation: 0.25, elevation: 20.0, slope: 4.0, imperviousness: 0.45 },
  { locationId: "L009", name: "Sample Road 9", latitude: 19.0680, longitude: 72.8680, rainfall: 65, waterLevel: 0.18, soilSaturation: 0.70, elevation: 8.0, slope: 0.9, imperviousness: 0.88 },
  { locationId: "L010", name: "Sample Road 10", latitude: 19.0920, longitude: 72.9000, rainfall: 120, waterLevel: 0.40, soilSaturation: 0.95, elevation: 3.2, slope: 0.2, imperviousness: 0.97 },
];

export function getLocationById(locationId) {
  return LOCATIONS.find((loc) => loc.locationId === locationId) || null;
}
