# Todoist CLI
Interactive CLI client for [Todoist](http://www.todoist.com) written in Python.
## Work in progress!

## Dependencies
- [Click](http://click.pocoo.org/5/)
- [Blessings](https://github.com/erikrose/blessings)
- [PyTodoist](https://github.com/Garee/pytodoist)

## Setup
#### 1. Install the dependencies:
```bash
    $ pip install pytodoist blessings click
```
#### 2. Download `*.py` files:
```bash
    $ git clone https://github.com/ViliamV/todoist_cli.git
    $ cd todoist_cli/
```
#### 3. Run `create_login.py` to save your Todoist credentials:
```bash
    $ ./create_login.py
```
#### 4. Run `todoist_cli.py`.
```bash
    $ ./todoist_cli.py
```

## Features
- View tasks
- Complete tasks
- Undo completing task
