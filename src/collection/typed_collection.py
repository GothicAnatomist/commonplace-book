"""
_summary_

_extended_summary_
"""
from abc import ABC
from collections.abc import Collection, Generator, Reversible
from typing import (
    Any,
    Generic,
    Iterable,
    List,
    Optional,
    Self,
    Tuple,
    Type,
    TypeVarTuple,
    Union,
    Unpack,
    get_args,
)
from warnings import warn

from collection.exception import InvalidItemType, ItemAlreadyExists

ItemType = TypeVarTuple("ItemType")


class TypedCollection(ABC, Collection, Reversible, Generic[Unpack[ItemType]]):
    """
    Abstract collection class with defined member type(s).

    An abstract collection class where specific member object types are
    permitted to be stored. The required type(s) are defined using the generic
    typing syntax when the subclass inherits this collection.

    Args:
        ABC (ABC): Helper class for creating abstract classes
        Collection (Collection): Inheriting from Collection
        Reversible (Reversible): Inheriting from Reversible
        Generic (ItemType): Generic typing to define which object types are
        valid within the collection using the TypeVarTuple, ItemType.
    """
    def __init__(self, coll: Optional[List[Union[Unpack[ItemType]]]] = None,
                 unique: bool = True) -> None:
        if coll is None:
            coll = list()
        self._collection: List[Union[Unpack[ItemType]]] = coll
        self._unique: bool = unique

    def __len__(self) -> int:
        return len(self._collection)

    def __iter__(self) -> Generator[Union[Unpack[ItemType]], Any, None]:
        for item in self._collection:
            yield item

    def __reversed__(self) -> Generator[Union[Unpack[ItemType]], Any, None]:
        for item in reversed(self._collection):
            yield item

    def __contains__(self, item: Union[Unpack[ItemType]]) -> bool:
        return item in self._collection

    def __add__(self, other) -> Self:
        new_collection = self.__class__()
        new_collection.extend(self)

        if isinstance(other, self._item_type):
            new_collection.append(other)
            return new_collection

        if isinstance(other, type(self)):
            new_collection.extend(other)
            return new_collection

        raise TypeError(
            "Object passed is not instance of "
            f"'{self._item_type}' or '{type(self)}'"
        )

    def __radd__(self, other) -> Self:
        return self.__add__(other)

    @property
    def _item_type(self) -> Tuple[Type, ...]:
        return get_args(type(self).__orig_bases__[0])  # pylint: disable=[no-member] # type: ignore # noqa

    def append(self, item: Union[Unpack[ItemType]]) -> None:
        """
        Append object to the end of the collection.

        Args:
            item (Union[Unpack[ItemType]]): Object of type defined by generic
            TypeVar tuple.

        Raises:
            InvalidItemType: Type of item not compatible with collection.
            ItemAlreadyExists: Item already exists in collection with unique
            constraint.
        """
        if not isinstance(item, self._item_type):
            raise InvalidItemType(type(item), self._item_type)

        if self._unique and item in self._collection:
            raise ItemAlreadyExists()

        self._collection.append(item)

    def extend(self, collection: Iterable, ignore_error: bool = False) -> None:
        """
        Extend collection by appending elements from the iterable.

        Args:
            collection (Iterable): Iterable containing objects to add to
            collection.
            ignore_error (bool, optional): Boolean to determine whether to
            raise exceptions if an invalid object is found. Defaults to False.

        Raises:
            iit: Exception where object item is of an invalid type
            iae: Exception where object item already exists in collection
            where collection has a unique constraint.
        """
        for item in collection:
            try:
                self.append(item)
            except InvalidItemType as iit:
                if ignore_error:
                    warn(f"Item of type {type(item)} is not valid in this "
                         "collection and was not added.", UserWarning)
                else:
                    raise iit
            except ItemAlreadyExists as iae:
                if ignore_error:
                    warn("This collection has a unique constraint and the item"
                         " passed already exists.", UserWarning)
                else:
                    raise iae
