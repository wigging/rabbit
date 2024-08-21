"""Class for receiving messages."""

from typing import Callable
from .rabbitmq import RabbitMQ


class MessageReceiver:
    """A class to receive messages."""

    def __init__(self):
        broker = RabbitMQ()
        broker.connect()
        broker.show_config()
        self.broker = broker

    def consume(self):
        """Consume messages from sender."""

        def callback(channel, method, properties, body):
            print(f"[*] Received message {body}")
            print("[x] Done\n")

        self.broker.consume(queue_name="message", callback=callback)

    def consume_callback(self, callback: Callable):
        """Consume messages from sender using provided callback function."""
        self.broker.consume(queue_name="message", callback=callback)