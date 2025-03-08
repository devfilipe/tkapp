# TkApp - Tkinter Application Launcher

A simple Tkinter-based launcher that dynamically loads and categorizes application configurations from a JSON configuration file (`tkapp.conf`) and launches them as standalone processes.

This project includes contributions generated with the assistance of OpenAI's ChatGPT language model.

## Features

- Applications are organized into categories, each displayed in separate tabs.
- Each application has an `enabled` flag to control its visibility.
- Launches applications in separate processes.

## Instructions

Install Poetry:

If you haven't installed Poetry yet, follow the instructions at https://python-poetry.org/docs/#installation.

## Setup

Install dependencies using Poetry:

```bash
poetry install
```

## Usage

Create your `tkapp.conf` file and have fun!

```bash
poetry run python tkapp.py --config tkapp.conf
```
