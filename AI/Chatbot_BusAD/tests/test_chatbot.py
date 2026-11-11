"""Regression checks for the assignment examples and actual conversation bugs."""
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from context import create_context
from conversation import fallback, goodbye, greeting, help as help_response
from intent_detection import detect_intent
from intents import patterns
from main import respond


class ChatbotTests(unittest.TestCase):
    def test_all_40_patterns_and_punctuation_variants(self):
        self.assertEqual(len(patterns), 8)
        self.assertEqual(sum(map(len, patterns.values())), 40)
        for intent, examples in patterns.items():
            self.assertEqual(len(set(examples)), 5)
            for question in examples:
                with self.subTest(intent=intent, question=question):
                    self.assertEqual(detect_intent(question, patterns), intent)
                    self.assertEqual(detect_intent('  ' + question.upper() + '?!  ', patterns), intent)

    def test_unrelated_questions_and_ambiguous_bus_use_fallback(self):
        for question in ("what is the weather today", "I need a pizza", "how do I cook pasta",
                         "what is 2 plus 2", "tell me a joke", "bus", "", "   "):
            with self.subTest(question=question):
                self.assertEqual(respond(question, create_context()), fallback())

    def test_tied_scores_and_duplicate_patterns_are_ambiguous(self):
        tied = {"one": ["bus fare alpha", "bus fare beta"],
                "two": ["bus fare gamma", "bus fare delta"]}
        self.assertIsNone(detect_intent("bus fare", tied))
        self.assertIsNone(detect_intent("bus fare", {"one": ["bus fare"], "two": ["bus fare"]}))
        self.assertIsNone(detect_intent("bus fare", {}))

    def test_general_commands_normalize_punctuation(self):
        for question, expected in (("HI!", greeting()), ("what can you do?", help_response()),
                                   ("help!", help_response()), ("bye.", goodbye())):
            with self.subTest(question=question):
                self.assertEqual(respond(question, create_context()), expected)

    def test_explicit_recharge_overrides_previous_route(self):
        context = create_context()
        respond("which bus goes to nyu abu dhabi", context)
        self.assertIn("recharge your Hafilat card", respond("and how do I recharge my card", context))
        self.assertEqual(context["last_intent"], "card_recharge")

    def test_card_price_followup_uses_previous_topic(self):
        context = create_context()
        self.assertIn("smart card", respond("what is a hafilat card", context))
        self.assertIn("anonymous Hafilat card costs", respond("and its price?", context))

    def test_unknown_followup_preserves_context_without_reusing_answer(self):
        context = create_context()
        respond("what is a hafilat card", context)
        previous = context.copy()
        self.assertEqual(respond("what about pizza?", context), fallback())
        self.assertEqual(context, previous)

    def test_weekend_followup_does_not_repeat_weekday_times(self):
        context = create_context()
        respond("when does the next bus arrive", context)
        reply = respond("and on Saturday?", context)
        self.assertIn("don't have weekend", reply)
        self.assertNotIn("06:36", reply)

    def test_unknown_route_is_remembered_and_can_be_replaced(self):
        context = create_context()
        self.assertIn("don't have information for route 94", respond("what time does bus 94 arrive", context))
        self.assertIn("don't have information for route 94", respond("and its operating hours?", context))
        self.assertEqual(context["current_route"], "94")
        self.assertIn("06:36", respond("what about 170?", context))
        self.assertEqual(context["current_route"], "170")

    def test_destination_controls_followup_direction(self):
        context = create_context()
        respond("which bus goes to nyu abu dhabi", context)
        self.assertEqual(context["current_destination"], "NYU Abu Dhabi")
        self.assertIn("don't have departure times toward NYU Abu Dhabi", respond("and the timetable?", context))
        self.assertIn("06:36", respond("what about al zeina?", context))
        self.assertEqual(context["current_destination"], "Al Zeina")

    def test_unknown_destination_does_not_silently_become_route_170(self):
        context = create_context()
        self.assertIn("don't have route information for yas island", respond("which bus goes to yas island", context))
        self.assertIn("don't have route information for yas island", respond("and the timetable?", context))

    def test_frequency_question_explains_variable_intervals(self):
        reply = respond("how often does this bus run", create_context())
        self.assertIn("intervals vary", reply)
        self.assertNotIn("15 minutes", reply)
        self.assertIn("don't have live arrival predictions", reply)

    def test_times_are_for_nyu_departures_reaching_al_zeina(self):
        # Official route 170 PDF, page 3: exclude city-originating early trips
        # and the 23:03 NYU departure with no onward time at Al Zeina.
        for question in ("when do the buses start operating", "when does the next bus arrive"):
            with self.subTest(question=question):
                reply = respond(question, create_context())
                self.assertIn("Saadiyat New York University 2", reply)
                self.assertIn("06:36", reply)
                self.assertIn("22:21", reply)
                self.assertNotIn("05:00", reply)
                self.assertNotIn("23:03", reply)

    def test_personalized_card_channels_do_not_include_anonymous_retailers(self):
        reply = respond("Can I get a personalized Hafilat card at Lulu?", create_context())
        self.assertIn("customer happiness offices", reply)
        self.assertIn("Airport office", reply)
        self.assertIn("https://hafilat.darb.ae", reply)
        self.assertNotIn("Lulu", reply)
        self.assertNotIn("vending machines", reply)

    def test_standard_fare_is_not_presented_as_an_intercity_fare(self):
        for question in ("How much does the bus to Dubai cost?",
                         "How much does an intercity bus ride cost?",
                         "How much does an inter-city bus ride cost?"):
            with self.subTest(question=question):
                reply = respond(question, create_context())
                self.assertIn("don't have intercity bus fares", reply)
                self.assertNotIn("0.05", reply)
                self.assertNotIn("5.0", reply)
        reply = respond("how much does a bus ride cost", create_context())
        self.assertIn("Standard Service", reply)
        self.assertIn("excluding intercity", reply)
        self.assertIn("0.05", reply)

    def test_operating_hours_and_schedule_remain_distinct(self):
        context = create_context()
        reply = respond("when does the bus service end", context)
        self.assertEqual(context["last_intent"], "operating_hours")
        self.assertIn("22:21", reply)
        respond("which bus goes to al zeina", context)
        self.assertIn("22:21", respond("when does it stop running?", context))
        self.assertEqual(context["last_intent"], "operating_hours")

    def test_sessions_do_not_share_context(self):
        first, second = create_context(), create_context()
        respond("what time does bus 94 arrive", first)
        self.assertIn("06:36", respond("when does the next bus arrive", second))

    def test_cli_handles_empty_input_and_punctuated_exit(self):
        result = subprocess.run([sys.executable, "-B", str(PROJECT / "main.py")],
                                input="\nhelp!\nbye!\nignored\n", capture_output=True,
                                text=True, check=True, timeout=5)
        self.assertEqual(result.stderr, "")
        self.assertIn(fallback(), result.stdout)
        self.assertIn(help_response(), result.stdout)
        self.assertEqual(result.stdout.count("You: "), 3)
        self.assertTrue(result.stdout.rstrip().endswith(goodbye()))

    def test_cli_handles_eof(self):
        result = subprocess.run([sys.executable, "-B", str(PROJECT / "main.py")],
                                input="", capture_output=True, text=True, check=True, timeout=5)
        self.assertEqual(result.stderr, "")
        self.assertTrue(result.stdout.rstrip().endswith(goodbye()))


if __name__ == "__main__":
    unittest.main()
