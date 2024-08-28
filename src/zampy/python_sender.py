"""Class for sending Python commands."""

from .rabbitmq import RabbitMQ


class PythonSender:
    """A class to send Python commands."""

    def __init__(self, show_config=False):
        self.broker = RabbitMQ()

        if show_config:
            self.broker.show_config()

    def connect(self):
        """Connect to the RabbitMQ broker."""
        self.broker.connect()

    def close(self):
        """Close the RabbitMQ broker connection."""
        self.broker.close()

    def run_command(self, cmd: str):
        """Run a Python command."""
        self.broker.publish(queue_name="python", body=cmd)

    def run_task(self, task: str):
        """Run a Python task."""
        self.broker.publish_durable(queue_name="python_task", body=task)
