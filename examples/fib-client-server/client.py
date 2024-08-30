"""here."""

import zampy


def main():
    """here."""
    client = zampy.FibClient()

    response = client.call(35)
    print(f"[x] Got {response}")


if __name__ == "__main__":
    main()
