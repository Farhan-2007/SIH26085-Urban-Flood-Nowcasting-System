import GISMap from "./gis/GISMap";

import "./FloodMap.css";


export default function FloodMap({

  locations,
  selected,
  selectedLocation,
  onSelectLocation,
  routeData,

}) {


  return (

    <section
      className="panel flood-map"
      aria-labelledby="flood-map-heading"
    >


      {/* ================================================== */}
      {/* HEADER */}
      {/* ================================================== */}

      <div className="panel-header">

        <h2 id="flood-map-heading">

          Geographic Flood-Risk Map

        </h2>


        <span className="eyebrow">

          {

            selectedLocation

              ? `Selected: ${

                  selectedLocation.location_name

                } • ${

                  selected?.label ||
                  "NOW"

                }`

              : "Select a location on the map"

          }

        </span>

      </div>


      {/* ================================================== */}
      {/* GIS MAP */}
      {/* ================================================== */}

      <div className="panel-body flood-map__body">

        <GISMap

          locations={locations}

          selected={selected}

          selectedLocation={selectedLocation}

          onSelectLocation={onSelectLocation}

          routeData={routeData}

        />

      </div>


    </section>

  );

}