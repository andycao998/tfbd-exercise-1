# Week 1 Assignment: Warehouse Restock Manifest Validator

## Setup
After cloning repository:
1. `cd warehouse_validator`
1. Initialize .venv: `python -m venv .venv`
1. Activate .venv:
    - Windows Powershell: `.venv\Scripts\Activate.ps1`
    - macOS & Linux: `source venv/bin/activate`
1. `cd ..` (back into exercise-1 directory)
1. Install dependencies: `pip install -e .`
1. Install optional dependencies (for tests): `pip install -e ".[test]"`
1. Run tests: `pytest -q`