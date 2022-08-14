from dataclasses import dataclass

from .main import Event


@dataclass
class AdvanceRNG(Event):
    rng_index: int
    number_of_times: int

    def __post_init__(self) -> None:
        for _ in range(self.number_of_times):
            self._advance_rng(self.rng_index)

    def __str__(self) -> str:
        return f'Advanced rng{self.rng_index} {self.number_of_times} times'
