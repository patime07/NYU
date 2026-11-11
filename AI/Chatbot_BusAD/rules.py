"""Eight intent rules, with explicit checks for unavailable route information."""
from context import ROUTE_INTENTS
from intent_detection import preprocess


def generate_response(intent, knowledge_base, context=None, user_input=""):
    
    if intent is None or intent not in knowledge_base:
        return "Sorry, I don't have information about that. Ask me about Abu Dhabi buses or Hafilat cards."

    facts = knowledge_base[intent]
    context = context or {}
    route = context.get("current_route") or "170"
    destination = context.get("current_destination")
    words = set(preprocess(user_input).split())

    if intent in ROUTE_INTENTS:
        if route != "170":
            return f"I don't have information for route {route}. My knowledge base only covers route 170."
        if destination and destination not in knowledge_base["bus_routes"]["known_destinations"]:
            return f"I don't have route information for {destination}. I only know the listed stops on route 170."
        if intent in {"operating_hours", "bus_schedules"}:
            if words & {"saturday", "sunday", "weekend", "weekends", "holiday", "holidays"}:
                return ("I don't have weekend or holiday departure times. The stored timetable covers "
                        "weekdays only. Check the official timetable: "
                        f"{knowledge_base['bus_schedules']['timetable_source']}.")
            if destination and destination != "Al Zeina":
                return (f"I don't have departure times toward {destination}. The stored timetable only "
                        "covers departures from NYU Abu Dhabi toward Al Zeina.")

    if intent == "hafilat_card":
        anonymous_locations = ", ".join(facts["anonymous_purchase_locations"])
        personalized_locations = ", ".join(facts["personalized_purchase_locations"])
        if words & {"personalized", "personalised"}:
            return f"Official personalized Hafilat card application channels: {personalized_locations}."
        types = ", ".join(facts.get("card_types", []))
        return (f"{facts['description']} Available card types: {types}. "
                f"Anonymous cards: {anonymous_locations}. "
                f"Personalized card applications: {personalized_locations}.")

    elif intent == "card_pricing":
        anonymous = facts.get("anonymous_card_price")
        personalized = facts.get("personalized_card_price")
        return (f"An anonymous Hafilat card costs {anonymous} AED and a personalized "
                f"card costs {personalized} AED.")

    elif intent == "operating_hours":
        return (f"For route 170, the first listed weekday departure from Saadiyat New York University 2 "
                f"that reaches Al Zeina is {facts['route_170_start']} and the last is "
                f"{facts['route_170_end']}.")

    elif intent == "bus_routes":
        prefix = f"For travel to {destination}, " if destination else ""
        return f"{prefix}Route {route}: {facts['route_170']}."

    elif intent == "card_recharge":
        locations = ", ".join(facts.get("recharge_locations", []))
        online = facts.get("online_recharge")
        response = f"You can recharge your Hafilat card at: {locations}."
        if online:
            response += f" Online recharge: {facts.get('recharge_website')}."
        return response

    elif intent == "bus_fares":
        if words & {"intercity", "dubai"} or {"inter", "city"} <= words:
            return ("I don't have intercity bus fares, including services to Dubai. "
                    f"The stored fare only covers {facts['service_scope']}.")
        if words & {"discount", "discounts"}:
            return (f"For {facts['service_scope']}, the stored policy lists free travel for children aged "
                    f"{facts['free_travel_age_max']} and under. I don't have other discount policies.")
        return (f"For {facts['service_scope']}, the stored fare is a base fare of "
                f"{facts['base_fare']} {facts['currency']}, plus "
                f"{facts['distance_fare']} {facts['currency']} per kilometer, "
                f"up to {facts['maximum_fare']} {facts['currency']}.")

    elif intent == "bus_stops":
        prefix = "I can't determine your nearest stop without location data. " if "nearest" in words else ""
        return (f"{prefix}The main bus station is {facts['main_bus_station']}. "
                f"Route 170 serves {facts['route_170_stop']}.")

    elif intent == "bus_schedules":
        frequency = (f"{facts['route_170_frequency_note']} "
                     if words & {"often", "frequency"} else "")
        return (f"{frequency}I don't have live arrival predictions. "
                f"For route 170 from Saadiyat New York University 2 reaching Al Zeina, the stored weekday "
                f"first departure is {facts['route_170_first_departure']} and the last "
                f"is {facts['route_170_last_departure']}. Check the official timetable "
                f"for exact departures: {facts['timetable_source']}.")

    return "Sorry, I don't have a response for you"
