"""
A client object for users.
"""

from .rabbitmq import RabbitMQ


class Client:
    """Client class for users."""

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

    def run_python_script(self, script: str):
        """Run a python script."""
        self.broker.publish(queue_name="python", body=script)
