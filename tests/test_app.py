import importlib.util
import unittest
from pathlib import Path


@unittest.skipUnless(importlib.util.find_spec("streamlit"), "Install requirements for UI tests.")
class AppTests(unittest.TestCase):
    def test_both_conversions_and_error_feedback(self):
        from streamlit.testing.v1 import AppTest

        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
        self.assertFalse(app.exception)
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.success[0].value, "Aligned outputs match for this input.")
        app.radio[0].set_value("Moore → Mealy").run()
        self.assertFalse(app.success)
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertTrue(app.success)
        self.assertIn("['1', '1']", [element.value.split("Aligned: ")[-1] for element in app.text])
        app.text_input(key="word").set_value("2").run()
        self.assertIn("Unknown input symbol", app.error[0].value)
        app.text_area[0].set_value("A,0,B").run()
        app.button[0].click().run()
        self.assertIn("Missing transition", app.error[0].value)
        self.assertFalse(app.success)
