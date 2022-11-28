import csv

from .autoabilities import AUTOABILITIES
from .characters import CHARACTERS
from .constants import EquipmentType
from .equipment import Equipment
from .file_functions import get_resource_path


def _get_shops_equipment(file_path: str) -> tuple[Equipment]:
    """"""
    absolute_file_path = get_resource_path(file_path)
    with open(absolute_file_path) as file_object:
        equipments_file_reader = csv.reader(file_object, delimiter=",")
        equipments = []
        for line in equipments_file_reader:
            if int(line[5], 16) == 0:
                equipment_type = EquipmentType.WEAPON
            else:
                equipment_type = EquipmentType.ARMOR
            owner_index = int(line[4], 16)
            for character in CHARACTERS.values():
                if character.index == owner_index:
                    break
            slots = int(line[11], 16)
            abilities = []
            for ability, is_active in zip(line[14:21:2], line[15:22:2]):
                if int(is_active, 16) == 0x80:
                    abilities.append(AUTOABILITIES[int(ability, 16)])
            base_weapon_damage = int(line[9], 16)
            bonus_crit = int(line[10], 16)
            equipment = Equipment(
                owner=character,
                type_=equipment_type,
                slots=slots,
                abilities=tuple(abilities),
                base_weapon_damage=base_weapon_damage,
                bonus_crit=bonus_crit,
            )
            equipments.append(equipment)
    return tuple(equipments)


def _get_equipment_shops(file_path: str) -> dict[str, tuple[Equipment]]:
    equipments = list(_get_shops_equipment("tracker\\data\\ffx_shop_arms.csv"))
    absolute_file_path = get_resource_path(file_path)
    shops = {}
    with open(absolute_file_path) as file_object:
        shops_file_reader = csv.reader(file_object, delimiter=",")
        next(shops_file_reader)
        for line in shops_file_reader:
            shops[line[0]] = [equipments.pop(0) for _ in range(int(line[1]))]
    return shops


EQUIPMENT_SHOPS = _get_equipment_shops("tracker\\data\\equipment_shops.csv")
