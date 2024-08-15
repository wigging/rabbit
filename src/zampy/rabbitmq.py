"""
A class for working with RabbitMQ.
"""

import os
import textwrap
import pika
from dotenv import load_dotenv


class RabbitMQ:
    """Class for working with RabbitMQ"""

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
        self.channel = None

    def show_config(self):
        """Show configuration"""
        config_description = f"""
        RabbitMQ configuration
        username    {self.username}
        password    {self.password}
        host        {self.host}
        port        {self.port}
        """

        print(textwrap.dedent(config_description))

    def connect(self):
        """Establish a connection"""
        creds = pika.PlainCredentials(self.username, self.password)
        params = pika.ConnectionParameters(credentials=creds)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()

    def publish(self, body: str):
        """Publish as message"""
        if not self.channel:
            raise Exception("Connection is not established.")

        self.channel.queue_declare(queue="hello")
        self.channel.basic_publish(exchange="", routing_key="hello", body="date")

        print("[x] Sent the 'date' command")
