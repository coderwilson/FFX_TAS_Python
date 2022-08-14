import csv
from dataclasses import dataclass, field

from .constants import Element, ElementalAffinity, Stat
from .file_functions import get_resource_path


@dataclass
class Character:
    name: str
    index: int
    _default_stats: dict[Stat, int] = field(default_factory=dict)
    elemental_affinities: dict[Element, ElementalAffinity] = field(
        default_factory=dict)

    def __str__(self) -> str:
        return self.name


@dataclass
class CharacterState(Character):
    stats: dict[Stat, int] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.reset()

    def set_stat(self, stat: Stat, value: int) -> None:
        match stat:
            case Stat.HP:
                max_value = 99999
            case Stat.MP:
                max_value = 9999
            case Stat.CHEER | Stat.FOCUS:
                max_value = 5
            case Stat.PIERCING:
                max_value = 1
            case Stat():
                max_value = 255
            case _:
                raise ValueError(f'Invalid stat name: {stat}')
        value = min(max(value, 0), max_value)
        self.stats[stat] = value

    def reset(self) -> None:
        self.stats = self._default_stats.copy()


def _get_characters(file_path: str) -> dict[str, Character]:
    """"""
    absolute_file_path = get_resource_path(file_path)
    with open(absolute_file_path) as file_object:
        file_reader = csv.reader(file_object, delimiter=',')
        # skips first line
        next(file_reader)
        characters = {}
        for line in file_reader:
            name = line[0]
            index = int(line[1])
            default_stats = {
                Stat.HP: int(line[2]),
                Stat.MP: int(line[3]),
                Stat.STRENGTH: int(line[4]),
                Stat.DEFENSE: int(line[5]),
                Stat.MAGIC: int(line[6]),
                Stat.MAGIC_DEFENSE: int(line[7]),
                Stat.AGILITY: int(line[8]),
                Stat.LUCK: int(line[9]),
                Stat.EVASION: int(line[10]),
                Stat.ACCURACY: int(line[11]),
                Stat.WEAPON_DAMAGE: int(line[12]),
                Stat.BONUS_CRIT: int(line[13]),
                Stat.BONUS_STRENGTH: int(line[14]),
                Stat.BONUS_MAGIC: int(line[15]),
                Stat.PIERCING: int(line[16]),
                Stat.CHEER: 0,
                Stat.FOCUS: 0,
            }
            elemental_affinities = {
                Element.FIRE: ElementalAffinity(line[17]),
                Element.ICE: ElementalAffinity(line[18]),
                Element.THUNDER: ElementalAffinity(line[19]),
                Element.WATER: ElementalAffinity(line[20]),
                Element.HOLY: ElementalAffinity(line[21]),
            }
            characters[name.lower()] = Character(
                name=name,
                index=index,
                _default_stats=default_stats,
                elemental_affinities=elemental_affinities,
                )
    return characters


CHARACTERS = _get_characters('tracker\\data\\characters.csv')
