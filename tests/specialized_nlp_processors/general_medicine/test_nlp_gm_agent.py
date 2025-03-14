import unittest
import json
from unittest.mock import patch, MagicMock
from agents.specialized_nlp_processors.general_medicine.nlp_gm_agent import GeneralMedicineAgent


class TestGeneralMedicineAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize General Medicine NLP Agent for testing."""
        cls.nlp_agent = GeneralMedicineAgent()

    def test_analyze_transcription_no_keywords(self):
        """Test transcription analysis when no medical keywords are present."""
        transcription = "The patient is feeling well and has no complaints."
        result = self.nlp_agent.analyze_transcription(transcription)

        #  Expect no findings
        self.assertEqual(result["analysis"], [])
        self.assertEqual(result["recommendation"], "No significant issues detected")

    def test_analyze_transcription_with_headache(self):
        """Test transcription analysis when 'headache' is mentioned."""
        transcription = "The patient is experiencing severe headaches."
        result = self.nlp_agent.analyze_transcription(transcription)

        #  Expect a headache-related finding
        self.assertIn("Possible migraine or neurological issue", result["analysis"])
        self.assertEqual(result["recommendation"], "Further testing may be required")

    def test_analyze_transcription_with_fatigue(self):
        """Test transcription analysis when 'fatigue' is mentioned."""
        transcription = "The patient reports ongoing fatigue and lack of energy."
        result = self.nlp_agent.analyze_transcription(transcription)

        # Expect a fatigue-related finding
        self.assertIn("Possible anemia or chronic fatigue syndrome", result["analysis"])
        self.assertEqual(result["recommendation"], "Further testing may be required")

    def test_analyze_transcription_with_multiple_issues(self):
        """Test when multiple medical conditions are mentioned in transcription."""
        transcription = "The patient has a headache, feels tired, and has a fever."
        result = self.nlp_agent.analyze_transcription(transcription)

        #  Expect findings for headache, fatigue, and fever
        self.assertIn("Possible migraine or neurological issue", result["analysis"])
        self.assertIn("Possible anemia or chronic fatigue syndrome", result["analysis"])
        self.assertIn("Potential infection or flu symptoms", result["analysis"])
        self.assertEqual(result["recommendation"], "Further testing may be required")

    @patch("agents.specialized_nlp_processors.general_medicine.nlp_gm_agent.MessageBroker")
    def test_handle_message(self, mock_broker):
        """Test message handling and RabbitMQ message sending."""
        test_message = {
            "transcription": "The patient has severe fatigue and constant headaches.",
            "metadata": {"patient_id": "12345"}
        }
        test_message_json = json.dumps(test_message)

        # Mock broker instance
        mock_broker_instance = mock_broker.return_value
        self.nlp_agent.broker = mock_broker_instance

        # Run the message handler
        self.nlp_agent.handle_message(test_message_json)

        # Assertions
        expected_analysis = {
            "nlp_type": "general_medicine",
            "patient_id": "12345",
            "analysis_result": {
                "analysis": [
                    "Possible migraine or neurological issue",
                    "Possible anemia or chronic fatigue syndrome"
                ],
                "recommendation": "Further testing may be required"
            }
        }

        # Ensure message was sent to RabbitMQ
        mock_broker_instance.send_message.assert_called_once()
        args, _ = mock_broker_instance.send_message.call_args
        queue_name, sent_message = args
        sent_message_data = json.loads(sent_message)

        self.assertEqual(queue_name, "notes_generator")  # Expected output queue
        self.assertEqual(sent_message_data, expected_analysis)


if __name__ == "__main__":
    unittest.main()
