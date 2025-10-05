from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from enum import Enum


class SubscriptionTier(str, Enum):
    """Single free tier used across the public experience."""

    FREE = "free"

    def meets(self, minimum: "SubscriptionTier") -> bool:  # pragma: no cover - kept for legacy calls
        """Compatibility helper so existing checks continue to pass."""

        return True


__all__ = ["SubscriptionTier"]
