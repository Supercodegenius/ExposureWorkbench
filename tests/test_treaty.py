import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class TreatyScreenTests(unittest.TestCase):
    def test_treaty_layout_editing_and_navigation(self) -> None:
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(app_path)).run(timeout=20)
        app.button(key="nav_treaty").click().run(timeout=20)

        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.text_input(key="treaty_reinsured").value, "AEGIS")
        self.assertEqual(app.text_input(key="treaty_programme").value, "AEGIS GL 2012")
        self.assertEqual(app.number_input(key="treaty_excess").value, 7500000.0)
        self.assertEqual(
            [tab.label for tab in app.tabs],
            ["Layers", "Currencies", "Types", "Locales", "Benefit", "Retro"],
        )
        self.assertEqual(len(app.dataframe[0].value), 2)
        self.assertIn("Stretch", app.dataframe[0].value.columns)
        self.assertTrue(next(button for button in app.button if button.label == "Save").disabled)

        app.text_input(key="treaty_programme").set_value("Edited Treaty").run(timeout=20)
        self.assertEqual(app.text_input(key="treaty_programme").value, "Edited Treaty")
        self.assertEqual(len(app.exception), 0)

        app.button(key="nav_home").click().run(timeout=20)
        self.assertEqual(app.session_state["page"], "Home")
        self.assertEqual(len(app.exception), 0)

        app.button(key="nav_reinsured_lines").click().run(timeout=20)
        self.assertEqual(app.session_state["page"], "Import Reinsured Lines")
        self.assertEqual(len(app.exception), 0)


if __name__ == "__main__":
    unittest.main()
