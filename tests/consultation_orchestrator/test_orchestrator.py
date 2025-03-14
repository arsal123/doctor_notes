import unittest
import json
from unittest.mock import patch, MagicMock
from agents.consultation_orchestrator.consultation_orchestrator_agent import ConsultationOrchestrator
from agents.notes_generator.config import NotesConfig


class TestConsultationOrchestrator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize the Consultation Orchestrator for testing."""
        cls.orchestrator = ConsultationOrchestrator()

    def test_analyze_transcription_for_nlp_general(self):
        """Test that only general medicine NLP is selected for a normal consultation."""
        transcription = "The patient feels tired."
        consultation_type = "general_medicine"

        result = self.orchestrator.analyze_transcription_for_nlp(transcription, consultation_type)

        expected = ["nlp_general"]
        self.assertListEqual(sorted(result), sorted(expected))

    def test_analyze_transcription_for_nlp_with_mental_health(self):
        """Test that mental health NLP is selected when related keywords appear."""
        transcription = "The patient has been feeling anxious and stressed lately."
        consultation_type = "general_medicine"

        result = self.orchestrator.analyze_transcription_for_nlp(transcription, consultation_type)

        expected = ["nlp_general", "nlp_mental"]
        self.assertListEqual(sorted(result), sorted(expected))

    def test_analyze_transcription_for_nlp_with_nutrition(self):
        """Test that nutrition NLP is selected when diet-related keywords appear."""
        transcription = "The patient has an unhealthy diet and struggles with weight gain."
        consultation_type = "general_medicine"

        result = self.orchestrator.analyze_transcription_for_nlp(transcription, consultation_type)

        expected = ["nlp_general", "nlp_nutrition"]
        self.assertListEqual(sorted(result), sorted(expected))

    def test_analyze_transcription_for_nlp_with_multiple_conditions(self):
        """Test when multiple NLP agents should be triggered."""
        transcription = "The patient feels anxious, has a headache, and struggles with nutrition."
        consultation_type = "general_medicine"

        result = self.orchestrator.analyze_transcription_for_nlp(transcription, consultation_type)

        expected = ["nlp_general", "nlp_mental", "nlp_nutrition"]
        self.assertListEqual(sorted(result), sorted(expected))

    @patch("agents.consultation_orchestrator.consultation_orchestrator_agent.MessageBroker")
    def test_process_transcription(self, mock_broker):
        """Test processing transcription to ensure messages are sent correctly."""
        test_transcription = "The patient has a headache and stress."
        test_metadata = {"patient_id": "12345", "doctor_id": "67890", "consultation_type": "general_medicine"}
        request = {
            "transcription": test_transcription,
            "metadata": test_metadata
        }

        mock_broker_instance = mock_broker.return_value
        self.orchestrator.broker = mock_broker_instance

        # Run the function
        self.orchestrator.process_transcription(json.dumps(request))

        # Verify messages were sent to the expected NLP agents
        expected_nlp_message_mental = {
            "request_type": "nlp_analysis",
            "transcription": test_transcription,
            "metadata": test_metadata
        }
        expected_nlp_message_general = expected_nlp_message_mental.copy()

        mock_broker_instance.send_message.assert_any_call("nlp_general", json.dumps(expected_nlp_message_general))
        mock_broker_instance.send_message.assert_any_call("nlp_mental", json.dumps(expected_nlp_message_mental))

        # Verify that the Notes Generator was notified
        expected_notes_message = {
            "event_type": "nlp_processing_started",
            "patient_id": "12345",
            "doctor_id": "67890",
            "transcription": test_transcription,
            "metadata": test_metadata,
            "expected_agents": sorted(["nlp_general", "nlp_mental"])  # Ensure this matches actual output
        }

        # Convert to JSON format for direct comparison
        expected_json = json.dumps(expected_notes_message, sort_keys=True)

        # Capture the actual message sent
        actual_json = None
        for call in mock_broker_instance.send_message.call_args_list:
            queue, message = call[0]
            if queue == NotesConfig.RABBITMQ_QUEUE_INPUT:
                actual_json = message
                break

        # Check if the messages match
        self.assertEqual(expected_json, actual_json)

if __name__ == "__main__":
    unittest.main()
