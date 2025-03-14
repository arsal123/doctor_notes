import unittest
import json
import time
from broker.broker import MessageBroker

class TestMessageBroker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.broker = MessageBroker()
        cls.test_queue = "test_queue"
        cls.broker.channel.queue_purge(cls.test_queue)

    def test_send_message(self):
        """Test sending a message to RabbitMQ."""
        test_message = {"message": "Hello, Multi-Agent System!"}
        try:
            self.broker.send_message(self.test_queue, json.dumps(test_message))
            self.assertTrue(True)  # Passes if no exception occurs
        except Exception as e:
            self.fail(f"send_message failed with exception: {e}")

    def test_consume_message_on_demand(self):
        """Test consuming a message on-demand (non-blocking)."""
        received_messages = []

        def callback(message):
            received_messages.append(json.loads(message))

        test_message = {"message": "Testing On-Demand Consumer"}
        self.broker.send_message(self.test_queue, json.dumps(test_message))

        # Wait briefly to ensure the message is processed
        time.sleep(1)

        # Try consuming the message
        success = self.broker.consume_message_on_demand(self.test_queue, callback)

        self.assertTrue(success, "No message was received from the queue.")
        self.assertEqual(len(received_messages), 1)
        self.assertEqual(received_messages[0]["message"], "Testing On-Demand Consumer")

    def test_consume_messages_real_time(self):
        """Test real-time message consumption (only process one message for test)."""
        received_messages = []

        def callback(message):
            received_messages.append(json.loads(message))
            self.broker.channel.stop_consuming()  # Stop after receiving one message

        test_message = {"message": "Testing Real-Time Consumer"}
        self.broker.send_message(self.test_queue, json.dumps(test_message))

        # Consume message in real-time (this should not block forever)
        self.broker.consume_messages_real_time(self.test_queue, callback)

        self.assertEqual(len(received_messages), 1)
        self.assertEqual(received_messages[0]["message"], "Testing Real-Time Consumer")

if __name__ == "__main__":
    unittest.main()
