"""Server to analyze Fibonacci numbers."""

import zampy


def main():
    """Run server."""
    server = zampy.FibServer()
    server.run_even_odd()


if __name__ == "__main__":
    main()
