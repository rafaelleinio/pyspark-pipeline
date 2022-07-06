# Pyspark Pipeline
![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-brightgreen.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![aa](https://img.shields.io/badge/code%20quality-flake8-blue)](https://github.com/PyCQA/flake8)
[![Checked with mypy](https://camo.githubusercontent.com/59eab954a267c6e9ff1d80e8055de43a0ad771f5e1f3779aef99d111f20bee40/687474703a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667)](http://mypy-lang.org/)

[Build Status](https://github.com/rafaelleinio/pyspark-test/actions):

| Core     | Docker Image 
| -------- | -------- 
| ![Tests](https://github.com/rafaelleinio/pyspark-test/workflows/Tests/badge.svg?branch=main)     | ![Build Docker Image](https://github.com/rafaelleinio/pyspark-test/workflows/Build%20Docker%20Image/badge.svg?branch=main)    

## Introduction
This repository shows a simple implementation of an data aggregation pipeline.
The Top Revenue pipeline implementation can be found [here](https://github.com/rafaelleinio/pyspark-pipeline/blob/main/pyspark_pipeline/pipelines/top_revenue.py)

## Getting started

#### Clone the project:

```bash
git clone git@github.com:rafaelleinio/pyspark-test.git
cd pyspark-test
```

#### Run app in docker compose
```bash
make app
```

Inside app interactive shell:
```
# pcli --help
Usage: pcli [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  init-db  Initialize the database with all models declared in domain.
  run      Trigger a pipeline ETL.

```

```
/# pcli run --help
Usage: pcli run [OPTIONS]

  Trigger a pipeline ETL.

  Args:     pipeline: choice of pipelines to run.

Options:
  --pipeline [top_revenue|sample]
                                  [default: PipelineEnum.top_revenue]
  --help                          Show this message and exit.
```

#### Teardown docker compose
```bash
make teardown
```


## Development

### Install dependencies

```bash
make requirements
```

### Code Style
Apply code style with black and isort
```bash
make apply-style
```

Perform all checks (flake8, black and mypy)
```bash
make checks
```

### Testing and Coverage
Unit tests:
```bash
make unit-tests
```
Integration tests:
```bash
make integration-tests
```
All (unit + integration) tests:
```bash
make tests
```

e2e tests (with docker compose):
```bash
make e2e-tests
```
