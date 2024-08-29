"""Receive messages emitted from sender using exchange fanout."""

import zampy


def main():
    """Receive messages."""
    receiver = zampy.MessageReceiver()
    receiver.consume_emit()


if __name__ == "__main__":
    main()
