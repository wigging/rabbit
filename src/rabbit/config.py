import os
import pika
from dotenv import load_dotenv


def get_config() -> dict:
    """Get RabbitMQ configuration."""

    # Load environment variables from `.env` file if it exists
    path = os.getcwd() + "/.env"

    if os.path.isfile(path):
        load_dotenv(path)

    # If environment variables don't exist then use defaults from pika
    default_username = pika.ConnectionParameters.DEFAULT_USERNAME
    default_password = pika.ConnectionParameters.DEFAULT_PASSWORD
    default_host = pika.ConnectionParameters.DEFAULT_HOST
    default_port = pika.ConnectionParameters.DEFAULT_PORT

    username = os.getenv("RABBITMQ_USERNAME", default_username)
    password = os.getenv("RABBITMQ_PASSWORD", default_password)
    host = os.getenv("RABBITMQ_HOST", default_host)
    port = int(os.getenv("RABBITMQ_PORT", default_port))

    # Return the RabbitMQ configuration as a dictionary
    config = {"username": username, "password": password, "host": host, "port": port}
    return config
