"""Server to calculate Fibonacci numbers."""

import rabbit


def main():
    """Run server."""
    server = rabbit.FibServer()
    server.run_number()


if __name__ == "__main__":
    main()
