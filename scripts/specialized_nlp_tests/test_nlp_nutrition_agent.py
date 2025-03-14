import json
from broker.broker import MessageBroker
from agents.consultation_orchestrator.config import OrchestratorConfig

broker = MessageBroker()

test_message = {
    "transcription": "The patient has been skipping meals, eating junk food, and has gained weight recently.",
    "metadata": {"patient_id": "12345",
                 "doctor_id": "D5678",
                 "consultation_type": "general_medicine"
                 }
}

broker.send_message(OrchestratorConfig.NLP_AGENT_QUEUES['nutrition'], json.dumps(test_message))
print(f"Test message sent to Nutrition NLP Agent: {OrchestratorConfig.NLP_AGENT_QUEUES['nutrition']}")
