import { useEffect, useState } from "react";
import {
  getSystemInfo,
  getForecastTimeline,
  getRainfallHistory,
  getAlerts,
  getRiskZones,
  getLastUpdated,
} from "../services/api";

// Loads every dashboard data slice through the service layer and exposes
// the currently-selected forecast step. Kept as a single hook so App.jsx
// stays a thin composition layer rather than a data-fetching component.
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
      const [info, forecast, rainfall, activeAlerts, zones, updated] = await Promise.all([
        getSystemInfo(),
        getForecastTimeline(),
        getRainfallHistory(),
        getAlerts(),
        getRiskZones(),
        getLastUpdated(),
      ]);

      if (cancelled) return;

      setSystemInfo(info);
      setTimeline(forecast);
      setRainfallHistory(rainfall);
      setAlerts(activeAlerts);
      setRiskZones(zones);
      setLastUpdated(updated);
      setLoading(false);
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
