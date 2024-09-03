"""Send name of Python script to the receiver."""

import rabbit


def main():
    """Run Python script."""
    sender = rabbit.PythonSender()
    sender.connect()
    sender.run_command("--version")
    sender.run_command("hello.py")
    sender.close()


if __name__ == "__main__":
    main()
