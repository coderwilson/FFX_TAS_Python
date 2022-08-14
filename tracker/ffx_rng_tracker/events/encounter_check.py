from dataclasses import dataclass, field
from typing import Iterator

from ..data.encounter_formations import Zone
from ..gamestate import GameState
from .main import Event


@dataclass
class EncounterCheck(Event):
    max_distance: int
    zone: Zone
    encounter: bool = field(init=False, repr=False)
    distance: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.encounter, self.distance = self.check_encounter()

    def __str__(self) -> str:
        string = f'{self.zone.name}'
        if self.encounter:
            string += f'Encounter at {self.distance} units'
        else:
            string += f'No encounters for {self.distance} units'
        return string

    def check_encounter(self) -> tuple[bool, int]:
        steps = self.max_distance // 10
        live_steps = max(steps - self.zone.grace_period, 0)
        if live_steps == 0:
            return False, self.max_distance
        for steps in range(1, live_steps + 1):
            rng_roll = self._advance_rng(0) & 255
            counter = steps * 256 // self.zone.threat_modifier
            if rng_roll < counter:
                encounter = True
                distance = (self.zone.grace_period + steps) * 10
                break
        else:
            encounter = False
            distance = self.max_distance
        return encounter, distance


def walk(gamestate: GameState,
         distance: int,
         zone: Zone,
         ) -> Iterator[EncounterCheck]:
    while distance > 0:
        encounter_check = EncounterCheck(gamestate, distance, zone)
        yield encounter_check
        distance -= encounter_check.distance
