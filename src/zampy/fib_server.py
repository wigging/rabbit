"""Server class."""

import pika


def fib(n: int) -> int:
    """Calculate a Fibonacci number.

    This function deliberately runs slow so keep `n` below 40.
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


class FibServer:
    """Server that calculates Fibonacci numbers."""

    def __init__(self):
        self.params = pika.ConnectionParameters(host="localhost")

    def _callback_number(self, channel, method, properties, body):
        """Callback function used by run_number function."""
        n = int(body)

        print(f"[.] Run fib({n})")
        response = fib(n)
        print("[.] Result is", response)

        channel.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=str(response),
        )

        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run_number(self):
        """Run server for calculating Fibonacci number."""
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="rpc_queue")

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue="rpc_queue", on_message_callback=self._callback_number)
        print("[.] Awaiting client number requests")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        if self.connection.is_open:
            self.connection.close()
            print("\n[x] Stopped consuming and closed connection.")

    def _callback_even_odd(self, channel, method, properties, body):
        """here."""
        n = int(body)

        print(f"[.] Analyze number {n}")
        if n % 2 == 0:
            response = "even"
        else:
            response = "odd"
        print("[.] Result is", response)

        channel.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=response,
        )

        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run_even_odd(self):
        """Run server to determine if number is even or odd."""
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="rpc_queue2")

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue="rpc_queue2", on_message_callback=self._callback_even_odd)
        print("[.] Awaiting client even/odd requests")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        if self.connection.is_open:
            self.connection.close()
            print("\n[x] Stopped consuming and closed connection.")
