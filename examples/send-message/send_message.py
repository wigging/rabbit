"""
Send a message to the consumer.
"""

import zampy


def main():
    """Run client to send a message."""
    client = zampy.Client()
    client.connect()
    client.send_message("hello there")
    client.close()


if __name__ == "__main__":
    main()
