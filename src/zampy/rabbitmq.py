"""
A class for working with RabbitMQ.
"""

import os
import textwrap
import pika
from dotenv import load_dotenv
from typing import Callable


class RabbitMQ:
    """Class for working with RabbitMQ."""

    def __init__(self):
        # Load environment variables from .env file if it exists
        path = os.getcwd() + "/.env"

        if os.path.isfile(path):
            load_dotenv(path)

        # If environment variables don't exist then use defaults from pika
        default_username = pika.ConnectionParameters.DEFAULT_USERNAME
        default_password = pika.ConnectionParameters.DEFAULT_PASSWORD
        default_host = pika.ConnectionParameters.DEFAULT_HOST
        default_port = pika.ConnectionParameters.DEFAULT_PORT

        self.username = os.getenv("RABBITMQ_USERNAME", default_username)
        self.password = os.getenv("RABBITMQ_PASSWORD", default_password)
        self.host = os.getenv("RABBITMQ_HOST", default_host)
        self.port = int(os.getenv("RABBITMQ_PORT", default_port))
        self.connection = None
        self.channel = None

    def show_config(self):
        """Show configuration."""
        config_description = f"""
        RabbitMQ configuration
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

    def publish(self, queue_name: str, body: str):
        """Publish a message"""
        if not self.channel:
            raise Exception("Connection is not established.")

        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=body)

        print(f"● Sent '{body}' to queue '{queue_name}'")

    def consume(self, queue_name: str, callback: Callable):
        """Consume messages."""
        if not self.channel:
            raise Exception("⃠ Connection is not established.")

        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("○ Waiting for sender. Press CTRL+C to exit.\n")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.close()
        print("\n● Stopped consuming and closed connection.")
