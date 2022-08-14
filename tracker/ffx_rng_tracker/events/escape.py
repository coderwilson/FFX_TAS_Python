from dataclasses import dataclass, field

from ..data.characters import Character
from .main import Event


@dataclass
class Escape(Event):
    character: Character
    escape: bool = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.escape = self._get_escape()

    def __str__(self) -> str:
        string = f'{self.character.name}: Escape ->'
        if self.escape:
            string += ' Succeeded'
        else:
            string += ' Failed'
        return string

    def _get_escape(self) -> bool:
        index = 20 + self.character.index
        escape_roll = self._advance_rng(index) & 255
        return escape_roll < 191
