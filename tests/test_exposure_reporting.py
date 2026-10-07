import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class ExposureReportingScreenTests(unittest.TestCase):
    def test_exposure_reporting_page_and_navigation(self) -> None:
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(app_path)).run(timeout=20)
        app.button(key="nav_exposure_reporting").click().run(timeout=20)

        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state["page"], "Exposure Reporting")
        self.assertTrue(any("Exposure Reporting</h1>" in item.value for item in app.markdown))
        self.assertIn("not implemented yet", app.info[0].value)
        self.assertEqual(len(app.file_uploader), 0)

        app.button(key="nav_treaty").click().run(timeout=20)
        self.assertEqual(app.session_state["page"], "Treaty")
        self.assertEqual(len(app.exception), 0)

        app.button(key="nav_reinsured_lines").click().run(timeout=20)
        self.assertEqual(app.session_state["page"], "Import Reinsured Lines")
        self.assertEqual(len(app.exception), 0)

        app.button(key="nav_home").click().run(timeout=20)
        self.assertEqual(app.session_state["page"], "Home")
        app.button(key="open_exposure_reporting").click().run(timeout=20)
        self.assertEqual(app.session_state["page"], "Exposure Reporting")
        self.assertEqual(len(app.exception), 0)


if __name__ == "__main__":
    unittest.main()
