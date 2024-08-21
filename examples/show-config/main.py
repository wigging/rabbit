"""
Use the show_config parameter to print out the RabbitMQ configuration.

Add a .env file to this directory to load environment variables defined in the file.

show-config
├── .env
└── main.py

Contents of the .env file can be something like:

RABBITMQ_USERNAME="homersimp"
RABBITMQ_PASSWORD="spring*field&2024"
"""

import zampy


def main():
    """Run this example."""
    _ = zampy.MessageSender(show_config=True)



if __name__ == "__main__":
    main()
