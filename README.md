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

## Configuration
The script can be modified by providing the following values through either the `.env` file or environment variables:

| Name             | Type | Description |
| ---------------- | ---- | ----------- |
| ETHERS_FILENAME  | str  | (Optional) Defines the name of the ethers file. Defaults to `ethers`. |
| NETBOX_API_TOKEN | str  | Your NetBox token for the `NETBOX_URL` instance. |
| NETBOX_URL       | str  | The base URL to the instance of the NetBox instance you wish to connec to. |

