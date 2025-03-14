import unittest
from agents.stt_processor.stt_agent import STTProcessor
from agents.stt_processor.config import STTConfig

class TestSTTProcessor(unittest.TestCase):

    def test_integration_transcribe_vosk(self):
        STTConfig.USE_WHISPER = False
        stt_processor = STTProcessor()
        transcript = stt_processor.transcribe_vosk("/Users/egor.krylovich/workspace/multiagent-medical-system/data/sample_audio/test.wav")
        print(f"Final Transcript: {transcript}")
        self.assertNotEqual(transcript, "", "Transcription should not be empty")

    def test_integration_transcribe_whisper(self):
        STTConfig.USE_WHISPER = True
        stt_processor = STTProcessor()
        transcript = stt_processor.transcribe_whisper("/Users/egor.krylovich/workspace/multiagent-medical-system/data/sample_audio/test.wav")
        print(f"Final Transcript: {transcript}")
        # TBD Fix several warnings. At least one related to unclosed tokinezer?
        self.assertNotEqual(transcript, "", "Transcription should not be empty")