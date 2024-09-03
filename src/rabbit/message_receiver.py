"""Class for receiving messages."""

import pika
import textwrap
from typing import Callable
from .config import get_config


class MessageReceiver:
    """A class to receive messages."""

    def __init__(self):
        config = get_config()

        self.username = config["username"]
        self.password = config["password"]
        self.host = config["host"]
        self.port = config["port"]
        self.connection = None
        self.channel = None

        self._show_config()
        self._connect()

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

    def _connect(self):
        """Establish a connection."""
        creds = pika.PlainCredentials(self.username, self.password)
        params = pika.ConnectionParameters(credentials=creds)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

    def close(self):
        """Close the connection."""
        if self.connection and self.connection.is_open:
            self.connection.close()

    def consume(self):
        """Consume messages from sender."""
        if not self.channel:
            raise Exception("Uh oh! Connection is not established.")

        def callback(channel, method, properties, body):
            print(f"[.] Received message {body}")
            print("[x] Done\n")

        queue_name = "message"
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("[.] Waiting for sender. Press CTRL+C to exit.\n")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.close()
        print("\n[x] Stopped consuming and closed connection.")

    def consume_callback(self, callback: Callable):
        """Consume messages from sender using provided callback function."""
        if not self.channel:
            raise Exception("Uh oh! Connection is not established.")

        queue_name = "message"
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("[.] Waiting for sender. Press CTRL+C to exit.\n")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.close()
        print("\n[x] Stopped consuming and closed connection.")

    def consume_emit(self):
        """Consume messages from sender via exchange using fanout."""
        if not self.channel:
            raise Exception("Uh oh! Connection is not established.")

        def callback(channel, method, properties, body):
            print(f"[.] Received message {body}")
            print("[x] Done\n")

        exchange = "emit_message"
        self.channel.exchange_declare(exchange=exchange, exchange_type="fanout")

        result = self.channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=exchange, queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("[.] Waiting for sender. Press CTRL+C to exit.\n")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.close()
        print("\n[x] Stopped consuming and closed connection.")
