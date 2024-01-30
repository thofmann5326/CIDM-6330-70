# Example application code for the python architecture book

## Chapters

I have separated each of P&G's chapters so that they exist independent of each other.


## Requirements

It is expected that you will create a virtual environment using the standard python tools:

`python -m venv .venv`

Then you can bring in the requirements:

`python -m pip install -r requirements.txt`

## Creating a local virtualenv (optional)

```bash
python -m venv .venv && source .venv/bin/activate # or however you like to create virtualenvs

# note, unless using gitbash, you'll need to use the Activate.ps1 script in windows

# for chapter 1
pip install pytest 

# for chapter 2
pip install pytest sqlalchemy

# for chapter 4+5
pip install -r requirements.txt

# for chapter 6+
pip install requirements.txt
pip install -e src/
```

**NOTE:** as each chapter changes - from 6 to 13 - it will be necessary to re-run `pip install -e src/` to refresh the package to include code changes.

## Running the tests

```bash
pytest tests/unit
pytest tests/integration
pytest tests/e2e
```

## Database

I am using a SQLite file database for the examples rather than Postgres.