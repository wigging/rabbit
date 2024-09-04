"""Class for sending Python commands."""

import pika
import textwrap
from .config import get_config

class PythonSender:
    """A class to send Python commands."""

    def __init__(self, show_config=False):
        config = get_config()

        self.username = config["username"]
        self.password = config["password"]
        self.host = config["host"]
        self.port = config["port"]
        self.connection = None
        self.channel = None

        if show_config:
            self._show_config()

    def _show_config(self):
        """Show configuration."""
        config_description = f"""
        Configuration for RabbitMQ is the following:
        username    {self.username}
        password    {self.password}
        host        {self.host}
        port        {self.port}
        """

        print(textwrap.dedent(config_description))

    def connect(self):
        """Connect to the RabbitMQ broker."""
        creds = pika.PlainCredentials(self.username, self.password)
        params = pika.ConnectionParameters(credentials=creds)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

    def close(self):
        """Close the RabbitMQ broker connection."""
        if self.connection and self.connection.is_open:
            self.connection.close()

    def run_command(self, cmd: str):
        """Run a Python command."""
        if not self.channel:
            raise Exception("Uh oh! Connection is not established.")

        queue_name = "python"
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=cmd)

        print(f"[x] Sent '{cmd}' to queue '{queue_name}'")

    def run_task(self, task: str):
        """Run a Python task using a durable queue."""
        if not self.channel:
            raise Exception("Uh oh! Connection is not established.")

        queue_name = "python_task"
        self.channel.queue_declare(queue=queue_name, durable=True)

        props = pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=task, properties=props)

        print(f"[x] Sent '{task}' to durable queue '{queue_name}'")
