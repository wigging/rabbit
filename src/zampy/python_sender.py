"""Class for sending Python script names."""

from .rabbitmq import RabbitMQ


class PythonSender:
    """A class to send Python script names."""

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

    def run_script(self, name: str):
        """Run a Python script using the provided script name."""
        self.broker.publish(queue_name="python", body=name)
