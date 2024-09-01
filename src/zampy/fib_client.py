"""Client class."""

import pika
import uuid


class FibClient:
    """Client for Fibonacci numbers."""

    def __init__(self):
        params = pika.ConnectionParameters(host="localhost")
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        self.number_queue = "fib_number"
        self.evenodd_queue = "fib_evenodd"

        self.corr_id = str(uuid.uuid4())
        self.corr_id2 = str(uuid.uuid4())

        self.response = None
        self.response2 = None

    def _callback_number(self, channel, method, properties, body):
        """Callback function used by the _consume_number function."""
        if self.corr_id == properties.correlation_id:
            self.response = body

    def _consume_number(self):
        """Consume for a Fibonacci number."""
        self.channel.queue_declare(queue=self.number_queue, exclusive=True)

        self.channel.basic_consume(
            queue=self.number_queue,
            on_message_callback=self._callback_number,
            auto_ack=True,
        )

    def request_number(self, n: int) -> int:
        """Request a Fibonacci number from server."""
        self._consume_number()
        print(f"[.] Requesting fib({n})")

        self.channel.basic_publish(
            exchange="",
            routing_key="rpc_queue",
            properties=pika.BasicProperties(
                reply_to=self.number_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n),
        )

        while self.response is None:
            self.connection.process_data_events(time_limit=30)

        return int(self.response)

    def _callback_evenodd(self, channel, method, properties, body):
        """Callback function used by the _consume_evenodd function."""
        if self.corr_id2 == properties.correlation_id:
            self.response2 = body

    def _consume_evenodd(self):
        """Consume for even/odd analysis of a Fibonacci number."""
        self.channel.queue_declare(queue=self.evenodd_queue, exclusive=True)

        self.channel.basic_consume(
            queue=self.evenodd_queue,
            on_message_callback=self._callback_evenodd,
            auto_ack=True,
        )

    def request_evenodd(self, n: int) -> str:
        """Request even/odd analysis of Fibonacci number from server."""
        self._consume_evenodd()
        print(f"[.] Requesting even/odd analysis of {n}")

        self.channel.basic_publish(
            exchange="",
            routing_key="rpc_queue2",
            properties=pika.BasicProperties(
                reply_to=self.evenodd_queue,
                correlation_id=self.corr_id2,
            ),
            body=str(n),
        )

        while self.response2 is None:
            self.connection.process_data_events(time_limit=30)

        return self.response2.decode('ascii')
