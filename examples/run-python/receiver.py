"""Run a Python script using script name sent from client."""

import zampy


def main():
    """Run Python script."""
    receiver = zampy.PythonReceiver()
    receiver.run_script()


if __name__ == "__main__":
    main()
