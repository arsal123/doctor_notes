import json
import wave
import logging
import whisper
from vosk import Model, KaldiRecognizer
from broker.broker import MessageBroker
from agents.stt_processor.config import STTConfig

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class STTProcessor:
    """Speech-to-Text Processor using Whisper or Vosk."""

    def __init__(self):
        """Initialize STT model based on configuration."""
        self.broker = MessageBroker()

        if STTConfig.USE_WHISPER:
            logger.info(f"Using Whisper model: {STTConfig.WHISPER_MODEL_SIZE}")
            self.model = whisper.load_model(STTConfig.WHISPER_MODEL_SIZE)
        else:
            logger.info(f"Using Vosk model from: {STTConfig.VOSK_MODEL_PATH}")
            self.model = Model(STTConfig.VOSK_MODEL_PATH)

    def process_audio(self, audio_path):
        """Transcribe audio file to text using Whisper or Vosk."""
        if STTConfig.USE_WHISPER:
            return self.transcribe_whisper(audio_path)
        else:
            return self.transcribe_vosk(audio_path)

    def transcribe_whisper(self, audio_path):
        """Transcribe using Whisper."""
        result = self.model.transcribe(audio_path)
        return result["text"]

    def transcribe_vosk(self, audio_path):
        """Transcribe using Vosk."""
        wf = wave.open(audio_path, "rb")
        recognizer = KaldiRecognizer(self.model, wf.getframerate())
        transcript = ""

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                transcript += result["text"] + " "
        return transcript.strip()

    def handle_message(self, message):
        """Process an audio message from the queue."""
        message_data = json.loads(message)
        audio_path = message_data["audio_path"]
        metadata = message_data.get("metadata", {})

        logger.info(f"Processing audio file: {audio_path}")
        text = self.process_audio(audio_path)

        response = {
            "transcription": text,
            "metadata": metadata
        }

        # Send transcription to Orchestrator queue
        self.broker.send_message(STTConfig.RABBITMQ_QUEUE_OUTPUT, json.dumps(response))
        logger.info("Transcription sent successfully.")

    def start(self):
        """Start listening for audio messages from RabbitMQ."""
        logger.info("STT Processor is listening for audio messages...")
        self.broker.consume_messages_real_time(STTConfig.RABBITMQ_QUEUE_INPUT, self.handle_message)

if __name__ == "__main__":
    stt_processor = STTProcessor()
    stt_processor.start()
