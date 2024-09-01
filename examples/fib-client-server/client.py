"""Example of calculating Fibonacci numbers.

The `server.py` and `server2.py` must be running in separate terminal sessions
before running this example.

Number 35 takes a while to compute so good for a long running task.
Number 18 gives an even analysis result.
"""

import zampy


def main():
    """Run the client."""
    n = 35

    client = zampy.FibClient()
    response = client.request_number(n)
    print(f"[x] Got {response}")

    response2 = client.request_evenodd(response)
    print(f"[x] Got {response2}")


if __name__ == "__main__":
    main()
