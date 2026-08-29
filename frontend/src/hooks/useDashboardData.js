import { useEffect, useState } from "react";

import {
  getSystemInfo,
  getRainfallHistory,
  getRiskZones,
  getLastUpdated,
  analyseFloodConditions,
  getLocationsRisk,
} from "../services/api";


/*
 * Convert backend forecast data into
 * dashboard timeline data.
 */
function buildDashboardTimeline(analyserResult) {
  const backendTimeline = analyserResult.forecast;

  const selectedForecast = backendTimeline.filter(
    (step) =>
      [0, 60, 120, 180].includes(
        step.forecast_minutes
      )
  );

  return selectedForecast.map((step) => {
    let label = "NOW";

    if (step.forecast_minutes === 60) {
      label = "+1 HR";
    } else if (step.forecast_minutes === 120) {
      label = "+2 HR";
    } else if (step.forecast_minutes === 180) {
      label = "+3 HR";
    }

    return {
      id: `${step.forecast_minutes}min`,

      label,

      timeOffsetHours:
        step.forecast_minutes / 60,

      riskScore:
        step.forecast_minutes === 0
          ? analyserResult.analysis.flood_condition_index
          : step.risk_score,

      riskLevel:
        step.forecast_minutes === 0
          ? analyserResult.analysis.condition.toUpperCase()
          : step.risk_level.toUpperCase(),

      rainfallIntensity:
        step.rainfall,

      recentRainfall:
        step.rainfall,

      drainageCapacityUsed:
        Math.round(
          step.drainage_capacity_used * 100
        ),

      surfaceRunoff:
        step.surface_runoff >= 70
          ? "Very High"
          : step.surface_runoff >= 50
            ? "High"
            : step.surface_runoff >= 30
              ? "Moderate"
              : "Low",

      /*
       * Backend analyser stores water level
       * as a ratio between 0 and 1.
       * Convert it to percentage for dashboard.
       */
      waterLevel:
        Math.round(
          analyserResult.analysis
            .water_level_smoothed * 100
        ),

      soilSaturation:
        Math.round(
          analyserResult.analysis
            .soil_saturation_smoothed * 100
        ),

      forecastNote:
        step.prediction_status === "Intensifying"
          ? "Flood risk is increasing based on current rainfall and drainage conditions."
          : step.prediction_status === "Receding"
            ? "Flood risk is receding as rainfall decreases, although localized flooding may persist."
            : "Current flood conditions are stable.",
    };
  });
}


/*
 * Generate dynamic alerts from
 * backend GIS risk data.
 */
function buildDynamicAlerts(locations) {
  if (!locations || locations.length === 0) {
    return [];
  }

  const grouped = {
    CRITICAL: [],
    HIGH: [],
    MODERATE: [],
  };

  locations.forEach((location) => {
    const level =
      location.risk_level?.toUpperCase();

    if (grouped[level]) {
      grouped[level].push(location);
    }
  });

  const alerts = [];

  if (grouped.CRITICAL.length > 0) {
    const locationNames =
      grouped.CRITICAL
        .map(
          (location) =>
            location.location_name
        )
        .join(", ");

    alerts.push({
      id: "ALERT-CRITICAL",

      severity: "CRITICAL",

      title: "Critical Flood Warning",

      message:
        `Severe flooding risk predicted in ${grouped.CRITICAL.length} location(s). Immediate attention is recommended.`,

      zone:
        locationNames,

      time:
        "Forecast",
    });
  }

  if (grouped.HIGH.length > 0) {
    const locationNames =
      grouped.HIGH
        .map(
          (location) =>
            location.location_name
        )
        .join(", ");

    alerts.push({
      id: "ALERT-HIGH",

      severity: "HIGH",

      title: "High Flood Risk",

      message:
        `High flood risk detected in ${grouped.HIGH.length} location(s). Monitor drainage and traffic conditions.`,

      zone:
        locationNames,

      time:
        "Forecast",
    });
  }

  if (grouped.MODERATE.length > 0) {
    const locationNames =
      grouped.MODERATE
        .map(
          (location) =>
            location.location_name
        )
        .join(", ");

    alerts.push({
      id: "ALERT-MODERATE",

      severity: "MEDIUM",

      title: "Flood Risk Monitoring",

      message:
        `Moderate flood risk detected in ${grouped.MODERATE.length} location(s). Conditions should be monitored.`,

      zone:
        locationNames,

      time:
        "Forecast",
    });
  }

  return alerts;
}


export function useDashboardData() {

  const [loading, setLoading] =
    useState(true);

  const [systemInfo, setSystemInfo] =
    useState(null);

  const [timeline, setTimeline] =
    useState([]);

  const [rainfallHistory, setRainfallHistory] =
    useState([]);

  const [alerts, setAlerts] =
    useState([]);

  const [riskZones, setRiskZones] =
    useState([]);

  const [locations, setLocations] =
    useState([]);

  const [lastUpdated, setLastUpdated] =
    useState(null);

  const [analysis, setAnalysis] =
    useState(null);

  const [selectedLocation, setSelectedLocation] =
    useState(null);

  const [selectedStep, setSelectedStep] =
    useState(0);


  /*
   * Initial dashboard loading.
   */
  useEffect(() => {

    let cancelled = false;


    async function loadAll() {

      try {

        /*
         * Load general dashboard data
         * and current GIS risks.
         */
        const [
          info,
          zones,
          updated,
          locationsRisk,
        ] = await Promise.all([

          getSystemInfo(),

          getRiskZones(),

          getLastUpdated(),

          getLocationsRisk(0),

        ]);


        if (cancelled) return;


        setSystemInfo(
          info
        );

        setRiskZones(
          zones
        );

        setLastUpdated(
          updated
        );


        /*
         * Load current GIS locations.
         */
        setLocations(
          locationsRisk
        );


        /*
         * Generate current alerts.
         */
        setAlerts(
          buildDynamicAlerts(
            locationsRisk
          )
        );


        /*
         * Automatically select
         * first location.
         */
        if (locationsRisk.length > 0) {

          const firstLocation =
            locationsRisk[0];


          setSelectedLocation(
            firstLocation
          );


          /*
           * Load rainfall history
           * for selected location.
           */
          const rainfall =
            await getRainfallHistory(
              firstLocation.location_id
            );


          if (cancelled) return;


          setRainfallHistory(
            rainfall
          );


          /*
           * Analyse selected location.
           */
          const analyserResult =
            await analyseFloodConditions({

              location_id:
                firstLocation.location_id,

            });


          if (cancelled) return;


          /*
           * Update real-time analysis.
           */
          setAnalysis(
            analyserResult.analysis
          );


          /*
           * Generate forecast timeline.
           */
          setTimeline(
            buildDashboardTimeline(
              analyserResult
            )
          );

        }


        /*
         * Start dashboard at NOW.
         */
        setSelectedStep(0);


        setLoading(false);


      } catch (error) {

        console.error(
          "Failed to load dashboard data:",
          error
        );


        if (!cancelled) {

          setLoading(
            false
          );

        }

      }

    }


    loadAll();


    return () => {

      cancelled = true;

    };

  }, []);


  /*
   * Update GIS risks and alerts
   * when forecast timeline changes.
   */
  useEffect(() => {

    let cancelled = false;


    async function updateLocationsRisk() {

      try {

        if (!timeline.length) {
          return;
        }


        const selectedForecast =
          timeline[selectedStep];


        if (!selectedForecast) {
          return;
        }


        /*
         * Convert forecast hours
         * into backend minutes.
         */
        const forecastMinutes =
          Math.round(
            selectedForecast.timeOffsetHours * 60
          );


        /*
         * Load risk data for all
         * GIS locations.
         */
        const updatedLocations =
          await getLocationsRisk(
            forecastMinutes
          );


        if (cancelled) return;


        /*
         * Update GIS markers.
         */
        setLocations(
          updatedLocations
        );


        /*
         * IMPORTANT:
         * Update selected location with
         * the latest forecast risk data.
         */
        setSelectedLocation(
          (currentLocation) => {

            if (!currentLocation) {
              return null;
            }


            return (

              updatedLocations.find(
                (location) =>

                  location.location_id ===
                  currentLocation.location_id

              )

              ||

              currentLocation

            );

          }
        );


        /*
         * Update alerts.
         */
        setAlerts(
          buildDynamicAlerts(
            updatedLocations
          )
        );


      } catch (error) {

        console.error(
          "Failed to update GIS risk data:",
          error
        );

      }

    }


    updateLocationsRisk();


    return () => {

      cancelled = true;

    };

  }, [

    selectedStep,
    timeline,

  ]);


  /*
   * Currently selected
   * forecast timeline step.
   */
  const selected =
    timeline[selectedStep] || null;


  /*
   * Called when user selects
   * a location from GIS map.
   */
  const handleSelectLocation = async (
    location
  ) => {

    try {

      setLoading(
        true
      );


      /*
       * Load rainfall history
       * for clicked location.
       */
      const rainfall =
        await getRainfallHistory(
          location.location_id
        );


      /*
       * Analyse clicked location.
       */
      const analyserResult =
        await analyseFloodConditions({

          location_id:
            location.location_id,

        });


      /*
       * Update selected location.
       */
      setSelectedLocation(
        location
      );


      /*
       * Update rainfall chart.
       */
      setRainfallHistory(
        rainfall
      );


      /*
       * Update analysis.
       */
      setAnalysis(
        analyserResult.analysis
      );


      /*
       * Generate timeline.
       */
      setTimeline(
        buildDashboardTimeline(
          analyserResult
        )
      );


      /*
       * Reset to NOW.
       */
      setSelectedStep(
        0
      );


    } catch (error) {

      console.error(
        "Failed to analyse selected location:",
        error
      );


    } finally {

      setLoading(
        false
      );

    }

  };


  return {

    loading,

    systemInfo,

    timeline,

    selected,

    selectedStep,

    setSelectedStep,

    rainfallHistory,

    alerts,

    riskZones,

    locations,

    lastUpdated,

    analysis,

    selectedLocation,

    handleSelectLocation,

  };

}