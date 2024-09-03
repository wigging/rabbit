"""A class for working with RabbitMQ."""

import textwrap
import pika
from typing import Callable
from .config import get_config


class RabbitMQ:
    """Class for working with RabbitMQ."""

    def __init__(self):
        config = get_config()

        self.username = config["username"]
        self.password = config["password"]
        self.host = config["host"]
        self.port = config["port"]
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
        """Publish a message."""
        if not self.channel:
            raise Exception("Connection is not established.")

        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=body)

        print(f"● Sent '{body}' to queue '{queue_name}'")

    def publish_durable(self, queue_name: str, body: str):
        """Publish a message using a durable queue."""
        if not self.channel:
            raise Exception("Connection is not established.")

        self.channel.queue_declare(queue=queue_name, durable=True)

        props = pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=body, properties=props)

        print(f"● Sent '{body}' to durable queue '{queue_name}'")

    def publish_fanout(self, exchange: str, body: str):
        """Publish a message to an exchange using fanout."""
        if not self.channel:
            raise Exception("Connection is not established.")

        self.channel.exchange_declare(exchange=exchange, exchange_type="fanout")
        self.channel.basic_publish(exchange=exchange, routing_key="", body=body)

        print(f"● Sent '{body}' to exchange '{exchange}'")

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

    def consume_durable(self, queue_name: str, callback: Callable):
        """Consume messages using durable queue."""
        if not self.channel:
            raise Exception("⃠ Connection is not established.")

        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        print("○ Waiting for sender. Press CTRL+C to exit.\n")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.close()
        print("\n● Stopped consuming and closed connection.")

    def consume_fanout(self, exchange: str, callback: Callable):
        """Consume messages from exchange using fanout."""
        if not self.channel:
            raise Exception("⃠ Connection is not established.")

        self.channel.exchange_declare(exchange=exchange, exchange_type="fanout")

        result = self.channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=exchange, queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("○ Waiting for sender. Press CTRL+C to exit.\n")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.close()
        print("\n● Stopped consuming and closed connection.")
