import os
from dotenv import load_dotenv

load_dotenv()


class OrchestratorConfig:
    """Configuration for the Consultation Orchestrator."""

    # RabbitMQ Queues
    RABBITMQ_QUEUE_INPUT = os.getenv("RABBITMQ_ORCHESTRATOR_INPUT", "orchestrator_input")

    # NLP Agent Routing (Mapping Consultation Types to Queues)
    NLP_AGENT_QUEUES = {
        "general_medicine": os.getenv("RABBITMQ_NLP_GENERAL", "nlp_general"),
        "mental_health": os.getenv("RABBITMQ_NLP_MENTAL", "nlp_mental"),
        "nutrition": os.getenv("RABBITMQ_NLP_NUTRITION", "nlp_nutrition")
    }

    # Medical History Agent Queue
    MEDICAL_HISTORY_QUEUE = os.getenv("RABBITMQ_MEDICAL_HISTORY", "medical_history_agent")
