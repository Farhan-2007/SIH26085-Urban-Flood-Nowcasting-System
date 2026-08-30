import { useEffect, useState } from "react";

import {
  getSystemInfo,
  getRainfallHistory,
  getRiskZones,
  getLastUpdated,
  analyseFloodConditions,
  getLocationsRisk,
} from "../services/api";


// --------------------------------------------------
// Convert backend forecast into dashboard timeline
// --------------------------------------------------

function buildDashboardTimeline(analyserResult) {

  const backendTimeline =
    analyserResult.forecast || [];


  const selectedForecast =
    backendTimeline.filter(
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


    const riskScore =
      step.forecast_minutes === 0
        ? (
            analyserResult.analysis
              ?.flood_condition_index
            ??
            step.risk_score
          )
        : step.risk_score;


    const riskLevel =
      step.forecast_minutes === 0
        ? (
            analyserResult.analysis
              ?.condition
            ||
            step.risk_level
            ||
            "LOW"
          ).toUpperCase()
        : (
            step.risk_level
            ||
            "LOW"
          ).toUpperCase();


    return {

      // ==========================================
      // IDENTIFICATION
      // ==========================================

      id:
        `${step.forecast_minutes}min`,

      label,


      // ==========================================
      // TIME
      // ==========================================

      forecast_minutes:
        step.forecast_minutes,

      timeOffsetHours:
        step.forecast_minutes / 60,


      // ==========================================
      // RISK
      // Both camelCase and snake_case
      // ==========================================

      riskScore:
        riskScore,

      riskLevel:
        riskLevel,

      risk_score:
        riskScore,

      risk_level:
        riskLevel,


      // ==========================================
      // RAINFALL
      // ==========================================

      rainfall:
        step.rainfall,

      rainfallIntensity:
        step.rainfall,

      recentRainfall:
        step.rainfall,


      // ==========================================
      // DRAINAGE
      // ==========================================

      drainage_capacity_used:
        step.drainage_capacity_used,

      drainageCapacityUsed:
        Math.round(
          (step.drainage_capacity_used || 0) * 100
        ),


      // ==========================================
      // RUNOFF
      // ==========================================

      surface_runoff:
        step.surface_runoff,

      surfaceRunoff:
        step.surface_runoff >= 70
          ? "Very High"
          : step.surface_runoff >= 50
            ? "High"
            : step.surface_runoff >= 30
              ? "Moderate"
              : "Low",


      // ==========================================
      // EXCESS WATER
      // ==========================================

      excess_water:
        step.excess_water,

      excessWater:
        step.excess_water,


      // ==========================================
      // PREDICTION
      // ==========================================

      prediction_status:
        step.prediction_status,

      predictionStatus:
        step.prediction_status,


      // ==========================================
      // ANALYSIS
      // ==========================================

      waterLevel:
        analyserResult.analysis
          ?.water_level_smoothed ?? 0,

      soilSaturation:
        Math.round(
          (
            analyserResult.analysis
              ?.soil_saturation_smoothed ?? 0
          ) * 100
        ),


      // ==========================================
      // FORECAST NOTE
      // ==========================================

      forecastNote:

        step.prediction_status ===
        "Intensifying"

          ? "Flood risk is increasing based on current rainfall and drainage conditions."

          : step.prediction_status ===
            "Receding"

            ? "Flood risk is receding as rainfall decreases, although localized flooding may persist."

            : "Current flood conditions are stable.",

    };

  });

}


// --------------------------------------------------
// Generate dynamic alerts
// --------------------------------------------------

function buildDynamicAlerts(locations) {

  if (
    !locations ||
    locations.length === 0
  ) {

    return [];

  }


  const groupedLocations = {

    CRITICAL: [],

    HIGH: [],

    MODERATE: [],

  };


  locations.forEach((location) => {

    const level =
      location.risk_level
        ?.toUpperCase();


    if (
      groupedLocations[level]
    ) {

      groupedLocations[level].push(
        location
      );

    }

  });


  const alerts = [];


  // --------------------------------------------
  // CRITICAL ALERT
  // --------------------------------------------

  if (
    groupedLocations.CRITICAL.length > 0
  ) {

    const zones =
      groupedLocations.CRITICAL
        .map(
          (location) =>
            location.location_name
        )
        .join(", ");


    alerts.push({

      id:
        "critical-flood-warning",

      severity:
        "CRITICAL",

      title:
        "Critical Flood Warning",

      message:
        `Critical flood conditions detected in ${zones}. Immediate attention is recommended.`,

      zone:
        `${groupedLocations.CRITICAL.length} location(s)`,

      time:
        "Live",

    });

  }


  // --------------------------------------------
  // HIGH ALERT
  // --------------------------------------------

  if (
    groupedLocations.HIGH.length > 0
  ) {

    const zones =
      groupedLocations.HIGH
        .map(
          (location) =>
            location.location_name
        )
        .join(", ");


    alerts.push({

      id:
        "high-flood-risk",

      severity:
        "HIGH",

      title:
        "High Flood Risk",

      message:
        `High flood risk detected in ${zones}. Monitor drainage and traffic conditions.`,

      zone:
        `${groupedLocations.HIGH.length} location(s)`,

      time:
        "Live",

    });

  }


  // --------------------------------------------
  // MODERATE ALERT
  // --------------------------------------------

  if (
    groupedLocations.MODERATE.length > 0
  ) {

    const zones =
      groupedLocations.MODERATE
        .map(
          (location) =>
            location.location_name
        )
        .join(", ");


    alerts.push({

      id:
        "moderate-flood-risk",

      severity:
        "MEDIUM",

      title:
        "Flood Risk Monitoring",

      message:
        `Moderate flood risk detected in ${zones}. Conditions should be monitored.`,

      zone:
        `${groupedLocations.MODERATE.length} location(s)`,

      time:
        "Live",

    });

  }


  return alerts;

}


// --------------------------------------------------
// Dashboard Hook
// --------------------------------------------------

export function useDashboardData() {


  const [loading, setLoading] =
    useState(true);


  const [systemInfo, setSystemInfo] =
    useState(null);


  const [timeline, setTimeline] =
    useState([]);


  const [
    rainfallHistory,
    setRainfallHistory,
  ] =
    useState([]);


  const [alerts, setAlerts] =
    useState([]);


  const [riskZones, setRiskZones] =
    useState([]);


  const [locations, setLocations] =
    useState([]);


  const [
    lastUpdated,
    setLastUpdated,
  ] =
    useState(null);


  const [analysis, setAnalysis] =
    useState(null);


  const [
    selectedLocation,
    setSelectedLocation,
  ] =
    useState(null);


  const [
    selectedStep,
    setSelectedStep,
  ] =
    useState(0);


  // ------------------------------------------------
  // Initial dashboard loading
  // ------------------------------------------------

  useEffect(() => {


    let cancelled = false;


    async function loadAll() {

      try {


        const [

          info,

          zones,

          updated,

          locationsRisk,

        ] =
          await Promise.all([

            getSystemInfo(),

            getRiskZones(),

            getLastUpdated(),

            getLocationsRisk(0),

          ]);


        if (cancelled) {
          return;
        }


        // ----------------------------------------
        // System information
        // ----------------------------------------

        setSystemInfo(
          info
        );


        setRiskZones(
          zones
        );


        // ----------------------------------------
        // Fix lastUpdated
        // Convert backend value into Date object
        // ----------------------------------------

        if (updated) {

          let updatedDate;


          if (
            updated instanceof Date
          ) {

            updatedDate =
              updated;

          } else if (
            typeof updated === "object"
          ) {

            const dateValue =
              updated.last_updated
              ||
              updated.timestamp
              ||
              updated.updated_at;


            updatedDate =
              dateValue
                ? new Date(dateValue)
                : new Date();

          } else {

            updatedDate =
              new Date(updated);

          }


          setLastUpdated(
            updatedDate
          );

        }


        // ----------------------------------------
        // GIS locations
        // ----------------------------------------

        setLocations(
          locationsRisk
        );


        // ----------------------------------------
        // Dynamic alerts
        // ----------------------------------------

        setAlerts(
          buildDynamicAlerts(
            locationsRisk
          )
        );


        // ----------------------------------------
        // Select first location
        // ----------------------------------------

        if (
          locationsRisk &&
          locationsRisk.length > 0
        ) {


          const firstLocation =
            locationsRisk[0];


          setSelectedLocation(
            firstLocation
          );


          // --------------------------------------
          // Rainfall history
          // --------------------------------------

          const rainfall =
            await getRainfallHistory(
              firstLocation.location_id
            );


          if (cancelled) {
            return;
          }


          setRainfallHistory(
            rainfall
          );


          // --------------------------------------
          // Flood analysis
          // --------------------------------------

          const analyserResult =
            await analyseFloodConditions({

              location_id:
                firstLocation.location_id,

            });


          if (cancelled) {
            return;
          }


          // --------------------------------------
          // Analysis
          // --------------------------------------

          setAnalysis(
            analyserResult.analysis
          );


          // --------------------------------------
          // Timeline
          // --------------------------------------

          const dashboardTimeline =
            buildDashboardTimeline(
              analyserResult
            );


          setTimeline(
            dashboardTimeline
          );


          setSelectedStep(
            0
          );

        }


        setLoading(
          false
        );


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

      cancelled =
        true;

    };


  }, []);


  // ------------------------------------------------
  // Update GIS markers when timeline changes
  // ------------------------------------------------

  useEffect(() => {


    let cancelled = false;


    async function updateLocationsRisk() {

      try {


        if (
          !timeline.length
        ) {

          return;

        }


        const selectedForecast =
          timeline[selectedStep];


        if (
          !selectedForecast
        ) {

          return;

        }


        // ----------------------------------------
        // IMPORTANT
        // Use forecast_minutes directly
        // ----------------------------------------

        const forecastMinutes =
          selectedForecast.forecast_minutes;


        // ----------------------------------------
        // Get updated location risk
        // ----------------------------------------

        const updatedLocations =
          await getLocationsRisk(
            forecastMinutes
          );


        if (cancelled) {
          return;
        }


        // ----------------------------------------
        // Update GIS markers
        // ----------------------------------------

        setLocations(
          updatedLocations
        );


        // ----------------------------------------
        // Update alerts
        // ----------------------------------------

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

      cancelled =
        true;

    };


  }, [

    selectedStep,

    timeline,

  ]);


  // ------------------------------------------------
  // Currently selected forecast
  // ------------------------------------------------

  const selected =
    timeline[selectedStep]
    ||
    null;


  // ------------------------------------------------
  // Handle GIS marker click
  // ------------------------------------------------

  const handleSelectLocation =
    async (location) => {

      try {


        setLoading(
          true
        );


        // --------------------------------------
        // Load rainfall history
        // --------------------------------------

        const rainfall =
          await getRainfallHistory(
            location.location_id
          );


        // --------------------------------------
        // Analyse location
        // --------------------------------------

        const analyserResult =
          await analyseFloodConditions({

            location_id:
              location.location_id,

          });


        // --------------------------------------
        // Update selected location
        // --------------------------------------

        setSelectedLocation(
          location
        );


        // --------------------------------------
        // Update rainfall
        // --------------------------------------

        setRainfallHistory(
          rainfall
        );


        // --------------------------------------
        // Update analysis
        // --------------------------------------

        setAnalysis(
          analyserResult.analysis
        );


        // --------------------------------------
        // Update timeline
        // --------------------------------------

        setTimeline(
          buildDashboardTimeline(
            analyserResult
          )
        );


        // --------------------------------------
        // Reset to NOW
        // --------------------------------------

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


  // ------------------------------------------------
  // Return dashboard data
  // ------------------------------------------------

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