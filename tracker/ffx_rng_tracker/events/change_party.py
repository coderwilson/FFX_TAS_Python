from dataclasses import dataclass, field

from ..data.characters import Character
from .main import Event


@dataclass
class ChangeParty(Event):
    party_formation: list[Character]
    _old_party: list[Character] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._old_party = self.gamestate.party
        self.gamestate.party = self.party_formation

    def __str__(self) -> str:
        character_names = [c.name for c in self.party_formation]
        return f'Party changed to: {", ".join(character_names)}'

    def rollback(self) -> None:
        self.gamestate.party = self._old_party
        return super().rollback()
