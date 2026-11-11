"""Deterministic pattern matching; no model or external dependencies."""
import re


# Function words alone must not turn unrelated questions into bus questions.
STOP_WORDS = set("a an the i my you your we it its this that is are do does can "
                 "could would should have has be to of for on at in by with and "
                 "or what which where when how much there me get".split())
ALIASES = {"buses": "bus", "cards": "card", "fares": "fare", "routes": "route",
           "stops": "stop", "schedules": "schedule", "costs": "cost"}
DOMAIN_WORDS = set("bus hafilat card route fare recharge refill timetable schedule "
                   "departure operating nyu zeina".split())


def preprocess(text):
    # Use the same normalization for patterns, commands, and user input.
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())


def content_words(text):
    return {ALIASES.get(word, word) for word in preprocess(text).split()
            if word not in STOP_WORDS}


def pattern_text(text):
    # Route numbers are entities, not different intents; validate them in rules.py.
    return re.sub(r"\b(bus|route)\s+\d+\b", r"\1 number", preprocess(text))


def score_intents(user_input, patterns):
    """Add 0.5 per shared content word, summed across an intent's patterns."""
    question_words = content_words(user_input)
    scores = {}

    for intent, examples in patterns.items():
        total = 0.0
        for example in examples:
            pattern_words = content_words(example)
            total += 0.5 * len(question_words & pattern_words)
        scores[intent] = total

    return scores


def detect_intent(user_input, patterns, min_score=1.0):
    # A unique full pattern is stronger evidence than aggregate word overlap.
    question = pattern_text(user_input)
    exact = [intent for intent, examples in patterns.items()
             if question in {pattern_text(example) for example in examples}]
    if exact:
        return exact[0] if len(exact) == 1 else None

    words = content_words(user_input)
    if not words & DOMAIN_WORDS or words <= {"bus", "card", "route"}:
        return None

    scores = score_intents(user_input, patterns)
    if not scores:
        return None

    highest = max(scores.values())
    if highest < min_score:
        return None

    winners = [intent for intent, score in scores.items() if score == highest]
    return winners[0] if len(winners) == 1 else None
