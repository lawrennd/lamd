"""Configuration package — ``Interface`` lives in ``lamd.config.interface``."""

from __future__ import annotations

import importlib
from typing import Any

__all__ = ["Interface", "interface"]


def __getattr__(name: str) -> Any:
    if name == "interface":
        mod = importlib.import_module(".interface", __name__)
        globals()["interface"] = mod
        return mod
    if name == "Interface":
        iface = importlib.import_module(".interface", __name__).Interface
        globals()["Interface"] = iface
        return iface
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
