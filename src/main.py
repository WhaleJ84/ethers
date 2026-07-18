import logging
from os import getenv
from re import match

from pynetbox import api
from pynetbox.core.endpoint import RecordSet

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

    """
    ETHERS: list = []

    nb: api = api(
        url,
        token,
    )

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

    return ETHERS


if __name__ == "__main__":
    ethers = get_ethers_list()
    print('\n'.join(ethers))
