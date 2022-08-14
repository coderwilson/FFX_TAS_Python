from dataclasses import dataclass

from ..data.characters import CharacterState
from ..data.constants import Stat
from .main import Event


@dataclass
class ChangeStat(Event):
    character: CharacterState
    stat: Stat
    stat_value: int

    def __post_init__(self) -> None:
        self.stat_value = self._set_stat()

    def __str__(self) -> str:
        return (f'{self.character.name}\'s {self.stat} '
                f'changed to {self.stat_value}')

    def _set_stat(self) -> int:
        self.character.set_stat(self.stat, self.stat_value)
        return self.character.stats[self.stat]
