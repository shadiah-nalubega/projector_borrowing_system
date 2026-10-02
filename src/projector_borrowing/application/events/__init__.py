"""In-process delivery of domain events to their handlers."""

from .event_dispatcher import EventDispatcher

__all__ = ["EventDispatcher"]
