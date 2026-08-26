import { useEffect, useState } from "react";

import {
  getSystemInfo,
  getRainfallHistory,
  getAlerts,
  getRiskZones,
  getLastUpdated,
  getBackendForecast,
} from "../services/api";

export function useDashboardData() {
  const [loading, setLoading] = useState(true);
  const [systemInfo, setSystemInfo] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [rainfallHistory, setRainfallHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [riskZones, setRiskZones] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [selectedStep, setSelectedStep] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function loadAll() {
      try {
        const [
          info,
          backendForecast,
          rainfall,
          activeAlerts,
          zones,
          updated,
        ] = await Promise.all([
          getSystemInfo(),
          getBackendForecast(),
          getRainfallHistory(),
          getAlerts(),
          getRiskZones(),
          getLastUpdated(),
        ]);

        if (cancelled) return;

        const backendTimeline = backendForecast.forecast;

        /*
         * Backend:
         * 0   min → NOW
         * 30  min → intermediate prediction
         * 60  min → +1 HR
         * 120 min → +2 HR
         * 180 min → +3 HR
         */

        const selectedForecast = backendTimeline.filter(
          (step) => [0, 60, 120, 180].includes(step.forecast_minutes)
        );

        const dashboardTimeline = selectedForecast.map((step) => {
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
            timeOffsetHours: step.forecast_minutes / 60,

            riskScore: step.risk_score,
            riskLevel: step.risk_level.toUpperCase(),

            rainfallIntensity: step.rainfall,
            recentRainfall: step.rainfall,

            /*
             * Friend's predictor gives drainage utilisation
             * as a ratio, e.g. 1.67 = 167%.
             */
            drainageCapacityUsed: Math.round(
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
             * These aren't currently returned by predictor.py.
             * Keep safe placeholder values until we expose them
             * from FactorAnalyzer.
             */
            waterLevel: 0,
            soilSaturation: 0,

            forecastNote:
              step.prediction_status === "Intensifying"
                ? "Flood risk is increasing based on current rainfall and drainage conditions."
                : step.prediction_status === "Receding"
                ? "Flood risk is receding as rainfall decreases, although localized flooding may persist."
                : "Current flood conditions are stable.",
          };
        });

        setSystemInfo(info);
        setTimeline(dashboardTimeline);
        setRainfallHistory(rainfall);
        setAlerts(activeAlerts);
        setRiskZones(zones);
        setLastUpdated(updated);

        setSelectedStep(0);
        setLoading(false);
      } catch (error) {
        console.error("Failed to load dashboard data:", error);

        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadAll();

    return () => {
      cancelled = true;
    };
  }, []);

  const selected = timeline[selectedStep] || null;

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
    lastUpdated,
  };
}