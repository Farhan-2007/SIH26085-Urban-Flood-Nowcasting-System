import { CircleMarker, Popup } from "react-leaflet";
import { getRiskColor } from "./riskColor";


function normalizeRiskLevel(level, score) {
  const normalized = String(level || "").toUpperCase();

  // Backend uses "Moderate", map uses "MEDIUM"
  if (normalized === "MODERATE") {
    return "MEDIUM";
  }

  // Valid risk levels
  if (
    ["LOW", "MEDIUM", "HIGH", "CRITICAL"].includes(
      normalized
    )
  ) {
    return normalized;
  }

  // Fallback based on risk score
  if (score >= 80) {
    return "CRITICAL";
  }

  if (score >= 60) {
    return "HIGH";
  }

  if (score >= 30) {
    return "MEDIUM";
  }

  return "LOW";
}


export default function LocationMarkers({
  locations,
  forecastLabel,
  selectedLocation,
  onSelectLocation,
}) {

  console.log(
    "GIS Locations:",
    locations
  );


  // Do not render markers if
  // location data is unavailable.
  if (
    !locations ||
    locations.length === 0
  ) {
    return null;
  }


  return (
    <>

      {locations.map((location) => {

        /*
         * Convert risk score safely.
         *
         * If the backend returns null,
         * undefined, or invalid data,
         * default to 0.
         */
        const riskScore =
          Number(location.risk_score) || 0;


        /*
         * Normalize backend risk level
         * for map visualization.
         */
        const riskLevel =
          normalizeRiskLevel(
            location.risk_level,
            riskScore
          );


        /*
         * Get marker color based
         * on normalized risk level.
         */
        const markerColor =
          getRiskColor(riskLevel);


        /*
         * Locations with a risk score
         * of 70 or above are treated
         * as flood hotspots.
         */
        const isHotspot =
          riskScore >= 70;


        /*
         * Check whether this location
         * is currently selected.
         *
         * Comparing location IDs instead
         * of entire objects ensures this
         * still works after GIS data
         * refreshes for another forecast.
         */
        const isSelected =
          selectedLocation?.location_id ===
          location.location_id;


        return (
          <CircleMarker
            key={location.location_id}

            center={[
              location.latitude,
              location.longitude,
            ]}

            /*
             * Selected location is largest.
             * Hotspots are larger than
             * normal locations.
             */
            radius={
              isSelected
                ? 16
                : isHotspot
                  ? 14
                  : 10
            }

            pathOptions={{

              /*
               * Selected location gets
               * a strong black border.
               */
              color:
                isSelected
                  ? "#000000"
                  : markerColor,

              fillColor:
                markerColor,

              /*
               * Selected marker is fully
               * visible.
               */
              fillOpacity:
                isSelected
                  ? 1
                  : 0.8,

              /*
               * Increase border thickness
               * for hotspots and selected
               * locations.
               */
              weight:
                isSelected
                  ? 5
                  : isHotspot
                    ? 4
                    : 2,

            }}

            /*
             * Clicking a location sends
             * the selected location back
             * to useDashboardData().
             */
            eventHandlers={{

              click: () => {

                onSelectLocation?.(
                  location
                );

              },

            }}
          >

            <Popup>

              {/* Location name */}

              <strong>
                {location.location_name}
              </strong>


              {/* Selected indicator */}

              {isSelected && (
                <>

                  <br />

                  <strong>
                    📍 SELECTED LOCATION
                  </strong>

                </>
              )}


              <br />

              Location ID:{" "}
              {location.location_id}


              <br />

              Forecast:{" "}
              {forecastLabel || "NOW"}


              <br />

              Risk:{" "}
              {riskLevel}


              <br />

              Risk Score:{" "}
              {riskScore.toFixed(1)}
              /100


              <br />

              Rainfall:{" "}
              {location.rainfall ?? "N/A"}
              {" mm/hr"}


              <br />

              Surface Runoff:{" "}
              {location.surface_runoff ?? "N/A"}


              <br />

              Drainage Used:{" "}

              {location.drainage_capacity_used !==
              undefined
                ? `${Math.round(
                    location.drainage_capacity_used * 100
                  )}%`
                : "N/A"}


              {/* Hotspot warning */}

              {isHotspot && (
                <>

                  <br />

                  <strong>
                    🔥 FLOOD HOTSPOT
                  </strong>

                </>
              )}

            </Popup>

          </CircleMarker>
        );

      })}

    </>
  );
}