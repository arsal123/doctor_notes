import unittest
import json
from unittest.mock import patch, MagicMock
from agents.specialized_nlp_processors.mental_health.nlp_mh_agent import MentalHealthAgent


class TestMentalHealthAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize Mental Health NLP Agent for testing."""
        cls.nlp_agent = MentalHealthAgent()

    def test_analyze_transcription_no_keywords(self):
        """Test transcription analysis when no mental health keywords are present."""
        transcription = "The patient is feeling okay and has no psychological concerns."
        result = self.nlp_agent.analyze_transcription(transcription)

        # Expect no findings
        self.assertEqual(result["analysis"], [])
        self.assertEqual(result["recommendation"], "No significant mental health issues detected")

    def test_analyze_transcription_with_depression(self):
        """Test transcription analysis when 'depressed' is mentioned."""
        transcription = "The patient feels hopeless and worthless."
        result = self.nlp_agent.analyze_transcription(transcription)

        # Expect a depression-related finding
        self.assertIn("Possible depression symptoms", result["analysis"])
        self.assertEqual(result["recommendation"], "Further psychological evaluation may be required")

    def test_analyze_transcription_with_multiple_issues(self):
        """Test when multiple mental health concerns are mentioned."""
        transcription = "The patient feels anxious, has mood swings, and is having trouble sleeping."
        result = self.nlp_agent.analyze_transcription(transcription)

        # Expect multiple findings
        self.assertIn("Possible anxiety disorder", result["analysis"])
        self.assertIn("Possible mood disorder", result["analysis"])
        self.assertIn("Possible sleep disorder", result["analysis"])
        self.assertEqual(result["recommendation"], "Further psychological evaluation may be required")

    @patch("agents.specialized_nlp_processors.mental_health.nlp_mh_agent.MessageBroker")
    def test_handle_message(self, mock_broker):
        """Test message handling and RabbitMQ message sending."""
        test_message = {
            "transcription": "The patient is feeling anxious and has insomnia.",
            "metadata": {"patient_id": "67890"}
        }
        test_message_json = json.dumps(test_message)

        mock_broker_instance = mock_broker.return_value
        self.nlp_agent.broker = mock_broker_instance

        self.nlp_agent.handle_message(test_message_json)

        mock_broker_instance.send_message.assert_called_once()


if __name__ == "__main__":
    unittest.main()
