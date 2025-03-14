import os
from dotenv import load_dotenv

load_dotenv()

class NLPConfig:
    """Configuration settings for NLP Agents."""

    # Where NLP results are sent
    RABBITMQ_QUEUE_OUTPUT = os.getenv("NOTES_QUEUE", "notes_generator")

    # Where NLP results are sent
    OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY", "empty_key")

    # Logging Level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Models configuration
    MENTAL_HEALTH_MODEL_CONFIG = [{"model": "gpt-4o-mini-2024-07-18", "api_key": OPEN_AI_API_KEY}]
    GENERAL_MEDICINE_MODEL_CONFIG = [{"model": "gpt-4o-mini-2024-07-18", "api_key": OPEN_AI_API_KEY}]
    NUTRITION_MODEL_CONFIG = [{"model": "gpt-4o-mini-2024-07-18", "api_key": OPEN_AI_API_KEY}]
