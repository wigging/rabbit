"""here."""

import pika
import uuid


class FibClient:
    """here."""

    def __init__(self):
        params = pika.ConnectionParameters(host="localhost")
        self.connection = pika.BlockingConnection(params)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

        self.response = None
        self.corr_id = None

    def on_response(self, channel, method, properties, body):
        """here."""
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call(self, n: int) -> int:
        """here."""
        print(f"[.] Requesting fib({n})")

        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange="",
            routing_key="rpc_queue",
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n),
        )

        while self.response is None:
            self.connection.process_data_events(time_limit=30)

        return int(self.response)
