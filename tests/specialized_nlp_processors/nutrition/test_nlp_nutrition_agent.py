import unittest
import json
from unittest.mock import patch, MagicMock
from agents.specialized_nlp_processors.nutrition.nlp_nutrition_agent import NutritionNLP


class TestNutritionNLP(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize Nutrition NLP Agent for testing."""
        cls.nlp_agent = NutritionNLP()

    def test_analyze_transcription_no_keywords(self):
        """Test transcription analysis when no nutrition-related keywords are present."""
        transcription = "The patient is eating a balanced diet and feels fine."
        result = self.nlp_agent.analyze_transcription(transcription)

        # Expect no findings
        self.assertEqual(result["analysis"], [])
        self.assertEqual(result["recommendation"], "No significant nutrition issues detected")

    def test_analyze_transcription_with_unhealthy_diet(self):
        """Test transcription analysis when unhealthy eating is mentioned."""
        transcription = "The patient eats junk food and skips meals."
        result = self.nlp_agent.analyze_transcription(transcription)

        # Expect nutrition-related findings
        self.assertIn("Patient may have an unhealthy diet", result["analysis"])
        self.assertIn("Possible malnutrition or appetite issues", result["analysis"])
        self.assertEqual(result["recommendation"], "Nutritional assessment and dietary counseling may be required")

    def test_analyze_transcription_with_multiple_issues(self):
        """Test when multiple nutrition issues are mentioned."""
        transcription = "The patient is overweight and has a vitamin deficiency."
        result = self.nlp_agent.analyze_transcription(transcription)

        # Expect multiple findings
        self.assertIn("Potential weight management issue", result["analysis"])
        self.assertIn("Potential vitamin or nutrient deficiency", result["analysis"])
        self.assertEqual(result["recommendation"], "Nutritional assessment and dietary counseling may be required")

    @patch("agents.specialized_nlp_processors.nutrition.nlp_nutrition_agent.MessageBroker")
    def test_handle_message(self, mock_broker):
        """Test message handling and RabbitMQ message sending."""
        test_message = {
            "transcription": "The patient is skipping meals and has gained weight.",
            "metadata": {"patient_id": "54321"}
        }
        test_message_json = json.dumps(test_message)

        mock_broker_instance = mock_broker.return_value
        self.nlp_agent.broker = mock_broker_instance

        self.nlp_agent.handle_message(test_message_json)

        mock_broker_instance.send_message.assert_called_once()


if __name__ == "__main__":
    unittest.main()
