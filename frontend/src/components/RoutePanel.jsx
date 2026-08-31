import { useEffect, useMemo, useState } from "react";

import { getSafeRoute } from "../services/api";

import "./RoutePanel.css";


export default function RoutePanel({
  locations,
  selectedLocation,
  selected,
  routeData,
  onRouteDataChange,
}) {

  // ==========================================================
  // STATE
  // ==========================================================

  const [startId, setStartId] =
    useState("");

  const [endId, setEndId] =
    useState("L010");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState(null);

  // Show all affected roads or only first 3
  const [showAllAffected, setShowAllAffected] =
    useState(false);


  // ==========================================================
  // FORECAST TIME
  // ==========================================================

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
  // RESET "SEE MORE" WHEN ROUTE DATA CHANGES
  // ==========================================================

  useEffect(() => {

    setShowAllAffected(false);

  }, [
    routeData
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


      const data =
        await getSafeRoute(
          startId,
          endId,
          forecastMinutes
        );


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
  // SAFE ROUTE
  // ==========================================================

  const safeRoute =
    routeData?.safer_route;


  // ==========================================================
  // BUILD ROAD NAME MAP
  //
  // Converts:
  //
  // REAL_R001
  //
  // into:
  //
  // Dadar → Mahim
  //
  // We use backend road data first and affected-road data
  // as a fallback.
  // ==========================================================

  const roadNameMap = useMemo(() => {

    const map = {};


    // --------------------------------------------------------
    // 1. Use roads returned by backend
    // --------------------------------------------------------

    const roads =
      routeData?.roads || [];


    roads.forEach((road) => {

      const roadId =
        road?.road_id ||
        road?.id;


      if (!roadId) {
        return;
      }


      // Backend already provides road_name
      if (
        road?.road_name &&
        road.road_name !== roadId
      ) {

        map[roadId] =
          road.road_name;

        return;

      }


      // Build from endpoint names
      if (
        road?.from_name &&
        road?.to_name
      ) {

        map[roadId] =
          `${road.from_name} → ${road.to_name}`;

      }

    });


    // --------------------------------------------------------
    // 2. Use affected roads as fallback
    // --------------------------------------------------------

    const affectedRoads =
      routeData?.affected_roads || [];


    affectedRoads.forEach((road) => {

      if (!road?.road_id) {
        return;
      }


      if (
        road.from_name &&
        road.to_name
      ) {

        map[road.road_id] =
          `${road.from_name} → ${road.to_name}`;

      }

    });


    return map;

  }, [
    routeData
  ]);


  // ==========================================================
  // GET READABLE ROAD NAME
  // ==========================================================

  function getRoadDisplayName(
    roadId
  ) {

    if (!roadId) {
      return "Unknown Road";
    }


    return (
      roadNameMap[roadId] ||
      roadId
    );

  }


  // ==========================================================
  // AFFECTED ROADS
  // ==========================================================

  const affectedRoads =
    routeData?.affected_roads || [];


  const visibleAffectedRoads =
    showAllAffected
      ? affectedRoads
      : affectedRoads.slice(
          0,
          3
        );


  const hasMoreAffectedRoads =
    affectedRoads.length > 3;


  // ==========================================================
  // RENDER
  // ==========================================================

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

          {
            forecastMinutes === 0
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

            {
              loading
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


              {/* ================================================== */}
              {/* ROUTE SUMMARY */}
              {/* ================================================== */}

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


              {/* ================================================== */}
              {/* ROADS USED */}
              {/* ================================================== */}

              <div className="route-roads">

                <span className="route-label">
                  🛣️ Safe roads for your route
                </span>


                <div className="route-road-list">

                  {
                    safeRoute.roads_used?.map(
                      (roadId) => (

                        <span
                          key={roadId}
                          className="route-road"
                          title={roadId}
                        >

                          {
                            getRoadDisplayName(
                              roadId
                            )
                          }

                        </span>

                      )
                    )
                  }

                </div>

              </div>


              {/* ================================================== */}
              {/* HIGH RISK ROADS AVOIDED */}
              {/* ================================================== */}

              <div className="route-avoided">

                <span className="route-label">

                  ⚠️ Avoid These High-Risk Roads

                </span>


                <div className="route-road-list">

                  {
                    (
                      safeRoute
                        .avoided_high_risk_road_names
                        ?.length
                        ? safeRoute
                            .avoided_high_risk_road_names
                        : safeRoute
                            .avoided_high_risk_roads
                    )?.map(
                      (road, index) => (

                        <span
                          key={`${road}-${index}`}
                          className="route-road route-road--avoid"
                        >

                          {
                            safeRoute
                              .avoided_high_risk_road_names
                              ?.length
                              ? road
                              : getRoadDisplayName(
                                  road
                                )
                          }

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
          affectedRoads.length > 0 && (

            <div className="affected-roads">

              <div className="affected-roads-header">

                <h3>
                  Affected Roads
                </h3>

              </div>


              {/* ================================================== */}
              {/* AFFECTED ROAD LIST */}
              {/* ================================================== */}

              <div className="affected-road-list">

                {
                  visibleAffectedRoads.map(
                    (road) => (

                      <div
                        key={
                          road.road_id
                        }
                        className="affected-road"
                      >

                        {/* LEFT */}

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


                        {/* RIGHT */}

                        <div className="affected-road-status">

                          <span
                            className={
                              `risk-tag risk-tag--${(
                                road.risk_level ||
                                "low"
                              ).toLowerCase()}`
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


              {/* ================================================== */}
              {/* SEE MORE / SEE LESS */}
              {/* ================================================== */}

              {
                hasMoreAffectedRoads && (

                  <div className="affected-roads-toggle">

                    <button
                      type="button"
                      className="affected-roads-toggle-button"
                      onClick={() =>
                        setShowAllAffected(
                          (current) =>
                            !current
                        )
                      }
                    >

                      {
                        showAllAffected
                          ? "See Less Affected Roads"
                          : `See More Affected Roads (${affectedRoads.length - 3} more)`
                      }

                    </button>

                  </div>

                )
              }

            </div>

          )
        }

      </div>

    </section>

  );

}