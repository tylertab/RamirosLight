from __future__ import annotations

from threading import Lock
from typing import Any, Dict, Type


class SingletonMeta(type):
    """Thread-safe Singleton metaclass."""

    _instances: Dict[Type[Any], Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:  # type: ignore[override]
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ResettableSingletonMeta(SingletonMeta):
    def reset_instance(cls) -> None:  # type: ignore[override]
        with cls._lock:
            cls._instances.pop(cls, None)
