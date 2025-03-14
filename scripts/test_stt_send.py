import json
import sys
import os

# Ensure we can import from the main directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from broker.broker import MessageBroker

broker = MessageBroker()

test_message = {
    "audio_path": "/Users/egor.krylovich/workspace/multiagent-medical-system/data/sample_audio/integration_test/triggers_all_agents.wav",
    "metadata": {"patient_id": "12345",
                 "doctor_id": "D5678",
                 "consultation_type": "general_medicine"
                 }
}

broker.send_message("stt_processor_queue", json.dumps(test_message))
print("Test audio message sent to STT queue.")
