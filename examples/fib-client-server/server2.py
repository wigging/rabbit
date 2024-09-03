"""Server to analyze Fibonacci numbers."""

import rabbit


def main():
    """Run server."""
    server = rabbit.FibServer()
    server.run_even_odd()


if __name__ == "__main__":
    main()
