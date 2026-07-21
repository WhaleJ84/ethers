from enum import StrEnum
from json import dumps

from pydantic import BaseModel, ConfigDict, computed_field


class NetBoxError(Exception):
    """Base exception for Netbox errors.

    Args:
        message (str): Description of the error.
        error (str): Content from the error itself.
        status_code (int): HTTP status code.
    """
    def __init__(self, message: str, error: str, status_code: int, *args) -> None:
        self.message = message
        self.error: str = error
        self.status_code = status_code
        super().__init__(*args)

    def __str__(self) -> str:
        return dumps({
            "message": self.message,
            "error": self.error,
            "status_code": self.status_code,
        })


class NetBoxAssignedObjectTypes(StrEnum):
    DCIM_INTERFACE = "dcim.interface"
    VIRTUALIZATION_VMINTERFACE = "virtualization.vminterface"


class NetBoxBaseModel(BaseModel):
    id: int = 1
    _base_url: str = 'https://netbox.example.com'


class NetBoxMacAddress(NetBoxBaseModel):
    mac_address: str = '00:11:22:AA:BB:CC'
    assigned_object_type: NetBoxAssignedObjectTypes
    assigned_object_id: int = 1

    @computed_field
    @property
    def url(self) -> str:
        return f"{self._base_url}/api/dcim/mac_addresses/{self.id}"

    model_config = ConfigDict(extra="allow", use_enum_values=True)

