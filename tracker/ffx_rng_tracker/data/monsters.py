import csv
from dataclasses import dataclass, field
from itertools import count

from ..configs import Configs
from ..utils import add_bytes, stringify
from .actions import MONSTER_ACTIONS, Action
from .autoabilities import AUTOABILITIES
from .characters import CHARACTERS, Character
from .constants import (Element, ElementalAffinity, EquipmentSlots,
                        EquipmentType, GameVersion, Rarity, Stat, Status)
from .file_functions import get_resource_path
from .items import ITEMS, ItemDrop
from .text_characters import TEXT_CHARACTERS


@dataclass
class Monster:
    name: str
    stats: dict[Stat, int]
    elemental_affinities: dict[Element, ElementalAffinity]
    status_resistances: dict[Status, int]
    poison_tick_damage: int
    zanmato_level: int
    armored: bool
    undead: bool
    auto_statuses: list[Status]
    gil: int
    ap: dict[str, int]
    item_1: dict[str, int | dict[Rarity, ItemDrop | None]]
    item_2: dict[str, int | dict[Rarity, ItemDrop | None]]
    steal: dict[str | Rarity, int | ItemDrop | None]
    bribe: dict[str, int | ItemDrop | None]
    equipment: dict[str, int | list | dict[Character, list[int]]]
    actions: dict[str, Action]
    zones: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return self.name


def _get_prize_structs(file_path: str) -> dict[str, list[int]]:
    """Retrieves the prize structs for enemies."""
    absolute_file_path = get_resource_path(file_path)
    with open(absolute_file_path) as file_object:
        file_reader = csv.reader(file_object, delimiter=',')
        monsters_data = {}
        for line in file_reader:
            prize_struct = [int(value, 16) for value in line]
            # gets the name of the monster from the prize struct itself
            # name is null (0x00) terminated
            monster_name = ''
            for character_id in prize_struct[408:430]:
                if character_id == 0:
                    break
                monster_name += TEXT_CHARACTERS[character_id]
            monster_name = stringify(monster_name)
            # if the name is already in the dictionary
            # appends it with an underscore and a number
            # from 2 to 8
            if monster_name in monsters_data:
                for i in count(2):
                    new_name = f'{monster_name}_{i}'
                    if new_name not in monsters_data:
                        monsters_data[new_name] = prize_struct
                        break
            else:
                monsters_data[monster_name] = prize_struct
    return monsters_data


def _patch_prize_structs_for_hd(prize_structs: dict[str, list[int]],
                                ) -> dict[str, list[int]]:
    """Apply changes made in the HD version to the prize structs."""
    def patch_abilities(monster_name: str,
                        abilities: tuple[int, int, int, int, int, int, int],
                        equipment_type: EquipmentType = EquipmentType.WEAPON,
                        ) -> None:
        """Modifies ability values 1-7 of every character's weapon
        or armor ability array.
        """
        # base address for abilities in the prize struct
        base_address = 178
        type_offset = 0 if equipment_type == EquipmentType.WEAPON else 1
        # place the abilities values at the correct offsets
        for owner_index in range(7):
            offset = (type_offset + (owner_index * 2)) * 16
            for slot in range(7):
                slot_offset = (slot + 1) * 2
                address = base_address + offset + slot_offset
                prize_structs[monster_name][address] = abilities[slot]

    # in the HD version equipment droprates were modified
    # from 8/255 to 12/255 for these enemies
    monster_names = (
        'condor', 'dingo', 'water_flan', 'condor_2', 'dingo_2',
        'water_flan_2', 'dinonix', 'killer_bee', 'yellow_element',
        'worker', 'vouivre_2', 'raldo_2', 'floating_eye', 'ipiria',
        'mi\'ihen_fang', 'raldo', 'vouivre', 'white_element', 'funguar',
        'gandarewa', 'lamashtu', 'raptor', 'red_element', 'thunder_flan',
        'bite_bug', 'bunyip', 'garm', 'simurgh', 'snow_flan', 'bunyip_2',
        'aerouge', 'buer', 'gold_element', 'kusariqqu', 'melusine',
        'blue_element', 'iguion', 'murussu', 'wasp', 'evil_eye',
        'ice_flan', 'mafdet', 'snow_wolf', 'guado_guardian_2', 'alcyone',
        'mech_guard', 'mushussu', 'sand_wolf', 'bomb_2', 'evil_eye_2',
        'guado_guardian_3', 'warrior_monk', 'warrior_monk_2', 'aqua_flan',
        'bat_eye', 'cave_iguion', 'sahagin_2', 'swamp_mafdet',
        'sahagin_3', 'flame_flan', 'mech_scouter', 'mech_scouter_2',
        'nebiros', 'shred', 'skoll', 'flame_flan', 'nebiros', 'shred',
        'skoll', 'dark_element', 'imp', 'nidhogg', 'yowie',
    )
    for monster_name in monster_names:
        prize_structs[monster_name][139] = 12

    # all the enemies that have ability arrays modified in the HD version
    # besaid
    patch_abilities('dingo', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('condor', (0, 0, 0, 0, 126, 126, 126))
    patch_abilities('water_flan', (42, 42, 42, 42, 125, 125, 125))
    patch_abilities('dingo_2', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('condor_2', (0, 0, 0, 0, 126, 126, 126))
    patch_abilities('water_flan_2', (42, 42, 42, 42, 125, 125, 125))

    # kilika
    patch_abilities('dinonix', (38, 42, 38, 30, 126, 126, 126))
    patch_abilities('killer_bee', (38, 42, 34, 30, 126, 126, 126))
    patch_abilities('yellow_element', (38, 38, 38, 38, 125, 125, 125))

    # luca
    patch_abilities('vouivre_2', (38, 42, 34, 30, 124, 124, 124))

    # mi'ihen
    patch_abilities('raldo_2', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('bomb', (30, 30, 30, 30, 30, 30, 125))
    patch_abilities('dual_horn', (67, 30, 30, 30, 30, 127, 127))
    patch_abilities('floating_eye', (38, 42, 34, 30, 99, 126, 126))
    patch_abilities('ipiria', (38, 42, 38, 30, 126, 126, 126))
    patch_abilities('mi\'ihen_fang', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('raldo', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('vouivre', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('white_element', (34, 34, 34, 34, 125, 125, 125))

    # mushroom rock road
    patch_abilities('gandarewa', (38, 38, 38, 38, 125, 125, 125))
    patch_abilities('lamashtu', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('raptor', (38, 42, 38, 30, 126, 126, 126))
    patch_abilities('red_element', (30, 30, 30, 30, 125, 125, 125))
    patch_abilities('thunder_flan', (38, 38, 38, 38, 125, 125, 125))

    # djose highroad
    patch_abilities('bite_bug', (38, 42, 34, 30, 126, 126, 126))
    patch_abilities('bunyip', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('garm', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('simurgh', (0, 0, 0, 0, 126, 126, 126))
    patch_abilities('snow_flan', (34, 34, 34, 34, 125, 125, 125))

    # moonflow
    patch_abilities('bunyip_2', (38, 42, 34, 30, 124, 124, 124))

    # thunder plains
    patch_abilities('aerouge', (38, 38, 38, 38, 125, 125, 125))
    patch_abilities('buer', (38, 42, 34, 30, 99, 126, 126))
    patch_abilities('gold_element', (38, 38, 38, 38, 125, 125, 125))
    patch_abilities('kusariqqu', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('melusine', (38, 42, 38, 30, 126, 126, 126))

    # macalania woods
    patch_abilities('blue_element', (42, 42, 42, 42, 125, 125, 125))
    patch_abilities('chimera', (104, 104, 103, 103, 103, 103, 125))
    patch_abilities('iguion', (38, 42, 38, 30, 126, 126, 126))
    patch_abilities('murussu', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('wasp', (38, 42, 34, 30, 126, 126, 126))

    # lake macalania
    patch_abilities('evil_eye', (38, 42, 34, 30, 99, 126, 126))
    patch_abilities('ice_flan', (34, 34, 34, 34, 125, 125, 125))
    patch_abilities('mafdet', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('snow_wolf', (38, 42, 34, 30, 124, 124, 124))

    # bikanel
    patch_abilities('alcyone', (0, 0, 0, 0, 126, 126, 126))
    patch_abilities('mushussu', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('sand_wolf', (38, 42, 34, 30, 124, 124, 124))

    # home
    patch_abilities('bomb_2', (30, 30, 30, 30, 30, 30, 125))
    patch_abilities('chimera_2', (104, 104, 103, 103, 103, 103, 125))
    patch_abilities('dual_horn_2', (67, 67, 67, 30, 30, 127, 127))
    patch_abilities('evil_eye_2', (38, 42, 34, 30, 99, 126, 126))

    # via purifico
    patch_abilities('aqua_flan', (42, 42, 42, 42, 125, 125, 125))
    patch_abilities('bat_eye', (38, 42, 34, 30, 99, 126, 126))
    patch_abilities('cave_iguion', (38, 42, 38, 30, 126, 126, 126))
    patch_abilities('swamp_mafdet', (38, 42, 34, 30, 124, 124, 124))

    # calm lands
    patch_abilities('chimera_brain', (104, 104, 104, 104, 103, 103, 125))
    patch_abilities('flame_flan', (30, 30, 30, 30, 125, 125, 125))
    patch_abilities('nebiros', (38, 42, 34, 30, 126, 126, 126))
    patch_abilities('shred', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('skoll', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('defender_x', (100, 99, 99, 99, 99, 99, 124))

    # cavern of the stolen fayth
    patch_abilities('dark_element', (42, 30, 30, 34, 125, 125, 125))
    patch_abilities('defender', (99, 99, 99, 99, 98, 98, 124))
    patch_abilities('ghost', (104, 104, 104, 103, 103, 103, 125))
    patch_abilities('imp', (38, 38, 38, 38, 125, 125, 125))
    patch_abilities('nidhogg', (38, 42, 34, 30, 124, 124, 124))
    patch_abilities('valaha', (67, 67, 67, 30, 30, 127, 127))
    patch_abilities('yowie', (38, 42, 38, 30, 126, 126, 126))
    return prize_structs


def get_raw_data_string(prize_struct: list[str]) -> str:
    string = ''
    for index, byte in enumerate(prize_struct):
        # every 16 bytes make a new line
        if index % 16 == 0:
            string += '\n'
            string += ' '.join(
                [f'[{hex(index + i)[2:]:>3}]' for i in range(16)])
            string += '\n'
        # print the bytes' value
        # string += f' {hex(byte)[2:]:>3}  '
        string += f' {byte:>3}  '
        # string += f' {byte:08b}  '
    return string


def _get_monster_data(monster_id: str, prize_struct: list[int]) -> Monster:
    """Get a Monster from his prize struct."""

    def get_elements() -> dict[str, str]:
        elements = {
            Element.FIRE: 0b00001,
            Element.ICE: 0b00010,
            Element.THUNDER: 0b00100,
            Element.WATER: 0b01000,
            Element.HOLY: 0b10000,
        }
        affinities = {}
        for element, value in elements.items():
            if prize_struct[43] & value:
                affinities[element] = ElementalAffinity.ABSORBS
            elif prize_struct[44] & value:
                affinities[element] = ElementalAffinity.IMMUNE
            elif prize_struct[45] & value:
                affinities[element] = ElementalAffinity.RESISTS
            elif prize_struct[46] & value:
                affinities[element] = ElementalAffinity.WEAK
            else:
                affinities[element] = ElementalAffinity.NEUTRAL
        return affinities

    def get_abilities(address: int) -> dict[str, list[str | None]]:
        abilities = {}
        equipment_types = (EquipmentType.WEAPON, 0), (EquipmentType.ARMOR, 16)
        for equipment_type, offset in equipment_types:
            abilities[equipment_type] = []
            for i in range(address + offset, address + 16 + offset, 2):
                if prize_struct[i + 1] == 128:
                    ability_name = AUTOABILITIES[prize_struct[i]]
                else:
                    ability_name = None
                abilities[equipment_type].append(ability_name)
        return abilities

    monster_name = ''
    for character_id in prize_struct[408:430]:
        if character_id == 0:
            break
        monster_name += TEXT_CHARACTERS[character_id]
    for i in range(16):
        if monster_id.endswith(f'_{i}'):
            monster_name += f'#{i}'
            break

    stats = {
        Stat.HP: add_bytes(*prize_struct[20:24]),
        Stat.MP: add_bytes(*prize_struct[24:28]),
        'overkill_threshold': add_bytes(*prize_struct[28:32]),
        Stat.STRENGTH: prize_struct[32],
        Stat.DEFENSE: prize_struct[33],
        Stat.MAGIC: prize_struct[34],
        Stat.MAGIC_DEFENSE: prize_struct[35],
        Stat.AGILITY: prize_struct[36],
        Stat.LUCK: prize_struct[37],
        Stat.EVASION: prize_struct[38],
        Stat.ACCURACY: prize_struct[39],
    }

    gil = add_bytes(*prize_struct[128:130])
    ap = {
        'normal': add_bytes(*prize_struct[130:132]),
        'overkill': add_bytes(*prize_struct[132:134])
    }
    item_1 = {
        'drop_chance': prize_struct[136],
        'normal': {Rarity.COMMON: None, Rarity.RARE: None},
        'overkill': {Rarity.COMMON: None, Rarity.RARE: None},
    }
    if prize_struct[141] == 32:
        item_1['normal'][Rarity.COMMON] = ItemDrop(
            ITEMS[prize_struct[140]], prize_struct[148], False)
    if prize_struct[143] == 32:
        item_1['normal'][Rarity.RARE] = ItemDrop(
            ITEMS[prize_struct[142]], prize_struct[149], True)
    if prize_struct[153] == 32:
        item_1['overkill'][Rarity.COMMON] = ItemDrop(
            ITEMS[prize_struct[152]], prize_struct[160], False)
    if prize_struct[155] == 32:
        item_1['overkill'][Rarity.RARE] = ItemDrop(
            ITEMS[prize_struct[154]], prize_struct[161], True)

    item_2 = {
        'drop_chance': prize_struct[137],
        'normal': {Rarity.COMMON: None, Rarity.RARE: None},
        'overkill': {Rarity.COMMON: None, Rarity.RARE: None},
    }
    if prize_struct[145] == 32:
        item_2['normal'][Rarity.COMMON] = ItemDrop(
            ITEMS[prize_struct[144]], prize_struct[150], False)
    if prize_struct[147] == 32:
        item_2['normal'][Rarity.RARE] = ItemDrop(
            ITEMS[prize_struct[146]], prize_struct[151], True)
    if prize_struct[157] == 32:
        item_2['overkill'][Rarity.COMMON] = ItemDrop(
            ITEMS[prize_struct[156]], prize_struct[162], False)
    if prize_struct[159] == 32:
        item_2['overkill'][Rarity.RARE] = ItemDrop(
            ITEMS[prize_struct[158]], prize_struct[163], True)

    steal = {
        'base_chance': prize_struct[138],
        Rarity.COMMON: None,
        Rarity.RARE: None,
    }
    if prize_struct[165] == 32:
        steal[Rarity.COMMON] = ItemDrop(
            ITEMS[prize_struct[164]], prize_struct[168], False)
    if prize_struct[167] == 32:
        steal[Rarity.RARE] = ItemDrop(
            ITEMS[prize_struct[166]], prize_struct[169], True)
    bribe = {
        'cost': float('nan'),
        'item': None,
    }
    if prize_struct[171] == 32:
        bribe['item'] = ItemDrop(
            ITEMS[prize_struct[170]], prize_struct[172], False)

    elemental_affinities = get_elements()

    status_resistances = {
        Status.DEATH: prize_struct[47],
        Status.ZOMBIE: prize_struct[48],
        Status.PETRIFY: prize_struct[49],
        Status.POISON: prize_struct[50],
        Status.POWER_BREAK: prize_struct[51],
        Status.MAGIC_BREAK: prize_struct[52],
        Status.ARMOR_BREAK: prize_struct[53],
        Status.MENTAL_BREAK: prize_struct[54],
        Status.CONFUSE: prize_struct[55],
        Status.BERSERK: prize_struct[56],
        Status.PROVOKE: prize_struct[57],
        Status.THREATEN: prize_struct[58],
        Status.SLEEP: prize_struct[59],
        Status.SILENCE: prize_struct[60],
        Status.DARK: prize_struct[61],
        Status.PROTECT: prize_struct[62],
        Status.SHELL: prize_struct[63],
        Status.REFLECT: prize_struct[64],
        Status.NULBLAZE: prize_struct[65],
        Status.NULFROST: prize_struct[66],
        Status.NULSHOCK: prize_struct[67],
        Status.NULTIDE: prize_struct[68],
        Status.REGEN: prize_struct[69],
        Status.HASTE: prize_struct[70],
        Status.SLOW: prize_struct[71],
    }
    poison_tick_damage = stats[Stat.HP] * prize_struct[42] // 100
    undead = prize_struct[72] == 2
    auto_statuses = []
    if prize_struct[74] & 0b00100000:
        auto_statuses.append(Status.REFLECT)
    if (prize_struct[75] & 0b00000011
            and prize_struct[74] & 0b11000000):
        auto_statuses.append(Status.NULALL)
    if prize_struct[75] & 0b00000100:
        auto_statuses.append(Status.REGEN)

    equipment = {
        'drop_chance': prize_struct[139],
        'bonus_critical_chance': prize_struct[175],
        'base_weapon_damage': prize_struct[176],
        'slots_modifier': prize_struct[173],
        'slots_range': [],
        'max_ability_rolls_modifier': prize_struct[177],
        'max_ability_rolls_range': [],
        'added_to_inventory': bool(prize_struct[174]),
    }

    for i in range(8):
        slots_mod = equipment['slots_modifier'] + i - 4
        slots = ((slots_mod + ((slots_mod >> 31) & 3)) >> 2)
        if slots < EquipmentSlots.MIN:
            slots = EquipmentSlots.MIN.value
        elif slots > EquipmentSlots.MAX:
            slots = EquipmentSlots.MAX.value
        equipment['slots_range'].append(slots)
        ab_mod = equipment['max_ability_rolls_modifier'] + i - 4
        ab_rolls = (ab_mod + ((ab_mod >> 31) & 7)) >> 3
        equipment['max_ability_rolls_range'].append(ab_rolls)

    equipment['ability_arrays'] = {}
    for c, i in zip(CHARACTERS.values(), range(178, 371, 32)):
        equipment['ability_arrays'][c.name] = get_abilities(i)

    armored = bool(prize_struct[40] & 0b00000001)
    zanmato_level = prize_struct[402]
    actions = MONSTER_ACTIONS[monster_id]
    if not actions:
        actions.update(MONSTER_ACTIONS['generic_actions'])
    monster = Monster(
        name=monster_name,
        stats=stats,
        elemental_affinities=elemental_affinities,
        status_resistances=status_resistances,
        poison_tick_damage=poison_tick_damage,
        zanmato_level=zanmato_level,
        armored=armored,
        undead=undead,
        auto_statuses=auto_statuses,
        gil=gil,
        ap=ap,
        item_1=item_1,
        item_2=item_2,
        steal=steal,
        bribe=bribe,
        equipment=equipment,
        actions=actions,
    )
    return monster


PRIZE_STRUCTS = _get_prize_structs('tracker\\data\\ffx_mon_data.csv')
if Configs.game_version is GameVersion.HD:
    PRIZE_STRUCTS = _patch_prize_structs_for_hd(PRIZE_STRUCTS)

MONSTERS = {k: _get_monster_data(k, v) for k, v in PRIZE_STRUCTS.items()}
