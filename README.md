# Rabbit

Rabbit is a Python package that demonstrates various [RabbitMQ](https://www.rabbitmq.com) workflows using the [Pika](https://github.com/pika/pika) client library. The goal is to show how RabbitMQ workflows can be implemented as a Python package using a simple design.

## Installation

This project uses [conda](https://conda.org) to create a Python virtual environment. Create the conda environment using the following command:

```text
conda env create --file environment.yml
```

Activate the environment as shown below. This will install the rabbit package in editable mode within the conda environment. See the comments in the `environment.yml` for more details.

```text
conda activate rabbit
```

A Docker compose file is also provided for running a RabbitMQ broker with default settings. Use the command shown below to run the broker in a Docker container. See the `compose.yaml` file for more details.

```text
docker compose up
```

## Examples

See the `examples` directory for several examples. Each example is in its own sub-directory. Read the comments in each example files for more details.
