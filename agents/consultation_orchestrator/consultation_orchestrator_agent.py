import json
import logging
import os
import openai

from broker.broker import MessageBroker
from agents.consultation_orchestrator.config import OrchestratorConfig
from agents.notes_generator.config import NotesConfig
import autogen

# Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
models_config_list = [{"model": "gpt-4o-mini-2024-07-18", "api_key": OPEN_AI_API_KEY}]

class ConsultationOrchestrator:
    """Orchestrates consultations by routing transcriptions to the right agents."""
    # print('Here is the open api key', OPEN_API_KEY)
    # openai.api_key = OPEN_AI_API_KEY
    main_doc_llm_config = {
        "config_list": models_config_list,
        "timeout": 120,
    }

    main_doctor = None

    def init_main_doctor_agent(self):
        self.main_doctor = autogen.AssistantAgent(
            name="MainDoctor",
            llm_config=self.main_doc_llm_config,
            system_message="""
                You are a general AI doctor. Your job is to analyze patient transcripts 
                and decide which specialists (Mental Health, General Medicine, Nutrition) should review the case. 
                Respond ONLY with a comma-separated list of required specialists.
            """,
        )

    def __init__(self):
        """Initialize Message Broker and Configurations."""
        self.broker = MessageBroker()
        self.init_main_doctor_agent()

    def analyse_transcript_and_specify_agents(self, transcription, consultation_type):
        """Analyze the transcription and specify the agents to consult."""
        llm_recommend_agents = self.main_doctor.generate_reply(messages=[{"content": transcription,
                                              "role": "user"
                                              }]).split(',')
        agents_dict = {
            "Mental Health": "mental_health",
            "General Medicine": "general_medicine",
            "Nutrition": "nutrition"
        }

        agents_queue = set()

        if consultation_type in OrchestratorConfig.NLP_AGENT_QUEUES:
            agents_queue.add(OrchestratorConfig.NLP_AGENT_QUEUES.get(consultation_type))


        for k in llm_recommend_agents:
            if k in agents_dict:
                print(f"Agent {agents_dict[k]} is recommended")
                agents_queue.add(OrchestratorConfig.NLP_AGENT_QUEUES.get(agents_dict[k]))

        return agents_queue

    def auto_process_transcription(self, message): # noqa: C901
        """Handle transcription and determine next steps."""
        message_data = json.loads(message)
        transcription = message_data["transcription"]
        metadata = message_data.get("metadata", {})

        """Process transcription and notify NLP agents + Notes Generator."""
        patient_id = metadata.get("patient_id", "unknown")
        doctor_id = metadata.get("doctor_id", "unknown")
        consultation_type = metadata.get("consultation_type", "general_medicine").lower()

        logger.info(f"Processing transcription for patient: {patient_id}")

        # Analyse the transcript and specify the agents to consult
        agents_queue = self.analyse_transcript_and_specify_agents(transcription, consultation_type)

        # Send messages to NLP agents
        for nlp_queue in agents_queue:
            if nlp_queue:
                self.send_to_nlp_agent(nlp_queue, transcription, metadata)

    #   Last part for notes
        notes_event = {
            "event_type": "nlp_processing_started",
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "transcription": transcription,
            "metadata": metadata,
            "expected_agents": sorted(list(agents_queue))
        }
        self.broker.send_message(NotesConfig.RABBITMQ_QUEUE_INPUT, json.dumps(notes_event, sort_keys=True))

        logger.info("NLP Processing Started Notification Sent to Notes Generator.")
        # Send transcription to Notes Generator


    def send_to_nlp_agent(self, queue_name, transcription, metadata):
        """Send transcription data to a specific NLP agent."""
        message = json.dumps({
            "request_type": "nlp_analysis",
            "transcription": transcription,
            "metadata": metadata
        })
        logger.info(f"Sending to NLP Agent: {queue_name}")
        self.broker.send_message(queue_name, message)

    # def send_to_medical_history_agent(self, metadata):
    #     """Request medical history for the patient."""
    #     message = json.dumps({
    #         "request_type": "medical_history",
    #         "patient_id": metadata["patient_id"]
    #     })
    #     logger.info(f"Requesting medical history for patient {metadata['patient_id']}")
    #     self.broker.send_message(OrchestratorConfig.MEDICAL_HISTORY_QUEUE, message)

    def start(self):
        """Start listening for messages from RabbitMQ."""
        logger.info("Consultation Orchestrator is listening for messages...")
        self.broker.consume_messages_real_time(
            OrchestratorConfig.RABBITMQ_QUEUE_INPUT, self.auto_process_transcription
        )

if __name__ == "__main__":
    orchestrator = ConsultationOrchestrator()
    orchestrator.start()
