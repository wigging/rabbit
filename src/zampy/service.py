"""
A service object for workstations or servers.
"""

from typing import Callable
from .rabbitmq import RabbitMQ


class Service:
    """Service class for workstation or server."""

    def __init__(self):
        broker = RabbitMQ()
        broker.connect()
        broker.show_config()
        self.broker = broker

    def consume_message(self, callback: Callable):
        """Consume messages from client."""
        self.broker.consume(queue_name="message", callback=callback)
