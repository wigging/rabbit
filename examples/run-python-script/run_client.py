"""
Send name of Python script to the service.
"""

import zampy


def main():
    """Run client to send name of Python script."""
    client = zampy.Client()
    client.connect()
    client.run_python_script("sayhello.py")
    client.close()


if __name__ == "__main__":
    main()
