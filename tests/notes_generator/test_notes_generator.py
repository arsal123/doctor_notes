import unittest
import json
from unittest.mock import patch, MagicMock
from agents.notes_generator.notes_agent import NotesGenerator


class TestNotesGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize Notes Generator for testing."""
        cls.notes_generator = NotesGenerator()

    @patch("agents.notes_generator.notes_agent.MessageBroker")
    def test_handle_nlp_start_event(self, mock_broker):
        """Test initializing tracking when consultation starts."""
        event_message = {
            "event_type": "nlp_processing_started",
            "patient_id": "12345",
            "doctor_id": "56789",
            "transcription": "Patient reports headaches and fatigue.",
            "expected_agents": ["nlp_general", "nlp_mental"],
            "metadata": {}
        }

        self.notes_generator.handle_message(json.dumps(event_message))

        key = "12345-56789"
        self.assertIn(key, self.notes_generator.pending_cases)
        self.assertEqual(self.notes_generator.pending_cases[key]["transcription"],
                         "Patient reports headaches and fatigue.")


if __name__ == "__main__":
    unittest.main()
