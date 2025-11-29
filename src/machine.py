
from pydantic_core import PydanticCustomError
from pydantic import BaseModel, field_validator
import resources


class Machine(BaseModel):
    name: str
    os: str
    cpu: int
    ram: float | int

    # Initialize Machine
    def __init__(self, **data):
        super().__init__(**data)

    # Get Machine parameters as dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "os": self.os,
            "cpu": self.cpu,
            "ram": self.ram
        }

    # Validations:

    # Validate name with custom validator

    @field_validator("name", mode="after")
    @classmethod
    def name_validator(cls, name: str) -> str:
        if not (2 <= len(name) <= 12):
            raise PydanticCustomError(
                "name_error", "Name length should be 4 to 12 characters")
        return name

    # Validate OS with custom validator
    @field_validator("os", mode="after")
    @classmethod
    def os_validator(cls, os: str) -> str:
        if not (os in resources.os):
            available_os = "or ".join(resources.os)
            raise PydanticCustomError(
                "os_error", f"OS should be {available_os}")
        return os

    # Validate CPU with custom validator
    @field_validator("cpu", mode="after")
    @classmethod
    def cpu_validator(cls, cpu: int) -> int:
        if not (0 < cpu <= resources.cpu):
            raise PydanticCustomError(
                "cpu_error", f"CPU count should be 1 to {resources.cpu}")
        return cpu

    # Validate RAM with custom validator
    @field_validator("ram", mode="after")
    @classmethod
    def ram_validator(cls, ram: float) -> float | int:
        if not (0 < ram <= resources.ram):
            raise PydanticCustomError(
                "ram_error", f"RAM should be 1 to {resources.ram} GiB",)
        return ram
