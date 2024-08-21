"""A basic Python script."""

import random


def main():
    """Greet characters from the Simpsons show."""
    name = ["homer", "bart", "lisa", "krusty", "marge", "maggie", "ned", "barney", "selma"]
    s = f"hello {random.choice(name)}"
    print(s)


if __name__ == "__main__":
    main()
