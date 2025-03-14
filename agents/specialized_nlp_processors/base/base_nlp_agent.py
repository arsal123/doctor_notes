import json
import logging
from broker.broker import MessageBroker
from autogen import AssistantAgent
from agents.specialized_nlp_processors.config import NLPConfig

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class BaseNLPAgent:
    """Base class for NLP Agents analyzing medical transcriptions with follow-up support."""

    def __init__(self, agent_name, system_message, model_config, queue_name, nlp_type):
        """Initialize the NLP agent with specific configuration."""
        self.broker = MessageBroker()
        self.agent_name = agent_name
        self.queue_name = queue_name
        self.nlp_type = nlp_type

        self.nlp_assistant = AssistantAgent(
            name=agent_name,
            system_message=system_message,
            llm_config={"config_list": model_config, "seed": 42},
        )

    def handle_message(self, message):
        """Process an incoming transcription message from Consultation Orchestrator."""
        message_data = json.loads(message)
        is_follow_up = message_data.get("is_follow_up", False)
        if is_follow_up:
            self.process_follow_up_message(message_data)
        else:
            self.process_transcription_message(message_data)


    def process_transcription_message(self, message_data):
        transcription = message_data["transcription"]
        metadata = message_data.get("metadata", {})
        patient_id = metadata.get("patient_id")
        doctor_id = metadata.get("doctor_id")

        logger.info(f"Processing NLP for: {transcription}")

        # Analyze the transcription
        analysis_result = self.analyze_transcription(patient_id, doctor_id, transcription)

        response = {
            "nlp_type": self.nlp_type,
            "patient_id": metadata.get("patient_id"),
            "doctor_id": metadata.get("doctor_id"),
            "analysis_result": analysis_result
        }
        logger.info(response)
        # Send structured data back to the NOTES Generator
        self.broker.send_message(NLPConfig.RABBITMQ_QUEUE_OUTPUT, json.dumps(response))
        logger.info("NLP Analysis Sent.")

    def analyze_transcription(self, patient_id, doctor_id, transcription):
        """Analyze transcription and extract relevant medical insights."""
        reference_prompt = f"""
                You are assisting user ID: {patient_id} and doctor id: {doctor_id}. Provide responses accordingly.
                ### ** Expected Response Format (JSON)**
                DO NOT include any markdown formatting (such as ```json or ```). Only return a raw JSON object.
                our responses must strictly follow this JSON schema:
                {{
                    "symptoms_identified": ["List of extracted symptoms"],
                    "possible_conditions": ["List of potential conditions based on symptoms"],
                    "risk_factors": ["Identified risk factors (e.g., age, lifestyle, medical history)"],
                    "recommended_tests": ["Suggested diagnostic tests (e.g., blood tests, imaging, specialist consult)"],
                    "treatment_guidelines": ["General treatment recommendations (aligned with standard medical protocols)"],
                    "urgency_level": "Routine follow-up OR Immediate medical attention",
                    "lifestyle_recommendations": ["Advice related to diet, exercise, stress management, etc."],
                    "referral_suggestions": ["If needed, suggest referral to a specialist (e.g., cardiologist, neurologist)"],
                }}
                Target response length 100 words
        """
        messages = [{"content": reference_prompt, "role": "system"}, {"content": transcription, "role": "user"}]
        response = self.nlp_assistant.generate_reply(messages)
        logger.info(response)
        return json.loads(response)

    def process_follow_up_message(self, message_data):

        logger.info(f"Processing Follow up question by NLP for: {message_data}")
        question = message_data["question"]
        metadata = message_data.get("metadata", {})
        patient_id = metadata.get("patient_id")
        doctor_id = metadata.get("doctor_id")

        reference_prompt = f"""
            We previously discussed the transcript of a conversation between doctor {doctor_id} and patient {patient_id}. This is a follow-up question regarding the same transcript.
            You response shouldn't follow json for this follow-up question. Response should be short.
        """
        messages = [{"content": reference_prompt, "role": "system"}, {"content": question, "role": "user"}]
        response = self.nlp_assistant.generate_reply(messages=messages)
        logger.info(response)
        logger.info(f"Processing Follow up question by completed for {patient_id} and {doctor_id}.")


    def start(self):
        """Start listening for messages from Consultation Orchestrator."""
        logger.info(f"🩺 NLP Agent is listening on {self.queue_name}...")
        self.broker.consume_messages_real_time(self.queue_name, self.handle_message)
