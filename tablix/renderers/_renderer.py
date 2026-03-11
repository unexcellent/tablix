from abc import ABC, abstractmethod


class _Renderer(ABC):
    @abstractmethod
    def lines(self) -> list[str]:
        return NotImplementedError  # type: ignore

    def __str__(self) -> str:
        string = ""
        for line in self.lines():
            string += line + "\n"
        return string[:-1]
