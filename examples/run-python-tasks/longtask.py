"""A Python script that represents a long running task."""

import time


def main():
    """Run a task for five seconds."""
    print("Running a task...")
    time.sleep(5)
    print("Task is done.")


if __name__ == "__main__":
    main()
