"""
Consume messages from the sender.
"""

import zampy


def callback(ch, method, properties, body):
    print(f"[*] Received message {body}")
    print("[x] Done\n")


def main():
    """Run service to consume messages."""
    service = zampy.RabbitMQ()
    service.connect()
    service.show_config()
    service.consume(callback)


if __name__ == "__main__":
    main()
