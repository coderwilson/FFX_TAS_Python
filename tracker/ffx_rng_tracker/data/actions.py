import json
from dataclasses import dataclass, field

from .constants import DamageType, Element, Status
from .file_functions import get_resource_path


@dataclass(frozen=True)
class Action:
    name: str
    has_target: bool = True
    multitarget: bool = False
    random_targeting: bool = False
    can_miss: bool = True
    accuracy: int = 90
    does_damage: bool = True
    hits: int = 1
    can_crit: bool = True
    uses_bonus_crit: bool = True
    bonus_crit: int = 0
    damage_type: DamageType = DamageType.STRENGTH
    base_damage: int = 0
    element: Element | None = None
    statuses: dict[Status, int] = field(default_factory=dict)
    rank: int = 3

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class YojimboAction:
    name: str
    compatibility_modifier: int
    needed_motivation: int | None = None

    def __str__(self) -> str:
        return self.name


def _get_action(action: dict) -> Action:
    if action.get("damage_type") is not None:
        action["damage_type"] = DamageType(action["damage_type"])

    if action.get("element") is not None:
        action["element"] = Element(action["element"])

    if action.get("statuses") is not None:
        action["statuses"] = {Status(s): v for s, v in action["statuses"].items()}

    return Action(**action)


def _get_actions(file_path: str) -> dict[str, Action]:
    absolute_file_path = get_resource_path(file_path)
    with open(absolute_file_path) as file_object:
        data: dict[str, dict] = json.load(file_object)
    actions = {}
    for name, action in data.items():
        if name.startswith("#"):
            continue
        actions[name] = _get_action(action)
    return actions


def _get_monster_actions(file_path: str) -> dict[str, dict[str, Action]]:
    absolute_file_path = get_resource_path(file_path)
    with open(absolute_file_path) as file_object:
        data: dict[str, dict[str, dict]] = json.load(file_object)
    monster_actions = {}
    for monster_name, _actions in data.items():
        actions = {}
        for name, action in _actions.items():
            if name.startswith("#"):
                continue
            actions[name] = _get_action(action)
        monster_actions[monster_name] = actions
    return monster_actions


ACTIONS = _get_actions("tracker\\data\\actions.json")
MONSTER_ACTIONS = _get_monster_actions("tracker\\data\\monster_actions.json")

YOJIMBO_ACTIONS = {
    "daigoro": YojimboAction("Daigoro", -1, 0),
    "kozuka": YojimboAction("Kozuka", 0, 32),
    "wakizashi_st": YojimboAction("Wakizashi ST", 1, 48),
    "wakizashi_mt": YojimboAction("Wakizashi MT", 3, 63),
    "zanmato": YojimboAction("Zanmato", 4, 80),
    "dismiss": YojimboAction("Dismiss", 0),
    "first_turn_dismiss": YojimboAction("First turn Dismiss", -3),
    # 'death': YojimboAction('Death', -10),
    "autodismiss": YojimboAction("Autodismiss", -20),
}
