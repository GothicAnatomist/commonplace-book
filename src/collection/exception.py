from __future__ import annotations

from typing import Tuple, Type


class InvalidItemType(Exception):
    """
    Exception raised for errors in the type of object being added to a
    TypedCollection.
    """

    def __init__(
        self, attempted_type: Type, type_tup: Tuple[Type, ...], *args: object
    ) -> None:
        atype_name = attempted_type.__name__
        ptype_names = [t.__name__ for t in type_tup]
        message = (
            f"Passed object of type '{atype_name}', is not an instance "
            f"of permitted type(s) ({', '.join(ptype_names)})"
        )
        super().__init__(message, *args)


class ItemAlreadyExists(Exception):
    """
    Exception raised for errors when an item attempting to be added to a
    unique TypedCollection already exists.
    """

    def __init__(self, *args: object) -> None:
        message = "Object passed already exists in collection."
        super().__init__(message, *args)
