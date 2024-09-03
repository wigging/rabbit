"""Class for sending messages."""

import pika
import textwrap
from .config import get_config


class MessageSender:
    """A class to send messages."""

    def __init__(self, show_config=False):
        config = get_config()

        self.username = config["username"]
        self.password = config["password"]
        self.host = config["host"]
        self.port = config["port"]
        self.connection = None
        self.channel = None

        if show_config:
            self.show_config()

    def show_config(self):
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
        """Establish a connection."""
        creds = pika.PlainCredentials(self.username, self.password)
        params = pika.ConnectionParameters(credentials=creds)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

    def close(self):
        """Close the connection."""
        if self.connection and self.connection.is_open:
            self.connection.close()

    def send_message(self, msg: str):
        """Send a message via publish method."""
        if not self.channel:
            raise Exception("Uh oh! Connection is not established.")

        queue_name = "message"
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=msg)

        print(f"[x] Sent '{msg}' to queue '{queue_name}'")

    def emit_message(self, msg: str):
        """Send message to all message receivers via exchange using fanout."""
        if not self.channel:
            raise Exception("Uh oh! Connection is not established.")

        exchange = "emit_message"
        self.channel.exchange_declare(exchange=exchange, exchange_type="fanout")
        self.channel.basic_publish(exchange=exchange, routing_key="", body=msg)

        print(f"[x] Sent '{msg}' to exchange '{exchange}'")
