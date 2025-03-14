import unittest
import json
from unittest.mock import patch, MagicMock
from agents.stt_processor.stt_agent import STTProcessor

class TestSTTProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize the STT Processor for testing."""
        cls.stt_processor = STTProcessor()

    @patch("agents.stt_processor.stt_agent.whisper.load_model")
    def test_whisper_transcription(self, mock_load_model):
        """Test Whisper transcription process."""
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "Hello world"}
        mock_load_model.return_value = mock_model

        self.stt_processor.model = mock_model

        result = self.stt_processor.transcribe_whisper("data/sample_audio/test.wav")
        self.assertEqual(result, "Hello world")


    def test_vosk_transcription(self):
        print("TBD")

    @patch("agents.stt_processor.stt_agent.wave.open")
    @patch("agents.stt_processor.stt_agent.STTProcessor.transcribe_whisper", return_value="Hello world")
    @patch("agents.stt_processor.stt_agent.MessageBroker")
    def test_handle_message(self, mock_broker, mock_transcribe_whisper, mock_wave_open):
        """Test message handling and RabbitMQ message sending."""
        test_message = {
            "audio_path": "data/sample_audio/test.wav",
            "metadata": {"patient_id": "12345"}
        }
        test_message_json = json.dumps(test_message)

        mock_broker_instance = mock_broker.return_value
        self.stt_processor.broker = mock_broker_instance

        mock_wave_file = MagicMock()
        mock_wave_open.return_value.__enter__.return_value = mock_wave_file
        mock_wave_file.getframerate.return_value = 16000
        mock_wave_file.readframes.side_effect = [b"\x01\x02" * 2000, b""]

        # Run function
        self.stt_processor.handle_message

if __name__ == "__main__":
    unittest.main()
