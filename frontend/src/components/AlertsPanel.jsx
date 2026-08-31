import "./AlertsPanel.css";


const SEVERITY_COLOR_VAR = {

  CRITICAL: "--color-risk-critical",

  HIGH: "--color-risk-high",

  MODERATE: "--color-risk-moderate",

  LOW: "--color-risk-low",

};


// ============================================================
// FORMAT ALERT TIME
// ============================================================

function formatTime(value) {

  if (!value) {
    return "Live";
  }


  const date =
    new Date(value);


  if (
    Number.isNaN(
      date.getTime()
    )
  ) {

    return value;

  }


  return (

    date.toLocaleTimeString(

      "en-IN",

      {

        hour: "2-digit",

        minute: "2-digit",

        hour12: false,

      }

    )

    + " IST"

  );

}


// ============================================================
// ALERTS PANEL
// ============================================================

export default function AlertsPanel({

  alerts = [],

}) {


  // Remove duplicate alerts using alert ID
  const uniqueAlerts =

    Array.from(

      new Map(

        alerts.map(

          (alert) => [

            alert.id,

            alert,

          ]

        )

      ).values()

    );


  // Recomputing this key whenever the alert set's ids/messages change
  // (e.g. when the forecast timeline advances to a new step) causes the
  // list below to remount, replaying the fade/slide-in animation defined
  // in AlertsPanel.css. When the underlying alerts are unchanged, the key
  // stays the same and nothing re-animates.
  const alertsRenderKey = uniqueAlerts
    .map((alert) => `${alert.id}:${alert.message}`)
    .join("|");

  return (

    <section

      className="panel"

      aria-labelledby="alerts-heading"

    >


      {/* ================================================== */}
      {/* HEADER */}
      {/* ================================================== */}

      <div className="panel-header">

        <h2 id="alerts-heading">

          Alerts &amp; Warnings

        </h2>


        <span className="eyebrow">

          {uniqueAlerts.length} Active
          {" · "}
          Live Risk Data

        </span>

      </div>


      {/* ================================================== */}
      {/* ALERT LIST */}
      {/* ================================================== */}

      <div className="panel-body alerts-panel__body" key={alertsRenderKey}>


        {/* NO ALERTS */}

        {uniqueAlerts.length === 0 && (

          <p className="alerts-panel__empty">

            No active alerts for the monitored zone.

          </p>

        )}


        {/* ALERT ITEMS */}

        {uniqueAlerts.map(

          (alert) => {


            const colorVar =

              SEVERITY_COLOR_VAR[
                alert.severity
              ]

              || "--color-info";


            return (

              <div

                className="alert-item"

                key={alert.id}

                style={{

                  borderLeftColor:
                    `var(${colorVar})`,

                }}

              >


                {/* ALERT TITLE */}

                <div className="alert-item__top">


                  <span

                    className="alert-item__title"

                    style={{

                      color:
                        `var(${colorVar})`,

                    }}

                  >

                    {alert.title}

                  </span>


                  {/* ALERT TIME */}

                  <span className="mono alert-item__time">

                    {formatTime(
                      alert.time
                    )}

                  </span>


                </div>


                {/* ALERT MESSAGE */}

                <p className="alert-item__message">

                  {alert.message}

                </p>


                {/* ALERT METADATA */}

                <div className="alert-item__meta">


                  <span>

                    Location:{" "}

                    {
                      alert.zone ||
                      "Monitored Zone"
                    }

                  </span>


                  <span className="mono">

                    {alert.id}

                  </span>


                </div>


              </div>

            );

          }

        )}


      </div>


    </section>

  );

}