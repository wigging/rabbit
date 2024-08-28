"""Send Python task to the receiver."""

import zampy


def main():
    """Run Python task."""
    sender = zampy.PythonSender()
    sender.connect()
    sender.run_task("longtask.py")
    sender.close()


if __name__ == "__main__":
    main()
