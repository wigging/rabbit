"""Run Python tasks received from sender."""

import rabbit


def main():
    """Run Python tasks."""
    receiver = rabbit.PythonReceiver()
    receiver.consume_task()


if __name__ == "__main__":
    main()
