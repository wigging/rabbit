"""Send Python task to the receiver."""

import rabbit


def main():
    """Run Python task."""
    sender = rabbit.PythonSender()
    sender.connect()
    sender.run_task("longtask.py")
    sender.close()


if __name__ == "__main__":
    main()
