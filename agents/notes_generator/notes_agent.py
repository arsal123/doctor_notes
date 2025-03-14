import json
import logging
from autogen import AssistantAgent
from broker.broker import MessageBroker
from agents.notes_generator.config import NotesConfig
import os
from dotenv import load_dotenv
from database.database import save_notes_to_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
model_config = [{"model": "gpt-4o-mini-2024-07-18", "api_key": OPEN_AI_API_KEY}]

class NotesGenerator:
    """Generates final consultation notes after all NLP agents finish processing."""

    def __init__(self):
        """Initialize Notes Generator and connect to the message broker."""
        self.broker = MessageBroker()
        self.pending_cases = {}  # Stores NLP responses until all agents complete
        self.unregistered_nlp_results = {}  # Buffer for NLP results received before init event
        self.nlp_assistant = AssistantAgent(
            name="NotesGeneratorAgent",
            system_message="""
                You are medicine notes generator. You will be responsible for generating summary based on conversation transcript between doctor and patient. 
            """,
            llm_config={"config_list": model_config, "seed": 42},
        )

    def process_nlp_result(self, message_data):
        """Store NLP analysis result and check if all responses are received."""
        patient_id = message_data.get("patient_id", "unknown")
        doctor_id = message_data.get("doctor_id", "unknown")
        key = f"{patient_id}-{doctor_id}"

        if key not in self.pending_cases:
            logger.warning(f"No active case found for {key}. Buffering NLP result.")
            if key not in self.unregistered_nlp_results:
                self.unregistered_nlp_results[key] = []
            self.unregistered_nlp_results[key].append(message_data)
            return

        # Store NLP analysis results
        self.pending_cases[key]["nlp_results"].append(message_data)

        # Check if all expected NLP agents have responded
        expected_agents = set(self.pending_cases[key]["expected_agents"])
        received_agents = {result["nlp_type"] for result in self.pending_cases[key]["nlp_results"]}

        if received_agents == expected_agents:
            logger.info(f"All NLP results received for {key}. Generating final notes.")
            self.generate_notes(self.pending_cases.pop(key))  # Remove case and generate notes

    def process_nlp_start_event(self, message_data):
        """Initialize tracking for a new consultation session."""
        patient_id = message_data.get("patient_id", "unknown")
        doctor_id = message_data.get("doctor_id", "unknown")
        key = f"{patient_id}-{doctor_id}"

        self.pending_cases[key] = {
            "transcription": message_data["transcription"],
            "metadata": message_data["metadata"],
            "expected_agents": sorted(list(message_data["expected_agents"])),
            "nlp_results": []
        }

        logger.info(f"Notes tracking started for {key}. Waiting for NLP results.")

        # Process any buffered NLP messages for this patient
        if key in self.unregistered_nlp_results:
            for buffered_message in self.unregistered_nlp_results.pop(key):
                logger.info(f"Processing buffered NLP message for {key}")
                self.process_nlp_result(buffered_message)

    def generate_notes(self, case_data):
        """Generate structured notes document once all NLP agents complete processing."""
        patient_id = case_data["metadata"]["patient_id"]
        doctor_id = case_data["metadata"]["doctor_id"]

        transcription = case_data["transcription"]
        nlp_results = case_data["nlp_results"]

        # Merge NLP results
        # analysis_summary = {result["nlp_type"]: result["analysis_result"] for result in nlp_results}

        transcription_summary = self.nlp_assistant.generate_reply(messages=[{"content": transcription,
                                                                             "role": "user"
                                                                             }])

        # Example structured document
        notes_document = {
            "transcription_summary": transcription_summary,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "transcription": transcription,
            "analysis_summary": nlp_results
        }

        # Send structured notes to the final storage system
        # self.broker.send_message(NotesConfig.RABBITMQ_QUEUE_OUTPUT, json.dumps(notes_document))
        save_notes_to_db(patient_id, doctor_id, transcription, nlp_results, transcription_summary)

        logger.info(f"Final Consultation Notes Saved for Patient: {patient_id} and Doctor: {doctor_id}")



    def handle_message(self, message):
        """Route messages based on event type."""
        message_data = json.loads(message)

        if message_data.get("event_type") == "nlp_processing_started":
            self.process_nlp_start_event(message_data)
        else:
            self.process_nlp_result(message_data)

    def start(self):
        """Start listening for messages from NLP Agents & Consultation Orchestrator."""
        logger.info(f"📄 Notes Generator is listening on {NotesConfig.RABBITMQ_QUEUE_INPUT}...")
        self.broker.consume_messages_real_time(NotesConfig.RABBITMQ_QUEUE_INPUT, self.handle_message)


if __name__ == "__main__":
    agent = NotesGenerator()
    agent.start()
