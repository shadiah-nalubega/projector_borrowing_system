"""The EventPublisher contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class EventPublisher(ABC):
    """Deliver a domain event to whoever handles it.

    The application service depends on this abstraction, not on how events
    are delivered, so the delivery mechanism can change without touching it.
    """

    @abstractmethod
    def publish(self, event: object) -> None:
        """Hand the event to its handlers."""
