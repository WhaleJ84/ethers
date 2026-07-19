import logging
from ast import literal_eval
from json import dumps
from os import getenv
from re import match

from pynetbox import api
from pynetbox.core.endpoint import RecordSet
from pynetbox.core.query import RequestError
from requests.exceptions import ConnectionError

logging.basicConfig(level=logging.INFO)


class NetboxError(Exception):
    """Base exception for Netbox errors.

    Args:
        message (str): Description of the error.
        error (str): Content from the error itself.
        status_code (int): HTTP status code.
    """
    def __init__(self, message: str, error: str, status_code: int, *args) -> None:
        self.message = message
        self.error = error
        self.status_code = status_code
        super().__init__(*args)

    def __str__(self):
        return dumps({
            "message": self.message,
            "error": self.error,
            "status_code": self.status_code,
        })


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
        raise NetboxError(**error_msg)
    except RequestError as e:
        endpoint: str = e.base
        error: str = str(literal_eval(e.error)['detail'])
        status_code: int = int(e.req.status_code)
        error_msg: dict = {
            "message": f"Failed to query '{endpoint}'",
            "error": error,
            "status_code": status_code,
        }
        raise NetboxError(**error_msg)

    return ETHERS


if __name__ == "__main__":
    ethers = get_ethers_list()
    print('\n'.join(ethers))
