import Header from "./components/Header";
import LocationSelector from "./components/LocationSelector";
import RiskOverview from "./components/RiskOverview";
import RiskFactorsPanel from "./components/RiskFactorsPanel";
import RainfallPanel from "./components/RainfallPanel";
import FloodMap from "./components/FloodMap";
import ForecastTimeline from "./components/ForecastTimeline";
import AlertsPanel from "./components/AlertsPanel";
import Footer from "./components/Footer";
import { useFloodData } from "./hooks/useFloodData";
import { normalizeRiskLevel, scoreToRiskLevel } from "./utils/riskLevel";
import { forecastMinutesLabel } from "./utils/forecastLabels";
import { generateAlerts } from "./utils/generateAlerts";
import "./App.css";

export default function App() {
  const {
    locations,
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
    retry,
  } = useFloodData();

  const currentRiskLevel = selectedForecast
    ? normalizeRiskLevel(selectedForecast.risk_level) || scoreToRiskLevel(selectedForecast.risk_score)
    : null;

  const alerts =
    status === "ready"
      ? generateAlerts({ analysis, forecast, locationName: selectedLocation?.name })
      : [];

  return (
    <>
      <Header apiStatus={status} />
      <LocationSelector
        locations={locations}
        locationId={locationId}
        onChange={setLocationId}
        selectedLocation={selectedLocation}
      />

      <main className="dashboard">
        {status === "loading" && (
          <div className="dashboard__state">
            <span className="mono">Loading flood-risk data for {selectedLocation?.name}…</span>
          </div>
        )}

        {status === "error" && (
          <div className="dashboard__state dashboard__state--error">
            <p>{errorMessage || "Unable to retrieve current flood-risk data."}</p>
            <p className="dashboard__state-hint">
              Make sure the Flask backend is running locally (python -m backend.app) and reachable at
              http://localhost:5000.
            </p>
            <button type="button" className="dashboard__retry" onClick={retry}>
              Retry
            </button>
          </div>
        )}

        {status === "ready" && (
          <>
            <RiskOverview
              selectedForecast={selectedForecast}
              analysis={analysis}
              locationName={selectedLocation?.name}
              lastUpdated={lastUpdated}
            />

            <RiskFactorsPanel
              selectedForecast={selectedForecast}
              analysis={analysis}
              location={selectedLocation}
            />

            <RainfallPanel forecast={forecast} selectedForecast={selectedForecast} />

            <FloodMap
              locations={locations}
              locationId={locationId}
              onSelectLocation={setLocationId}
              currentRiskLevel={currentRiskLevel}
              forecastLabel={selectedForecast ? forecastMinutesLabel(selectedForecast.forecast_minutes) : null}
            />

            <ForecastTimeline
              forecast={forecast}
              selectedStep={selectedStep}
              onSelectStep={setSelectedStep}
            />

            <AlertsPanel alerts={alerts} />
          </>
        )}
      </main>

      <Footer />
    </>
  );
}
