"""Class for receiving Python commands."""

import pika
import textwrap
import subprocess
from .config import get_config


class PythonReceiver:
    """A class to receive Python commands."""

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
        """Consume Python commands from sender."""
        if not self.channel:
            raise Exception("Uh oh! Connection is not established.")

        def callback(channel, method, properties, body):
            cmd = body.decode().strip()
            print(f"[.] Run the Python command 'python {cmd}'")

            subprocess.run(["python", cmd])
            print("[x] Done\n")

        queue_name = "python"
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("[.] Waiting for sender. Press CTRL+C to exit.\n")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.close()
        print("\n[x] Stopped consuming and closed connection.")

    def consume_task(self):
        """Consume Python tasks from sender."""
        if not self.channel:
            raise Exception("Uh oh! Connection is not established.")

        def callback(channel, method, properties, body):
            cmd = body.decode().strip()
            print(f"[.] Run the Python task 'python {cmd}'")

            subprocess.run(["python", cmd])
            print("[x] Done\n")

            channel.basic_ack(delivery_tag=method.delivery_tag)

        queue_name = "python_task"
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        print("[.] Waiting for sender. Press CTRL+C to exit.\n")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.close()
        print("\n[x] Stopped consuming and closed connection.")
