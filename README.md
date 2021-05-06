

# Legiti Challenge
_A nice project solution for building and running pipelines for feature store._

![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-brightgreen.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![aa](https://img.shields.io/badge/code%20quality-flake8-blue)](https://github.com/PyCQA/flake8)
[![Checked with mypy](https://camo.githubusercontent.com/59eab954a267c6e9ff1d80e8055de43a0ad771f5e1f3779aef99d111f20bee40/687474703a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667)](http://mypy-lang.org/)

[Build Status](https://github.com/rafaelleinio/pyspark-test/actions):

| Core     | Docker Image 
| -------- | -------- 
| ![Tests](https://github.com/rafaelleinio/pyspark-test/workflows/Tests/badge.svg?branch=main)     | ![Build Docker Image](https://github.com/rafaelleinio/pyspark-test/workflows/Build%20Docker%20Image/badge.svg?branch=main)    

## Introduction
This repository shows a simple implementation of an data aggregation pipeline.

The Top Revenue pipeline implementation can be found [here](https://github.com/rafaelleinio/pyspark-test/blob/main/pyspark_test/pipelines/top_revenue.py)

## Getting started

#### Clone the project:

```bash
git clone git@github.com:rafaelleinio/pyspark-test.git
cd pyspark-test
```

#### Build Docker image
```bash
docker build --tag pyspark-test .
```

#### Run the Top Revenue pipeline
```bash
docker run -v $(pwd)/data:/pyspark-test/data pyspark-test
```
> the results will be available under `data/output/output.csv`

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
All tests:
```bash
make tests
```
