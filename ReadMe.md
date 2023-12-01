# Playground ELK

This repository was forked from the project [elastic-stack-docker-part-two](./README_ELK.md) and modified to be used as
a playground for the ELK stack.

## Requirements

- Docker, Docker Compose
- Python 3.11
- Setup environment

```shell
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r ./playground/requirements.txt
```

## Usage

### Playground

Generate random data and send it to the ELK stack.

```shell
python ./playground/gen_data.py
```