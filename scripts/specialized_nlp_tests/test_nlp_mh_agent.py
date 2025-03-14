import json
from broker.broker import MessageBroker
from agents.consultation_orchestrator.config import OrchestratorConfig

broker = MessageBroker()

test_message = {
    "transcription": "The patient feels hopeless, has been having mood swings, and is experiencing trouble sleeping.",
    "metadata": {"patient_id": "12345",
                 "doctor_id": "D5678",
                 "consultation_type": "general_medicine"
                 }
}

broker.send_message(OrchestratorConfig.NLP_AGENT_QUEUES['mental_health'], json.dumps(test_message))
print(f"Test message sent to Mental Health NLP Agent: {OrchestratorConfig.NLP_AGENT_QUEUES['mental_health']}")
