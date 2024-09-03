"""Class for receiving Python commands."""

import subprocess
from .rabbitmq import RabbitMQ


class PythonReceiver:
    """A class to receive Python commands."""

    def __init__(self):
        broker = RabbitMQ()
        broker.connect()
        broker.show_config()
        self.broker = broker

    def consume(self):
        """Run Python commands from sender."""

        def callback(channel, method, properties, body):
            cmd = body.decode().strip()
            print(f"○ Run the Python command 'python {cmd}'")

            subprocess.run(["python", cmd])
            print("● Done\n")

        self.broker.consume(queue_name="python", callback=callback)

    def consume_task(self):
        """Run Python tasks from sender."""

        def callback(channel, method, properties, body):
            cmd = body.decode().strip()
            print(f"○ Run the Python task 'python {cmd}'")

            subprocess.run(["python", cmd])
            print("● Done\n")

            channel.basic_ack(delivery_tag=method.delivery_tag)

        self.broker.consume_durable(queue_name="python_task", callback=callback)
