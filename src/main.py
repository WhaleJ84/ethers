import logging
from ast import literal_eval
from os import getenv
from re import match

from src.models import NetBoxError

from pynetbox import api
from pynetbox.core.endpoint import RecordSet
from pynetbox.core.query import RequestError
from requests.exceptions import ConnectionError

logging.basicConfig(level=logging.INFO)


def get_ethers_list(
    url: str = getenv("NETBOX_URL", ""),
    token: str = getenv("NETBOX_API_TOKEN", ""),
) -> list[str]:
    """Generates output for ``/etc/ethers`` file.

    Args:
        url (str): The base URL to the instance of NetBox you wish to connect to.
        token (str): Your NetBox token.

    Returns:
        list[str]: List of valid '<MAC>\t<DEVICE>-<INTERFACE>' strings.

    Raises:
        NetboxError: If ``token`` value is an invalid API key for the NetBox URL.
    """
    ETHERS: list = []

    nb: api = api(
        url,
        token,
    )
    try:
        for device in nb.dcim.devices.all():
            device_name: str = device.name if device.name else device.display
            mac_addresses: RecordSet = nb.dcim.mac_addresses.filter(device_id=device.id)
            if len( mac_addresses) == 0:
                logging.info('%s has no MAC addresses', device_name)
                continue
            for mac in mac_addresses:
                interface = nb.dcim.interfaces.get(mac.assigned_object_id)
                device_interface = f"{device_name}-{interface}"
                if not match(r'^[\w-]+$', device_interface):
                    logging.warning('Unable to add %s.', device_interface)
                    continue
                ETHERS.append(f"{mac}\t{device_interface}")
    except ConnectionError as e:
        endpoint: str = e.request.url
        error: str = str(e)
        status_code: int = 404
        error_msg: dict = {
            "message": f"Failed to query '{endpoint}'",
            "error": error,
            "status_code": status_code,
        }
        raise NetBoxError(**error_msg)
    except RequestError as e:
        endpoint: str = e.base
        error: str = str(literal_eval(e.error)['detail'])
        status_code: int = int(e.req.status_code)
        error_msg: dict = {
            "message": f"Failed to query '{endpoint}'",
            "error": error,
            "status_code": status_code,
        }
        raise NetBoxError(**error_msg)

    return ETHERS

def create_ethers_file(
    content: list[str],
    file_name: str = getenv("ETHERS_FILENAME", "ethers"),
) -> None:
    """Creates ``file_name`` with the output of ``content``.

    Args:
        content (list[str]): An array of lines to be written to ``file_name``.
        file_name (str): Name of the file created with the output of ``content``. Defaults to ``ethers``.
    """
    with open(file_name, 'w') as file:
        file.write('\n'.join(content))


if __name__ == "__main__":
    ethers_content = get_ethers_list()
    create_ethers_file(ethers_content)

