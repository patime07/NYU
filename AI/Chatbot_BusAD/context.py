"""Remember a topic, route, and destination for limited follow-up questions."""
import re

from intent_detection import preprocess


ROUTE_INTENTS = {"bus_routes", "bus_schedules", "operating_hours", "bus_stops"}
DESTINATIONS = {
    "nyu": "NYU Abu Dhabi",
    "nyu abu dhabi": "NYU Abu Dhabi",
    "nyu ad": "NYU Abu Dhabi",
    "new york university": "NYU Abu Dhabi",
    "al zeina": "Al Zeina",
    "abu dhabi bus station": "Abu Dhabi Bus Station",
}


def create_context():
    return {"last_intent": None, "current_route": None, "current_destination": None}


def resolve_intent(user_input, detected_intent, context):
    """Prefer explicit topics; only inherit the topic for recognized ellipses."""
    text = preprocess(user_input)
    words = set(text.split())
    followup = text.startswith(("and ", "what about ", "how about ", "its ",
                               "when does it ", "where does it "))
    short = re.sub(r"^(?:and|what about|how about)\s+", "", text)
    route = re.search(r"\b(?:route|bus)\s+(\d+)\b", text)
    if not route and followup:
        route = re.fullmatch(r"(?:and|what about|how about)\s+(\d+)", text)

    destination = re.search(r"\b(?:to|toward|towards)\s+(.+?)(?:\s+by bus)?$", text)
    destination_name = destination.group(1) if destination else None
    if followup and not destination_name:
        if short in DESTINATIONS:
            destination_name = short

    intent = detected_intent
    if followup and context["last_intent"] in ROUTE_INTENTS:
        # A route/destination alone changes the entity, not the previous topic.
        if short in DESTINATIONS or re.fullmatch(r"(?:(?:bus|route)\s+)?\d+", short):
            intent = context["last_intent"]
    if intent is None and followup and context["last_intent"]:
        if words & {"recharge", "refill"} or "top up" in text:
            intent = "card_recharge"
        elif words & {"price", "cost", "fare"}:
            intent = ("card_pricing" if context["last_intent"] in
                      {"hafilat_card", "card_pricing", "card_recharge"} else "bus_fares")
        elif words & {"start", "end", "operating", "hours"} or "stop running" in text:
            intent = "operating_hours"
        elif words & {"schedule", "timetable", "arrive", "departure", "frequency", "often"}:
            intent = "bus_schedules"
        elif words & {"stop", "station"}:
            intent = "bus_stops"
        elif words & {"route", "go", "destination"}:
            intent = "bus_routes"
        elif context["last_intent"] in ROUTE_INTENTS:
            # Unrecognized follow-ups (e.g. "what about pizza?") stay unknown.
            if route or destination_name or words & {"saturday", "sunday", "weekend",
                                                    "weekends", "weekday", "weekdays"}:
                intent = context["last_intent"]

    if intent in ROUTE_INTENTS:
        if route:
            if route.group(1) != context["current_route"]:
                context["current_destination"] = None
            context["current_route"] = route.group(1)
        if destination_name:
            # Retain unknown destinations too, so the answer can explain the limit.
            destination_name = destination_name.removeprefix("the ")
            context["current_destination"] = DESTINATIONS.get(destination_name, destination_name)
    return intent


def update_context(intent, context):
    if intent is not None:
        context["last_intent"] = intent
        if intent in ROUTE_INTENTS and context["current_route"] is None:
            context["current_route"] = "170"
        if intent in {"bus_schedules", "operating_hours"} and context["current_destination"] is None:
            context["current_destination"] = "Al Zeina"
