import Header from "./components/Header";
import SystemInfoBar from "./components/SystemInfoBar";
import RiskOverview from "./components/RiskOverview";
import RiskFactorsPanel from "./components/RiskFactorsPanel";
import RainfallPanel from "./components/RainfallPanel";
import FloodMap from "./components/FloodMap";
import ForecastTimeline from "./components/ForecastTimeline";
import AlertsPanel from "./components/AlertsPanel";
import Footer from "./components/Footer";
import { useDashboardData } from "./hooks/useDashboardData";
import "./App.css";

export default function App() {
  const {
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
  } = useDashboardData();

  if (loading) {
    return (
      <div className="app-loading">
        <span className="mono">Loading nowcasting data…</span>
      </div>
    );
  }

  return (
    <>
      <Header systemInfo={systemInfo} />
      <SystemInfoBar systemInfo={systemInfo} lastUpdated={lastUpdated} />

      <main className="dashboard">
        <div className="dashboard__row dashboard__row--top">
          <RiskOverview selected={selected} />
        </div>

        <RiskFactorsPanel selected={selected} />

        <RainfallPanel selected={selected} history={rainfallHistory} />

        <FloodMap zones={riskZones} />

        <ForecastTimeline
          timeline={timeline}
          selectedStep={selectedStep}
          onSelectStep={setSelectedStep}
        />

        <AlertsPanel alerts={alerts} />
      </main>

      <Footer systemInfo={systemInfo} />
    </>
  );
}
