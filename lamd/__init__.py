"""lamd package.

Heavy dependencies (pandas, lynguine) are not imported here. They load when
submodules such as ``lamd.util`` or ``lamd.config.interface`` are first used,
so CLI entry points like ``maketalk`` and ``dependencies`` start quickly.
"""

from __future__ import annotations

import importlib
from typing import Any

__all__ = ["config", "util"]


def __getattr__(name: str) -> Any:
    if name in ("util", "config"):
        # importlib avoids recursion with ``from lamd import util``
        mod = importlib.import_module(f".{name}", __name__)
        globals()[name] = mod
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
