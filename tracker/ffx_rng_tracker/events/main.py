from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ..gamestate import GameState


@dataclass
class Event(ABC):
    """Abstract base class for all events."""
    gamestate: GameState
    _rng_rolls: dict[int, int] = field(
        default_factory=dict, init=False, repr=False)

    @abstractmethod
    def __str__(self) -> str:
        pass

    def _advance_rng(self, index: int) -> int:
        rng_rolls = self._rng_rolls.get(index, 0)
        self._rng_rolls[index] = rng_rolls + 1
        return self.gamestate._rng_tracker.advance_rng(index)

    def rollback(self) -> None:
        for index, rolls in self._rng_rolls.items():
            self.gamestate._rng_tracker._rng_current_positions[index] -= rolls
