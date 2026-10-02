from collections import defaultdict
from typing import Any, Callable


class EventDispatcher:
    """Simple in-process dispatcher: calls each subscribed handler in order."""

    def __init__(self) -> None:
        self._handlers: dict[type, list[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: object) -> None:
        for handler in self._handlers[type(event)]:
            handler(event)
