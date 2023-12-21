# Playground ELK

This repository was forked from the project [elastic-stack-docker-part-two](./README_ELK.md) and modified to be used as
a playground for the ELK stack.

## Requirements

- Docker, Docker Compose
- Python 3.11
- Setup environment

To run script for generating random data, you need to setup the environment:
```shell
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r ./playground/requirements.txt
``` 

### Run environment

Run ELK stack:
```shell
docker-compose up -d
```

and then run the script for generating the data:
```shell
python ./playground/gen_data.py 
```
it will generate 20000 random records and send them to the elastic.
You can change parameters in the script:

- docs_number - number of documents to generate
- index_name - name of the index to send data to
- max_seconds - max number of seconds to generate data

Script stops when one of the conditions is met (docs_number or max_seconds)

## Usage

### Playground

Generate random data and send it to the ELK stack.

```shell
python ./playground/gen_data.py
```