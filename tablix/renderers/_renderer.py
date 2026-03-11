from abc import ABC, abstractmethod
from pathlib import Path


class _Renderer(ABC):
    @abstractmethod
    def lines(self) -> list[str]:
        return NotImplementedError  # type: ignore

    def write_to(self, path: Path | str) -> None:
        with open(path, "w") as output_file:  # noqa: PTH123
            output_file.writelines(f"{line}\n" for line in self.lines())

    def __str__(self) -> str:
        string = ""
        for line in self.lines():
            string += line + "\n"
        return string[:-1]
