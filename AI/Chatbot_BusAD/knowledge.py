"""Static facts checked against Abu Dhabi Mobility on 2026-11-10, not live data."""

# Sources for the facts below; URLs are references and are not fetched at runtime.
FACT_SOURCES = {
    "anonymous_card": "https://admobility.gov.ae/en/pb-bus-service/hafilat-cards",
    "personalized_card": "https://admobility.gov.ae/en/pb-bus-service/hafilat-personalized-card",
    "recharge": "https://admobility.gov.ae/en/pb-bus-service/recharge-hafilat-cards",
    "fares": "https://admobility.gov.ae/en/pb-bus-service/hafilat-public-buses-fees",
    "route_170": "https://admobility.gov.ae/ckfinder/userfiles/files/BusService170.pdf",
}

knowledge_base = {
    "hafilat_card": {
        "description": (
            "Hafilat is a smart card used to pay for public "
            "bus journeys in Abu Dhabi. Tap the card when "
            "boarding and alighting."
        ),
        "anonymous_purchase_locations": [
            "Bus station customer happiness offices",
            "Ticket vending machines",
            "Lulu Hypermarket",
            "Lulu Exchange",
            "Abu Dhabi Cooperative Society",
            "Zayed International Airport office"
        ],
        "personalized_purchase_locations": [
            "Bus station customer happiness offices",
            "Zayed International Airport office",
            "Online application through https://hafilat.darb.ae"
        ],
        "card_types": [
            "Anonymous Card",
            "Personalized Card"
        ]
    },

    "card_pricing": {
        "anonymous_card_price": 10,
        "personalized_card_price": 0,
        "anonymous_card_validity_years": 16,
        "personalized_card_validity_years": 16
    },

    #for the sake of simplicity we choose one route which is the 170 (stops at NYU AD)
    "operating_hours": {
        "route_170_start": "06:36",
        "route_170_end": "22:21",
        # Official timetable, page 3: 05:00 starts in the city; the 23:03 NYU
        # departure only has times through Madinat Zayed Shopping Centre.
        "note": "Weekday departures from Saadiyat New York University 2 reaching Al Zeina"
    },

    "bus_routes": {
        "route_170": "Al Zeina - Abu Dhabi Bus Station - NYU Abu Dhabi",
        "known_destinations": ["Al Zeina", "Abu Dhabi Bus Station", "NYU Abu Dhabi"],
    },

    "card_recharge": {
        "recharge_locations": [
            "Bus stations",
            "Bus stops",
            "Shopping centers",
            "MBME recharge machines",
            "Online through Hafilat website"
        ],
        "online_recharge": True,
        "recharge_website": "https://hafilat.darb.ae",
        "maximum_balance": 150,
        "online_recharge_delay_hours": 2
    },

    "bus_fares": {
        "service_scope": "Standard Service within cities and their suburbs, excluding intercity services",
        "base_fare": 2.0,
        "distance_fare": 0.05,
        "maximum_fare": 5.0,
        "currency": "AED",
        "free_travel_age_max": 10
    },

    "bus_stops": {
        "main_bus_station": "Abu Dhabi Bus Station",
        "route_170_stop": "NYU Abu Dhabi"
    },

    "bus_schedules": {
        "route_170_first_departure": "06:36",
        "route_170_last_departure": "22:21",
        "route_170_frequency_note": "Departure intervals vary by time of day; there is no fixed all-day frequency.",
        "timetable_source": FACT_SOURCES["route_170"]
    }
}
