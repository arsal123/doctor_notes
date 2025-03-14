import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class STTConfig:
    """Configuration settings for the Speech-to-Text Processor."""

    # Choose STT Model (Whisper or Vosk)
    USE_WHISPER = os.getenv("USE_WHISPER", "true").lower() == "true"

    # Whisper Model Settings
    WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")  # tiny, base, small, medium, large

    # Vosk Model Settings (If Whisper is disabled)
    VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "../../models/vosk-model")

    # RabbitMQ Configuration
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_QUEUE_INPUT = "stt_processor_queue"
    RABBITMQ_QUEUE_OUTPUT = "orchestrator_input"
