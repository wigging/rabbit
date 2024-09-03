"""Send messages to all consumers using exchange fanout."""

import rabbit


def main():
    """Send message to all consumers."""
    sender = rabbit.MessageSender()
    sender.connect()
    sender.emit_message("log message")
    sender.close()


if __name__ == "__main__":
    main()
