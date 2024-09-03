"""Send messages to the receiver."""

import rabbit


def main():
    """Send some messages."""
    sender = rabbit.MessageSender()
    sender.connect()
    sender.send_message("hello there")
    sender.close()

    sender.connect()
    for i in range(5):
        sender.send_message(f"count is {i}")
    sender.close()


if __name__ == "__main__":
    main()
