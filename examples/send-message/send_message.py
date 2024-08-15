"""
Send a message to the consumer.
"""

import zampy


def main():
    """Run client to send a message."""
    client = zampy.Client()
    client.send_message("hello there")


if __name__ == "__main__":
    main()
