"""Receive messages from the sender."""

import rabbit


def example1():
    """Consume messages with default callback."""
    receiver = rabbit.MessageReceiver()
    receiver.consume()


def example2():
    """Consume messages with user defined callback function."""

    def callback(channel, method, properties, body):
        msg = body.decode().strip()
        print(f"○ Received message '{msg}' from sender. Woo hoo!")
        print("● Completed\n")

    receiver = rabbit.MessageReceiver()
    receiver.consume_callback(callback)


def main():
    """Run an example."""

    # example1()
    example2()


if __name__ == "__main__":
    main()
