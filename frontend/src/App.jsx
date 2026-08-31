import { useState } from "react";

import Header from "./components/Header";
import SystemInfoBar from "./components/SystemInfoBar";
import RiskOverview from "./components/RiskOverview";
import RiskFactorsPanel from "./components/RiskFactorsPanel";
import RainfallPanel from "./components/RainfallPanel";
import FloodMap from "./components/FloodMap";
import ForecastTimeline from "./components/ForecastTimeline";
import AlertsPanel from "./components/AlertsPanel";
import Footer from "./components/Footer";
import RoutePanel from "./components/RoutePanel";

import { useDashboardData } from "./hooks/useDashboardData";

import "./App.css";


export default function App() {

  const [routeData, setRouteData] =
    useState(null);


  const {
    loading,
    systemInfo,
    timeline,
    selected,
    selectedStep,
    setSelectedStep,
    rainfallHistory,
    alerts,
    lastUpdated,
    analysis,
    locations,
    selectedLocation,
    handleSelectLocation,
  } = useDashboardData();


  if (loading) {

    return (

      <div className="app-loading">

        <span className="mono">
          Loading nowcasting data…
        </span>

      </div>

    );

  }


  return (

    <>

      <Header
        systemInfo={systemInfo}
      />


      <SystemInfoBar
        systemInfo={systemInfo}
        lastUpdated={lastUpdated}
      />


      <main className="dashboard">


        {/* 1. RISK OVERVIEW */}

        <div className="dashboard__row dashboard__row--top">

          <RiskOverview
            selectedForecast={selected}
            analysis={analysis}
            locationName={selectedLocation?.location_name}
            lastUpdated={lastUpdated}
          />

        </div>


        {/* 2. RISK FACTORS */}

        <RiskFactorsPanel
          selectedForecast={selected}
          analysis={analysis}
          location={selectedLocation}
        />


        {/* 3. RAINFALL CONDITIONS + ALERTS & WARNINGS — side by side */}

        <div className="dashboard__row dashboard__row--split">

          <RainfallPanel
            selected={selected}
            history={rainfallHistory}
            analysis={analysis}
          />

          <AlertsPanel
            alerts={alerts}
          />

        </div>


        {/* 4. GIS MAP */}

        <FloodMap
          locations={locations}
          selected={selected}
          selectedLocation={selectedLocation}
          onSelectLocation={handleSelectLocation}
          routeData={routeData}
        />


        {/* 5. SAFE ROUTING */}

        <RoutePanel
          locations={locations}
          selectedLocation={selectedLocation}
          selected={selected}
          routeData={routeData}
          onRouteDataChange={setRouteData}
        />


        {/* 6. FORECAST TIMELINE */}

        <ForecastTimeline
          forecast={timeline}
          selectedStep={selectedStep}
          onSelectStep={setSelectedStep}
        />


      </main>


      <Footer
        systemInfo={systemInfo}
      />

    </>

  );

}
