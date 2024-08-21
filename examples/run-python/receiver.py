"""Run a Python commands received from sender."""

import zampy


def main():
    """Run Python commands."""
    receiver = zampy.PythonReceiver()
    receiver.consume()


if __name__ == "__main__":
    main()
