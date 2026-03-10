from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Format:
    """Information about the target formatting of a field."""

    bold: bool = False
    italic: bool = False

    @classmethod
    def default(cls) -> Format:
        """Return the default format for table content."""
        return Format()
