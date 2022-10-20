import json
from dataclasses import dataclass, field

from .constants import EncounterCondition
from .file_functions import get_resource_path
from .monsters import MONSTERS, Monster


class Formation(list[Monster]):
    def __str__(self) -> str:
        return ", ".join([str(m) for m in self])

    def __format__(self, __format_spec: str) -> str:
        return format(str(self), __format_spec)


@dataclass
class Zone:
    name: str
    formations: list[Formation]
    forced_condition: EncounterCondition | None
    danger_value: int
    grace_period: int = field(init=False, repr=False)
    threat_modifier: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.grace_period = self.danger_value // 2
        self.threat_modifier = self.danger_value * 4

    def __str__(self) -> str:
        return self.name


@dataclass
class Boss:
    name: str
    formation: Formation
    forced_condition: EncounterCondition | None

    def __str__(self) -> str:
        return self.name


@dataclass
class Simulation:
    name: str
    monsters: Formation
    forced_condition: EncounterCondition | None

    def __str__(self) -> str:
        return self.name


Formations = tuple[dict[str, Boss], dict[str, Simulation], dict[str, Zone]]


def _get_formations(file_path: str) -> Formations:
    """Retrieves the encounter formations."""
    absolute_file_path = get_resource_path(file_path)
    with open(absolute_file_path) as file_object:
        formations: dict[str, dict] = json.load(file_object)
    bosses = {}
    for boss, data in formations["bosses"].items():
        for condition in EncounterCondition:
            if condition.lower() == data["forced_condition"]:
                break
        else:
            condition = None
        bosses[boss] = Boss(
            data["name"], Formation(MONSTERS[m] for m in data["formation"]), condition
        )

    simulations = {}
    for encounter, data in formations["simulation"].items():
        for condition in EncounterCondition:
            if condition.lower() == data["forced_condition"]:
                break
        else:
            condition = None
        simulations[encounter] = Simulation(
            data["name"], Formation(MONSTERS[m] for m in data["monsters"]), condition
        )

    zones: dict[str, Zone] = {}
    for encounter, data in formations["random"].items():
        for condition in EncounterCondition:
            if condition.lower() == data["forced_condition"]:
                break
        else:
            condition = None
        zones[encounter] = Zone(
            data["name"],
            [Formation(MONSTERS[m] for m in f) for f in data["formations"]],
            condition,
            data["danger_value"],
        )
        for formation in zones[encounter].formations:
            for monster in formation:
                if zones[encounter].name not in monster.zones:
                    monster.zones.append(zones[encounter].name)

    return bosses, simulations, zones


BOSSES, SIMULATIONS, ZONES = _get_formations("tracker\\data\\formations.json")
FORMATIONS = BOSSES | SIMULATIONS | ZONES
