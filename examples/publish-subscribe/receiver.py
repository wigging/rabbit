"""Receive messages emitted from sender using exchange fanout."""

import rabbit


def main():
    """Receive messages."""
    receiver = rabbit.MessageReceiver()
    receiver.consume_emit()


if __name__ == "__main__":
    main()
