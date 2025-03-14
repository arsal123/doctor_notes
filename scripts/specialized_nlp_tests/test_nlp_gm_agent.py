import json
from broker.broker import MessageBroker
from agents.consultation_orchestrator.config import OrchestratorConfig

broker = MessageBroker()

test_message = {
    "transcription": """
        The patient is feeling very tired and has a persistent headache.
    """,
    "metadata": {"patient_id": "12345",
                 "doctor_id": "D5678",
                 "consultation_type": "general_medicine"
                 }
}

broker.send_message(OrchestratorConfig.NLP_AGENT_QUEUES['general_medicine'], json.dumps(test_message))
print(f"Test message sent to General Medicine NLP Agent: {OrchestratorConfig.NLP_AGENT_QUEUES['general_medicine']}")
