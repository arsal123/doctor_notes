import os
from dotenv import load_dotenv

load_dotenv()

class NotesConfig:
    """Configuration settings for the Notes Generator."""

    # RabbitMQ Queue for receiving NLP results
    RABBITMQ_QUEUE_INPUT = os.getenv("RABBITMQ_NOTES_INPUT", "notes_generator")

    # Where notes data is sent
    RABBITMQ_QUEUE_OUTPUT = os.getenv("RABBITMQ_NOTES_OUTPUT", "notes_output")

    # Logging Level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
