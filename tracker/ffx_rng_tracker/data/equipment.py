import csv
from dataclasses import dataclass, field

from .autoabilities import AUTOABILITIES, Autoability
from .characters import Character
from .constants import EquipmentType
from .file_functions import get_resource_path
from .monsters import Monster


@dataclass
class Equipment:
    owner: Character
    type_: EquipmentType
    slots: int
    abilities: tuple[Autoability]
    base_weapon_damage: int
    bonus_crit: int
    name: str = field(init=False, repr=False)
    gil_value: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.name = self.get_name()
        self.gil_value = self.get_gil_value()

    def __str__(self) -> str:
        abilities = [str(a) for a in self.abilities]
        for _ in range(self.slots - len(abilities)):
            abilities.append("-")
        string = (
            f"{self.name} "
            f"({self.owner.name}) "
            f'[{", ".join(abilities)}]'
            f"[{self.gil_value // 4} gil]"
        )
        return string

    def get_gil_value(self) -> None:
        slots_factor = (1, 1, 1.5, 3, 5)
        empty_slots_factor = (1, 1, 1.5, 3, 400)
        empty_slots = self.slots - len(self.abilities)
        abilities_values = [a.gil_value for a in self.abilities]
        base_gil_value = sum(abilities_values)
        gil_value = int(
            (50 + base_gil_value)
            * slots_factor[self.slots]
            * empty_slots_factor[empty_slots]
        )
        return gil_value

    def get_name(self) -> str:
        ability_indexes = [AUTOABILITIES.index(a) for a in self.abilities]
        if self.type_ == EquipmentType.WEAPON:
            name = get_weapon_name(self.owner.index, ability_indexes, self.slots)
        elif self.type_ == EquipmentType.ARMOR:
            name = get_armor_name(self.owner.index, ability_indexes, self.slots)
        return name


@dataclass
class EquipmentDrop:
    equipment: Equipment
    killer: Character
    monster: Monster
    killer_is_owner: bool

    def __str__(self) -> str:
        string = str(self.equipment)
        if self.monster.equipment["drop_chance"] == 255:
            string += " (guaranteed)"
        if self.killer_is_owner:
            string += " (for killer)"
        return string


def _get_equipment_names(file_path: str) -> dict[str, tuple[str]]:
    """Retrieves the equipment names."""
    weapon_names = []
    armor_names = []
    absolute_file_path = get_resource_path(file_path)
    with open(absolute_file_path) as file_object:
        file_reader = csv.reader(file_object, delimiter=",")
        # skips first 3 lines
        for _ in range(3):
            next(file_reader)
        # get weapons' names lists
        for _ in range(66):
            weapon_names.append(next(file_reader))
        # skips empty line
        next(file_reader)
        # get armors' names lists
        for _ in range(84):
            armor_names.append(next(file_reader))

    equipment_names = {
        "weapon": tuple(weapon_names),
        "armor": tuple(armor_names),
    }
    return equipment_names


def get_weapon_name(owner_index: int, abilities: list[int], slots: int) -> str:
    """Returns a weapon's name given the owner,
    the abilities and the number of slots.
    """
    # get number of certain ability types in the equipment
    elemental_strikes = len([a for a in (30, 34, 38, 42) if a in abilities])
    status_strikes = len(
        [a for a in (46, 50, 54, 58, 62, 66, 70, 74) if a in abilities]
    )
    status_touches = len(
        [a for a in (47, 51, 55, 59, 63, 67, 71, 75) if a in abilities]
    )
    strength_bonuses = len([a for a in (98, 99, 100, 101) if a in abilities])
    magic_bonuses = len([a for a in (102, 103, 104, 105) if a in abilities])

    # check conditions for names in order of priority
    if 122 in abilities:  # Capture
        index = 0
    elif elemental_strikes == 4:  # All four elemental -strikes
        index = 1
    elif 25 in abilities:  # Break Damage Limit
        index = 2
    # Triple Overdrive, Triple AP and Overdrive → AP
    elif 15 in abilities and 19 in abilities and 17 in abilities:
        index = 3
    # Triple Overdrive and Overdrive → AP
    elif 15 in abilities and 17 in abilities:
        index = 4
    # Double Overdrive and Double AP
    elif 14 in abilities and 18 in abilities:
        index = 5
    elif 15 in abilities:  # Triple Overdrive
        index = 6
    elif 14 in abilities:  # Double Overdrive
        index = 7
    elif 19 in abilities:  # Triple AP
        index = 8
    elif 18 in abilities:  # Double AP
        index = 9
    elif 17 in abilities:  # Overdrive → AP
        index = 10
    elif 16 in abilities:  # SOS Overdrive
        index = 11
    elif 13 in abilities:  # One MP Cost
        index = 12
    elif status_strikes == 4:  # Any four status -strike
        index = 13
    elif strength_bonuses == 4:  # All four Strength +X%
        index = 14
    elif magic_bonuses == 4:  # All four Magic +X%
        index = 15
    # Magic Booster and three Magic +X%
    elif 6 in abilities and magic_bonuses == 3:
        index = 16
    elif 12 in abilities:  # Half MP Cost
        index = 17
    elif 26 in abilities:  # Gillionaire
        index = 18
    elif elemental_strikes == 3:  # Any three elemental -strike
        index = 19
    elif status_strikes == 3:  # Any three status -strike
        index = 20
    # Magic Counter and Counter-Attack or Evade & Counter
    elif 5 in abilities and (3 in abilities or 4 in abilities):
        index = 21
    # Counter-Attack or Evade & Counter
    elif 3 in abilities or 4 in abilities:
        index = 22
    elif 5 in abilities:  # Magic Counter
        index = 23
    elif 6 in abilities:  # Magic Booster
        index = 24
    elif 7 in abilities:  # Alchemy
        index = 25
    elif 1 in abilities:  # First Strike
        index = 26
    elif 2 in abilities:  # Initiative
        index = 27
    elif 46 in abilities:  # Deathstrike
        index = 28
    elif 74 in abilities:  # Slowstrike
        index = 29
    elif 54 in abilities:  # Stonestrike
        index = 30
    elif 58 in abilities:  # Poisonstrike
        index = 31
    elif 62 in abilities:  # Sleepstrike
        index = 32
    elif 66 in abilities:  # Silencestrike
        index = 33
    elif 70 in abilities:  # Darkstrike
        index = 34
    elif strength_bonuses == 3:  # Any three Strength +X%
        index = 35
    elif magic_bonuses == 3:  # Any three Magic +X%
        index = 36
    elif elemental_strikes == 2:  # Any two elemental -strike
        index = 37
    elif status_touches >= 2:  # Any two status -touch
        index = 38
    elif 47 in abilities:  # Deathtouch
        index = 39
    elif 75 in abilities:  # Slowtouch
        index = 40
    elif 55 in abilities:  # Stonetouch
        index = 41
    elif 59 in abilities:  # Poisontouch
        index = 42
    elif 63 in abilities:  # Sleeptouch
        index = 43
    elif 67 in abilities:  # Silencetouch
        index = 44
    elif 71 in abilities:  # Darktouch
        index = 45
    elif 0 in abilities:  # Sensor
        index = 46
    elif 30 in abilities:  # Firestrike
        index = 47
    elif 34 in abilities:  # Icestrike
        index = 48
    elif 38 in abilities:  # Lightningstrike
        index = 49
    elif 42 in abilities:  # Waterstrike
        index = 50
    elif 124 in abilities:  # Distill Power
        index = 51
    elif 125 in abilities:  # Distill Mana
        index = 52
    elif 126 in abilities:  # Distill Speed
        index = 53
    elif 127 in abilities:  # Distill Ability
        index = 54
    elif slots == 4:  # 4-slot weapon
        index = 55
    # Magic +X% and Strength +X%
    elif strength_bonuses >= 1 and magic_bonuses >= 1:
        index = 56
    elif slots == 2 or slots == 3:  # 2 or 3 slot weapon
        index = 57
    elif 104 in abilities or 105 in abilities:  # Magic +10% or Magic +20%
        index = 58
    # Strength +10% or Strength +20%
    elif 100 in abilities or 101 in abilities:
        index = 59
    elif 103 in abilities:  # Magic +5%
        index = 60
    elif 102 in abilities:  # Magic +3%
        index = 61
    elif 99 in abilities:  # Strength +5%
        index = 62
    elif 98 in abilities:  # Strength +3%
        index = 63
    elif 11 in abilities:  # Piercing
        index = 64
    elif slots == 1:  # One slot
        index = 65
    else:  # No slots
        index = 65

    return EQUIPMENT_NAMES["weapon"][index][owner_index]


def get_armor_name(owner_index: int, abilities: list[int], slots: int) -> str:
    """Returns an armor's name given the owner,
    the abilities and the number of slots.
    """
    # get number of certain ability types in the equipment
    elemental_eaters = len([a for a in (33, 37, 41, 45) if a in abilities])
    elemental_proofs = len([a for a in (32, 36, 40, 44) if a in abilities])
    status_proofs = len(
        [a for a in (48, 52, 56, 60, 64, 68, 72, 76, 78, 80, 82) if a in abilities]
    )
    defense_bonuses = len([a for a in (106, 107, 108, 109) if a in abilities])
    magic_defense_bonuses = len([a for a in (110, 111, 112, 113) if a in abilities])
    hp_bonuses = len([a for a in (114, 115, 116, 117) if a in abilities])
    mp_bonuses = len([a for a in (118, 119, 120, 121) if a in abilities])
    auto_statuses = len([a for a in (84, 85, 86, 87, 88) if a in abilities])
    elemental_soses = len([a for a in (94, 95, 96, 97) if a in abilities])
    status_soses = len([a for a in (89, 90, 91, 92, 93) if a in abilities])

    # check conditions for names in order of priority
    # Break HP Limit and Break MP Limit
    if 23 in abilities and 24 in abilities:
        index = 0
    elif 128 in abilities:  # Ribbon
        index = 1
    elif 23 in abilities:  # Break HP Limit
        index = 2
    elif 24 in abilities:  # Break MP Limit
        index = 3
    elif elemental_eaters == 4:  # Four elemental -eater abilities
        index = 4
    elif elemental_proofs == 4:  # Four elemental -proof abilities
        index = 5
    # Auto Shell, Auto Protect, Auto Reflect and Auto Regen
    elif 84 in abilities and 85 in abilities and 88 in abilities and 87 in abilities:
        index = 6
    # Auto-Potion, Auto Med and Auto Phoenix
    elif 8 in abilities and 9 in abilities and 10 in abilities:
        index = 7
    elif 8 in abilities and 9 in abilities:  # Auto Potion and Auto Med
        index = 8
    elif status_proofs == 4:  # Any four status -proof abilities
        index = 9
    elif defense_bonuses == 4:  # All four Defense +X%
        index = 10
    elif magic_defense_bonuses == 4:  # All four Magic Defense +X%
        index = 11
    elif hp_bonuses == 4:  # All four HP +X%
        index = 12
    elif mp_bonuses == 4:  # All four MP +X%
        index = 13
    elif 22 in abilities:  # Master Thief
        index = 14
    elif 21 in abilities:  # Pickpocket
        index = 15
    elif 27 in abilities and 28 in abilities:  # HP Stroll and MP Stroll
        index = 16
    elif auto_statuses == 3:  # Any three auto- status abilities
        index = 17
    elif elemental_eaters == 3:  # Any three -eater abilities
        index = 18
    elif 27 in abilities:  # HP Stroll
        index = 19
    elif 28 in abilities:  # MP Stroll
        index = 20
    elif 10 in abilities:  # Auto Phoenix
        index = 21
    elif 9 in abilities:  # Auto Med
        index = 22
    elif elemental_soses == 4:  # Four elemental SOS- abilities
        index = 23
    elif status_soses == 4:  # Any four SOS- status abilities
        index = 24
    elif status_proofs == 3:  # Any three status -proof abilities
        index = 25
    elif 29 in abilities:  # No Encounters
        index = 26
    elif 8 in abilities:  # Auto Potion
        index = 27
    elif elemental_proofs == 3:  # Any three elemental -proof abilities
        index = 28
    elif status_soses == 3:  # Any three SOS- status abilities
        index = 29
    elif auto_statuses == 2:  # Any two auto- status abilities
        index = 30
    elif elemental_soses == 2:  # Any two elemental SOS- abilities
        index = 31
    elif 87 in abilities or 92 in abilities:  # Auto Regen or SOS Regen
        index = 32
    elif 86 in abilities or 91 in abilities:  # Auto Haste or SOS Haste
        index = 33
    # Auto Reflect or SOS Reflect
    elif 88 in abilities or 93 in abilities:
        index = 34
    elif 84 in abilities or 89 in abilities:  # Auto Shell or SOS Shell
        index = 35
    # Auto Protect or SOS Protect
    elif 85 in abilities or 90 in abilities:
        index = 36
    elif defense_bonuses == 3:  # Any three Defense +X%
        index = 37
    elif magic_defense_bonuses == 3:  # Any three Magic Defense +X%
        index = 38
    elif hp_bonuses == 3:  # Any three HP +X%
        index = 39
    elif mp_bonuses == 3:  # Any three MP +X%
        index = 40
    # Any two elemental -proof or -eater of different elements
    elif elemental_eaters + elemental_proofs >= 2:
        index = 41
    elif status_proofs == 2:  # Any two status -proof abilities
        index = 42
    elif 33 in abilities:  # Fire Eater
        index = 43
    elif 37 in abilities:  # Ice Eater
        index = 44
    elif 41 in abilities:  # Lightning Eater
        index = 45
    elif 45 in abilities:  # Water Eater
        index = 46
    elif 82 in abilities:  # Curseproof
        index = 47
    elif 78 in abilities or 79 in abilities:  # Confuse Ward/Proof
        index = 48
    elif 80 in abilities or 81 in abilities:  # Berserk Ward/Proof
        index = 49
    elif 76 in abilities or 77 in abilities:  # Slow Ward/Proof
        index = 50
    elif 48 in abilities or 49 in abilities:  # Death Ward/Proof
        index = 51
    elif 52 in abilities or 53 in abilities:  # Zombie Ward/Proof
        index = 52
    elif 56 in abilities or 57 in abilities:  # Stone Ward/Proof
        index = 53
    elif 60 in abilities or 61 in abilities:  # Poison Ward/Proof
        index = 54
    elif 64 in abilities or 65 in abilities:  # Sleep Ward/Proof
        index = 55
    elif 68 in abilities or 69 in abilities:  # Silence Ward/Proof
        index = 56
    elif 72 in abilities or 73 in abilities:  # Dark Ward/Proof
        index = 57
    elif 31 in abilities or 32 in abilities:  # Fire Ward/Proof
        index = 58
    elif 35 in abilities or 36 in abilities:  # Ice Ward/Proof
        index = 59
    elif 39 in abilities or 40 in abilities:  # Lightning Ward/Proof
        index = 60
    elif 43 in abilities or 44 in abilities:  # Water Ward/Proof
        index = 61
    elif 94 in abilities:  # SOS NulTide
        index = 62
    elif 97 in abilities:  # SOS NulBlaze
        index = 63
    elif 96 in abilities:  # SOS NulShock
        index = 64
    elif 95 in abilities:  # SOS NulFrost
        index = 65
    # Any two HP +X% and any two MP +X%
    elif hp_bonuses == 2 and mp_bonuses == 2:
        index = 66
    elif slots == 4:  # Four slots
        index = 67
    # Defense +X% and Magic Defense +X%
    elif defense_bonuses >= 1 and magic_defense_bonuses >= 1:
        index = 68
    elif defense_bonuses == 2:  # Any two Defense +X%
        index = 69
    elif magic_defense_bonuses == 2:  # Any two Magic Defense +X%
        index = 70
    elif hp_bonuses == 2:  # Any two HP +X%
        index = 71
    elif mp_bonuses == 2:  # Any two MP +X%
        index = 72
    # Defense +10% or Defense +20%
    elif 108 in abilities or 109 in abilities:
        index = 73
    # Magic Defense +10% or Magic Defense +20%
    elif 112 in abilities or 113 in abilities:
        index = 74
    elif 120 in abilities or 121 in abilities:  # MP +20% or MP +30%
        index = 75
    elif 116 in abilities or 117 in abilities:  # HP +20% or HP +30%
        index = 76
    elif slots == 3:  # Three slots
        index = 77
    # Defense +3% or Defense +5%
    elif 106 in abilities or 107 in abilities:
        index = 78
    # Magic Defense +3% or Magic Defense +5%
    elif 110 in abilities or 111 in abilities:
        index = 79
    elif 118 in abilities or 119 in abilities:  # MP +5% or MP +10%
        index = 80
    elif 114 in abilities or 115 in abilities:  # HP +5% or HP +10%
        index = 81
    elif slots == 2:  # Two slots
        index = 82
    elif slots == 1:  # One slot
        index = 83
    else:  # No slots
        index = 83

    return EQUIPMENT_NAMES["armor"][index][owner_index]


EQUIPMENT_NAMES = _get_equipment_names("tracker\\data\\equipment_names.csv")
