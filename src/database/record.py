from __future__ import annotations

import typing
import dataclasses
import copy

from .base_class import LoadableDataclass

class Record:
    """Base class used to interface with the Database.

    Direct usage is not recommended. Either:
    - Subclass and use with dataclasses @dataclass. You MUST set default values for all fields.
    - Subclass and overwrite `__init__`, (@classmethod) `from_dict`, `to_dict`
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_dict(cls, data: dict) -> typing.Self:
        if dataclasses.is_dataclass(cls):
            # data = {  # A) If it's None, pass it as None
            #     field.name: data.get(field.name) for field in dataclasses.fields(cls)
            # }
            data = {  # B) If it is None, use the class's default value (or error if there isn't one)
                field.name: value for field in dataclasses.fields(cls)
                if (value := data.get(field.name)) is not None
            }
        else:
            data = {k: v for k, v in data if not k.startswith("_")}
        try:
            return cls(**data)
        except TypeError:
            raise TypeError(f"Error while loading class {cls!r}, parameters supplied: {data}")

    def to_dict(self) -> dict:
        data = copy.copy(self)
        for attr, val in vars(data).items():
            if isinstance(val, LoadableDataclass):
                setattr(data, attr, val.to_dict())
        if dataclasses.is_dataclass(data):
            data = dataclasses.asdict(data)
        else:
            data = {k: v for k, v in vars(data).items() if not k.startswith("_")}
        return data
