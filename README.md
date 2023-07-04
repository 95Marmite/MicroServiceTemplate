# MicroServiceTemplate

Micro Service Template

## Table of content

- [Project structure]()
- [Install poetry](#install-poetry)

## Project structure

## Install Poetry

Start by installing Poetry on your system. Open a terminal or command prompt in the project folder and
run the following command:

```
pip install poetry
```

Installing Dependencies:
Run the following command to install the dependencies specified in your "pyproject.toml" file:

```
poetry install --with dev
#or
poetry install
```

Poetry will resolve and install the required packages and their dependencies within a virtual environment.

Activate the Poetry envirement with:

```
poetry shell
```

Add new requirements:

```
poetry add pandas
# or for dev requirements
poetry add isort --group dev
```

## Pre-commit

