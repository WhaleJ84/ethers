# Ethers

Generates output in `/etc/ethers` format to associate MAC addresses with an interface from a particular device.
NetBox data is used as the Source of Truth.

## Usage
1. Create `.env file`.
```
cp .env-example .env
```
2. Populate empty variables in `.env` with to match your NetBox instance.
3. Install project dependencies.
```
# pip
python3.12 -m venv .venv
source .venv/bin/activate
pip install .

# poetry
poetry install

# uv
uv sync
```
4. Run project.
```
# pip
set -a; source .env; set +a; python -m src.main

# poetry
source .env && poetry run python src.main

# uv
uv run --env-file .env -m src.main
```

