"""Storage shared by the in-memory repositories."""

from __future__ import annotations

import copy


class InMemoryStore[Key, Aggregate]:
    """Keep aggregates in a dictionary, storing and returning copies.

    Copies behave like a real database: changes to an aggregate are lost unless
    it is saved again.
    """

    def __init__(self) -> None:
        self._items: dict[Key, Aggregate] = {}

    def get(self, key: Key) -> Aggregate | None:
        item = self._items.get(key)
        return copy.deepcopy(item) if item is not None else None

    def put(self, key: Key, item: Aggregate) -> None:
        self._items[key] = copy.deepcopy(item)
