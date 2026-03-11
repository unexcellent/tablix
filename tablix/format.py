from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class Format:
    """Information about the target formatting of a field."""

    bold: bool = False
    italic: bool = False
    align: Literal["left", "center", "right"] = "left"
    merge_same: bool = False

    @classmethod
    def default(cls) -> Format:
        """Return the default format for table content."""
        return Format()
