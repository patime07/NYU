"""Print a reproducible conversation using the same response function as the CLI."""
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from context import create_context
from conversation import detect_conversation_type
from main import respond


def main():
    context = create_context()
    questions = (PROJECT / "examples" / "questions.txt").read_text(encoding="utf-8").splitlines()
    for number, question in enumerate(questions, 1):
        if number > 1:
            print()
        print(f"{number:02d}. User: {question}")
        print(f"Bot: {respond(question, context)}")
        if detect_conversation_type(question) == "goodbye":
            break


if __name__ == "__main__":
    main()
