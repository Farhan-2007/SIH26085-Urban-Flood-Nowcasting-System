import { useCallback, useEffect, useState } from "react";
import { LOCATIONS, getLocationById } from "../data/locations";
import { analyseLocation, ApiError } from "../services/api";

export function useFloodData() {
  const [locationId, setLocationId] = useState(LOCATIONS[0].locationId);
  const [status, setStatus] = useState("loading"); // "loading" | "ready" | "error"
  const [errorMessage, setErrorMessage] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [selectedStep, setSelectedStep] = useState(0);

  const load = useCallback(async (id) => {
    const location = getLocationById(id);
    if (!location) return;

    setStatus("loading");
    setErrorMessage(null);

    try {
      const result = await analyseLocation(location);
      setAnalysis(result.analysis || null);
      setForecast(Array.isArray(result.forecast) ? result.forecast : []);
      setSelectedStep(0);
      setLastUpdated(new Date());
      setStatus("ready");
    } catch (err) {
      const message =
        err instanceof ApiError
          ? err.message
          : "Unable to retrieve current flood-risk data.";
      setErrorMessage(message);
      setStatus("error");
      setAnalysis(null);
      setForecast([]);
    }
  }, []);

  useEffect(() => {
    load(locationId);
  }, [locationId, load]);

  const selectedLocation = getLocationById(locationId);
  const selectedForecast = forecast[selectedStep] || null;

  return {
    locations: LOCATIONS,
    locationId,
    setLocationId,
    selectedLocation,
    status,
    errorMessage,
    analysis,
    forecast,
    selectedStep,
    setSelectedStep,
    selectedForecast,
    lastUpdated,
    retry: () => load(locationId),
  };
}
