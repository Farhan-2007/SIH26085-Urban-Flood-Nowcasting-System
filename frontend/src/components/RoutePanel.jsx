import { useEffect, useState } from "react";
import { getSafeRoute } from "../services/api";

import "./RoutePanel.css";


export default function RoutePanel({
  locations,
  selectedLocation,
  selected,
  routeData,
  onRouteDataChange,
}) {

  const [startId, setStartId] =
    useState("");

  const [endId, setEndId] =
    useState("L010");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState(null);


  // Get currently selected forecast time
  const forecastMinutes =
    selected?.minutes ??
    selected?.forecast_minutes ??
    0;


  // ==========================================================
  // UPDATE START LOCATION WHEN GIS MARKER IS SELECTED
  // ==========================================================

  useEffect(() => {

    if (
      selectedLocation?.location_id
    ) {

      setStartId(
        selectedLocation.location_id
      );

    }

  }, [
    selectedLocation
  ]);


  // ==========================================================
  // LOAD SAFE ROUTE
  // ==========================================================

  async function loadRoute() {

    if (
      !startId ||
      !endId
    ) {

      return;

    }


    if (
      startId === endId
    ) {

      setError(
        "Start and destination locations must be different."
      );

      return;

    }


    try {

      setLoading(true);

      setError(null);


      // Send selected forecast time to backend
      const data =
        await getSafeRoute(
          startId,
          endId,
          forecastMinutes
        );


      // Send route data to App.jsx
      onRouteDataChange?.(
        data
      );

    } catch (error) {

      console.error(
        "Failed to load safe route:",
        error
      );


      setError(
        error.message ||
        "Unable to generate safe route."
      );

    } finally {

      setLoading(false);

    }

  }


  // ==========================================================
  // AUTOMATICALLY RECALCULATE ROUTE
  //
  // Updates when:
  // - Start location changes
  // - Destination changes
  // - Forecast timeline changes
  // ==========================================================

  useEffect(() => {

    if (

      startId &&
      endId &&
      startId !== endId

    ) {

      loadRoute();

    }

  }, [

    startId,
    endId,
    forecastMinutes,

  ]);


  // ==========================================================
  // ROUTE DATA
  // ==========================================================

  const safeRoute =
    routeData?.safer_route;


  return (

    <section className="panel route-panel">


      {/* ================================================== */}
      {/* HEADER */}
      {/* ================================================== */}

      <div className="panel-header">

        <h2>
          Safe Route Intelligence
        </h2>

        <span className="eyebrow">

          Dynamic Routing
          {" • "}
          {forecastMinutes === 0
            ? "NOW"
            : `+${forecastMinutes} min`
          }

        </span>

      </div>


      <div className="panel-body">


        {/* ================================================== */}
        {/* ROUTE CONTROLS */}
        {/* ================================================== */}

        <div className="route-controls">


          {/* START LOCATION */}

          <div className="route-control">

            <label>
              Start Location
            </label>

            <select

              value={startId}

              onChange={(event) =>
                setStartId(
                  event.target.value
                )
              }

            >

              <option value="">
                Select start location
              </option>


              {locations.map(
                (location) => (

                  <option

                    key={
                      location.location_id
                    }

                    value={
                      location.location_id
                    }

                  >

                    {
                      location.location_name
                    }

                  </option>

                )
              )}

            </select>

          </div>


          {/* DESTINATION */}

          <div className="route-control">

            <label>
              Destination
            </label>

            <select

              value={endId}

              onChange={(event) =>
                setEndId(
                  event.target.value
                )
              }

            >

              {locations.map(
                (location) => (

                  <option

                    key={
                      location.location_id
                    }

                    value={
                      location.location_id
                    }

                  >

                    {
                      location.location_name
                    }

                  </option>

                )
              )}

            </select>

          </div>


          {/* BUTTON */}

          <button

            className="route-button"

            onClick={loadRoute}

            disabled={loading}

          >

            {loading

              ? "Calculating..."

              : "Find Safe Route"

            }

          </button>

        </div>


        {/* ================================================== */}
        {/* ERROR */}
        {/* ================================================== */}

        {error && (

          <div className="route-error">

            {error}

          </div>

        )}


        {/* ================================================== */}
        {/* SAFE ROUTE RESULT */}
        {/* ================================================== */}

        {

          safeRoute &&
          safeRoute.found && (

            <div className="route-result">


              {/* ROUTE SUMMARY */}

              <div className="route-summary">

                <div>

                  <span>
                    Safe Route
                  </span>

                  <strong>

                    {
                      safeRoute.path_names?.join(
                        " → "
                      )
                    }

                  </strong>

                </div>


                <div className="route-distance">

                  <span>
                    Total Distance
                  </span>

                  <strong className="mono">

                    {
                      safeRoute.total_distance_km
                    } km

                  </strong>

                </div>

              </div>


              {/* ROADS USED */}

              <div className="route-roads">

                <span className="route-label">

                  Roads Used

                </span>


                <div className="route-road-list">

                  {

                    safeRoute.roads_used?.map(
                      (road) => (

                        <span

                          key={road}

                          className="route-road"

                        >

                          {road}

                        </span>

                      )
                    )

                  }

                </div>

              </div>


              {/* HIGH RISK ROADS AVOIDED */}

              <div className="route-avoided">

                <span className="route-label">

                  High-Risk Roads Avoided

                </span>


                <div className="route-road-list">

                  {

                    safeRoute
                      .avoided_high_risk_roads
                      ?.map(
                        (road) => (

                          <span

                            key={road}

                            className={
                              "route-road route-road--avoid"
                            }

                          >

                            {road}

                          </span>

                        )
                      )

                  }

                </div>

              </div>

            </div>

          )

        }


        {/* ================================================== */}
        {/* ROUTE NOT FOUND */}
        {/* ================================================== */}

        {

          safeRoute &&
          !safeRoute.found && (

            <div className="route-empty">

              No safe route could be found
              between the selected locations.

            </div>

          )

        }


        {/* ================================================== */}
        {/* AFFECTED ROADS */}
        {/* ================================================== */}

        {

          routeData?.affected_roads
            ?.length > 0 && (

              <div className="affected-roads">

                <h3>
                  Affected Roads
                </h3>


                <div className="affected-road-list">

                  {

                    routeData
                      .affected_roads
                      .map(
                        (road) => (

                          <div

                            key={road.road_id}

                            className="affected-road"

                          >

                            <div>

                              <strong>

                                {
                                  road.from_name
                                }

                                {" → "}

                                {
                                  road.to_name
                                }

                              </strong>


                              <span>

                                {
                                  road.distance_km
                                } km

                              </span>

                            </div>


                            <div className="affected-road-status">

                              <span

                                className={

                                  `risk-tag risk-tag--${

                                    road.risk_level.toLowerCase()

                                  }`

                                }

                              >

                                {
                                  road.risk_level
                                }

                              </span>


                              <span>

                                {
                                  road.trend
                                }

                              </span>

                            </div>

                          </div>

                        )
                      )

                  }

                </div>

              </div>

            )

        }

      </div>

    </section>

  );

}