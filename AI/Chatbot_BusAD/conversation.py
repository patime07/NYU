"""General conversational functions, separate from the eight domain intents."""
from intent_detection import preprocess


def greeting():
    return "Hello! Welcome to the Abu Dhabi Bus Assistant. How can I help you?"


def goodbye():
    return "Goodbye! Have a safe journey!"


def help():
    return (
        "I can help you with:\n"
        "- Hafilat cards and prices\n"
        "- Route 170 and its known stops\n"
        "- Stored weekday departures from NYU Abu Dhabi toward Al Zeina\n"
        "- Bus fares\n"
        "- Hafilat card recharge"
    )


def fallback():
    return (
        "Sorry, I didn't understand your question. "
        "Please ask about Abu Dhabi buses or type 'help' "
        "to see what I can assist you with."
    )



def detect_conversation_type(user_input):
    text = preprocess(user_input)

    greetings = {"hello", "hi", "hey", "good morning"}
    goodbyes = {"bye", "goodbye", "exit", "quit", "see you"}
    help_commands = {"help", "what can you do", "help me"}

    if text in greetings:
        return "greeting"

    elif text in goodbyes:
        return "goodbye"

    elif text in help_commands:
        return "help"

    return None
