"""Server class for calculating Fibonacci numbers."""

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
        params = pika.ConnectionParameters(host="localhost")
        self.connection = pika.BlockingConnection(params)

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="rpc_queue")

    def run(self):
        """Run the server."""

        def on_request(channel, method, properties, body):
            """Handle request and publish response."""
            n = int(body)

            print(f"[.] Run fib({n})")
            response = fib(n)

            channel.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=str(response),
            )

            channel.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue="rpc_queue", on_message_callback=on_request)

        print("[.] Awaiting RPC requests")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        if self.connection.is_open:
            self.connection.close()
            print("\n[x] Stopped consuming and closed connection.")
