"""
Consume messages from the sender.
"""

import zampy


def callback(ch, method, properties, body):
    print(f"[*] Received message {body}")
    print("[x] Done\n")


def main():
    """Run service to consume messages."""
    service = zampy.Service()
    service.consume_message(callback=callback)


if __name__ == "__main__":
    main()
