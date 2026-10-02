"""A simple in-process EventPublisher."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from projector_borrowing.application.events import EventPublisher


class InProcessEventDispatcher(EventPublisher):
    """Deliver each published event to the handlers subscribed to its type.

    Handlers run immediately, in subscription order, in the same process. No
    message broker is needed for this coursework.
    """

    def __init__(self) -> None:
        self._handlers: dict[type, list[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        """Register a handler to be called for every event of this type."""

        self._handlers[event_type].append(handler)

    def publish(self, event: object) -> None:
        """Call every handler subscribed to the event's type."""

        for handler in self._handlers[type(event)]:
            handler(event)
