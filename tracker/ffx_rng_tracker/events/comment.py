from dataclasses import dataclass

from .main import Event


@dataclass
class Comment(Event):
    text: str

    def __str__(self) -> str:
        return self.text
