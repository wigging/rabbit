"""Class for sending messages."""

from .rabbitmq import RabbitMQ

class MessageSender:
    """A class to send messages."""

    def __init__(self, show_config=False):
        self.broker = RabbitMQ()

        if show_config:
            self.broker.show_config()

    def connect(self):
        """Connect to the RabbitMQ broker."""
        self.broker.connect()

    def close(self):
        """Close the connection."""
        self.broker.close()

    def send_message(self, msg: str):
        """Send a message."""
        self.broker.publish(queue_name="message", body=msg)

    def emit_message(self, msg: str):
        """Send message to all message receivers."""
        self.broker.publish_fanout(exchange="emit_message", body=msg)
