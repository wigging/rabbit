"""Class for receiving Python script names."""

import subprocess
from .rabbitmq import RabbitMQ


class PythonReceiver:
    """A class to receive Python script names."""

    def __init__(self):
        broker = RabbitMQ()
        broker.connect()
        broker.show_config()
        self.broker = broker

    def run_script(self):
        """Run a Python script using script name from sender."""

        def callback(channel, method, properties, body):
            script = body.decode().strip()
            print(f"[*] Run the Python script '{script}'")

            subprocess.run(["python", script])
            print("[x] Done\n")

        self.broker.consume(queue_name="python", callback=callback)
