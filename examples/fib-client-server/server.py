"""Server to calculate Fibonacci numbers."""

import zampy


def main():
    """Run server."""
    server = zampy.FibServer()
    server.run_number()


if __name__ == "__main__":
    main()
