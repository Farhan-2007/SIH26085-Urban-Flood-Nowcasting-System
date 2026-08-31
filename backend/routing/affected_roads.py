"""
affected_roads.py
------------------

Identifies high-risk and critical locations that
affect the real-road routing decision.
"""


RISK_ORDER = [
    "Low",
    "Moderate",
    "High",
    "Critical"
]


def risk_rank(level):

    if level not in RISK_ORDER:
        return 0

    return RISK_ORDER.index(
        level
    )


def get_affected_roads(
    locations,
    risk_data
):

    affected = []

    for location in locations:

        location_id = (
            location["location_id"]
        )

        risk = risk_data.get(
            location_id,
            {}
        )

        risk_level = risk.get(
            "risk_level",
            "Low"
        )

        if risk_rank(
            risk_level
        ) < risk_rank("High"):

            continue

        if risk_level == "Critical":

            status = (
                "Critical - avoid"
            )

        else:

            status = (
                "High risk - caution"
            )

        affected.append({

            "location_id":
                location_id,

            "location_name":
                location[
                    "location_name"
                ],

            "latitude":
                location[
                    "latitude"
                ],

            "longitude":
                location[
                    "longitude"
                ],

            "risk_score":
                risk.get(
                    "risk_score",
                    0
                ),

            "risk_level":
                risk_level,

            "trend":
                risk.get(
                    "trend",
                    "Stable"
                ),

            "status":
                status,

        })

    affected.sort(
        key=lambda item:
            item["risk_score"],
        reverse=True
    )

    return affected


def get_shifting_risk(
    risk_data
):

    shifting = [

        {
            "location_id":
                location_id,

            **data

        }

        for location_id, data
        in risk_data.items()

        if data.get(
            "trend"
        ) == "Intensifying"

    ]

    shifting.sort(
        key=lambda item:
            item.get(
                "risk_score",
                0
            ),
        reverse=True
    )

    return shifting
