"""Run Python tasks received from sender."""

import zampy


def main():
    """Run Python tasks."""
    receiver = zampy.PythonReceiver()
    receiver.consume_task()


if __name__ == "__main__":
    main()
