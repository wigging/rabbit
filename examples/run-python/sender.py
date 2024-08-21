"""Send name of Python script to the receiver."""

import zampy


def main():
    """Run Python script."""
    sender = zampy.PythonSender()
    sender.connect()
    sender.run_command("--version")
    sender.run_command("hello.py")
    sender.close()


if __name__ == "__main__":
    main()
