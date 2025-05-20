from typing import Any, Callable, List

from . import util


class Compute:
    def __init__(self) -> None:
        pass

    def _compute_functions_list(self) -> List[Callable[..., Any]]:
        """Return a list of compute functions."""
        return []
