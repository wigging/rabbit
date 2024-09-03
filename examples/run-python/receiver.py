"""Run a Python commands received from sender."""

import rabbit


def main():
    """Run Python commands."""
    receiver = rabbit.PythonReceiver()
    receiver.consume()


if __name__ == "__main__":
    main()
