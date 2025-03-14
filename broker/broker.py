import os
import yaml
import pika
import time
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load static configuration from config.yaml
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Retrieve RabbitMQ credentials from .env
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

# Retrieve static settings from config.yaml
EXCHANGE_NAME = config["rabbitmq"]["exchange"]
QUEUE_NAMES = config["rabbitmq"]["queues"]
LOG_LEVEL = config["logging"]["level"].upper()

# Initialize logging
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MessageBroker:
    def __init__(self):
        """Initialize connection to RabbitMQ."""
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """Establish connection with RabbitMQ and handle disconnections."""
        while True:
            try:
                credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=RABBITMQ_HOST,
                        port=RABBITMQ_PORT,
                        credentials=credentials,
                        heartbeat=0,  # 🔥 Prevent RabbitMQ from closing idle connections
                        blocked_connection_timeout=None,  # 🔥 Prevent indefinite blocking
                        client_properties={"connection_name": "persistent_python_client"}
                    )
                )
                self.channel = self.connection.channel()
                self.channel.confirm_delivery()  # Enable publisher confirms
                logger.info("✅ Persistent connection to RabbitMQ established successfully.")
                break  # Exit loop if connection is successful

            except Exception as e:
                logger.error(f"❌ Failed to connect to RabbitMQ: {e}. Retrying in 5 seconds...")
                time.sleep(5)  # Wait before retrying

    def is_connection_open(self):
        """Check if RabbitMQ connection is still alive."""
        return (
                self.connection is not None and
                self.channel is not None and
                self.connection.is_open and
                self.channel.is_open
        )

    def declare_queue(self, queue_name):
        """Declare a queue if it doesn't exist."""
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
        except Exception as e:
            logger.error(f"Error declaring queue {queue_name}: {e}")

    def send_message(self, queue_name, message):
        """Send a message to a queue."""
        try:
            if not self.is_connection_open():
                logger.warning("⚠️ Connection closed. Reconnecting before sending message.")
                self.connect()  # Ensure connection is active

            self.declare_queue(queue_name)
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
            )
            logger.info(f"Message sent to {queue_name}: {message}")
        except Exception as e:
            logger.error(f"Failed to send message to {queue_name}: {e}")

    def consume_messages_real_time(self, queue_name, callback):
        """Continuously listen for messages and process them in real-time (for STT, NLP)."""
        try:
            if not self.is_connection_open():
                logger.warning("⚠️ Connection lost. Reconnecting for message consumption.")
                self.connect()

            self.declare_queue(queue_name)

            def wrapper(ch, method, properties, body):
                callback(body.decode())  # Process message
                ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

            self.channel.basic_consume(queue=queue_name, on_message_callback=wrapper)
            logger.info(f"[*] Listening on queue: {queue_name}")
            self.channel.start_consuming()  # Continuous message listening
        except Exception as e:
            logger.error(f"Error consuming messages from {queue_name}: {e}")

    def consume_message_on_demand(self, queue_name, callback):
        """Fetch a single message from a queue without blocking (for Orchestrator, Medical History)."""
        try:
            if not self.is_connection_open():
                logger.warning("⚠️ Connection lost. Reconnecting for message consumption.")
                self.connect()

            self.declare_queue(queue_name)
            method_frame, header_frame, body = self.channel.basic_get(queue=queue_name)

            if method_frame:
                callback(body.decode())  # Process message
                self.channel.basic_ack(method_frame.delivery_tag)  # Acknowledge message
                return True
            else:
                return False  # No message in queue
        except Exception as e:
            logger.error(f"Error consuming messages from {queue_name}: {e}")
            return False
