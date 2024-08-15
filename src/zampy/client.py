"""
A client object for users.
"""

from .rabbitmq import RabbitMQ


class Client:
    """Client class for users."""

    def __init__(self):
        broker = RabbitMQ()
        broker.connect()
        broker.show_config()
        self.broker = broker

    def send_message(self, msg: str):
        """Send a message."""
        self.broker.publish(msg)

    def send_command(self, cmd: str):
        """Send a shell command."""
        ...
