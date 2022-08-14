from dataclasses import dataclass

from ..data.characters import CHARACTERS, Character
from .main import Event


@dataclass
class Death(Event):
    dead_character: Character

    def __post_init__(self) -> None:
        for _ in range(3):
            self._advance_rng(10)
        if self.dead_character == CHARACTERS['yojimbo']:
            self._update_compatibility()

    def __str__(self) -> str:
        return f'Character death: {self.dead_character}'

    def _update_compatibility(self) -> None:
        compatibility = self.gamestate.compatibility
        self.gamestate.compatibility = max(compatibility - 10, 0)
