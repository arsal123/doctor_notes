import json
import uuid
import time
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.chat_bot import ChatBotAgent
from broker.broker import MessageBroker
from agents.consultation_orchestrator.config import OrchestratorConfig
from database.database import get_notes_from_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class TranscriptProcessingServer:
    def __init__(self):
        """Initialize Flask app and RabbitMQ brokers."""
        self.app = Flask(__name__)
        CORS(self.app)

        self.broker_for_send = MessageBroker()
        self.agent = ChatBotAgent()

        # Register routes
        self.app.add_url_rule("/process-transcript", "process_transcript", self.process_transcript, methods=["POST"])
        self.app.add_url_rule("/chat-agent", "chat_agent", self.chat_agent, methods=["POST"])

    def process_transcript(self):
        """Handles incoming transcript processing requests."""
        data = request.get_json()
        transcript = data.get("transcript")

        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400

        patient_id = str(uuid.uuid4())
        doctor_id = str(uuid.uuid4())
        correlation_id = patient_id + "-" + doctor_id
        consultation_type = "general_medicine"

        message = {
            "transcription": transcript,
            "metadata": {"patient_id": patient_id, "doctor_id": doctor_id, "consultation_type": consultation_type}
        }

        logger.info(f"Sending message to orchestrator: {correlation_id}")
        self.broker_for_send.send_message(OrchestratorConfig.RABBITMQ_QUEUE_INPUT, json.dumps(message))

        timeout = time.time() + 30  # Set timeout limit
        while time.time() < timeout:
            response = get_notes_from_db(patient_id, doctor_id)
            if response:
                return jsonify(response)
            time.sleep(0.5)  # Wait before checking again


        return jsonify({"error": "Processing timeout, please try again later"}), 504

    def chat_agent(self):
        data = request.get_json()
        user_message = data.get("message")
        patient_id = data.get("patient_id")

        print(f"Received user message: {user_message}")  # Debugging

        if not user_message:
            return jsonify({"reply": "Please ask a question."})

        ai_reply = self.agent.chat_with_bot(patient_id, user_message)

        print(f"AI Response: {ai_reply}")  # Debugging
        return jsonify({"reply": ai_reply})

        data = request.get_json()
        user_message = data.get("message")

        # Debugging - Print what is received from frontend
        print(f"Received user message: {user_message}")

        if not user_message:
            return jsonify({"reply": "Please ask a question."})

        ai_reply = agent.chat_with_bot(user_message)

        # Debugging - Print AI response
        print(f"AI Response: {ai_reply}")

        return jsonify({"reply": ai_reply})


    def run(self, port=5000):
        """Starts the Flask app."""
        logger.info("Starting Flask server...")
        self.app.run(debug=True, port=port, threaded=True)


if __name__ == "__main__":
    server = TranscriptProcessingServer()
    server.run()
