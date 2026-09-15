# Dev Setup

No build backend or dependencies are configured in `pyproject.toml` yet, so tests
and tooling run out of a local virtual environment instead of an installed package.

## Set up the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Run tests

```bash
source .venv/bin/activate
python -m pytest
```
