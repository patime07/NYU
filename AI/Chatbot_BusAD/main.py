from intents import patterns
from knowledge import knowledge_base
from intent_detection import detect_intent
from rules import generate_response
from context import create_context, resolve_intent, update_context
from conversation import detect_conversation_type, greeting, goodbye, help as help_response, fallback


def respond(user_input, context):
    """Shared entry point for the CLI, regression tests, and sample dialogue."""
    conversation_type = detect_conversation_type(user_input)
    commands = {"greeting": greeting, "goodbye": goodbye, "help": help_response}
    if conversation_type in commands:
        return commands[conversation_type]()
    if not user_input.strip():
        return fallback()
    detected_intent = detect_intent(user_input, patterns)
    intent = resolve_intent(user_input, detected_intent, context)
    update_context(intent, context)
    return generate_response(intent, knowledge_base, context, user_input) if intent else fallback()


def main():
    context = create_context()
    print(greeting())
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot:", goodbye())
            break
        response = respond(user_input, context)
        print("Bot:", response)
        if detect_conversation_type(user_input) == "goodbye":
            break


if __name__ == "__main__":
    main()
