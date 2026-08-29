import { Polyline, Popup } from "react-leaflet";

export default function RouteLines({
  locations,
  routeData,
}) {
  if (!locations || !routeData) {
    return null;
  }

  const saferRoute = routeData.safer_route;

  if (!saferRoute?.found) {
    return null;
  }

  const roads = routeData.roads || [];

  const roadsUsed =
    saferRoute.roads_used || [];

  const avoidedRoads =
    saferRoute.avoided_high_risk_roads || [];


  // ------------------------------------
  // LOCATION LOOKUP
  // ------------------------------------

  const locationMap = {};

  locations.forEach((location) => {

    locationMap[location.location_id] = location;

  });


  // ------------------------------------
  // SAFE ROUTE ROADS
  // ------------------------------------

  const safeRouteRoads =
    roads.filter((road) =>
      roadsUsed.includes(road.road_id)
    );


  // ------------------------------------
  // AFFECTED ROADS
  // ------------------------------------

  const affectedRoads =
    routeData.affected_roads || [];


  return (
    <>

      {/* ============================ */}
      {/* AVOIDED HIGH RISK ROADS RED */}
      {/* ============================ */}

      {affectedRoads
        .filter((road) =>
          avoidedRoads.includes(road.road_id)
        )
        .map((road) => {

          const from =
            locationMap[road.from_id];

          const to =
            locationMap[road.to_id];

          if (!from || !to) {
            return null;
          }

          return (
            <Polyline
              key={`avoided-${road.road_id}`}

              positions={[
                [
                  from.latitude,
                  from.longitude,
                ],

                [
                  to.latitude,
                  to.longitude,
                ],
              ]}

              pathOptions={{
                color: "#ef4444",
                weight: 5,
                opacity: 0.8,
                dashArray: "10 10",
              }}
            >

              <Popup>

                <strong>
                  ⚠ Avoided High-Risk Road
                </strong>

                <br />

                Road: {road.road_id}

                <br />

                {road.from_name}
                {" → "}
                {road.to_name}

                <br />

                Risk: {road.risk_level}

              </Popup>

            </Polyline>
          );
        })}


      {/* ============================ */}
      {/* SAFE ROUTE BLUE */}
      {/* ============================ */}

      {safeRouteRoads.map((road) => {

        const from =
          locationMap[road.from];

        const to =
          locationMap[road.to];

        if (!from || !to) {
          return null;
        }

        return (
          <Polyline
            key={`safe-${road.road_id}`}

            positions={[
              [
                from.latitude,
                from.longitude,
              ],

              [
                to.latitude,
                to.longitude,
              ],
            ]}

            pathOptions={{
              color: "#2563eb",
              weight: 7,
              opacity: 1,
            }}
          >

            <Popup>

              <strong>
                🛣️ Safer Route
              </strong>

              <br />

              Road: {road.road_id}

              <br />

              {from.location_name}
              {" → "}
              {to.location_name}

              <br />

              Distance: {road.distance_km} km

            </Popup>

          </Polyline>
        );
      })}

    </>
  );
}