EVENT_DATA = [
    {"category": "Concerts", "views": 12000, "registrations": 1800},
    {
        "category": "Corporate",
        "views": 6000,
        "registrations": 1200,
    },
    {
        "category": "Sports",
        "views": 9000,
        "registrations": 900,
    },
]


def get_event_performance() -> list[dict]:
    results = []
    for event in EVENT_DATA:
        conversion_rate = (event["registration"] / event["views"]) * 100

        results.append({**event, "conversion_rate": round(conversion_rate, 2)})

    return results
